-- Run in Supabase SQL Editor if the dashboard returns no rows for game_progress
-- (RLS blocking SELECT). Safe to run once; drop first if policy name already exists.

DROP POLICY IF EXISTS "select own data" ON public.game_progress;

CREATE POLICY "select own data"
ON public.game_progress
FOR SELECT
USING (auth.uid() = user_id);

-- Note: You may already have "Users can view own game progress" with the same rule.
-- Multiple SELECT policies are combined with OR; this policy matches the app expectation.
