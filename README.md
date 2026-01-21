# 🎯 Mock Interview Practice - Chrome Extension

A minimal Chrome extension for SWE intern LeetCode-style interview practice using a local Python backend with FastAPI, Ollama AI, and Piper TTS.

## 📁 Project Structure

```
Mintervier/
├── chrome-extension/        # Chrome extension files
│   ├── manifest.json       # Extension manifest (V3)
│   ├── popup.html          # Popup UI with chat interface
│   ├── popup.js            # Extension JavaScript logic
│   └── icon128.svg         # Extension icon
│
└── backend/                 # FastAPI backend
    ├── app.py              # Main FastAPI application
    ├── tts_helper.py       # Piper TTS helper utilities
    ├── requirements.txt    # Python dependencies
    └── audio/              # Generated TTS audio files (created at runtime)
```

## ✨ Features

- **Chrome Extension (Manifest V3)**
  - Clean chat-based interview interface
  - Select interview type (SWE Intern) and question type (LeetCode DSA)
  - Display AI-generated questions with TTS audio playback
  - End-of-session feedback with strengths, weaknesses, and actionable improvements

- **FastAPI Backend**
  - POST `/chat` - Send messages to AI interviewer
  - POST `/feedback` - Get end-of-session feedback
  - GET `/health` - Check server and Ollama status
  - Async endpoints for performance
  - In-memory session management
  - CORS enabled for Chrome extension

- **AI Integration**
  - Local Ollama LLM (GPT-OSS-7B or Llama 3.2)
  - LeetCode-style interview conversation flow
  - Contextual hints without giving away solutions
  - Tracks candidate progress for feedback

- **TTS (Text-to-Speech)**
  - Local Piper TTS for audio generation
  - AI responses converted to speech
  - Audio served via FastAPI static files
  - Auto-play in extension popup

## 🚀 Setup Instructions

### Prerequisites

1. **Python 3.10+**
   ```powershell
   python --version
   ```

2. **Ollama** (Local LLM runtime)
   - Download and install: https://ollama.ai/download
   - Install from PowerShell:
     ```powershell
     winget install Ollama.Ollama
     ```

3. **Piper TTS** (Optional but recommended)
   - Install via pip:
     ```powershell
     pip install piper-tts
     ```
   - Or download from: https://github.com/rhasspy/piper/releases

4. **Google Chrome** (for extension)

---

### Backend Setup

#### Step 1: Install Ollama and Pull Model

```powershell
# Start Ollama service (if not running)
ollama serve

# In a new terminal, pull the AI model
ollama pull llama3.2:latest
```

> **Note:** You can use other models like `llama3.1`, `mistral`, or `codellama`. Update the `OLLAMA_MODEL` in `app.py` if using a different model.

#### Step 2: Install Python Dependencies

```powershell
cd backend

# Create virtual environment (recommended)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

#### Step 3: Test Piper TTS (Optional)

```powershell
# Check if Piper is installed
python tts_helper.py

# Test TTS generation
python tts_helper.py "Hello, this is a test of the interview system"
# Creates test_speech.wav if successful
```

#### Step 4: Start FastAPI Server

```powershell
# Make sure you're in the backend directory
cd backend

# Run the server
python app.py

# Or use uvicorn directly
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Server will start at: **http://localhost:8000**

Check health: **http://localhost:8000/health**

---

### Chrome Extension Setup

#### Step 1: Load Extension in Chrome

1. Open Chrome and go to: `chrome://extensions/`

2. Enable **Developer mode** (toggle in top-right)

3. Click **"Load unpacked"**

4. Navigate to and select the `chrome-extension` folder

5. The extension should now appear in your extensions list

#### Step 2: Pin Extension (Optional)

1. Click the puzzle icon in Chrome toolbar
2. Find "Mock Interview Practice"
3. Click the pin icon to keep it visible

---

## 🎮 Usage

### Starting an Interview

1. **Make sure backend is running**:
   - Ollama service: `ollama serve`
   - FastAPI server: `python app.py` (in backend folder)

2. **Open the extension** by clicking the 🎯 icon in Chrome

3. **Configure interview**:
   - Interview Type: SWE Intern
   - Question Type: LeetCode-style DSA

4. **Click "Start Interview"**

5. The AI interviewer will:
   - Introduce itself
   - Ask the first LeetCode-style question
   - Play audio (if Piper TTS is available)

### During the Interview

- **Type your approach** or solution in the text box
- **Ask for hints** if you're stuck (e.g., "Can you give me a hint?")
- **Clarify the question** (e.g., "What are the input constraints?")
- The AI will respond with guidance without giving away the solution

### Ending the Interview

1. Click **"End Interview"** button

2. The AI will generate feedback with:
   - **Strengths**: What you did well
   - **Weaknesses**: Areas to improve
   - **Actionable Improvement**: One specific recommendation

3. Click **"Start New Interview"** to begin a new session

---

## 🔧 Configuration

### Changing the AI Model

Edit `backend/app.py`:

```python
OLLAMA_MODEL = "llama3.2:latest"  # Change to your preferred model
```

Available models:
- `llama3.2:latest` (recommended, ~3GB)
- `llama3.1:latest` (~4.7GB)
- `mistral:latest` (~4GB)
- `codellama:latest` (~4GB, good for coding)

Pull new models:
```powershell
ollama pull <model-name>
```

### Changing TTS Voice

