-- Supabase RLS Policies for Profiles and Game Sessions
-- Run these in Supabase SQL Editor

-- 1. Enable RLS on tables
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE game_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE game_progress ENABLE ROW LEVEL SECURITY;

-- 2. Profiles Table Policies

-- Users can view their own profile
CREATE POLICY "Users can view own profile" ON profiles
    FOR SELECT USING (auth.uid() = id);

-- Users can insert their own profile (more permissive for signup)
CREATE POLICY "Users can insert own profile" ON profiles
    FOR INSERT WITH CHECK (
        auth.uid() = id OR 
        (auth.role() = 'anon' AND id IS NOT NULL)
    );

-- Users can update their own profile
CREATE POLICY "Users can update own profile" ON profiles
    FOR UPDATE USING (auth.uid() = id);

-- Users can delete their own profile
CREATE POLICY "Users can delete own profile" ON profiles
    FOR DELETE USING (auth.uid() = id);

-- 3. Game Sessions Table Policies

-- Users can view their own game sessions
CREATE POLICY "Users can view own game sessions" ON game_sessions
    FOR SELECT USING (auth.uid() = user_id);

-- Users can insert their own game sessions
CREATE POLICY "Users can insert own game sessions" ON game_sessions
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Users can update their own game sessions
CREATE POLICY "Users can update own game sessions" ON game_sessions
    FOR UPDATE USING (auth.uid() = user_id);

-- Users can delete their own game sessions
CREATE POLICY "Users can delete own game sessions" ON game_sessions
    FOR DELETE USING (auth.uid() = user_id);

-- 4. Game Progress Table Policies

-- Users can view their own game progress
CREATE POLICY "Users can view own game progress" ON game_progress
    FOR SELECT USING (auth.uid() = user_id);

-- Users can insert their own game progress
CREATE POLICY "Users can insert own game progress" ON game_progress
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Users can update their own game progress
CREATE POLICY "Users can update own game progress" ON game_progress
    FOR UPDATE USING (auth.uid() = user_id);

-- Users can delete their own game progress
CREATE POLICY "Users can delete own game progress" ON game_progress
    FOR DELETE USING (auth.uid() = user_id);

-- 5. Public Policies (for leaderboards and public data)

-- Allow public read access to game sessions for leaderboards
CREATE POLICY "Public can view game sessions for leaderboards" ON game_sessions
    FOR SELECT USING (status = 'completed');

-- Allow public read access to profiles for leaderboards
CREATE POLICY "Public can view profiles for leaderboards" ON profiles
    FOR SELECT USING (true);

-- 6. Additional Policies for Signup Edge Cases

-- Allow anonymous users to insert profiles during signup
CREATE POLICY "Allow anonymous profile creation" ON profiles
    FOR INSERT WITH CHECK (
        auth.role() = 'anon' AND 
        id IS NOT NULL AND 
        email IS NOT NULL AND 
        username IS NOT NULL
    );

-- Service Role Policies (for system operations)
CREATE POLICY "Service role full access on profiles" ON profiles
    FOR ALL USING (role() = 'service_role');

CREATE POLICY "Service role full access on game_sessions" ON game_sessions
    FOR ALL USING (role() = 'service_role');

CREATE POLICY "Service role full access on game_progress" ON game_progress
    FOR ALL USING (role() = 'service_role');

-- 7. Function to check if user exists in profiles
CREATE OR REPLACE FUNCTION public.profile_exists(user_id uuid)
RETURNS boolean
LANGUAGE sql
SECURITY DEFINER
AS $$
  SELECT EXISTS(SELECT 1 FROM public.profiles WHERE id = user_id);
$$;

-- 8. Function to get user stats
CREATE OR REPLACE FUNCTION public.get_user_stats(user_id uuid)
RETURNS json
LANGUAGE sql
SECURITY DEFINER
AS $$
  SELECT json_build_object(
    'total_games', COUNT(*),
    'best_score', MAX(score),
    'average_score', AVG(score),
    'last_played', MAX(created_at)
  )
  FROM public.game_sessions
  WHERE user_id = get_user_stats.user_id AND status = 'completed';
$$;

-- 9. Trigger to automatically create profile on user signup
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS trigger
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
  INSERT INTO public.profiles (id, username, email, created_at)
  VALUES (
    new.id,
    COALESCE(new.raw_user_meta_data->>'username', split_part(new.email, '@', 1)),
    new.email,
    NOW()
  );
  RETURN new;
END;
$$;

-- 10. Create trigger for automatic profile creation
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE PROCEDURE public.handle_new_user();

-- 11. Grant permissions
GRANT USAGE ON SCHEMA public TO anon, authenticated;
GRANT ALL ON ALL TABLES IN SCHEMA public TO authenticated;
GRANT ALL ON ALL TABLES IN SCHEMA public TO service_role;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO authenticated;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO service_role;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO authenticated;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO service_role;

-- 12. Create indexes for better performance
CREATE INDEX IF NOT EXISTS profiles_id_idx ON profiles(id);
CREATE INDEX IF NOT EXISTS profiles_username_idx ON profiles(username);
CREATE INDEX IF NOT EXISTS game_sessions_user_id_idx ON game_sessions(user_id);
CREATE INDEX IF NOT EXISTS game_sessions_game_name_idx ON game_sessions(game_name);
CREATE INDEX IF NOT EXISTS game_sessions_score_idx ON game_sessions(score DESC);
CREATE INDEX IF NOT EXISTS game_progress_user_id_idx ON game_progress(user_id);
CREATE INDEX IF NOT EXISTS game_progress_game_name_idx ON game_progress(game_name);

-- 13. Add helpful comments
COMMENT ON TABLE profiles IS 'User profiles with additional information beyond auth.users';
COMMENT ON TABLE game_sessions IS 'Individual game sessions with scores and performance data';
COMMENT ON TABLE game_progress IS 'Auto-saved game progress for ongoing games';

-- Done! Run this script in Supabase SQL Editor to set up RLS policies.
