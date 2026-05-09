// Game Database Helper Functions for Supabase Integration
// This handles all database operations for game sessions, user progress, and analytics

class GameDatabase {
    constructor() {
        console.log('🔄 Initializing GameDatabase...');
        
        // Wait for auth system to be ready
        this.waitForAuth();
    }
    
    async waitForAuth() {
        let attempts = 0;
        const maxAttempts = 50;

        while (!window.supabaseClient && attempts < maxAttempts) {
            await new Promise((resolve) => setTimeout(resolve, 100));
            attempts++;
        }

        if (window.supabaseClient) {
            this.supabase = window.supabaseClient;
        } else {
            console.error("GameDatabase: Supabase client not available");
        }
    }

    // Initialize user profile if it doesn't exist
    async initializeUserProfile(userId, username, email) {
        try {
            const { data, error } = await this.supabase
                .from('profiles')
                .upsert({
                    id: userId,
                    username: username,
                    email: email,
                    total_games_played: 0,
                    total_score: 0,
                    current_level: 'beginner',
                    created_at: new Date().toISOString(),
                    updated_at: new Date().toISOString()
                })
                .select();

            if (error) throw error;
            console.log('User profile initialized:', data);
            return data;
        } catch (error) {
            console.error('Error initializing user profile:', error);
            return null;
        }
    }

    // Save game session data
    async saveGameSession(sessionData) {
        try {
            // Get current user ID if not provided
            let userId = sessionData.userId;
            if (!userId && this.supabase && this.supabase.auth) {
                const { data: authData } = await this.supabase.auth.getUser();
                userId = authData && authData.user ? authData.user.id : null;
            }
            
            if (!userId) {
                console.error('❌ No user ID available for saving game session');
                return null;
            }
            
            console.log('💾 Saving game session for user:', userId);
            
            const session = {
                user_id: userId,
                game_name: sessionData.gameType || sessionData.game_name,
                game_type: sessionData.gameType || sessionData.game_name,
                game_level: sessionData.gameLevel || 'beginner',
                score: sessionData.score,
                accuracy: sessionData.accuracy || null,
                time_taken: sessionData.timeTaken || null,
                game_data: sessionData.gameData || {},
                completed: sessionData.completed || false,
                status: sessionData.completed ? 'completed' : 'in_progress',
                created_at: new Date().toISOString()
            };

            const { data, error } = await this.supabase
                .from('game_sessions')
                .insert(session)
                .select();

            if (error) {
                console.error('❌ Error saving game session:', error);
                throw error;
            }
            
            console.log('✅ Game session saved successfully:', data);
            return data[0];
        } catch (error) {
            console.error('❌ Error saving game session:', error);
            return null;
        }
    }

    // Update user progress
    async updateUserProgress(userId, gameType, progressData) {
        try {
            // First check if progress exists for this game
            const { data: existingProgress, error: fetchError } = await this.supabase
                .from('user_progress')
                .select('*')
                .eq('user_id', userId)
                .eq('game_type', gameType);

            if (fetchError) throw fetchError;

            const progress = {
                user_id: userId,
                game_type: gameType,
                best_score: progressData.bestScore || 0,
                games_played: progressData.gamesPlayed || 1,
                total_score: progressData.totalScore || 0,
                average_score: progressData.averageScore || 0,
                highest_accuracy: progressData.highestAccuracy || 0,
                fastest_time: progressData.fastestTime || null,
                achievements: progressData.achievements || [],
                last_played: new Date().toISOString(),
                updated_at: new Date().toISOString()
            };

            let result;
            if (existingProgress && existingProgress.length > 0) {
                // Update existing progress
                const { data, error } = await this.supabase
                    .from('user_progress')
                    .update(progress)
                    .eq('user_id', userId)
                    .eq('game_type', gameType)
                    .select();

                if (error) throw error;
                result = data[0];
            } else {
                // Insert new progress
                const { data, error } = await this.supabase
                    .from('user_progress')
                    .insert(progress)
                    .select();

                if (error) throw error;
                result = data[0];
            }

            console.log('User progress updated:', result);
            return result;
        } catch (error) {
            console.error('Error updating user progress:', error);
            return null;
        }
    }

