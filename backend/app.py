from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Dict
import httpx
import subprocess
import os
import asyncio
from pathlib import Path
from kokoro_onnx import Kokoro

app = FastAPI(title="Mock Interview API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

AUDIO_DIR = Path("audio")
AUDIO_DIR.mkdir(exist_ok=True)

app.mount("/audio", StaticFiles(directory="audio"), name="audio")

sessions: Dict[str, List[Dict]] = {}

# Configuration
OLLAMA_API_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "llama3.2:latest"

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    session_id: str

class FeedbackRequest(BaseModel):
    messages: List[Message]
    session_id: str

class LeetCodeRequest(BaseModel):
    problem_id: str
    session_id: str

async def msg_ollama(messages: List[Dict]) -> str:
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            # Convert messages to Ollama format
            ollama_messages = [
                {"role": msg["role"] if msg["role"] != "system" else "system", 
                 "content": msg["content"]}
                for msg in messages
            ]
            
            response = await client.post(
                OLLAMA_API_URL,
                json={
                    "model": OLLAMA_MODEL,
                    "messages": ollama_messages,
                    "stream": False
                }
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=500,
                    detail=f"Ollama API error: {response.status_code}"
                )
            
            data = response.json()
            return data["message"]["content"]
            
    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            detail="Cannot connect to Ollama. Make sure Ollama is running (ollama serve)"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error calling Ollama: {str(e)}"
        )


_kokoro_model = None

def get_kokoro_model():
    global _kokoro_model
    if _kokoro_model is None:
        try:
            _kokoro_model = Kokoro(
                "voices/kokoro-v1.0.onnx", 
                "voices/voices-v1.0.bin"
            )
        except Exception as e:
            print(f"Failed to load Kokoro model: {e}")
            print("Make sure model files are downloaded to voices/ directory")
    return _kokoro_model

async def generate_tts(text: str, session_id: str) -> str:
    """Generate TTS audio using Kokoro"""
    try:
        model = get_kokoro_model()
        if model is None:
            print("Kokoro TTS not available")
            return None
        
        cleaned_text = text.replace('\n', ' ').strip()
        if not cleaned_text:
            return None
        
        output_file = AUDIO_DIR / f"speech_{session_id}_{len(text)}.wav"
        
        def generate():
            try:
                samples, sample_rate = model.create(
                    cleaned_text,
                    voice="af_heart",
                    speed=1.0,
                    lang="en-us"
                )
                import soundfile as sf
                sf.write(str(output_file), samples, sample_rate)
                return True
            except Exception as e:
                print(f"Kokoro generation error: {e}")
                return False
        
        loop = asyncio.get_event_loop()
        success = await loop.run_in_executor(None, generate)
        
        if success and output_file.exists():
            return f"/audio/{output_file.name}"
        else:
            return None
            
    except Exception as e:
        print(f"TTS generation error: {str(e)}")
        return None


@app.get("/")
async def root():
    return {
        "message": "Mock Interview API",
        "endpoints": {
            "/chat": "POST - Send chat messages",
            "/feedback": "POST - Get end-of-session feedback",
            "/health": "GET - Check API health"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    # Check if Ollama is reachable
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get("http://localhost:11434/api/tags")
            ollama_status = "connected" if response.status_code == 200 else "error"
    except:
        ollama_status = "disconnected"
    
    return {
        "status": "healthy",
        "ollama": ollama_status,
        "sessions": len(sessions)
    }


@app.post("/chat")
async def chat(request: ChatRequest):
    """Main chat endpoint"""
    try:
        # Store session messages
        sessions[request.session_id] = [msg.model_dump() for msg in request.messages]
        
        # Get AI response from Ollama
        ai_response = await msg_ollama(sessions[request.session_id])
        
        # Generate TTS audio
        audio_url = await generate_tts(ai_response, request.session_id)
        
        return {
            "message": ai_response,
            "audio_url": audio_url
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Chat error: {str(e)}"
        )


@app.post("/feedback")
async def get_feedback(request: FeedbackRequest):
    """Generate end-of-session feedback"""
    try:
        # Add feedback request to messages
        feedback_messages = [msg.model_dump() for msg in request.messages]
        feedback_messages.append({
            "role": "user",
            "content": """Please provide interview feedback in the exact following format:

                        Strengths: [List 2-3 specific strengths you observed]

                        Weaknesses: [List 2-3 areas that need improvement]

                        Actionable Improvement: [Provide ONE specific, actionable recommendation for improvement]

                        Keep it concise and constructive."""
        })
        
        # Get feedback from AI
        feedback_text = await msg_ollama(feedback_messages)
        
        # Parse feedback (simple parsing)
        feedback = {
            "strengths": "",
            "weaknesses": "",
            "improvement": ""
        }
        
        lines = feedback_text.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if line.lower().startswith('strengths:'):
                current_section = 'strengths'
                feedback['strengths'] = line.replace('Strengths:', '').strip()
            elif line.lower().startswith('weaknesses:'):
                current_section = 'weaknesses'
                feedback['weaknesses'] = line.replace('Weaknesses:', '').strip()
            elif line.lower().startswith('actionable improvement:'):
                current_section = 'improvement'
                feedback['improvement'] = line.replace('Actionable Improvement:', '').strip()
            elif current_section and line:
                feedback[current_section] += ' ' + line
        
        # If parsing failed, use raw text
        if not any(feedback.values()):
            feedback = {
                "strengths": "See full feedback below",
                "weaknesses": "See full feedback below",
                "improvement": feedback_text
            }
        
        return {"feedback": feedback}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Feedback error: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    print("Starting Mock Interview API server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
