# 🚀 Nexus AI - Complete Usage Guide

## 📋 Table of Contents
1. [First Time Setup](#first-time-setup)
2. [Starting Nexus AI](#starting-nexus-ai)
3. [Using the Interface](#using-the-interface)
4. [Feature Examples](#feature-examples)
5. [Troubleshooting](#troubleshooting)

---

## 🎯 First Time Setup

### Step 1: Install Ollama
```bash
# Download from: https://ollama.ai
# After installation, open terminal and run:
ollama serve
ollama pull mistral
```

### Step 2: Verify Python Dependencies
```bash
cd "d:\Nexus AI"
python test_setup.py
```

### Step 3: Install Missing Dependencies (if any)
```bash
pip install flask flask-cors playwright requests
playwright install chrome
```

---

## 🚀 Starting Nexus AI

### Method 1: Using Batch Files (Easiest)

1. **Start Backend:**
   - Double-click `start_backend.bat`
   - Wait for "Running on http://localhost:5000"
   - Keep this window open

2. **Open Frontend:**
   - Double-click `open_frontend.bat`
   - Browser will open automatically

### Method 2: Manual Start

1. **Terminal 1 - Start Ollama:**
```bash
ollama serve
```

2. **Terminal 2 - Start Backend:**
```bash
cd "d:\Nexus AI\backend"
python app.py
```

3. **Browser:**
   - Open `d:\Nexus AI\frontend\index.html`
   - Or use local server:
```bash
cd "d:\Nexus AI\frontend"
python -m http.server 8000
# Visit: http://localhost:8000
```

---

## 💬 Using the Interface

### Main Components

#### 1️⃣ **Sidebar**
- **New Chat** button - Start fresh conversation
- **Chat History** - Previous conversations
- **User Info** - Your profile and status

#### 2️⃣ **Welcome Screen** (shows on new chat)
- **Nexus AI Logo** - Animated gradient logo
- **Feature Cards** - Overview of capabilities
- **Example Prompts** - Click to try instantly

#### 3️⃣ **Message Area**
- **User Messages** - Your questions (right side)
- **Assistant Messages** - Nexus AI responses (left side)
- **Status Badges** - 🧠 Mistral AI, 🌐 Web Search
- **Sources** - Links to information sources

#### 4️⃣ **Input Area**
- **Text Box** - Type your question
- **Send Button** - Submit question
- **Shortcuts:**
  - `Enter` = Send
  - `Shift + Enter` = New line

---

## 🎨 Feature Examples

### 🔥 Today's Information (Priority +1000)
```
❓ What's the weather today?
❓ Today's news headlines
❓ Current stock price of Apple
```
**Result:** Gets latest information with high priority

---

### 📅 Specific Date Queries (Priority +3000)
```
❓ What's happening on October 10, 2025?
❓ Events on 10 oct 2025
❓ December 25, 2024 forecast
```
**Result:** Exact date match with 📅 visual marker

---

### 📚 Historical Ranges (Priority +5000 Supreme)
```
❓ What happened between 2003 and 2006?
❓ Movies from 2019 to 2023
❓ Events from 2001 through 2005
```
**Result:** Wikipedia articles prioritized, comprehensive coverage

---

### 🧠 General Knowledge (Local AI)
```
❓ What is machine learning?
❓ Explain quantum physics
❓ How does photosynthesis work?
```
**Result:** Fast response from Mistral model

---

### 🌐 Current Information (Web Search)
```
❓ Who is the current president of USA?
❓ Latest iPhone price
❓ Current population of India
```
**Result:** Web search if Mistral is uncertain

---

## 🎯 Understanding Status Indicators

### 🧠 **Mistral AI**
- Local AI model response
- Fast, private, offline-capable
- Shows when Mistral answered

### 🌐 **Web Search**
- DuckDuckGo search used
- Online information gathered
- Shows when web search performed

### 📚 **Sources**
- Links to information sources
- Click to verify information
- Wikipedia sources specially marked

### 🤔 **Thinking...**
- Processing your question
- Shows animated dots
- Backend is working

---

## 🛠️ Troubleshooting

### ❌ "Backend not running" Error

**Solution:**
1. Open `start_backend.bat`
2. Wait for "Running on http://localhost:5000"
3. Refresh browser

---

### ❌ "Ollama connection failed"

**Solution:**
```bash
# Terminal 1:
ollama serve

# Terminal 2:
ollama pull mistral

# Verify:
ollama list
```

---

### ❌ Chrome won't open

**Solution:**
```bash
playwright install chrome
```

Or edit `backend/agent_step3.py`:
```python
channel="msedge"  # Use Edge instead
```

---

### ❌ CAPTCHA appearing

**Should not happen!** Nexus AI uses DuckDuckGo which is CAPTCHA-free.

If it happens:
1. Check `backend/agent_step3.py` uses DuckDuckGo
2. Verify anti-detection scripts loaded
3. Try incognito/private mode

---

### ❌ Slow responses

**Normal timing:**
- Local AI: 3-5 seconds
- Web Search: 10-20 seconds

**If slower:**
1. Check internet connection
2. Verify Ollama is running
3. Close unnecessary tabs
4. Check CPU usage

---

### ❌ Port 5000 already in use

**Solution:**

Edit `backend/app.py`:
```python
app.run(host='0.0.0.0', port=5001)  # Change port
```

Edit `frontend/script.js`:
```javascript
const API_URL = 'http://localhost:5001';  # Match port
```

---

## 💡 Pro Tips

### 🎯 **Get Better Results**

1. **Be Specific:**
   - ❌ "weather"
   - ✅ "weather today in Hyderabad"

2. **Use Date Formats:**
   - ✅ "10 oct 2025"
   - ✅ "October 10, 2025"
   - ✅ "2003 to 2006"

3. **Historical Research:**
   - Add "wikipedia" for better results
   - Use year ranges: "2001-2005"

4. **Current Info:**
   - Use "today", "current", "latest"
   - Specify location when needed

---

### ⌨️ **Keyboard Shortcuts**

- `Enter` - Send message
- `Shift + Enter` - New line
- `Ctrl + L` - Focus input (browser)
- `F5` - Refresh page (browser)

---

### 🎨 **Interface Tips**

1. **New Chat:**
   - Click "New Chat" to start fresh
   - History saved automatically

2. **Example Prompts:**
   - Click welcome screen examples
   - Customize for your needs

3. **Sources:**
   - Click source links to verify
   - Wikipedia = most reliable

4. **Status Badges:**
   - Watch for status changes
   - Understand information source

---

## 📊 Performance Guide

### Expected Response Times

| Query Type | Response Time | Method |
|-----------|---------------|--------|
| General Knowledge | 3-5 seconds | 🧠 Mistral |
| Today's Info | 10-15 seconds | 🌐 Web Search |
| Historical Range | 15-25 seconds | 📚 Wikipedia |
| Specific Date | 10-20 seconds | 🌐 Web Search |

---

### System Requirements

- **CPU:** Dual-core 2.0 GHz (recommended 4-core)
- **RAM:** 4 GB minimum (8 GB recommended)
- **Storage:** 10 GB free space
- **Browser:** Chrome, Edge, Firefox (latest)
- **Internet:** 5 Mbps (for web search)

---

## 🎓 Advanced Usage

### Custom Date Formats
```python
# Nexus AI understands:
"10 oct 2025"
"October 10, 2025"
"10/10/2025"
"2025-10-10"
```

### Range Query Formats
```python
# All work:
"2003 to 2006"
"2003-2006"
"2003 through 2006"
"from 2003 till 2006"
```

### Priority Boosting
```
🥇 +5000: Wikipedia + Historical Range
🥈 +3000: Exact Date Match
🥉 +1000: Recent/Today
   +500: Wikipedia General
   +0: Standard Results
   -800: Old Content
```

---

## 🔧 Configuration

### Change Search Engine
Edit `backend/agent_step3.py`:
```python
# Current: DuckDuckGo (CAPTCHA-free)
# Not recommended: Google, Bing (have CAPTCHA)
```

### Adjust Browser Mode
```python
headless=False  # Visible browser
headless=True   # Hidden browser (faster)
```

### Modify Priorities
```python
# In extract_answer_from_results():
if is_wikipedia and is_range_query:
    priority += 5000  # Adjust this
```

---

## 📞 Getting Help

### Check Logs
```bash
# Backend logs
cd "d:\Nexus AI\backend"
python app.py
# Watch console output

# Browser console
# Press F12 in browser
# Check Console tab
```

### Verify Setup
```bash
cd "d:\Nexus AI"
python test_setup.py
```

### Health Check
```bash
# Browser or curl:
http://localhost:5000/health

# Should return:
{"status": "ok", "message": "Nexus AI Backend is running"}
```

---

## 🎉 Enjoy Nexus AI!

You now have a powerful AI assistant that combines:
- 🧠 Local AI (privacy & speed)
- 🌐 Web search (current info)
- 📚 Wikipedia (research)
- 🔥 Smart prioritization (accuracy)

**Start asking questions and explore the power of Nexus AI!**

---

## 📝 Quick Start Checklist

- [ ] Ollama installed and running
- [ ] Python dependencies installed
- [ ] Backend started (`start_backend.bat`)
- [ ] Frontend opened (`open_frontend.bat`)
- [ ] First question asked successfully
- [ ] Sources verified
- [ ] Features tested (today, dates, ranges)

---

**Happy Exploring! 🚀**

*Made with ❤️ for intelligent, privacy-focused AI assistance*
