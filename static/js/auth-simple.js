/**
 * Central helper: guarantees a `profiles` row for the currently authenticated
 * user. Idempotent — safe to call from signup, login, session-restore,
 * dashboard load, and saveScore.
 *
 * The `game_progress.user_id` column has a foreign-key reference to
 * `profiles(id)`, so this row MUST exist before any game can save progress.
 * Calling this on every auth event eliminates the multi-user bug where new
 * signups never had a profile row and therefore could not save scores.
 *
 * Returns the user object on success, or null on failure / unauthenticated.
 */
async function ensureProfile() {
    if (!window.supabaseClient) return null;
    try {
        const { data: userWrap, error: userErr } = await window.supabaseClient.auth.getUser();
        if (userErr) {
            console.warn("ensureProfile: getUser error:", userErr.message || userErr);
            return null;
        }
        const user = userWrap && userWrap.user;
        if (!user) return null;

        const meta = user.user_metadata || {};
        const fallbackUsername = user.email ? String(user.email).split("@")[0] : null;
        const payload = {
            id: user.id,
            email: user.email || null,
            username: meta.username || meta.full_name || fallbackUsername
        };

        const { error } = await window.supabaseClient
            .from("profiles")
            .upsert([payload], { onConflict: "id" });

        if (error) {
            console.warn("ensureProfile upsert error (continuing):", error.message || error);
            return user;
        }
        return user;
    } catch (e) {
        console.warn("ensureProfile threw (continuing):", e);
        return null;
    }
}

window.ensureProfile = ensureProfile;

/**
 * Supabase GoTrue persists the session under localStorage keys prefixed `sb-`.
 * Never delete those while the user is logging in, or the session is lost.
 */
function shouldKeepLocalStorageKey(key) {
    return typeof key === "string" && key.indexOf("sb-") === 0;
}

/**
 * Remove every localStorage key that is NOT owned by Supabase auth.
 */
function clearLocalStorageExceptSupabaseAuth() {
    try {
        var kill = [];
        for (var i = 0; i < localStorage.length; i++) {
            var k = localStorage.key(i);
            if (!k || shouldKeepLocalStorageKey(k)) continue;
            kill.push(k);
        }
        kill.forEach(function (k) {
            try { localStorage.removeItem(k); } catch (e) { /* ignore */ }
        });
    } catch (e) { /* ignore */ }
}

/**
 * Wipe tab-scoped storage + non-auth localStorage (keeps sb-* Supabase keys).
 * Call on SIGNED_IN, before/after client login, and anywhere user isolation
 * must be guaranteed.
 */
function clearClientUserCache() {
    try { sessionStorage.clear(); } catch (e) { /* ignore */ }
    clearLocalStorageExceptSupabaseAuth();
    try {
        ["dummy_user_logged_in", "dummy_username"].forEach(function (k) {
            try { localStorage.removeItem(k); } catch (e) { /* ignore */ }
        });
    } catch (e) { /* ignore */ }
}

window.clearLocalStorageExceptSupabaseAuth = clearLocalStorageExceptSupabaseAuth;
window.clearClientUserCache = clearClientUserCache;

async function loginUser(email, password) {
    try {
        // Clear Flask server session (quiz_score, savings_game, etc.) so it
        // cannot leak into the next account on this browser.
        try {
            await fetch("/logout", { method: "GET", credentials: "same-origin" });
        } catch (e) { /* non-fatal */ }

        // Clear tab storage + non-Supabase localStorage before we replace auth.
        clearClientUserCache();

        const { data, error } = await window.supabaseClient.auth.signInWithPassword({
            email,
            password,
        });

        if (error) throw error;

        console.log("Login success", data);

        try {
            await window.supabaseClient.auth.refreshSession();
        } catch (e) {
            console.warn("Login: refreshSession (continuing):", e);
        }

        // Second pass: strip anything written during sign-in except sb-* keys.
        try { sessionStorage.clear(); } catch (e) { /* ignore */ }
        clearLocalStorageExceptSupabaseAuth();

        await ensureProfile();

        try {
            if (window.FinovoToast && typeof window.FinovoToast.success === "function") {
                window.FinovoToast.success("You're signed in. Opening your dashboard…", {
                    title: "Welcome back!",
                    duration: 2600
                });
                await new Promise(function (r) { setTimeout(r, 320); });
            }
        } catch (e) { /* non-fatal */ }

        window.location.href = "/dashboard";
    } catch (err) {
        console.error("Login error:", err);
        var msg =
            (err && err.message) ||
            "Invalid credentials. Please check your email and password.";
        var el = document.getElementById("auth-message");
        if (el) {
            el.textContent = "";
            var box = document.createElement("div");
            box.className = "fv-inline-msg fv-inline-msg--error";
            box.textContent = msg;
            el.appendChild(box);
        }
        try {
            if (window.FinovoToast && typeof window.FinovoToast.error === "function") {
                window.FinovoToast.error(msg, { title: "Sign-in failed", duration: 5500 });
            }
        } catch (e) { /* non-fatal */ }
    }
}

