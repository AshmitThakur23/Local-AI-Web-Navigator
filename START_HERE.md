# 🚀 NEXUS AI - START HERE!

## ✨ **ONE-CLICK START - Super Easy!**

### 🎯 Just Double-Click This File:
```
START_NEXUS_AI.bat
```

**That's it!** Everything will start automatically! 🎉

---

## 📋 What Happens Automatically:

1. ✅ **Checks Ollama** - Starts if needed
2. ✅ **Starts Backend** - Opens in new window (keep it open!)
3. ✅ **Opens Browser** - Frontend loads automatically

---

## ⚠️ IMPORTANT - READ THIS!

### The Backend Window MUST Stay Open!

When you run `START_NEXUS_AI.bat`, you'll see **2-3 windows open**:

1. **Startup Window** (this closes automatically)
2. **Backend Server Window** ⚠️ **KEEP THIS OPEN!**
   - Green or black text
   - Says "Nexus AI Backend - Keep This Open"
   - Shows "Running on http://localhost:5000"
3. **Ollama Window** (if it wasn't running)
4. **Browser** (frontend interface)

### ⚠️ If You Close the Backend Window:
- ❌ Frontend will show "backend server is running" error
- ❌ No questions will be answered
- ✅ Just run `START_NEXUS_AI.bat` again to restart!

---

## 🎯 Quick Start Steps:

1. **Double-click** `START_NEXUS_AI.bat`
2. **Wait** ~10 seconds for everything to start
3. **Browser opens** automatically with Nexus AI
4. **Start asking** questions! 🎉

---

## 💡 Common Issues & Solutions:

### ❌ "Backend server is running" error in browser

**Cause:** Backend window was closed or didn't start

**Solution:**
1. Look for the backend window (green/black text)
2. If you don't see it, run `START_NEXUS_AI.bat` again
3. Wait 10 seconds, then refresh browser

---

### ❌ Ollama not starting

**Solution:**
1. Download from: https://ollama.ai
2. Install it
3. Run: `ollama pull mistral`
4. Then run `START_NEXUS_AI.bat` again

---

### ❌ Port 5000 already in use

**Solution:**
1. Close any backend windows
2. Run this to kill the process:
   ```powershell
   Get-Process -Name python | Where-Object {$_.MainWindowTitle -like "*Backend*"} | Stop-Process
   ```
3. Run `START_NEXUS_AI.bat` again

---

## 🖥️ What You'll See:

### Startup Window:
```
═══════════════════════════════════════
    NEXUS AI - ONE-CLICK STARTUP
═══════════════════════════════════════

[1/3] 🧠 Checking Ollama...
   ✅ Ollama is already running!

[2/3] 🔧 Starting Flask Backend Server...
   ✅ Backend server starting on http://localhost:5000
   ⏳ Waiting 8 seconds for server to initialize...
   ✅ Backend is ready!

[3/3] 🌐 Opening Frontend Interface...
   ✅ Frontend opened in browser!

═══════════════════════════════════════
        ✅ NEXUS AI IS READY! ✅
═══════════════════════════════════════
```

### Backend Window (KEEP OPEN!):
```
════════════════════════════════════
   NEXUS AI BACKEND SERVER
   http://localhost:5000
   ⚠️  Keep this window OPEN!
════════════════════════════════════

🚀 Starting Nexus AI Backend...
📍 Server running on http://localhost:5000
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

### Browser (Frontend):
- Beautiful dark theme interface
- Chat interface like ChatGPT
- Type questions and get answers!

---

## 🎓 First Time Setup (One-Time):

If this is your **first time**, do this once:

### 1. Install Ollama:
```bash
# Download from: https://ollama.ai
# After install:
ollama serve
ollama pull mistral
```

### 2. Install Python Dependencies:
```bash
cd "d:\Nexus AI"
pip install flask flask-cors playwright requests
playwright install chrome
```

### 3. Then Start:
```bash
# Double-click:
START_NEXUS_AI.bat
```

---

## 📊 System Check:

Run this to verify everything is ready:
```bash
python test_setup.py
```

Should show all ✅ green checkmarks.

---

## 🎯 Usage Flow:

```
1. Double-click START_NEXUS_AI.bat
   ↓
2. Wait ~10 seconds
   ↓
3. Browser opens with Nexus AI
   ↓
4. Backend window stays open (green text)
   ↓
5. Type question: "What's the weather today?"
   ↓
6. Get intelligent answer!
   ↓
7. Keep asking questions...
   ↓
8. When done: Close backend window to stop
```

---

## 🛑 How to Stop Nexus AI:

1. **Close the Backend Window** (green/black one)
   - Or press `Ctrl+C` in that window
2. **Close the Browser** (optional)
3. **Ollama can keep running** for next time

---

## 💻 Alternative: Manual Start

If the batch file doesn't work:

### Terminal 1 - Ollama:
```bash
ollama serve
```

### Terminal 2 - Backend:
```bash
cd "d:\Nexus AI\backend"
python app.py
```

### Browser:
Open `d:\Nexus AI\frontend\index.html`

---

## 🎨 Features:

✅ **Smart Local AI** - Mistral via Ollama  
✅ **Web Search** - CAPTCHA-free DuckDuckGo  
✅ **Wikipedia Priority** - Best for research  
✅ **Today First** - Current info prioritized  
✅ **Specific Dates** - Exact date matching  
✅ **ChatGPT UI** - Beautiful dark theme  

---

## 📞 Need Help?

### Quick Checks:
```bash
# Is backend running?
curl http://localhost:5000/health

# Is Ollama running?
ollama list

# Check all systems:
python test_setup.py
```

### Documentation:
- **This file** - Quick start
- **USAGE_GUIDE.md** - Detailed guide
- **README.md** - Full documentation
- **ONE_CLICK_START.md** - Startup details

---

## 🎉 You're Ready!

**Just double-click `START_NEXUS_AI.bat` and enjoy!** 🚀

Remember:
- ✅ Backend window must stay open
- ✅ Wait ~10 seconds for startup
- ✅ Browser opens automatically
- ✅ Start asking questions!

---

**Made with ❤️ for maximum convenience**

*One-Click Startup - Keep Backend Window Open!*
