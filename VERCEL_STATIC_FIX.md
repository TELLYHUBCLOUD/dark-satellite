# Vercel Deployment - Static Files Fix

## Issue: CSS Not Loading on Vercel

If your CSS isn't loading on Vercel, follow these steps:

### Solution 1: Update vercel.json (Already Done)

The `vercel.json` has been updated to properly route static files.

### Solution 2: Redeploy to Vercel

```bash
vercel --prod
```

### Solution 3: Verify Static Files in Vercel Dashboard

1. Go to your Vercel project dashboard
2. Click on "Deployments"
3. Click on your latest deployment
4. Check "Source" tab to verify `static/css/style.css` is included

### Solution 4: Check Browser Console

1. Open your Vercel URL
2. Press F12 to open Developer Tools
3. Go to "Console" tab
4. Look for any 404 errors for CSS files
5. Go to "Network" tab and check if `style.css` loads

### Solution 5: Force Clear Cache

On your Vercel site:
- Press `Ctrl + Shift + R` (Windows/Linux)
- Press `Cmd + Shift + R` (Mac)

### Solution 6: Check Environment Variables

Make sure you've set in Vercel dashboard:
- `FLASK_ENV` = `production`
- `SECRET_KEY` = (your secret key)
- `MONGO_URI` = (your MongoDB Atlas connection string)

### Solution 7: Alternative - Use CDN for Static Files

If static files still don't work, you can use a CDN. Add this to your HTML `<head>`:

```html
<!-- Use CDN as fallback -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/yourusername/yourrepo@main/static/css/style.css">
```

### Debugging Commands

```bash
# Check if static files are in deployment
vercel ls

# View deployment logs
vercel logs

# Redeploy with verbose output
vercel --prod --debug
```

### Common Vercel Issues

1. **Static folder not included**: Make sure `static/` folder is in your repo
2. **Wrong route configuration**: Check `vercel.json` routes
3. **Cache issues**: Clear browser cache
4. **Build errors**: Check Vercel deployment logs

### Quick Fix: Inline Critical CSS

As a temporary solution, you can inline critical CSS in your HTML templates:

```html
<style>
  /* Copy critical CSS here */
  body { background: #0f172a; color: #f1f5f9; }
  /* ... */
</style>
```

---

**After updating vercel.json, redeploy:**

```bash
vercel --prod
```

The CSS should now load properly!
