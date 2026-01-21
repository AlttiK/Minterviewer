"""
Piper TTS Integration Helper

This module provides a simplified interface for Piper TTS.
Piper is a fast, local text-to-speech system.

Installation:
1. Install piper-tts: pip install piper-tts
2. Download a voice model (optional, uses default if not specified):
   - Visit: https://github.com/rhasspy/piper/releases
   - Download a .onnx model file and corresponding .json config
   
Usage:
    python tts_helper.py "Hello, this is a test"
"""

import sys
import subprocess
from pathlib import Path


def generate_speech(text: str, output_file: str = "output.wav", model: str = "en_US-lessac-medium"):
    """
    Generate speech from text using Piper
    
    Args:
        text: The text to convert to speech
        output_file: Path to output WAV file
        model: Piper voice model name
    """
    try:
        # Create command
        # Piper expects: echo "text" | piper --model <model> --output_file <file>
        cmd = f'echo "{text}" | piper --model {model} --output_file {output_file}'
        
        # Execute
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"✓ Speech generated: {output_file}")
            return True
        else:
            print(f"✗ Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"✗ Exception: {str(e)}")
        return False


def check_piper_installed():
    """Check if Piper is installed and available"""
    try:
        result = subprocess.run(
            ["piper", "--version"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("✓ Piper is installed")
            return True
        else:
            print("✗ Piper not found")
            return False
    except FileNotFoundError:
        print("✗ Piper not found in PATH")
        print("\nInstall Piper:")
        print("  pip install piper-tts")
        print("\nOr download from:")
        print("  https://github.com/rhasspy/piper/releases")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tts_helper.py \"Your text here\"")
        print("\nChecking Piper installation...")
        check_piper_installed()
        sys.exit(1)
    
    text = " ".join(sys.argv[1:])
    output = "test_speech.wav"
    
    print(f"Generating speech for: {text[:50]}...")
    generate_speech(text, output)
