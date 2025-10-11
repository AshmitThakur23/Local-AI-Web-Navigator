# 🚀 ONE-CLICK STARTUP GUIDE

## ⚡ Super Easy Start - Just One Command!

### Windows Users:
**Double-click this file:**
```
START_NEXUS_AI.bat
```

### Python Users (Any OS):
**Run this command:**
```bash
python start_nexus_ai.py
```

---

## ✨ What It Does Automatically:

1. ✅ **Checks Ollama** - Starts it if not running
2. ✅ **Starts Backend** - Flask server on port 5000
3. ✅ **Opens Frontend** - Browser opens automatically

**That's it!** Everything starts with ONE command! 🎉

---

## 🎯 What You'll See:

```
════════════════════════════════════════
    NEXUS AI - ONE-CLICK STARTUP
════════════════════════════════════════

[1/3] 🧠 Checking Ollama...
   ✅ Ollama is already running!

[2/3] 🔧 Starting Flask Backend Server...
   ✅ Backend server starting on http://localhost:5000
   ⏳ Waiting 3 seconds for server to initialize...
   ✅ Backend is ready!

[3/3] 🌐 Opening Frontend Interface...
   ✅ Frontend opened in browser!

════════════════════════════════════════
        ✅ NEXUS AI IS READY! ✅
════════════════════════════════════════
```

---

## 📊 What Runs:

| Component | Window | Status |
|-----------|--------|--------|
| Ollama Server | New window | Background |
| Backend API | New window | Port 5000 |
| Frontend | Browser | Auto-opens |

---

## 💡 Usage Tips:

### ✅ Normal Operation:
- **Start:** Run `START_NEXUS_AI.bat` (once)
- **Use:** Ask questions in browser
- **Stop:** Close backend window

### 🔄 Restart:
- Just run `START_NEXUS_AI.bat` again
- It checks what's running and starts what's needed

### 🛑 Stop Everything:
- Close the backend window (black console)
- Ollama can keep running for next time

---

## ⚠️ Troubleshooting:

### "Ollama is not running"
**Solution:** Script will try to start it automatically
- If fails, run manually: `ollama serve`

### "Backend won't start"
**Check:**
1. Port 5000 is free: `netstat -ano | findstr :5000`
2. Python installed: `python --version`
3. Dependencies: `pip install flask flask-cors`

### "Frontend won't open"
**Solution:**
- Manually open: `d:\Nexus AI\frontend\index.html`
- Or navigate in browser to the file

---

## 🎊 First Time Setup (One-Time Only):

If this is your first time:

1. **Install Ollama:**
   - Download: https://ollama.ai
   - Run: `ollama pull mistral`

2. **Install Dependencies:**
   ```bash
   cd "d:\Nexus AI"
   pip install flask flask-cors playwright requests
   playwright install chrome
   ```

3. **Then Start:**
   ```bash
   # Just double-click:
   START_NEXUS_AI.bat
   ```

---

## 📝 Advanced Options:

### Start in Background (Headless):
Edit `backend/agent_step3.py`:
```python
headless=True  # Change to True
```

### Change Port:
Edit `backend/app.py`:
```python
app.run(port=5001)  # Change from 5000
```
Also update `frontend/script.js`:
```javascript
const API_URL = 'http://localhost:5001';
```

---

## 🔍 Health Check:

After starting, verify everything:

```bash
# Check Ollama
curl http://127.0.0.1:11434/api/tags

# Check Backend
curl http://localhost:5000/health

# Should return:
{"status": "ok", "message": "Nexus AI Backend is running"}
```

---

## 🎯 Example Usage Flow:

```
1. Double-click START_NEXUS_AI.bat
2. Wait 10 seconds (automatic setup)
3. Browser opens with Nexus AI
4. Type question: "What's the weather today?"
5. Get answer with sources!
```

---

## 📞 Need Help?

### Quick Diagnostics:
```bash
python test_setup.py
```

### Documentation:
- **Full Guide:** USAGE_GUIDE.md
- **Quick Start:** QUICK_START.txt
- **Project Info:** README.md

---

## 🌟 That's It!

**One command starts everything:**
- ✅ No manual Ollama start
- ✅ No manual backend start
- ✅ No manual browser open
- ✅ Everything automatic!

**Just run `START_NEXUS_AI.bat` and you're ready!** 🚀

---

**Made with ❤️ for maximum convenience**

*Version: 1.0.0*  
*One-Click Startup - October 2024*
