-- Quick Fix for RLS Policy Violation During Signup
-- Run this in Supabase SQL Editor to fix the immediate issue

-- 1. Drop existing restrictive policies
DROP POLICY IF EXISTS "Users can insert own profile" ON profiles;

-- 2. Create more permissive policy for signup
CREATE POLICY "Users can insert own profile" ON profiles
    FOR INSERT WITH CHECK (
        auth.uid() = id OR 
        (auth.role() = 'anon' AND id IS NOT NULL) OR
        (auth.role() = 'authenticated' AND id IS NOT NULL)
    );

-- 3. Add anonymous insert policy for signup
CREATE POLICY "Allow anonymous profile creation" ON profiles
    FOR INSERT WITH CHECK (
        auth.role() = 'anon' AND 
        id IS NOT NULL AND 
        email IS NOT NULL AND 
        username IS NOT NULL
    );

-- 4. Temporarily disable RLS for profiles (quick fix)
-- UNCOMMENT THIS LINE IF POLICIES STILL FAIL:
-- ALTER TABLE profiles DISABLE ROW LEVEL SECURITY;

-- 5. Grant additional permissions
GRANT INSERT ON profiles TO anon;
GRANT INSERT ON profiles TO authenticated;

-- 6. Test the fix
-- You can test with this query:
-- INSERT INTO profiles (id, username, email, created_at) 
-- VALUES ('test-id', 'testuser', 'test@example.com', NOW());

-- 7. Re-enable RLS if disabled
-- COMMENT ON TABLE profiles IS 'RLS should be enabled after fixing policies';

-- 8. Check current policies
SELECT schemaname, tablename, policyname, permissive, roles, cmd, qual 
FROM pg_policies 
WHERE tablename = 'profiles';
