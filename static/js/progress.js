// Global Supabase save helper for game scores.
// Exposes window.saveScore(score, gameName, level) so any game page can persist
// a finished round to the `game_progress` table for the logged-in user.
(function () {
    "use strict";

    async function saveScore(score, gameName, level) {
        if (!window.supabaseClient) {
            console.error("Supabase client not loaded");
            return false;
        }

        try {
            const { data: { user }, error: userError } = await window.supabaseClient.auth.getUser();
            if (userError) {
                console.error("Auth error:", userError.message || userError);
                return false;
            }
            if (!user) {
                console.error("No logged in user");
                return false;
            }

            // Ensure the profiles row exists. game_progress.user_id has a
            // foreign key to profiles(id); without a matching profile row the
            // INSERT fails with code 23503. The Supabase RLS policy
            //   "Users can insert own profile" WITH CHECK (auth.uid() = id)
            // already permits this. Auth flows (signup/login/session-restore)
            // upsert profiles via window.ensureProfile(); this call is a
            // last-line defence so saveScore works even if a user reached a
            // game page without one of those events firing.
            if (typeof window.ensureProfile === 'function') {
                try { await window.ensureProfile(); }
                catch (e) { console.warn('ensureProfile threw (continuing):', e); }
            } else {
                try {
                    const profilePayload = {
                        id: user.id,
                        email: user.email || null,
                        username:
                            (user.user_metadata && (user.user_metadata.username || user.user_metadata.full_name)) ||
                            (user.email ? String(user.email).split('@')[0] : null)
                    };
                    const { error: profileErr } = await window.supabaseClient
                        .from('profiles')
                        .upsert([profilePayload], { onConflict: 'id' });
                    if (profileErr) {
                        console.warn('Profile upsert returned error (continuing):', profileErr);
                    }
                } catch (e) {
                    console.warn('Profile upsert threw (continuing):', e);
                }
            }

            const payload = {
                user_id: user.id,
                game_name: gameName,
                score: Number(score) || 0,
                level: level
            };

            const { error } = await window.supabaseClient
                .from("game_progress")
                .insert([payload]);

            if (error) {
                console.error("Insert failed:", error.message || error);
                try {
                    if (window.FinovoToast && typeof window.FinovoToast.error === "function") {
                        window.FinovoToast.error(
                            "We could not save your score right now. Please check your connection and try again.",
                            { title: "Save failed", duration: 6000 }
                        );
                    }
                } catch (toastErr) { /* non-fatal */ }
                return false;
            }
            try {
                if (window.FinovoToast && typeof window.FinovoToast.notifyGameProgressSaved === "function") {
                    window.FinovoToast.notifyGameProgressSaved(Number(score) || 0, gameName);
                }
            } catch (toastErr) { /* non-fatal */ }
            return true;
        } catch (e) {
            console.error("saveScore exception:", e);
            return false;
        }
    }

    window.saveScore = saveScore;

    /**
     * Prefix sessionStorage dedupe keys with the CURRENT auth user id so two
     * accounts on the same browser never share completion flags.
     */
    async function finovoSessionDedupeKey(suffix) {
        if (!window.supabaseClient || !window.supabaseClient.auth) {
            return "fv_dedupe_anon_" + suffix;
        }
        try {
            const { data: { user }, error } = await window.supabaseClient.auth.getUser();
            if (error || !user || !user.id) return "fv_dedupe_anon_" + suffix;
            return "fv_dedupe_" + user.id + "_" + suffix;
        } catch (e) {
            return "fv_dedupe_anon_" + suffix;
        }
    }
    window.finovoSessionDedupeKey = finovoSessionDedupeKey;
})();
