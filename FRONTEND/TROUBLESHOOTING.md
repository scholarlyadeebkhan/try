🔧 AarogyaLink Troubleshooting Guide
=======================================

This guide will help you fix the voice recording, image upload, and AI health scan issues.

## 📋 QUICK CHECKLIST

### 1. Browser Requirements ✅
- Use Chrome, Firefox, or Edge (latest versions)
- Enable JavaScript
- Allow camera and microphone permissions

### 2. Server Status ✅
- Flask server running on http://localhost:5000
- API keys configured in .env file
- No console errors in terminal

### 3. Browser Console Check ✅
- Open browser Developer Tools (F12)
- Check Console tab for errors
- Look for red error messages

## 🎤 VOICE RECORDING ISSUES

### Problem: "Voice recording not starting"
**Solutions:**
1. **Check Browser Permissions:**
   - Click the microphone icon in address bar
   - Select "Allow" for microphone access
   - Refresh the page and try again

2. **Browser Support Check:**
   - Open browser console (F12)
   - Look for "getUserMedia supported: true"
   - If false, update your browser

3. **HTTPS Requirement:**
   - Voice recording requires HTTPS or localhost
   - If using a different domain, ensure HTTPS

### Problem: "Recording starts but no audio captured"
**Solutions:**
1. Check microphone is working in other apps
2. Select correct microphone in browser settings
3. Ensure volume levels are adequate
4. Try a different browser

### Testing Voice Recording:
```
1. Click "Say Anything" tab
2. Click "Start Recording" 
3. Allow microphone permission when prompted
4. Speak for 5-10 seconds
5. Click "Stop Recording"
6. Check if audio is being processed
```

## 🖼️ IMAGE UPLOAD ISSUES

### Problem: "Image upload not working"
**Solutions:**
1. **File Format Check:**
   - Supported: PNG, JPG, JPEG, GIF, BMP, TIFF, WEBP
   - Max size: 16MB
   - Ensure file is not corrupted

2. **Backend Check:**
   - Server must be running
   - Check console for upload errors
   - Verify uploads/ directory exists

### Problem: "Image selected but not processed"
**Solutions:**
1. Check browser console for JavaScript errors
2. Verify backend is responding to uploads
3. Ensure Gemini API key is configured

### Testing Image Upload:
```
1. Click "Search with Image" tab
2. Click "Choose Image File"
3. Select a valid image file
4. Add description (optional)
5. Click "Analyze Image"
6. Check for response from AI
```

## 🤖 AI HEALTH SCAN ISSUES

### Problem: "Camera permission not requested"
**Solutions:**
1. **Manual Permission Grant:**
   - Go to browser settings
   - Find site permissions for localhost:5000
   - Enable camera access manually

2. **Browser Support:**
   - Ensure WebRTC is enabled
   - Check if camera works in other websites
   - Try different browser

### Problem: "Camera starts but AI model fails"
**Solutions:**
1. **Internet Connection:**
   - Model loads from teachablemachine.withgoogle.com
   - Ensure stable internet connection
   - Check firewall/antivirus blocking

2. **JavaScript Libraries:**
   - Verify TensorFlow.js loads
   - Check Teachable Machine library loads
   - Look for 404 errors in network tab

### Testing AI Health Scan:
```
1. Click "AI Health Scan" tab
2. Click "Start AI Analysis"
3. Allow camera permission
4. Position face in camera view
5. Wait for real-time predictions
6. Click "Get Health Advice"
```

## 🔍 DEBUGGING STEPS

### Step 1: Check Browser Console
```
1. Press F12 to open Developer Tools
2. Go to Console tab
3. Look for error messages (red text)
4. Share any errors you see
```

### Step 2: Test Server Health
```
1. Open new browser tab
2. Go to: http://localhost:5000/health
3. Should see: {"status": "healthy", ...}
4. If not, restart Flask server
```

### Step 3: Test Debug Page
```
1. Go to: http://localhost:5000/debug
2. Run all tests
3. Check which features fail
4. Review results
```

### Step 4: Check Network Activity
```
1. Open Developer Tools (F12)
2. Go to Network tab
3. Try uploading file or recording
4. Look for failed requests (red entries)
5. Check response details
```

## ⚠️ COMMON ERRORS & FIXES

### Error: "getUserMedia is not a function"
**Fix:** Update browser or enable WebRTC

### Error: "Permission denied"
**Fix:** Allow camera/microphone in browser settings

### Error: "Failed to load model"
**Fix:** Check internet connection and firewall

### Error: "Backend connection failed"
**Fix:** Restart Flask server with `python app.py`

### Error: "API key not configured"
**Fix:** Check .env file has valid Gemini API key

## 🛠️ ADVANCED TROUBLESHOOTING

### Reset Browser Permissions:
```
1. Go to browser settings
2. Find "Site Settings" or "Privacy & Security"
3. Clear data for localhost:5000
4. Restart browser and try again
```

### Check Flask Server Logs:
```
1. Look at terminal running Flask server
2. Check for error messages when uploading
3. Look for 404, 500, or other HTTP errors
4. Restart server if needed
```

### Verify File Structure:
```
Make sure these files exist:
✓ app.py
✓ templates/index.html
✓ .env (with API keys)
✓ uploads/ (directory)
✓ requirements.txt
```

## 🆘 EMERGENCY FIXES

### If nothing works:
1. **Restart everything:**
   ```
   1. Close browser completely
   2. Stop Flask server (Ctrl+C)
   3. Run: python app.py
   4. Open fresh browser window
   5. Go to http://localhost:5000
   ```

2. **Check API Keys:**
   ```
   1. Open .env file
   2. Verify GEMINI_API_KEY starts with "AIza"
   3. Ensure no extra spaces or quotes
   4. Restart server after changes
   ```

3. **Browser Reset:**
   ```
   1. Clear browser cache and cookies
   2. Disable browser extensions
   3. Try incognito/private mode
   4. Test in different browser
   ```

## 📞 GETTING HELP

If issues persist:
1. Check browser console for specific error messages
2. Note which browser and version you're using
3. Verify Flask server is running without errors
4. Test the debug page functionality
5. Share console errors for targeted help

## ✅ SUCCESS INDICATORS

You'll know it's working when:
- ✅ Voice: Recording timer appears and audio processes
- ✅ Image: Preview shows and AI analyzes the image
- ✅ AI Scan: Camera view appears with live predictions
- ✅ Chat: All interactions get AI responses

Remember: Some features require specific browser permissions and internet connectivity!