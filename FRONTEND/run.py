#!/usr/bin/env python3
"""
AarogyaLink Backend Runner
Simple script to run the Flask application with proper configuration
"""

import os
import sys
import webbrowser
import threading
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the Flask app
from app import app

def open_browser(url, delay=1.5):
    """Open the URL in Microsoft Edge browser after a delay"""
    def open_browser_delayed():
        time.sleep(delay)
        try:
            # Try to open in Microsoft Edge specifically
            edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
            if os.path.exists(edge_path):
                webbrowser.register('edge', None, webbrowser.BackgroundBrowser(edge_path))
                webbrowser.get('edge').open(url)
                print(f"✅ Opened {url} in Microsoft Edge")
            else:
                # Fallback to default browser if Edge not found in expected location
                webbrowser.open(url)
                print(f"✅ Opened {url} in default browser (Edge not found in expected location)")
        except Exception as e:
            print(f"❌ Failed to open browser: {e}")
            # Silent fallback - don't crash the app if browser opening fails
    
    # Run browser opening in a separate thread to not block Flask startup
    threading.Thread(target=open_browser_delayed, daemon=True).start()

if __name__ == '__main__':
    # Get configuration from environment variables
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 5000))
    
    print("=" * 60)
    print("🏥 AarogyaLink Backend Server")
    print("=" * 60)
    print(f"🌐 Server URL: http://{host}:{port}")
    print(f"🔧 Debug Mode: {debug}")
    print(f"📡 API Endpoints:")
    print(f"   • Health Check: http://{host}:{port}/health")
    print(f"   • Test API: http://{host}:{port}/api/test")
    print(f"   • Chat API: http://{host}:{port}/api/chat")
    print(f"   • Upload API: http://{host}:{port}/api/upload")
    print(f"   • Contact API: http://{host}:{port}/api/contact")
    print(f"   • Debug Tool: http://{host}:{port}/debug")
    print("=" * 60)
    print("💡 Make sure to configure your API keys in the .env file!")
    print("🌐 Opening Microsoft Edge automatically...")
    print("=" * 60)
    
    # Open browser automatically
    server_url = f"http://localhost:{port}"
    open_browser(server_url)
    
    # Run the Flask application
    app.run(
        debug=debug,
        host=host,
        port=port,
        threaded=True
    )