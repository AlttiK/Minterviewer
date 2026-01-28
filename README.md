# Minterviewer - Chrome Extension
### Mock Interview Practice

## Features

- **Chrome Extension (Manifest V3)**
  - Clean chat-based interview interface
  - Uses random Leetcode problem from Neetcode 150
  - Display AI-generated questions with TTS audio playback
  - End-of-session feedback with strengths, weaknesses, and actionable improvements

- **FastAPI Backend**
  - POST `/chat` - Send messages to AI interviewer
  - POST `/feedback` - Get end-of-session feedback
  - GET `/health` - Check server and Ollama status
  - Async endpoints for performance

- **AI Integration**
  - Local Ollama LLM Llama 3.2
  - LeetCode-style interview conversation flow
  - Tracks candidate progress for feedback

- **TTS (Text-to-Speech)**
  - Local Piper TTS for audio generation
  - AI responses converted to speech

## Setup Instructions

### Prerequisites

1. **Python 3.10+**
   ```powershell
   python --version
   ```

2. **Ollama** (Local LLM runtime)
   - Download and install: https://ollama.ai/download

3. **Piper TTS**
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

# If installed run the model
ollama run llama3.2:latest
```

#### Step 2: Install Python Dependencies

```powershell
cd backend

# Create virtual environment (recommended)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

#### Step 3: Start FastAPI Server

```powershell
# Make sure you're in the backend directory
cd backend

# Run the server
python app.py
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

---

## Usage

### Starting an Interview

1. **Make sure backend is running**:
   - Ollama service: `ollama serve`
   - FastAPI server: `python app.py` (in backend folder)

2. **Open the extension** by clicking the icon in Chrome

3. **Configure interview**:
   - Interview Type: SWE Intern
   - Question Type: LeetCode-style DSA

4. **Click "Start Interview"**

5. The AI interviewer will:
   - Introduce itself
   - Open Leetcode
   - Describe the first LeetCode-style question
   - Play audio

### During the Interview

- **Type your approach** or solution in the text box
- **Ask for hints** if you're stuck
- **Clarify the question** (e.g., "What are the input constraints?")
- The AI will keep track of all question, code and inputs

### Ending the Interview

1. Click **"End Interview"** button

2. The AI will generate feedback with:
   - **Strengths**: What you did well
   - **Weaknesses**: Areas to improve
   - **Actionable Improvement**: One specific recommendation

3. Click **"Return to Home Page"** to go back to interview setup

---

## API Documentation

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

## Dependencies

### Backend
- **FastAPI** - Web framework
- **Uvicorn** - ASGI server
- **httpx** - Async HTTP client for Ollama
- **pydantic** - Data validation
- **piper-tts** - Text-to-speech

### Chrome Extension
- No external dependencies

### External Services
- **Ollama** - Local LLM runtime
- **Piper** - Local TTS

---

## Privacy & Security

**Fully Local** - All data stays on your machine
- No cloud API calls
- No data collection
- No internet required

**Free & Open Source**
- All components are free
- No API keys needed
- No subscription costs

---

**Happy interviewing!**
