from flask import Flask, request, jsonify, render_template
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
from flask_cors import CORS
import os
import json
import base64
from datetime import datetime
import logging
from werkzeug.utils import secure_filename
import requests
import google.generativeai as genai
from PIL import Image
import io
import webbrowser
import threading
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# Create upload directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# API Keys Configuration
TEACHABLE_API_KEY = os.environ.get('TEACHABLE_API_KEY', 'your-teachable-api-key-here')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', 'your-gemini-api-key-here')

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Teachable API Configuration
TEACHABLE_BASE_URL = "https://api.teachable.com/v1"  # Update with actual Teachable API URL
TEACHABLE_HEADERS = {
    "Authorization": f"Bearer {TEACHABLE_API_KEY}",
    "Content-Type": "application/json"
}

# Allowed file extensions for uploads
ALLOWED_EXTENSIONS = {
    # Images
    'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'webp',
    # Audio
    'wav', 'mp3', 'mp4', 'webm', 'ogg', 'aac', 'm4a', 'flac'
}

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension"""
    if '.' not in filename:
        return False
    
    extension = filename.rsplit('.', 1)[1].lower()
    return extension in ALLOWED_EXTENSIONS

def get_file_type(filename):
    """Determine if file is image or audio based on extension"""
    if '.' not in filename:
        return 'unknown'
    
    extension = filename.rsplit('.', 1)[1].lower()
    
    image_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'webp'}
    audio_extensions = {'wav', 'mp3', 'mp4', 'webm', 'ogg', 'aac', 'm4a', 'flac'}
    
    if extension in image_extensions:
        return 'image'
    elif extension in audio_extensions:
        return 'audio'
    else:
        return 'unknown'

class HealthCompanionAPI:
    def __init__(self):
        try:
            # Initialize Gemini model
            self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
        except Exception as e:
            logger.error(f"Failed to initialize Gemini model: {e}")
            self.gemini_model = None

    def call_teachable_api(self, prompt, context=None):
        """Call Teachable's LLM API"""
        try:
            payload = {
                "prompt": prompt,
                "context": context or {},
                "max_tokens": 1000,
                "temperature": 0.7
            }
            
            response = requests.post(
                f"{TEACHABLE_BASE_URL}/completions",  # Update with actual endpoint
                headers=TEACHABLE_HEADERS,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Teachable API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error calling Teachable API: {e}")
            return None

    def call_gemini_api(self, prompt, image_data=None):
        """Call Gemini API"""
        try:
            if not self.gemini_model:
                return None

            if image_data:
                # Handle image input
                image = Image.open(io.BytesIO(image_data))
                response = self.gemini_model.generate_content([prompt, image])
            else:
                # Handle text input
                response = self.gemini_model.generate_content(prompt)
            
            return {
                "text": response.text,
                "usage": getattr(response, 'usage_metadata', {}),
                "safety_ratings": getattr(response, 'safety_ratings', [])
            }
            
        except Exception as e:
            logger.error(f"Error calling Gemini API: {e}")
            return None

    def process_health_query(self, query_type, content, file_data=None, predictions=None, source="text"):
        """Process health-related queries using both APIs"""
        
        # Enhanced health-specific prompt engineering
        health_context = """
        You are Dr. AarogyaLink, a friendly AI health companion.
        Keep responses short and conversational - like texting a doctor friend.
        
        **Response style:**
        - Acknowledge their concern briefly
        - Ask 1-2 key questions to understand better  
        - Give quick helpful thoughts
        - Keep total response under 3-4 sentences
        
        **Example format:**
        "That sounds uncomfortable! When did this start? Have you tried [simple remedy]? If it gets worse or doesn't improve in a day or two, I'd suggest seeing a doctor."
        
        **Tone:** Friendly, caring, conversational - like a knowledgeable friend.
        """
        
        # Special handling for voice inputs
        if source == "voice":
            health_context += """
            
            **Special Note for Voice Input:**
            The user has provided their health concern via voice input. Please ensure your response is clear and easy to understand when read aloud. 
            Consider that the user may have speech or hearing difficulties, so avoid complex medical jargon unless necessary.
            """
        
        if query_type == "text":
            # Use both APIs for text queries
            full_prompt = f"{health_context}\n\nUser Query: {content}\n\nRemember: Keep response conversational and under 3-4 sentences."
            
            # Try Gemini first
            gemini_response = self.call_gemini_api(full_prompt)
            
            # Try Teachable as backup or for comparison
            teachable_response = self.call_teachable_api(full_prompt)
            
            return {
                "primary_response": gemini_response.get("text") if gemini_response else None,
                "secondary_response": teachable_response.get("completion") if teachable_response else None,
                "source": "gemini" if gemini_response else "teachable",
                "timestamp": datetime.now().isoformat()
            }
            
        elif query_type == "image":
            # Use Gemini for image analysis
            image_prompt = f"{health_context}\n\nAnalyze this health image briefly: {content}\n\nKeep response under 3 sentences."
            
            gemini_response = self.call_gemini_api(image_prompt, file_data)
            
            return {
                "primary_response": gemini_response.get("text") if gemini_response else "Unable to analyze image",
                "source": "gemini",
                "safety_ratings": gemini_response.get("safety_ratings") if gemini_response else [],
                "timestamp": datetime.now().isoformat()
            }
            
        elif query_type == "audio":
            # For audio, convert to text first (you might need speech-to-text service)
            # Then process as text query
            text_content = content  # Assume content is already transcribed
            return self.process_health_query("text", text_content, source=source)

# Initialize the API handler
health_api = HealthCompanionAPI()

@app.route('/')
def index():
    """Serve the main HTML page"""
    return render_template('index.html')

@app.route('/debug')
def debug():
    """Serve the debug page"""
    with open('debug.html', 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/teach')
def teach():
    """Serve the teach.html page for image diagnosis"""
    with open('teach.html', 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/api/test')
def test_api():
    """Test endpoint to verify API is working"""
    return jsonify({
        "message": "AarogyaLink API is working!",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "teachable": bool(TEACHABLE_API_KEY != 'your-teachable-api-key-here'),
            "gemini": bool(GEMINI_API_KEY != 'your-gemini-api-key-here')
        }
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle text-based health queries (including voice input)"""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({"error": "Message is required"}), 400
        
        message = data['message']
        context = data.get('context', {})
        source = data.get('source', 'text')  # 'text' or 'voice'
        
        # Log the input source for analytics
        if source == 'voice':
            logger.info(f"Voice input received: {message[:100]}...")
        else:
            logger.info(f"Text input received: {message[:100]}...")
        
        # Process the query as text (voice is already transcribed)
        # Pass the source information to customize the response for voice inputs
        response = health_api.process_health_query("text", message, source=source)
        
        if response['primary_response']:
            return jsonify({
                "success": True,
                "response": response['primary_response'],
                "source": response['source'],
                "input_source": source,  # Include the input source in response
                "timestamp": response['timestamp']
            })
        else:
            return jsonify({"error": "Unable to process your query at the moment"}), 500
            
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle file uploads (images/audio)"""
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        query_type = request.form.get('type', 'auto')  # auto-detect if not specified
        description = request.form.get('description', '')
        
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Log file details for debugging
        logger.info(f"Received file: {file.filename}, Content-Type: {file.content_type}, Size: {len(file.read())} bytes")
        file.seek(0)  # Reset file pointer after reading for size
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_data = file.read()
            
            # Auto-detect file type if not specified
            if query_type == 'auto':
                query_type = get_file_type(filename)
                logger.info(f"Auto-detected file type: {query_type}")
            
            # Validate file size
            if len(file_data) == 0:
                return jsonify({"error": "File is empty"}), 400
            
            if len(file_data) > app.config['MAX_CONTENT_LENGTH']:
                return jsonify({"error": "File too large. Maximum size is 16MB."}), 413
            
            # Save file temporarily
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            try:
                with open(file_path, 'wb') as f:
                    f.write(file_data)
                logger.info(f"File saved temporarily to: {file_path}")
            except Exception as e:
                logger.error(f"Error saving file: {e}")
                return jsonify({"error": "Failed to save file"}), 500
            
            # Process based on file type
            try:
                if query_type == 'image':
                    # Validate image file
                    try:
                        img = Image.open(io.BytesIO(file_data))
                        img.verify()  # Verify it's a valid image
                        logger.info(f"Valid image file: {img.format}, {img.size}")
                    except Exception as e:
                        logger.error(f"Invalid image file: {e}")
                        return jsonify({"error": "Invalid image file"}), 400
                    
                    response = health_api.process_health_query("image", description, file_data)
                    
                elif query_type == 'audio':
                    # For audio files, we need speech-to-text conversion
                    # For now, provide a helpful response about audio processing
                    audio_description = f"Audio file received: {filename} ({len(file_data)} bytes). "
                    if description:
                        audio_description += f"Description: {description}"
                    else:
                        audio_description += "Please describe your symptoms or health concerns from the audio recording."
                    
                    # Note: You can integrate speech-to-text services here
                    # For example, Google Speech-to-Text, Azure Speech Services, etc.
                    response = health_api.process_health_query("text", audio_description)
                    
                else:
                    return jsonify({"error": f"Unsupported file type: {query_type}"}), 400
                
            except Exception as e:
                logger.error(f"Error processing {query_type} file: {e}")
                return jsonify({"error": f"Failed to process {query_type} file"}), 500
            
            # Clean up temporary file
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    logger.info(f"Cleaned up temporary file: {file_path}")
            except Exception as e:
                logger.warning(f"Failed to clean up temporary file: {e}")
            
            # Return response
            if response and response.get('primary_response'):
                return jsonify({
                    "success": True,
                    "response": response['primary_response'],
                    "source": response['source'],
                    "timestamp": response['timestamp'],
                    "file_info": {
                        "filename": filename,
                        "type": query_type,
                        "size": len(file_data)
                    }
                })
            else:
                return jsonify({"error": "Unable to process file at the moment"}), 500
        else:
            allowed_exts = ', '.join(sorted(ALLOWED_EXTENSIONS))
            return jsonify({
                "error": f"File type not allowed. Supported formats: {allowed_exts}"
            }), 400
            
    except Exception as e:
        logger.error(f"Error in upload endpoint: {e}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@app.route('/api/contact', methods=['POST'])
def contact():
    """Handle contact form submissions"""
    try:
        data = request.get_json()
        
        required_fields = ['name', 'email', 'message']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"{field} is required"}), 400
        
        # Here you would typically save to database or send email
        # For now, just log the contact attempt
        logger.info(f"Contact form submission from {data['email']}: {data['message']}")
        
        return jsonify({
            "success": True,
            "message": "Thank you for your message. We'll get back to you soon!"
        })
        
    except Exception as e:
        logger.error(f"Error in contact endpoint: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.errorhandler(413)
def too_large(e):
    return jsonify({"error": "File too large"}), 413

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "Internal server error"}), 500

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
                logger.info(f"Opened {url} in Microsoft Edge")
            else:
                # Fallback to default browser if Edge not found in expected location
                webbrowser.open(url)
                logger.info(f"Opened {url} in default browser (Edge not found in expected location)")
        except Exception as e:
            logger.error(f"Failed to open browser: {e}")
            # Silent fallback - don't crash the app if browser opening fails
    
    # Run browser opening in a separate thread to not block Flask startup
    threading.Thread(target=open_browser_delayed, daemon=True).start()

if __name__ == '__main__':
    # Check if API keys are configured
    if TEACHABLE_API_KEY == 'your-teachable-api-key-here':
        logger.warning("Teachable API key not configured!")
    
    if GEMINI_API_KEY == 'your-gemini-api-key-here':
        logger.warning("Gemini API key not configured!")
    
    # Server configuration
    host = '0.0.0.0'
    port = 5000
    debug = False  # Disable debug mode for production
    
    # Construct the URL for opening in browser
    server_url = f"http://localhost:{port}"
    
    print("=" * 60)
    print("🏥 AarogyaLink Backend Server")
    print("=" * 60)
    print(f"🌐 Server URL: {server_url}")
    print(f"🔧 Debug Mode: {debug}")
    print("📡 API Endpoints:")
    print(f"   • Health Check: {server_url}/health")
    print(f"   • Test API: {server_url}/api/test")
    print(f"   • Chat API: {server_url}/api/chat")
    print(f"   • Upload API: {server_url}/api/upload")
    print(f"   • Contact API: {server_url}/api/contact")
    print(f"   • Debug Tool: {server_url}/debug")
    print(f"   • Image Diagnosis: {server_url}/teach")
    print("=" * 60)
    print("💡 Make sure to configure your API keys in the .env file!")
    # Commented out browser auto-open for production
    # open_browser(server_url)
    
    # Start the Flask server with debug disabled for production
    app.run(debug=debug, host=host, port=port)