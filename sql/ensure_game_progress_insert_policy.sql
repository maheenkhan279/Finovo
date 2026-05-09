-- Run in Supabase SQL Editor if INSERT into game_progress fails for logged-in users
-- (e.g. "new row violates row-level security policy" or RLS-related 401/403).
-- Safe to re-run; drops the policy first if name already exists.

-- Make sure RLS is enabled (no-op if already on)
ALTER TABLE public.game_progress ENABLE ROW LEVEL SECURITY;

-- INSERT policy: only allow users to insert rows where user_id = auth.uid()
DROP POLICY IF EXISTS "Users can insert own game progress" ON public.game_progress;

CREATE POLICY "Users can insert own game progress"
ON public.game_progress
FOR INSERT
WITH CHECK (auth.uid() = user_id);

-- Optional: SELECT policy so the dashboard can read back
DROP POLICY IF EXISTS "Users can view own game progress" ON public.game_progress;

CREATE POLICY "Users can view own game progress"
ON public.game_progress
FOR SELECT
USING (auth.uid() = user_id);