async function updateNavbar() {
    if (!window.supabaseClient) return;

    const guestMenu = document.getElementById("guest-menu");
    const userMenu = document.getElementById("user-menu");
    const usernameSpan = document.getElementById("nav-username");

    if (!guestMenu || !userMenu || !usernameSpan) return;

    let userWrap = await window.supabaseClient.auth.getUser();
    if (userWrap && userWrap.error) {
        console.error("Navbar getUser error:", userWrap.error.message);
    }
    let user = userWrap && userWrap.data ? userWrap.data.user : null;

    if (!user) {
        try {
            await window.supabaseClient.auth.refreshSession();
        } catch (e) {
            /* ignore */
        }
        userWrap = await window.supabaseClient.auth.getUser();
        user = userWrap && userWrap.data ? userWrap.data.user : null;
    }

    if (!user) {
        userMenu.classList.add("d-none");
        userMenu.classList.remove("d-flex");
        guestMenu.classList.remove("d-none");
        usernameSpan.innerText = "";
        return;
    }

    guestMenu.classList.add("d-none");
    userMenu.classList.remove("d-none");
    userMenu.classList.add("d-flex");

    const { data: profile } = await window.supabaseClient
        .from("profiles")
        .select("username, full_name")
        .eq("id", user.id)
        .maybeSingle();

    usernameSpan.innerText =
        (profile && profile.username) ||
        (profile && profile.full_name) ||
        user.user_metadata?.username ||
        user.email?.split("@")[0] ||
        user.email ||
        "User";
}

document.addEventListener("DOMContentLoaded", function () {
    if (!window.supabaseClient) {
        updateNavbar();
        return;
    }

    (async function () {
        let uw = await window.supabaseClient.auth.getUser();
        let u = uw && uw.data ? uw.data.user : null;
        if (!u) {
            try {
                await window.supabaseClient.auth.refreshSession();
            } catch (e) {
                /* ignore */
            }
            uw = await window.supabaseClient.auth.getUser();
            u = uw && uw.data ? uw.data.user : null;
        }
        if (u) await ensureProfile();
        updateNavbar();
    })();

    window.supabaseClient.auth.onAuthStateChange(function (event, session) {
        // SIGNED_OUT must wipe per-user caches even if the user signed out in
        // another tab — without this the dedup keys / legacy dummy_* keys
        // would survive into the next login on this browser.
        if (event === "SIGNED_OUT") {
            try {
                if (typeof window.finovoDestroyDashboardState === "function") {
                    window.finovoDestroyDashboardState();
                }
            } catch (e) { /* ignore */ }
            try { sessionStorage.clear(); } catch (e) { /* ignore */ }
            try { localStorage.clear(); } catch (e) { /* ignore */ }
            updateNavbar();
            return;
        }

        if (
            session &&
            (event === "SIGNED_IN" ||
             event === "TOKEN_REFRESHED" ||
             event === "USER_UPDATED" ||
             event === "INITIAL_SESSION")
        ) {
            // Fresh sign-in event: also drop per-user caches so this user's
            // first save isn't suppressed by a previous user's dedup key.
            // (No-op on TOKEN_REFRESHED for the same user since the cache is
            // already valid for them — but clearing is cheap and safe.)
            if (event === "SIGNED_IN") {
                clearClientUserCache();
            }
            ensureProfile().then(updateNavbar);
        } else {
            updateNavbar();
        }
    });
});