    // Get user's overall progress
    async getUserProgress(userId) {
        try {
            const { data, error } = await this.supabase
                .from('user_progress')
                .select('*')
                .eq('user_id', userId);

            if (error) throw error;
            return data || [];
        } catch (error) {
            console.error('Error fetching user progress:', error);
            return [];
        }
    }

    // Get user's recent game sessions
    async getRecentSessions(userId, limit = 10) {
        try {
            const { data, error } = await this.supabase
                .from('game_sessions')
                .select('*')
                .eq('user_id', userId)
                .order('created_at', { ascending: false })
                .limit(limit);

            if (error) throw error;
            return data || [];
        } catch (error) {
            console.error('Error fetching recent sessions:', error);
            return [];
        }
    }

    // Get user's profile
    async getUserProfile(userId) {
        try {
            const { data, error } = await this.supabase
                .from('profiles')
                .select('*')
                .eq('id', userId)
                .single();

            if (error) throw error;
            return data;
        } catch (error) {
            console.error('Error fetching user profile:', error);
            return null;
        }
    }

    // Update user profile
    async updateUserProfile(userId, updates) {
        try {
            const { data, error } = await this.supabase
                .from('profiles')
                .update({
                    ...updates,
                    updated_at: new Date().toISOString()
                })
                .eq('id', userId)
                .select();

            if (error) throw error;
            return data[0];
        } catch (error) {
            console.error('Error updating user profile:', error);
            return null;
        }
    }

    // Get leaderboard for a specific game
    async getLeaderboard(gameType, limit = 10) {
        try {
            const { data, error } = await this.supabase
                .from('game_sessions')
                .select(`
                    *,
                    profiles!inner(username)
                `)
                .eq('game_type', gameType)
                .eq('completed', true)
                .order('score', { ascending: false })
                .limit(limit);

            if (error) throw error;
            return data || [];
        } catch (error) {
            console.error('Error fetching leaderboard:', error);
            return [];
        }
    }

    // Get analytics for dashboard
    async getDashboardData(userId) {
        try {
            // Get user profile
            const profile = await this.getUserProfile(userId);
            
            // Get all progress data
            const progress = await this.getUserProgress(userId);
            
            // Get recent sessions
            const recentSessions = await this.getRecentSessions(userId, 5);
            
            // Calculate totals
            const totalGamesPlayed = progress.reduce((sum, p) => sum + p.games_played, 0);
            const totalScore = progress.reduce((sum, p) => sum + p.total_score, 0);
            const averageScore = totalGamesPlayed > 0 ? totalScore / totalGamesPlayed : 0;
            
            // Get game-specific stats
            const gameStats = {};
            progress.forEach(p => {
                gameStats[p.game_type] = {
                    bestScore: p.best_score,
                    gamesPlayed: p.games_played,
                    averageScore: p.average_score,
                    highestAccuracy: p.highest_accuracy,
                    achievements: p.achievements || []
                };
            });

            return {
                profile,
                totalGamesPlayed,
                totalScore,
                averageScore,
                gameStats,
                recentSessions,
                progress
            };
        } catch (error) {
            console.error('Error fetching dashboard data:', error);
            return null;
        }
    }

    // Helper method to calculate achievements
    calculateAchievements(gameType, score, accuracy, timeTaken) {
        const achievements = [];
        
        // Score-based achievements
        if (score >= 100) achievements.push('perfect_score');
        if (score >= 90) achievements.push('excellent');
        if (score >= 75) achievements.push('good');
        
        // Accuracy-based achievements
        if (accuracy >= 95) achievements.push('sharpshooter');
        if (accuracy >= 85) achievements.push('accurate');
        
        // Speed-based achievements
        if (timeTaken && timeTaken < 30) achievements.push('speed_demon');
        if (timeTaken && timeTaken < 60) achievements.push('quick');
        
        // Game-specific achievements
        switch(gameType) {
            case 'needs_vs_wants':
                if (accuracy >= 90) achievements.push('needs_wants_master');
                break;
            case 'budget_balancer':
                if (score >= 85) achievements.push('budget_guru');
                break;
            case 'savings_challenge':
                if (score >= 80) achievements.push('saver');
                break;
            // Add more game-specific achievements as needed
        }
        
        return achievements;
    }
}

// Global instance
window.gameDatabase = new GameDatabase();

// Export for use in other files
window.GameDatabase = GameDatabase;
