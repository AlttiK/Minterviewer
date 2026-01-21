# 🎨 Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Chrome Browser                          │
│  ┌────────────────────────────────────────────────────┐     │
│  │  Chrome Extension (Manifest V3)                    │     │
│  │  ┌──────────────────────────────────────────────┐  │     │
│  │  │  Popup UI (HTML/CSS/JS)                      │  │     │
│  │  │  • Interview settings                        │  │     │
│  │  │  • Chat interface                            │  │     │
│  │  │  • Audio player                              │  │     │
│  │  │  • Feedback display                          │  │     │
│  │  └──────────────────────────────────────────────┘  │     │
│  └────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            ↕ HTTP/JSON
                    (localhost:8000)
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                           │
│  ┌────────────────────────────────────────────────────┐     │
│  │  API Endpoints                                     │     │
│  │  • POST /chat - Send messages                     │     │
│  │  • POST /feedback - Get feedback                  │     │
│  │  • GET /health - Health check                     │     │
│  │  • GET /audio/* - Serve audio files               │     │
│  └────────────────────────────────────────────────────┘     │
│                            ↕                                 │
│  ┌────────────────────────────────────────────────────┐     │
│  │  Session Manager                                   │     │
│  │  • In-memory storage                               │     │
│  │  • Message history                                 │     │
│  └────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────┘
          ↕ HTTP                              ↕ Shell
    (localhost:11434)                    (piper command)
┌──────────────────────┐            ┌──────────────────────┐
│   Ollama Service     │            │    Piper TTS         │
│  ┌────────────────┐  │            │  ┌────────────────┐  │
│  │  LLM Model     │  │            │  │  Voice Model   │  │
│  │  (llama3.2)    │  │            │  │  (en_US)       │  │
│  └────────────────┘  │            │  └────────────────┘  │
│  • Generate replies  │            │  • Text → Speech   │  │
│  • Context aware     │            │  • WAV output      │  │
└──────────────────────┘            └──────────────────────┘
```

## Data Flow

### 1. Start Interview
```
User clicks "Start Interview"
    ↓
Extension sends POST /chat with system prompt
    ↓
Backend forwards to Ollama
    ↓
Ollama generates first question
    ↓
Backend receives AI response
    ↓
Backend calls Piper TTS
    ↓
Piper generates speech.wav
    ↓
Backend returns { message, audio_url }
    ↓
Extension displays text + plays audio
```

### 2. User Responds
```
User types answer and clicks "Send"
    ↓
Extension sends POST /chat with conversation history
    ↓
Backend retrieves session from memory
    ↓
Backend forwards to Ollama with full context
    ↓
Ollama generates contextual response
    ↓
Backend generates TTS audio
    ↓
Backend returns response + audio
    ↓
Extension updates chat UI
```

### 3. End Interview
```
User clicks "End Interview"
    ↓
Extension sends POST /feedback
    ↓
Backend adds feedback prompt to messages
    ↓
Ollama analyzes full conversation
    ↓
Ollama generates feedback (strengths/weaknesses/tips)
    ↓
Backend parses feedback
    ↓
Backend returns structured feedback
    ↓
Extension displays feedback summary
```

## Component Interactions

```
Extension Components:
┌─────────────────┐
│  popup.html     │ → User Interface (HTML/CSS)
│  popup.js       │ → Logic & API calls
│  manifest.json  │ → Extension config
└─────────────────┘

Backend Components:
┌─────────────────┐
│  app.py         │ → FastAPI app + endpoints
│  tts_helper.py  │ → TTS utilities
│  sessions {}    │ → In-memory storage
└─────────────────┘

External Services:
┌─────────────────┐
│  Ollama         │ → AI model runtime
│  Piper          │ → TTS engine
└─────────────────┘
```

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | HTML/CSS/JS | Extension UI |
| **Extension** | Chrome Manifest V3 | Extension framework |
| **API** | FastAPI | Web server |
| **Runtime** | Uvicorn | ASGI server |
| **AI** | Ollama | LLM runtime |
| **Model** | Llama 3.2 | Language model |
| **TTS** | Piper | Speech synthesis |
| **HTTP** | httpx | Async HTTP client |
| **Data** | In-memory dict | Session storage |

## File Dependencies

```
Chrome Extension
├── manifest.json (entry point)
├── popup.html (loaded by manifest)
└── popup.js (loaded by popup.html)

Backend
├── app.py (entry point)
├── requirements.txt (dependencies)
└── tts_helper.py (imported by app.py)

Generated at Runtime
└── audio/
    └── speech_*.wav (TTS outputs)
```

## Network Ports

```
localhost:8000  → FastAPI backend
localhost:11434 → Ollama API
```

## Security Model

```
┌─────────────────────────────────────┐
│  Chrome Extension Security          │
│  • Runs in isolated sandbox         │
│  • Can only connect to localhost    │
│  • No external network access       │
└─────────────────────────────────────┘
         ↓ CORS (localhost only)
┌─────────────────────────────────────┐
│  FastAPI Backend Security           │
│  • CORS allows all origins (local)  │
│  • No authentication required       │
│  • Binds to 0.0.0.0:8000            │
└─────────────────────────────────────┘
         ↓ HTTP (localhost)
┌─────────────────────────────────────┐
│  Ollama Service                     │
│  • Runs locally only                │
│  • No internet access needed        │
│  • All data stays on machine        │
└─────────────────────────────────────┘
```

## Session Management

```
Session Lifecycle:

1. START
   User clicks "Start Interview"
      ↓
   Generate session_id (timestamp)
      ↓
   Create sessions[session_id] = []

2. ACTIVE
   Each chat message:
      ↓
   Append to sessions[session_id]
      ↓
   Send to Ollama with full history
      ↓
   Append AI response to session

3. END
   User clicks "End Interview"
      ↓
   Request feedback with full history
      ↓
   Session remains in memory until server restart
```

## Error Handling Flow

```
Extension Error Handling:
try {
    fetch(API_ENDPOINT)
} catch {
    Display error in UI
    Keep UI responsive
}

Backend Error Handling:
try {
    await ollama_api()
} catch OllamaConnectionError {
    Return 503 with helpful message
} catch Exception {
    Return 500 with error details
}

TTS Error Handling:
try {
    generate_tts()
} catch PiperNotFound {
    Return response without audio
    Log warning
} catch Exception {
    Continue without TTS
}
```

## Performance Characteristics

| Operation | Time | Notes |
|-----------|------|-------|
| Extension load | ~50ms | One-time |
| Start interview | 2-5s | Ollama model load |
| Chat response | 1-3s | Depends on model size |
| TTS generation | 0.5-1s | Per response |
| Audio playback | Varies | Depends on response length |
| Feedback generation | 2-4s | Analyzes full conversation |

## Resource Usage

| Component | RAM | Disk | CPU |
|-----------|-----|------|-----|
| Chrome Extension | ~10MB | ~30KB | Minimal |
| FastAPI Backend | ~50MB | ~10KB | Low |
| Ollama (idle) | ~100MB | ~2-4GB | Low |
| Ollama (active) | ~2-4GB | ~2-4GB | High |
| Piper TTS | ~50MB | ~5MB | Medium (burst) |

## Scalability Considerations

**Current Design (MVP):**
- ✅ Single user
- ✅ One interview at a time
- ✅ In-memory sessions
- ✅ Local execution

**To Scale (Future):**
- Add database (PostgreSQL/Redis)
- Add authentication (JWT)
- Add rate limiting
- Add session persistence
- Multi-user support
- Distributed deployment

## Extension vs Backend Responsibilities

| Responsibility | Extension | Backend |
|---------------|-----------|---------|
| UI rendering | ✅ | ❌ |
| User input | ✅ | ❌ |
| Audio playback | ✅ | ❌ |
| API calls | ✅ | ❌ |
| Session storage | ❌ | ✅ |
| AI communication | ❌ | ✅ |
| TTS generation | ❌ | ✅ |
| Business logic | ❌ | ✅ |

## Development Workflow

```
1. Modify Code
   ├── Extension: Reload in chrome://extensions
   └── Backend: Auto-reload with --reload flag

2. Test Changes
   ├── Extension: Open popup and test
   └── Backend: Run test_backend.py

3. Debug
   ├── Extension: Chrome DevTools (F12)
   └── Backend: Terminal logs + /health endpoint

4. Deploy
   ├── Extension: Package and submit to Chrome Web Store
   └── Backend: Docker + cloud hosting (if needed)
```

---

This architecture is designed to be:
- **Simple**: Minimal moving parts
- **Local**: No cloud dependencies
- **Fast**: Async operations throughout
- **Extensible**: Easy to add features
- **Debuggable**: Clear separation of concerns
