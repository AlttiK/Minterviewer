"""
Test Script for Mock Interview Backend

This script tests all components of the backend to ensure everything is working.
Run this after setting up the backend to verify your installation.

Usage:
    python test_backend.py
"""

import asyncio
import httpx
import sys


async def test_ollama():
    """Test Ollama connection"""
    print("\n🔍 Testing Ollama connection...")
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get("http://localhost:11434/api/tags")
            if response.status_code == 200:
                print("  ✅ Ollama is running and accessible")
                data = response.json()
                models = data.get("models", [])
                print(f"  📦 Found {len(models)} model(s):")
                for model in models[:3]:  # Show first 3 models
                    print(f"     - {model['name']}")
                return True
            else:
                print(f"  ❌ Ollama returned status code: {response.status_code}")
                return False
    except httpx.ConnectError:
        print("  ❌ Cannot connect to Ollama")
        print("     Start Ollama with: ollama serve")
        return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


async def test_backend():
    """Test FastAPI backend"""
    print("\n🔍 Testing FastAPI backend...")
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get("http://localhost:8000/health")
            if response.status_code == 200:
                print("  ✅ Backend is running")
                data = response.json()
                print(f"     Status: {data.get('status')}")
                print(f"     Ollama: {data.get('ollama')}")
                print(f"     Sessions: {data.get('sessions')}")
                return True
            else:
                print(f"  ❌ Backend returned status code: {response.status_code}")
                return False
    except httpx.ConnectError:
        print("  ❌ Cannot connect to backend")
        print("     Start backend with: python app.py")
        return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


async def test_chat():
    """Test chat endpoint"""
    print("\n🔍 Testing chat endpoint...")
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "http://localhost:8000/chat",
                json={
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a helpful assistant. Respond with 'Hello!' only."
                        },
                        {
                            "role": "user",
                            "content": "Hi"
                        }
                    ],
                    "session_id": "test_session"
                }
            )
            if response.status_code == 200:
                data = response.json()
                message = data.get("message", "")
                audio_url = data.get("audio_url")
                
                print("  ✅ Chat endpoint working")
                print(f"     AI Response: {message[:100]}...")
                if audio_url:
                    print(f"     Audio URL: {audio_url}")
                    print("     ✅ TTS is working")
                else:
                    print("     ℹ️  TTS not available (Piper not installed)")
                return True
            else:
                print(f"  ❌ Chat endpoint returned status code: {response.status_code}")
                return False
    except httpx.ConnectError:
        print("  ❌ Cannot connect to backend")
        return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def test_piper():
    """Test Piper TTS installation"""
    print("\n🔍 Testing Piper TTS...")
    try:
        import subprocess
        result = subprocess.run(
            ["piper", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print("  ✅ Piper is installed")
            return True
        else:
            print("  ⚠️  Piper command failed")
            return False
    except FileNotFoundError:
        print("  ℹ️  Piper not found (optional)")
        print("     Install with: pip install piper-tts")
        return None  # Not critical
    except Exception as e:
        print(f"  ⚠️  Error checking Piper: {e}")
        return None


async def run_tests():
    """Run all tests"""
    print("=" * 60)
    print("🎯 Mock Interview Backend - Test Suite")
    print("=" * 60)
    
    results = {}
    
    # Test Piper (optional)
    results['piper'] = test_piper()
    
    # Test Ollama
    results['ollama'] = await test_ollama()
    
    # Test Backend
    results['backend'] = await test_backend()
    
    # Test Chat (only if backend is running)
    if results['backend']:
        results['chat'] = await test_chat()
    else:
        results['chat'] = False
        print("\n⏭️  Skipping chat test (backend not running)")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    critical_tests = ['ollama', 'backend', 'chat']
    passed = sum(1 for test in critical_tests if results.get(test))
    total = len(critical_tests)
    
    print(f"\nCritical Tests: {passed}/{total} passed")
    print(f"  Ollama:  {'✅' if results['ollama'] else '❌'}")
    print(f"  Backend: {'✅' if results['backend'] else '❌'}")
    print(f"  Chat:    {'✅' if results['chat'] else '❌'}")
    
    if results['piper'] is not None:
        print(f"\nOptional Features:")
        print(f"  Piper TTS: {'✅' if results['piper'] else '⚠️'}")
    
    # Final verdict
    print("\n" + "=" * 60)
    if passed == total:
        print("🎉 All tests passed! Your setup is ready.")
        print("\nNext steps:")
        print("  1. Open Chrome → chrome://extensions/")
        print("  2. Load the chrome-extension folder")
        print("  3. Click the extension icon to start interviewing!")
        return 0
    else:
        print("⚠️  Some tests failed. Please fix the issues above.")
        print("\nCommon fixes:")
        if not results['ollama']:
            print("  • Start Ollama: ollama serve")
            print("  • Pull model: ollama pull llama3.2:latest")
        if not results['backend']:
            print("  • Start backend: python app.py")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(run_tests())
    sys.exit(exit_code)