Edit `backend/app.py`:

```python
PIPER_VOICE_MODEL = "en_US-lessac-medium"  # Change voice
```

Other voices:
- `en_US-amy-medium`
- `en_GB-alan-medium`
- `en_US-joe-medium`

Download voices from: https://github.com/rhasspy/piper/releases

### Disabling TTS

TTS is optional. If Piper is not installed:
- The extension will still work
- Only text will be displayed (no audio)
- No errors will occur

---

## 🧪 Testing

### Test Backend

```powershell
# Health check
curl http://localhost:8000/health

# Test chat endpoint
curl -X POST http://localhost:8000/chat `
  -H "Content-Type: application/json" `
  -d '{
    "messages": [
      {"role": "system", "content": "You are a technical interviewer"},
      {"role": "user", "content": "Ask me a LeetCode easy question"}
    ],
    "session_id": "test123"
  }'
```

### Test TTS

```powershell
cd backend
python tts_helper.py "This is a test of the text to speech system"
```

---

## 🐛 Troubleshooting

### Backend won't start

**Error: "Cannot connect to Ollama"**
```powershell
# Make sure Ollama is running
ollama serve

# Check if model is downloaded
ollama list
ollama pull llama3.2:latest
```

**Error: "Port 8000 already in use"**
```powershell
# Find and kill process using port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or change port in app.py
uvicorn.run(app, host="0.0.0.0", port=8001)
```

### Extension issues

**Error: "Could not connect to backend"**
- Make sure FastAPI server is running: `http://localhost:8000`
- Check browser console (F12) for detailed errors
- Verify CORS is enabled in `app.py`

**Audio not playing**
- Check if Piper is installed: `piper --version`
- TTS is optional; the extension works without it
- Check browser audio permissions

### TTS issues

**Piper not found**
```powershell
# Install Piper
pip install piper-tts

# Or download binary from GitHub
# https://github.com/rhasspy/piper/releases
```

**Voice model not found**
- Default voice should work with `pip install piper-tts`
- Download additional voices from Piper releases page
- Update `PIPER_VOICE_MODEL` in `app.py`

---

## 🔄 Future Extensions

This project is designed to be easily extensible:

### Add Voice Input
- Use Web Speech API in Chrome extension
- Add POST `/transcribe` endpoint in backend
- Use Whisper for local speech-to-text

### Replace Backend
- Node.js + Express.js version
- Use OpenAI API instead of Ollama
- Add database for session persistence

### Add More Interview Types
- System design interviews
- Behavioral questions
- Frontend coding challenges

### Enhanced Features
- Code editor in popup
- Syntax highlighting
- Test case validation
- Multi-round interviews

---

## 📝 API Documentation

### POST /chat

Send a message to the AI interviewer.

**Request:**
```json
{
  "messages": [
    {"role": "system", "content": "System prompt"},
    {"role": "user", "content": "User message"}
  ],
  "session_id": "unique-session-id"
}
```

**Response:**
```json
{
  "message": "AI response text",
  "audio_url": "/audio/speech_123.wav"
}
```

### POST /feedback

Get end-of-session feedback.

**Request:**
```json
{
  "messages": [...],
  "session_id": "unique-session-id"
}
```

**Response:**
```json
{
  "feedback": {
    "strengths": "Good problem-solving approach...",
    "weaknesses": "Could improve time complexity analysis...",
    "improvement": "Practice more dynamic programming problems"
  }
}
```

### GET /health

Check server health and Ollama connection.

**Response:**
```json
{
  "status": "healthy",
  "ollama": "connected",
  "sessions": 3
}
```

---

## 📦 Dependencies

### Backend
- **FastAPI** - Web framework
- **Uvicorn** - ASGI server
- **httpx** - Async HTTP client for Ollama
- **pydantic** - Data validation
- **piper-tts** - Text-to-speech (optional)

### Chrome Extension
- No external dependencies (vanilla JavaScript)

### External Services
- **Ollama** - Local LLM runtime (required)
- **Piper** - Local TTS (optional)

---

## 🔒 Privacy & Security

✅ **Fully Local** - All data stays on your machine
- No cloud API calls
- No data collection
- No internet required (after model downloads)

✅ **Free & Open Source**
- All components are free
- No API keys needed
- No subscription costs

---

## 📄 License

This project is provided as-is for educational purposes.

---

## 🤝 Contributing

This is a minimal starter template. Feel free to:
- Add new features
- Improve the UI
- Add more interview types
- Optimize performance
- Share improvements

---

## 💡 Tips

1. **First run may be slow** - Ollama needs to load the model into memory

2. **Use smaller models** for faster responses:
   - `llama3.2:1b` (1GB, very fast)
   - `qwen2.5:0.5b` (0.5GB, ultra fast)

3. **Disable TTS** if you don't need audio:
   - Significantly faster responses
   - Less disk space used

4. **Clear audio files** periodically:
   ```powershell
   rm backend/audio/*.wav
   ```

5. **Monitor Ollama** resource usage:
   - Ollama uses GPU if available (CUDA/Metal)
   - Falls back to CPU (slower)

---

## 📞 Support

If you encounter issues:

1. Check **Troubleshooting** section above
2. Verify all prerequisites are installed
3. Check terminal logs for error messages
4. Ensure Ollama service is running
5. Test backend independently before using extension

---

**Happy interviewing! 🚀**
