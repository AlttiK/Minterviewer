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
PIPER_VOICE_MODEL = "en_US-lessac-medium"

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    session_id: str

class FeedbackRequest(BaseModel):
    messages: List[Message]
    session_id: str


async def call_ollama(messages: List[Dict]) -> str:
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


async def generate_tts(text: str, session_id: str) -> str:
    """Generate TTS audio using Piper"""
    try:
        # Sanitize text for TTS (remove special characters that might cause issues)
        sanitized_text = text.replace('"', "'").replace('\n', ' ')
        
        # Output file path
        output_file = AUDIO_DIR / f"speech_{session_id}_{len(text)}.wav"
        
        # Check if Piper is available
        try:
            # Run Piper TTS command
            # Command: echo "text" | piper --model <model> --output_file <file>
            process = await asyncio.create_subprocess_shell(
                f'echo "{sanitized_text}" | piper --model {PIPER_VOICE_MODEL} --output_file "{output_file}"',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                print(f"Piper TTS error: {stderr.decode()}")
                return None
                
            if output_file.exists():
                return f"/audio/{output_file.name}"
            else:
                return None
                
        except FileNotFoundError:
            print("Piper not found. TTS disabled. Install with: pip install piper-tts")
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
        sessions[request.session_id] = [msg.dict() for msg in request.messages]
        
        # Get AI response from Ollama
        ai_response = await call_ollama(sessions[request.session_id])
        
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
        feedback_messages = [msg.dict() for msg in request.messages]
        feedback_messages.append({
            "role": "user",
            "content": """Please provide interview feedback in the following format:

Strengths: [List 2-3 specific strengths you observed]

Weaknesses: [List 2-3 areas that need improvement]

Actionable Improvement: [Provide ONE specific, actionable recommendation for improvement]

Keep it concise and constructive."""
        })
        
        # Get feedback from AI
        feedback_text = await call_ollama(feedback_messages)
        
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
    print("Make sure Ollama is running: ollama serve")
    print(f"Make sure you have the model: ollama pull {OLLAMA_MODEL}")
    uvicorn.run(app, host="0.0.0.0", port=8000)
