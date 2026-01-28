# 🚀 Quick Start Guide

## Fastest way to get started (5 minutes)

### 1. Install Ollama
```powershell
# Download and install from https://ollama.ai/download
# Or use winget:
winget install Ollama.Ollama
```

### 2. Start Ollama and Download Model
```powershell
# Terminal 1: Start Ollama service
ollama serve

# Terminal 2: Download AI model (one-time, ~2GB)
ollama pull llama3.2:latest
```

### 3. Setup Backend
```powershell
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Start server
python app.py
```

### 4. Load Chrome Extension
1. Open Chrome → `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select the `chrome-extension` folder
5. Click the 🎯 icon in Chrome toolbar

### 5. Start Interview!
- Click "Start Interview"
- Answer the LeetCode question
- Get AI feedback

---

## Optional: Enable TTS (Text-to-Speech)

```powershell
# Install Piper
pip install piper-tts

# Test it
cd backend
python tts_helper.py "Hello world"
```

---

## Troubleshooting One-Liners

```powershell
# Check if Ollama is running
ollama list

# Check if FastAPI is running
curl http://localhost:8000/health

# Check if Piper is installed
piper --version

# Restart everything
# Terminal 1:
ollama serve

# Terminal 2:
cd backend
python app.py
```

---

## Files You Need

**Chrome Extension:**
- ✅ `chrome-extension/manifest.json`
- ✅ `chrome-extension/popup.html`
- ✅ `chrome-extension/popup.js`
- ✅ `chrome-extension/icon128.svg`

**Backend:**
- ✅ `backend/app.py`
- ✅ `backend/requirements.txt`
- ✅ `backend/tts_helper.py`

**Documentation:**
- ✅ `README.md` (full guide)
- ✅ `QUICKSTART.md` (this file)

---

Done! Start interviewing in 5 minutes! 🎯
