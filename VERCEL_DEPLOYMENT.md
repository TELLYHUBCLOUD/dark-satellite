# Vercel Deployment Guide for O Level Exam Portal

## ⚠️ IMPORTANT: MongoDB Atlas Required

Vercel is a **serverless platform**, which means:
- No local MongoDB available
- You **MUST** use MongoDB Atlas (cloud database)
- Connection happens on each request (not at startup)

## 🚀 Step-by-Step Deployment

### Step 1: Create MongoDB Atlas Account

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register)
2. Sign up for free (no credit card required)
3. Create a new cluster (choose FREE tier - M0)
4. Wait for cluster to be created (2-3 minutes)

### Step 2: Configure MongoDB Atlas

1. **Create Database User:**
   - Go to "Database Access"
   - Click "Add New Database User"
   - Choose "Password" authentication
   - Username: `examportal` (or your choice)
   - Password: Generate a strong password (save it!)
   - Database User Privileges: "Read and write to any database"
   - Click "Add User"

2. **Whitelist All IPs (for Vercel):**
   - Go to "Network Access"
   - Click "Add IP Address"
   - Click "Allow Access from Anywhere"
   - This adds `0.0.0.0/0` (required for Vercel)
   - Click "Confirm"

3. **Get Connection String:**
   - Go to "Database" → "Connect"
   - Choose "Connect your application"
   - Driver: Python, Version: 3.12 or later
   - Copy the connection string
   - It looks like: `mongodb+srv://examportal:<password>@cluster0.xxxxx.mongodb.net/`
   - **Replace `<password>` with your actual password**
   - **Add database name at the end:** `mongodb+srv://examportal:yourpassword@cluster0.xxxxx.mongodb.net/olevel_exam`

### Step 3: Seed MongoDB Atlas Database

Before deploying, you need to populate your Atlas database with questions and admin.

1. **Update local `.env` file:**
   ```env
   MONGO_URI=mongodb+srv://examportal:yourpassword@cluster0.xxxxx.mongodb.net/olevel_exam
   ```

2. **Run seed script:**
   ```bash
   python seed_data.py
   ```

3. **Verify data:**
   - Go to MongoDB Atlas → "Browse Collections"
   - You should see:
     - `questions` collection (100 documents)
     - `admins` collection (1 document)

### Step 4: Deploy to Vercel

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel:**
   ```bash
   vercel login
   ```

3. **Deploy:**
   ```bash
   cd dark-satellite
   vercel
   ```

4. **Follow prompts:**
   - Set up and deploy? `Y`
   - Which scope? Choose your account
   - Link to existing project? `N`
   - Project name? `olevel-exam-portal` (or your choice)
   - Directory? `./` (current directory)
   - Override settings? `N`

### Step 5: Set Environment Variables in Vercel

After deployment, you need to set environment variables:

1. Go to your Vercel dashboard: https://vercel.com/dashboard
2. Select your project
3. Go to "Settings" → "Environment Variables"
4. Add these variables:

   | Name | Value |
   |------|-------|
   | `FLASK_ENV` | `production` |
   | `SECRET_KEY` | Generate a random string (e.g., `openssl rand -hex 32`) |
   | `MONGO_URI` | Your MongoDB Atlas connection string |

5. Click "Save"

### Step 6: Redeploy

After setting environment variables, redeploy:

```bash
vercel --prod
```

### Step 7: Test Your Deployment

1. Vercel will give you a URL like: `https://olevel-exam-portal.vercel.app`
2. Visit the URL
3. Test the following:
   - ✅ Home page loads
   - ✅ Register a student
   - ✅ Login with student credentials
   - ✅ Take exam (timer works)
   - ✅ Submit and view results
   - ✅ Admin login (`admin` / `admin123`)
   - ✅ Admin dashboard shows data

## 🔧 Troubleshooting

### Error: "Connection refused"
- **Cause:** MongoDB Atlas connection string not set in Vercel
- **Fix:** Set `MONGO_URI` environment variable in Vercel dashboard

### Error: "Authentication failed"
- **Cause:** Wrong password in connection string
- **Fix:** Verify password in MongoDB Atlas and update `MONGO_URI`

### Error: "IP not whitelisted"
- **Cause:** Vercel IPs not allowed in MongoDB Atlas
- **Fix:** Add `0.0.0.0/0` to Network Access in Atlas

### Error: "Database not found"
- **Cause:** Database name missing from connection string
- **Fix:** Ensure connection string ends with `/olevel_exam`

### No questions in exam
- **Cause:** Database not seeded
- **Fix:** Run `python seed_data.py` with Atlas connection string

### Admin login fails
- **Cause:** Admin not created in Atlas database
- **Fix:** Run `python seed_data.py` to create default admin

## 📝 Important Notes

1. **Free Tier Limits:**
   - MongoDB Atlas free tier: 512 MB storage
   - Vercel free tier: 100 GB bandwidth/month
   - Both are sufficient for college projects

2. **Connection String Security:**
   - Never commit `.env` file to Git
   - Never share your MongoDB password
   - Use environment variables in Vercel

3. **Database Persistence:**
   - Data in MongoDB Atlas persists between deployments
   - You only need to seed once

4. **Cold Starts:**
   - First request after inactivity may be slow (2-3 seconds)
   - This is normal for serverless platforms

## 🎉 Success!

Once deployed, you'll have:
- ✅ Live URL accessible from anywhere
- ✅ Cloud database (MongoDB Atlas)
- ✅ Automatic HTTPS
- ✅ Global CDN
- ✅ Perfect for college project submission

## 📞 Quick Reference

**MongoDB Atlas:** https://cloud.mongodb.com
**Vercel Dashboard:** https://vercel.com/dashboard
**Default Admin:** `admin` / `admin123` (change after first login!)

---

**Need help?** Check the error logs in Vercel dashboard under "Deployments" → Click deployment → "View Function Logs"
