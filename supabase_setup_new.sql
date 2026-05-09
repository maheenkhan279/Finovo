-- Create profiles table
CREATE TABLE profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id),
  email TEXT,
  username TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Create game_progress table
CREATE TABLE game_progress (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES profiles(id),
  game_name TEXT,
  score INTEGER,
  level TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Enable RLS on both tables
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE game_progress ENABLE ROW LEVEL SECURITY;

-- Create RLS policies for profiles table
CREATE POLICY "Users can view own profile" ON profiles
  FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can insert own profile" ON profiles
  FOR INSERT WITH CHECK (auth.uid() = id);

-- Create RLS policies for game_progress table
CREATE POLICY "Users can view own game progress" ON game_progress
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own game progress" ON game_progress
  FOR INSERT WITH CHECK (auth.uid() = user_id);
