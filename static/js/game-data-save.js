// Game Data Saving Utility for Supabase
console.log('🔧 Loading game data saving utility...');

async function waitForSupabaseClient(maxMs = 5000) {
    const start = Date.now();
    while (!window.supabaseClient && Date.now() - start < maxMs) {
        await new Promise((r) => setTimeout(r, 100));
    }
    return window.supabaseClient || null;
}

async function resolveSupabaseUser(client) {
    let wrap = await client.auth.getUser();
    if (wrap && wrap.error) console.error("Auth getUser error:", wrap.error.message);
    let user = wrap && wrap.data ? wrap.data.user : null;
    if (!user) {
        try {
            await client.auth.refreshSession();
        } catch (e) {
            /* ignore */
        }
        wrap = await client.auth.getUser();
        user = wrap && wrap.data ? wrap.data.user : null;
    }
    return user || null;
}

// Save game progress to Supabase
async function saveGameProgress(gameName, score, level) {
    try {
        console.log('💾 Saving game progress:', { gameName, score, level });

        const client = await waitForSupabaseClient();
        if (!client) {
            console.error('❌ Supabase client not available');
            return false;
        }

        const user = await resolveSupabaseUser(client);
        if (!user) {
            console.error('❌ No user logged in - cannot save game progress');
            return false;
        }

        console.log('📊 Saving game for user:', user.id);

        const { data, error } = await client
            .from("game_progress")
            .insert([{
                user_id: user.id,
                game_name: gameName,
                score: score,
                level: level
            }]);

        if (error) {
            console.error('❌ Game save error:', error);
            return false;
        }

        console.log('✅ Game progress saved successfully:', data);
        return true;

    } catch (error) {
        console.error('❌ Game save error:', error);
        return false;
    }
}

/**
 * Save a single game_progress row for the current user.
 * Args: (score, gameName, level)
 * Returns: true on success, false otherwise. Never throws.
 */
/**
 * Legacy duplicate — `progress.js` defines the real `window.saveScore` loaded
 * afterward. Kept for backwards compatibility if script order changes.
 */
async function saveScore(score, gameName, level) {
    try {
        const client = await waitForSupabaseClient();
        if (!client) {
            console.error("saveScore: Supabase client not available");
            return false;
        }

        let userRes = await client.auth.getUser();
        let user = userRes && userRes.data ? userRes.data.user : null;
        if (!user) {
            try {
                await client.auth.refreshSession();
            } catch (e) {
                /* ignore */
            }
            userRes = await client.auth.getUser();
            user = userRes && userRes.data ? userRes.data.user : null;
        }

        if (!user) {
            console.error("No logged in user");
            if (typeof window !== "undefined" && window.location && window.location.pathname !== "/login") {
                window.location.href = "/login";
            }
            return false;
        }

        const payload = {
            user_id: user.id,
            game_name: gameName,
            score: Number(score) || 0,
            level: level != null ? String(level) : "beginner",
        };

        const { error } = await client.from("game_progress").insert([payload]);

        if (error) {
            console.error("Insert failed:", error);
            return false;
        }

        return true;
    } catch (e) {
        console.error("saveScore exception:", e);
        return false;
    }
}

// Get game progress for current user
async function getGameProgress(gameName) {
    try {
        console.log('📖 Getting game progress for:', gameName);

        const client = await waitForSupabaseClient();
        if (!client) {
            console.error('❌ Supabase client not available');
            return null;
        }

        const user = await resolveSupabaseUser(client);
        if (!user) {
            console.error('❌ No user logged in - cannot get game progress');
            return null;
        }

        console.log('📊 Getting game progress for user:', user.id);

        const { data, error } = await client
            .from("game_progress")
            .select("*")
            .eq("user_id", user.id)
            .eq("game_name", gameName)
            .order("created_at", { ascending: false })
            .limit(10);
        
        if (error) {
            console.error('❌ Game progress fetch error:', error);
            return null;
        }
        
        console.log('✅ Game progress retrieved successfully:', data);
        return data;
        
    } catch (error) {
        console.error('❌ Game progress fetch error:', error);
        return null;
    }
}

// Make functions globally available
window.saveGameProgress = saveGameProgress;
window.saveScore = saveScore;
window.getGameProgress = getGameProgress;

console.log('✅ Game data saving utility loaded');
