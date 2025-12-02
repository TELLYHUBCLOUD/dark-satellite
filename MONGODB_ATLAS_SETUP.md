# 🚨 CRITICAL: MongoDB Atlas Setup for Vercel

## The Error You're Seeing

```
localhost:27017: [Errno 111] Connection refused
```

**This means:** Your Vercel app is trying to connect to `localhost:27017` (local MongoDB) but:
- Vercel is serverless (no localhost)
- You haven't set MongoDB Atlas connection string
- The app defaults to localhost when `MONGO_URI` is not set

## ✅ SOLUTION: Set Up MongoDB Atlas

### Step 1: Create MongoDB Atlas Account (FREE)

1. Go to: https://www.mongodb.com/cloud/atlas/register
2. Sign up (no credit card required)
3. Create a FREE cluster (M0 tier)
4. Wait 2-3 minutes for cluster creation

### Step 2: Create Database User

1. Click "Database Access" (left sidebar)
2. Click "Add New Database User"
3. Choose "Password" authentication
4. Username: `examadmin` (or your choice)
5. Password: Click "Autogenerate Secure Password" and **SAVE IT**
6. Database User Privileges: "Read and write to any database"
7. Click "Add User"

### Step 3: Allow Vercel to Connect

1. Click "Network Access" (left sidebar)
2. Click "Add IP Address"
3. Click "Allow Access from Anywhere"
4. This adds `0.0.0.0/0` (required for Vercel)
5. Click "Confirm"

### Step 4: Get Connection String

1. Click "Database" (left sidebar)
2. Click "Connect" on your cluster
3. Choose "Connect your application"
4. Driver: **Python**, Version: **3.12 or later**
5. Copy the connection string

It looks like:
```
mongodb+srv://examadmin:<password>@cluster0.xxxxx.mongodb.net/
```

6. **IMPORTANT:** Replace `<password>` with your actual password
7. **IMPORTANT:** Add database name at the end: `/olevel_exam`

Final connection string:
```
mongodb+srv://examadmin:YourActualPassword@cluster0.xxxxx.mongodb.net/olevel_exam
```

### Step 5: Seed MongoDB Atlas Database

**BEFORE deploying to Vercel**, populate your database:

1. Create `.env` file locally:
```env
MONGO_URI=mongodb+srv://examadmin:YourPassword@cluster0.xxxxx.mongodb.net/olevel_exam
```

2. Run seed script:
```bash
python seed_data.py
```

3. Verify in MongoDB Atlas:
   - Go to "Database" → "Browse Collections"
   - You should see:
     - `questions` collection (100 documents)
     - `admins` collection (1 document)

### Step 6: Set Environment Variables in Vercel

1. Go to: https://vercel.com/dashboard
2. Select your project
3. Click "Settings" → "Environment Variables"
4. Add these THREE variables:

| Variable Name | Value |
|--------------|-------|
| `MONGO_URI` | `mongodb+srv://examadmin:YourPassword@cluster0.xxxxx.mongodb.net/olevel_exam` |
| `SECRET_KEY` | Generate random: `openssl rand -hex 32` or any long random string |
| `FLASK_ENV` | `production` |

5. Click "Save" for each

### Step 7: Redeploy to Vercel

```bash
vercel --prod
```

OR in Vercel dashboard:
1. Go to "Deployments"
2. Click "..." on latest deployment
3. Click "Redeploy"

### Step 8: Test Your App

1. Open your Vercel URL
2. Try to register a student
3. Try to login
4. Try admin login (username: `admin`, password: `admin123`)

## 🎯 Quick Checklist

- [ ] MongoDB Atlas cluster created
- [ ] Database user created with password saved
- [ ] IP whitelist set to `0.0.0.0/0`
- [ ] Connection string obtained
- [ ] Database seeded locally (run `python seed_data.py`)
- [ ] `MONGO_URI` set in Vercel environment variables
- [ ] `SECRET_KEY` set in Vercel environment variables
- [ ] `FLASK_ENV` set to `production` in Vercel
- [ ] Redeployed to Vercel
- [ ] Tested registration and login

## 🔍 Verify It's Working

After redeployment, check:

1. **Registration page** - Should load without errors
2. **Register a student** - Should create account
3. **Login** - Should work with new account
4. **Admin login** - Should work with `admin`/`admin123`

## ⚠️ Common Mistakes

1. **Forgot to replace `<password>`** in connection string
2. **Didn't add `/olevel_exam`** at the end of connection string
3. **Didn't seed the database** before deploying
4. **Didn't redeploy** after setting environment variables
5. **Wrong IP whitelist** - must be `0.0.0.0/0` for Vercel

## 🆘 Still Not Working?

Check Vercel logs:
```bash
vercel logs
```

Or in Vercel dashboard:
1. Go to "Deployments"
2. Click on latest deployment
3. Click "View Function Logs"
4. Look for MongoDB connection errors

---

**After completing all steps, your app will work perfectly!** 🚀
