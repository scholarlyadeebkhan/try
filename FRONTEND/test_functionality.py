#!/usr/bin/env python3
"""
AarogyaLink Functionality Test Script
Tests voice recording, image upload, and AI health scan features
"""

import requests
import json
import os
import time
from datetime import datetime

API_BASE_URL = "http://localhost:5000"

def test_server_health():
    """Test if the server is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Server is healthy!")
            print(f"   Status: {data['status']}")
            print(f"   Gemini API: {'✅' if data['services']['gemini'] else '❌'}")
            print(f"   Teachable API: {'✅' if data['services']['teachable'] else '❌'}")
            return True
        else:
            print(f"❌ Server health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        print("   Make sure the server is running with: python app.py")
        return False

def test_text_chat():
    """Test text-based chat functionality"""
    print("\n🔤 Testing Text Chat...")
    
    test_message = "I have a headache that started this morning. It's throbbing and I feel nauseous."
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/chat",
            json={"message": test_message},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Text chat working!")
                print(f"   Response length: {len(data['response'])} characters")
                print(f"   Source: {data['source']}")
                return True
            else:
                print(f"❌ Chat failed: {data.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ Chat request failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Chat test error: {e}")
        return False

def test_image_upload():
    """Test image upload functionality"""
    print("\n🖼️ Testing Image Upload...")
    
    # Create a simple test image
    try:
        from PIL import Image
        import io
        
        # Create a simple red square image
        img = Image.new('RGB', (100, 100), color='red')
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        
        files = {'file': ('test_image.png', img_buffer, 'image/png')}
        data = {
            'type': 'image',
            'description': 'Test medical image for functionality testing'
        }
        
        response = requests.post(
            f"{API_BASE_URL}/api/upload",
            files=files,
            data=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Image upload working!")
                print(f"   Response length: {len(result['response'])} characters")
                print(f"   Source: {result['source']}")
                return True
            else:
                print(f"❌ Image upload failed: {result.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ Image upload request failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except ImportError:
        print("⚠️ PIL not available, skipping image test")
        return None
    except Exception as e:
        print(f"❌ Image upload test error: {e}")
        return False

def test_audio_upload():
    """Test audio upload functionality"""
    print("\n🎤 Testing Audio Upload...")
    
    try:
        # Create a simple test audio file (silence)
        import wave
        import struct
        
        # Create 1 second of silence
        sample_rate = 44100
        duration = 1
        frames = sample_rate * duration
        
        audio_buffer = io.BytesIO()
        with wave.open(audio_buffer, 'wb') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(sample_rate)
            
            # Write silence
            for _ in range(frames):
                wav_file.writeframes(struct.pack('<h', 0))
        
        audio_buffer.seek(0)
        
        files = {'file': ('test_audio.wav', audio_buffer, 'audio/wav')}
        data = {
            'type': 'audio',
            'description': 'Test audio recording for functionality testing'
        }
        
        response = requests.post(
            f"{API_BASE_URL}/api/upload",
            files=files,
            data=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Audio upload working!")
                print(f"   Response length: {len(result['response'])} characters")
                print(f"   Source: {result['source']}")
                return True
            else:
                print(f"❌ Audio upload failed: {result.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ Audio upload request failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Audio upload test error: {e}")
        return False


def main():
    """Run all functionality tests"""
    print("🏥 AarogyaLink Functionality Test")
    print("=" * 50)
    print(f"Testing server at: {API_BASE_URL}")
    print(f"Test time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # Test server health first
    if not test_server_health():
        print("\n❌ Server not available. Please start the server first.")
        return
    
    # Run all tests
    tests = [
        ("Text Chat", test_text_chat),
        ("Image Upload", test_image_upload),
        ("Audio Upload", test_audio_upload),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        result = test_func()
        results[test_name] = result
        time.sleep(1)  # Brief pause between tests
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = 0
    
    for test_name, result in results.items():
        if result is True:
            print(f"✅ {test_name}")
            passed += 1
        elif result is False:
            print(f"❌ {test_name}")
        else:
            print(f"⚠️ {test_name} (skipped)")
        
        if result is not None:
            total += 1
    
    if total > 0:
        print(f"\n🎯 {passed}/{total} tests passed ({passed/total*100:.1f}%)")
        
        if passed == total:
            print("\n🎉 All tests passed! Your AarogyaLink application is working correctly.")
        else:
            print(f"\n⚠️ {total-passed} test(s) failed. Please check the server logs and configuration.")
    else:
        print("\n⚠️ No tests could be run.")
    
    print("\n💡 Tips:")
    print("   • Make sure your API keys are configured in the .env file")
    print("   • Check the server console for detailed error messages")
    print("   • Try the debug page at: http://localhost:5000/debug")

if __name__ == "__main__":
    main()