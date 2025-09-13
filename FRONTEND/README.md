# AarogyaLink Flask Backend

A comprehensive Flask backend for the AarogyaLink health companion application with integrated Teachable LLM and Gemini API support.

## Features

- **Multi-Modal Health Queries**: Support for text, image, and audio inputs
- **Dual AI Integration**: Both Teachable LLM and Google Gemini APIs
- **RESTful API**: Clean endpoints for frontend integration
- **File Upload Support**: Handle images and audio files securely
- **Health-Focused AI**: Specialized prompts for health-related queries
- **CORS Enabled**: Ready for frontend integration
- **Error Handling**: Comprehensive error handling and logging

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Keys

Edit the `.env` file and add your actual API keys:

```env
TEACHABLE_API_KEY=your-actual-teachable-api-key
GEMINI_API_KEY=your-actual-gemini-api-key
SECRET_KEY=your-secret-key-for-flask
```

### 3. Run the Application

```bash
python app.py
```

The server will start on `http://localhost:5000`

## API Endpoints

### Health Check
- **GET** `/health`
- Returns server status and API availability

### Text Chat
- **POST** `/api/chat`
- Body: `{"message": "your health question", "context": {}}`
- Processes text-based health queries using both AI APIs

### File Upload
- **POST** `/api/upload`
- Form data with file and type (image/audio)
- Supports image analysis and audio processing

### Contact Form
- **POST** `/api/contact`
- Body: `{"name": "...", "email": "...", "message": "..."}`
- Handles contact form submissions

## Frontend Integration

Your existing `index.html` can be integrated by:

1. Moving it to a `templates` folder
2. Adding JavaScript to make API calls to the backend
3. Implementing file upload functionality for images/audio

## Example API Usage

### Text Query
```javascript
fetch('http://localhost:5000/api/chat', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        message: "I have a headache and feel tired",
        context: {}
    })
})
.then(response => response.json())
.then(data => console.log(data.response));
```

### Image Upload
```javascript
const formData = new FormData();
formData.append('file', imageFile);
formData.append('type', 'image');
formData.append('description', 'Rash on my arm');

fetch('http://localhost:5000/api/upload', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => console.log(data.response));
```

## Security Considerations

- API keys are stored in environment variables
- File uploads are validated and sanitized
- Maximum file size limits are enforced
- Temporary files are cleaned up after processing

## Next Steps

1. Replace placeholder API URLs with actual Teachable endpoints
2. Add speech-to-text service for audio processing
3. Implement user authentication if needed
4. Add database integration for chat history
5. Deploy to production with proper environment configuration

## API Key Setup

### Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env` file

### Teachable API Key
1. Contact Teachable support for API access
2. Follow their documentation for authentication
3. Update the `TEACHABLE_BASE_URL` and endpoints as needed

## Troubleshooting

- Ensure all dependencies are installed correctly
- Check that API keys are valid and have proper permissions
- Verify file upload permissions for the uploads directory
- Check logs for detailed error messages