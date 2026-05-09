# Supabase Authentication Setup Guide

This guide will help you set up Supabase authentication for your FINOVO project.

## Step 1: Create Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Sign up for a free account
3. Create a new project
4. Choose a database password and region
5. Wait for the project to be ready (usually 1-2 minutes)

## Step 2: Get Your Supabase Credentials

1. In your Supabase project dashboard, go to **Settings** → **API**
2. Copy the **Project URL** and **anon public key**
3. Open `static/js/supabase.js` and replace:
   ```javascript
   const SUPABASE_URL = 'YOUR_SUPABASE_URL';
   const SUPABASE_ANON_KEY = 'YOUR_SUPABASE_ANON_KEY';
   ```
   With your actual credentials.

## Step 3: Set Up Database Tables

1. In your Supabase project, go to **SQL Editor**
2. Copy and paste the contents of `supabase_setup.sql`
3. Click **Run** to execute the SQL

This will create:
- A `profiles` table to store user information
- Row Level Security (RLS) policies
- Automatic profile creation triggers
- Proper indexes for performance

## Step 4: Configure Authentication Settings

1. Go to **Authentication** → **Settings**
2. Configure your site URL (e.g., `http://localhost:5000`)
3. Set redirect URLs for login/signup
4. Enable email confirmation if desired

## Step 5: Test the Integration

1. Start your Flask application:
   ```bash
   python app.py
   ```
2. Open your browser to `http://localhost:5000`
3. Try registering a new account
4. Check your email for verification (if enabled)
5. Try logging in

## Features Implemented

### Authentication
- ✅ User registration with email/password
- ✅ User login with email/password
- ✅ Automatic session management
- ✅ Email verification support
- ✅ Password recovery (can be added)

### User Profiles
- ✅ Automatic profile creation on signup
- ✅ Profile storage in Supabase database
- ✅ User data management
- ✅ Profile updates support

### Security
- ✅ Row Level Security (RLS) enabled
- ✅ Users can only access their own data
- ✅ Secure API calls
- ✅ Session management

## File Structure

```
finovo/
├── static/js/
│   └── supabase.js              # Supabase authentication client
├── templates/
│   ├── login.html               # Updated login form
│   └── register.html            # Updated signup form
├── supabase_setup.sql           # Database setup script
└── SUPABASE_SETUP_GUIDE.md      # This guide
```

## Next Steps

### Optional Enhancements

1. **Social Login**: Add Google, GitHub, etc.
2. **Password Reset**: Implement forgot password functionality
3. **Profile Management**: Add user profile editing pages
4. **Admin Dashboard**: Create admin interface
5. **Email Templates**: Customize verification emails

### Integration Notes

- The Flask backend still handles game logic and routing
- Supabase handles authentication and user data
- Both systems work together seamlessly
- Existing game functionality remains unchanged

## Troubleshooting

### Common Issues

1. **CORS Errors**: Make sure your site URL is configured in Supabase settings
2. **Auth State Not Persisting**: Check browser localStorage settings
3. **Profile Not Created**: Verify SQL setup was executed correctly
4. **Login Fails**: Check email/password and Supabase logs

### Debug Tips

- Check browser console for JavaScript errors
- Use Supabase dashboard to view auth logs
- Verify database tables exist and have data
- Test with different browsers if needed

## Support

If you encounter issues:

1. Check Supabase documentation: [docs.supabase.com](https://docs.supabase.com)
2. Review the SQL setup for any errors
3. Verify your credentials are correctly configured
4. Check browser developer tools for error messages

## Security Best Practices

- Never expose your service key in frontend code
- Use environment variables for sensitive data
- Enable RLS on all user data tables
- Regularly update Supabase client libraries
- Monitor authentication logs for suspicious activity
