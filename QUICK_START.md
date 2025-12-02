# O Level Exam Portal - Quick Start Guide

## ⚠️ IMPORTANT: How to Run the Application

### The CSS won't load if you:
- ❌ Open HTML files directly in browser (file:///)
- ❌ Don't have Flask running
- ❌ Don't have Python installed

### ✅ Correct Way to Run:

**Step 1: Install Python**
- Download from https://www.python.org/downloads/
- Install and check "Add Python to PATH"

**Step 2: Install Dependencies**
```bash
cd dark-satellite
python -m pip install -r requirements.txt
```

**Step 3: Start Flask Server**
```bash
python app.py
```

**Step 4: Open in Browser**
```
http://localhost:5000
```
(NOT file:///C:/Users/...)

### Quick Test

If you want to test if CSS works without MongoDB:

```bash
python test_static.py
```

Then open: http://localhost:5000

### Troubleshooting

**CSS not loading?**
1. Make sure Flask is running (you should see "Running on http://127.0.0.1:5000")
2. Open http://localhost:5000 (not the file directly)
3. Check browser console (F12) for errors
4. Clear browser cache (Ctrl+F5)

**Python not found?**
- Install Python from python.org
- Make sure "Add to PATH" was checked during installation
- Restart terminal/command prompt

**Port 5000 already in use?**
- Change PORT in .env file to 5001 or another port
- Or stop other applications using port 5000

### For Vercel Deployment

CSS will work automatically on Vercel. Just follow VERCEL_DEPLOYMENT.md

---

**Remember:** Flask applications must run through a web server, not by opening HTML files directly!
