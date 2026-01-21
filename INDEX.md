# 📚 Documentation Index

Welcome to the Mock Interview Practice documentation!

## Quick Navigation

### 🚀 Getting Started
- **[QUICKSTART.md](QUICKSTART.md)** - 5-minute setup guide
- **[README.md](README.md)** - Complete documentation
- **Start Scripts:**
  - Windows: `start.ps1`
  - Linux/macOS: `start.sh`

### 📖 Documentation
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System design & architecture
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Complete project overview

### 🔧 Code Files

#### Chrome Extension
- `chrome-extension/manifest.json` - Extension configuration
- `chrome-extension/popup.html` - UI interface
- `chrome-extension/popup.js` - Extension logic
- `chrome-extension/icon*.png` - Extension icons

#### Backend
- `backend/app.py` - FastAPI server
- `backend/requirements.txt` - Python dependencies
- `backend/tts_helper.py` - TTS utilities
- `backend/test_backend.py` - Test suite
- `backend/generate_icons.py` - Icon generator

### 📋 Cheat Sheets

#### Installation Commands
```powershell
# 1. Install Ollama
winget install Ollama.Ollama

# 2. Start Ollama & download model
ollama serve
ollama pull llama3.2:latest

# 3. Setup backend
cd backend
pip install -r requirements.txt

# 4. Start server
python app.py
```

#### Quick Test
```powershell
# Test everything is working
cd backend
python test_backend.py
```

#### Chrome Extension Setup
1. Open `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select `chrome-extension` folder

## Documentation by Topic

### For First-Time Users
1. Read [QUICKSTART.md](QUICKSTART.md)
2. Run the setup commands
3. Load the extension
4. Start your first interview!

### For Developers
1. Read [ARCHITECTURE.md](ARCHITECTURE.md) for system design
2. Read [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) for implementation details
3. Review code files in `chrome-extension/` and `backend/`
4. Run `test_backend.py` to verify setup

### For Troubleshooting
- Check [README.md → Troubleshooting](README.md#troubleshooting)
- Run `backend/test_backend.py` to diagnose issues
- Check server logs in terminal
- Use Chrome DevTools (F12) for extension debugging

## File Structure

```
Mintervier/
├── 📄 README.md                 → Complete guide
├── 📄 QUICKSTART.md             → 5-minute setup
├── 📄 ARCHITECTURE.md           → System architecture
├── 📄 PROJECT_SUMMARY.md        → Project overview
├── 📄 INDEX.md                  → This file
├── 📄 .gitignore                → Git ignore rules
│
├── ⚡ start.ps1                 → Windows startup script
├── ⚡ start.sh                  → Linux/macOS startup script
│
├── 📁 chrome-extension/
│   ├── manifest.json            → Extension config (Manifest V3)
│   ├── popup.html               → UI interface
│   ├── popup.js                 → Extension logic
│   ├── icon16.png               → Small icon
│   ├── icon48.png               → Medium icon
│   ├── icon128.png              → Large icon
│   ├── icon128.svg              → SVG source
│   └── ICONS_README.txt         → Icon generation guide
│
└── 📁 backend/
    ├── app.py                   → FastAPI server
    ├── requirements.txt         → Python dependencies
    ├── tts_helper.py            → TTS utilities
    ├── test_backend.py          → Test suite
    ├── generate_icons.py        → Icon generator
    └── audio/                   → Generated TTS files (runtime)
```

## Technology Stack

| Component | Technology | Documentation |
|-----------|-----------|---------------|
| Extension | Chrome Manifest V3 | [Chrome Docs](https://developer.chrome.com/docs/extensions) |
| Backend | FastAPI | [FastAPI Docs](https://fastapi.tiangolo.com) |
| AI Model | Ollama | [Ollama Docs](https://ollama.ai) |
| TTS | Piper | [Piper GitHub](https://github.com/rhasspy/piper) |
| Server | Uvicorn | [Uvicorn Docs](https://www.uvicorn.org) |

## Common Tasks

### Start Development
```powershell
# Terminal 1: Ollama
ollama serve

# Terminal 2: Backend
cd backend
python app.py

# Chrome: Load extension
```

### Test Backend
```powershell
cd backend
python test_backend.py
```

### Generate Icons
```powershell
cd backend
pip install Pillow
python generate_icons.py
```

### Check Health
```powershell
# Backend health
curl http://localhost:8000/health

# Ollama models
ollama list
```

### View Logs
- Backend: Terminal where `python app.py` is running
- Extension: Chrome DevTools → Console
- Ollama: Terminal where `ollama serve` is running

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | API info |
| `/health` | GET | Health check |
| `/chat` | POST | Send messages |
| `/feedback` | POST | Get feedback |
| `/audio/*` | GET | Serve audio files |

## Support & Help

### Quick Fixes
- **"Cannot connect to Ollama"** → Run `ollama serve`
- **"Model not found"** → Run `ollama pull llama3.2:latest`
- **"Backend not running"** → Run `python app.py` in backend/
- **"Extension not loading"** → Check chrome://extensions for errors

### Testing Tools
- `backend/test_backend.py` - Full backend test
- `/health` endpoint - Quick status check
- Chrome DevTools - Extension debugging

### Resources
- [Ollama Models](https://ollama.ai/library)
- [Piper Voices](https://github.com/rhasspy/piper/releases)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [Chrome Extension Guide](https://developer.chrome.com/docs/extensions/mv3/getstarted/)

## Version Information

- **Project Version**: 1.0.0
- **Chrome Manifest**: V3
- **Python**: 3.10+
- **FastAPI**: 0.109+
- **Default Model**: llama3.2:latest

## Next Steps

After setup, you can:
1. ✅ Practice LeetCode-style interviews
2. 📚 Read [ARCHITECTURE.md](ARCHITECTURE.md) to understand the system
3. 🔧 Modify code to add new features
4. 🌟 Extend with voice input, code editor, etc.

---

**Need help?** Start with [QUICKSTART.md](QUICKSTART.md) for the fastest setup path!
