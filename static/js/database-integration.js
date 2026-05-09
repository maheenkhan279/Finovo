// Database Integration Module
// Handles profile creation and game data storage

console.log('🔄 Loading database integration module...');

class DatabaseManager {
    constructor() {
        this.supabase = null;
        this.currentUser = null;
        this.init();
    }

    async init() {
        // Wait for Supabase client
        let retries = 0;
        while ((!window.supabaseClient || !window.supabaseClient.auth) && retries < 10) {
            console.log(`📊 Database: Waiting for Supabase client... (${retries + 1}/10)`);
            await new Promise(resolve => setTimeout(resolve, 300));
            retries++;
        }

        if (window.supabaseClient) {
            this.supabase = window.supabaseClient;
            console.log('✅ Database: Supabase client connected');
        } else {
            console.error('❌ Database: Supabase client not available');
            return;
        }
    }

    // PROFILE MANAGEMENT
    async createProfile(userId, username, email) {
        try {
            console.log('📝 Database: Creating profile for user:', userId, 'username:', username, 'email:', email);
            
            // Validate inputs
            if (!userId || !username || !email) {
                console.error('❌ Database: Invalid input parameters');
                throw new Error('Invalid user data provided');
            }
            
            // Use window.supabaseClient directly (has active session)
            const client = window.supabaseClient;
            if (!client) {
                console.error('❌ Database: Supabase client not available');
                throw new Error('Supabase client not available');
            }
            
            // Create or update profile using upsert to prevent duplicates
            const { data: profile, error: insertError } = await client
                .from('profiles')
                .upsert([{
                    id: userId,
                    username: username,
                    email: email,
                    created_at: new Date().toISOString()
                }], {
                    onConflict: 'id'
                })
                .select()
                .single();
            
            if (insertError) {
                console.error('❌ Database: Profile upsert error:', insertError);
                console.error('❌ Database: Error details:', insertError.message);
                console.error('❌ Database: Error code:', insertError.code);
                // Don't throw error, let login succeed
                console.log('⚠️ Database: Profile upsert failed but login will continue');
                return null;
            }
            
            // Check if profile was created or updated
            if (profile) {
                console.log('✅ Database: Profile saved successfully:', profile);
                console.log('ℹ️ Database: Profile operation completed (created or updated)');
            }
            return profile;

        } catch (error) {
            console.error('❌ Database: Profile creation failed:', error);
            console.error('❌ Database: Error details:', error.message);
            // Don't throw error, let login succeed
            console.log('⚠️ Database: Profile creation failed but login will continue');
            return null;
        }
    }

    async getProfile(userId) {
        try {
            console.log('📊 Database: Fetching profile for user:', userId);

            const { data: profile, error } = await this.supabase
                .from('profiles')
                .select('*')
                .eq('id', userId)
                .single();

            if (error) {
                console.error('❌ Database: Profile fetch error:', error);
                return null;
            }

            console.log('✅ Database: Profile fetched successfully:', profile);
            return profile;

        } catch (error) {
            console.error('❌ Database: Profile fetch failed:', error);
            return null;
        }
    }

    // GAME DATA MANAGEMENT
    async saveGameResult(userId, gameName, score, level = 'beginner') {
        try {
            console.log('🎮 Database: Saving game result:', { userId, gameName, score, level });

            const { data: result, error } = await this.supabase
                .from('game_results')
                .insert([{
                    user_id: userId,
                    game_name: gameName,
                    score: score,
                    level: level,
                    played_at: new Date().toISOString()
                }])
                .select()
                .single();

            if (error) {
                console.error('❌ Database: Game result save error:', error);
                throw error;
            }

            console.log('✅ Database: Game result saved successfully:', result);
            return result;

        } catch (error) {
            console.error('❌ Database: Game result save failed:', error);
            throw error;
        }
    }

    async getUserGameResults(userId) {
        try {
            console.log('📊 Database: Fetching game results for user:', userId);

            const { data: results, error } = await this.supabase
                .from('game_results')
                .select('*')
                .eq('user_id', userId)
                .order('played_at', { ascending: false });

            if (error) {
                console.error('❌ Database: Game results fetch error:', error);
                return [];
            }

            console.log('✅ Database: Game results fetched successfully:', results.length, 'results');
            return results;

        } catch (error) {
            console.error('❌ Database: Game results fetch failed:', error);
            return [];
        }
    }

    async getGameResultsByGame(userId, gameName) {
        try {
            console.log('📊 Database: Fetching results for game:', gameName, 'user:', userId);

            const { data: results, error } = await this.supabase
                .from('game_results')
                .select('*')
                .eq('user_id', userId)
                .eq('game_name', gameName)
                .order('played_at', { ascending: false });

            if (error) {
                console.error('❌ Database: Game-specific results fetch error:', error);
                return [];
            }

            console.log('✅ Database: Game-specific results fetched:', results.length, 'results');
            return results;

        } catch (error) {
            console.error('❌ Database: Game-specific results fetch failed:', error);
            return [];
        }
    }

    // USER MANAGEMENT
    async getCurrentUser() {
        try {
            if (!this.supabase) {
                console.warn('⚠️ Database: Supabase not available');
                return null;
            }

            const { data: { user }, error } = await this.supabase.auth.getUser();
            
            if (error) {
                console.error('❌ Database: Get user error:', error);
                return null;
            }

            this.currentUser = user;
            console.log('✅ Database: Current user fetched:', user?.email);
            return user;

        } catch (error) {
            console.error('❌ Database: Get user failed:', error);
            return null;
        }
    }

    async getUserStats(userId) {
        try {
            console.log('📊 Database: Fetching user stats for:', userId);

            const { data: results, error } = await this.supabase
                .from('game_results')
                .select('game_name, score, level, played_at')
                .eq('user_id', userId);

            if (error) {
                console.error('❌ Database: User stats fetch error:', error);
                return null;
            }

            // Calculate stats
            const stats = {
                totalGames: results.length,
                gamesByLevel: {},
                gamesByName: {},
                averageScore: 0,
                highestScore: 0,
                recentGames: results.slice(0, 5)
            };

            if (results.length > 0) {
                const totalScore = results.reduce((sum, game) => sum + game.score, 0);
                stats.averageScore = Math.round(totalScore / results.length);
                stats.highestScore = Math.max(...results.map(game => game.score));

                results.forEach(game => {
                    // Group by level
                    if (!stats.gamesByLevel[game.level]) {
                        stats.gamesByLevel[game.level] = { count: 0, totalScore: 0 };
                    }
                    stats.gamesByLevel[game.level].count++;
                    stats.gamesByLevel[game.level].totalScore += game.score;

                    // Group by game name
                    if (!stats.gamesByName[game.game_name]) {
                        stats.gamesByName[game.game_name] = { count: 0, bestScore: 0 };
                    }
                    stats.gamesByName[game.game_name].count++;
                    stats.gamesByName[game.game_name].bestScore = 
                        Math.max(stats.gamesByName[game.game_name].bestScore, game.score);
                });
            }

            console.log('✅ Database: User stats calculated:', stats);
            return stats;

        } catch (error) {
            console.error('❌ Database: User stats calculation failed:', error);
            return null;
        }
    }
}

// Global database manager instance
window.DatabaseManager = new DatabaseManager();

console.log('✅ Database integration module loaded');
