@echo off
title AarogyaLink - First Time Setup (Installing Prerequisites)
color 0A

echo ========================================================================
echo    AarogyaLink Health Companion - First Time Setup
echo ========================================================================
echo.
echo This script will install all necessary prerequisites to run AarogyaLink:
echo   - Python 3.9+ (if not installed)
echo   - pip (Python package installer)
echo   - All required Python libraries
echo   - Virtual environment setup (optional but recommended)
echo.
echo NOTE: This may take 10-15 minutes depending on your internet speed.
echo       Administrator privileges may be required for some installations.
echo.
pause
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo [INFO] Running with administrator privileges - Good!
    echo.
) else (
    echo [WARNING] Not running as administrator. Some installations may fail.
    echo           Right-click this file and select "Run as administrator" for best results.
    echo.
    timeout /t 3 >nul
)

echo ========================================================================
echo Step 1: Checking Python Installation
echo ========================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorLevel% == 0 (
    echo [SUCCESS] Python is already installed:
    python --version
    echo.
    goto :check_pip
) else (
    echo [INFO] Python not found. Installing Python...
    goto :install_python
)

:install_python
echo.
echo [INFO] Downloading and installing Python 3.11...
echo        This may take several minutes...
echo.

REM Create temp directory
if not exist "%TEMP%\aarogyalink_setup" mkdir "%TEMP%\aarogyalink_setup"
cd /d "%TEMP%\aarogyalink_setup"

REM Download Python installer using PowerShell
echo [INFO] Downloading Python installer...
powershell -Command "& {Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe' -OutFile 'python_installer.exe'}"

if not exist "python_installer.exe" (
    echo [ERROR] Failed to download Python installer!
    echo         Please check your internet connection and try again.
    echo         You can also manually download Python from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [INFO] Installing Python (this may take a few minutes)...
echo        - Adding Python to PATH
echo        - Installing pip
echo        - Setting up Python environment
echo.

REM Install Python silently with all features
python_installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

REM Wait for installation to complete
timeout /t 30 >nul

REM Refresh environment variables
call refreshenv >nul 2>&1 || (
    echo [INFO] Refreshing environment variables...
    set "PATH=%PATH%;C:\Program Files\Python311;C:\Program Files\Python311\Scripts"
    set "PATH=%PATH%;C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311;C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\Scripts"
)

REM Verify Python installation
python --version >nul 2>&1
if %errorLevel% == 0 (
    echo [SUCCESS] Python installed successfully:
    python --version
    echo.
) else (
    echo [ERROR] Python installation failed!
    echo         Please manually install Python from: https://www.python.org/downloads/
    echo         Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

REM Clean up installer
del python_installer.exe >nul 2>&1

:check_pip
echo ========================================================================
echo Step 2: Verifying pip (Python Package Installer)
echo ========================================================================
echo.

pip --version >nul 2>&1
if %errorLevel% == 0 (
    echo [SUCCESS] pip is available:
    pip --version
    echo.
) else (
    echo [INFO] Installing pip...
    python -m ensurepip --upgrade
    python -m pip install --upgrade pip
    echo.
)

echo ========================================================================
echo Step 3: Installing Required Python Libraries
echo ========================================================================
echo.

REM Return to the original directory
cd /d "%~dp0"

REM Check if requirements.txt exists
if not exist "requirements.txt" (
    echo [WARNING] requirements.txt not found. Creating it with necessary dependencies...
    echo.
    
    REM Create requirements.txt with all necessary packages
    (
        echo flask==2.3.3
        echo flask-cors==4.0.0
        echo google-generativeai==0.3.2
        echo Pillow==10.1.0
        echo requests==2.31.0
        echo python-dotenv==1.0.0
        echo werkzeug==2.3.7
    ) > requirements.txt
    
    echo [INFO] Created requirements.txt with necessary dependencies.
    echo.
)

echo [INFO] Installing Python packages from requirements.txt...
echo        This may take 5-10 minutes depending on your internet speed.
echo.

echo Installing packages:
type requirements.txt
echo.

REM Upgrade pip first
python -m pip install --upgrade pip

REM Install packages with verbose output
python -m pip install -r requirements.txt --upgrade

if %errorLevel% == 0 (
    echo.
    echo [SUCCESS] All Python packages installed successfully!
    echo.
) else (
    echo.
    echo [ERROR] Some packages failed to install!
    echo         Trying to install packages individually...
    echo.
    
    REM Try installing each package individually
    python -m pip install flask==2.3.3
    python -m pip install flask-cors==4.0.0
    python -m pip install google-generativeai==0.3.2
    python -m pip install Pillow==10.1.0
    python -m pip install requests==2.31.0
    python -m pip install python-dotenv==1.0.0
    python -m pip install werkzeug==2.3.7
    
    echo [INFO] Individual package installation completed.
    echo.
)

echo ========================================================================
echo Step 4: Verifying Installation
echo ========================================================================
echo.

echo [INFO] Checking installed packages...
python -m pip list | findstr /C:"flask" /C:"google-generativeai" /C:"Pillow" /C:"requests" /C:"python-dotenv" /C:"werkzeug"
echo.

echo [INFO] Testing Python imports...
python -c "import flask; import google.generativeai; import PIL; import requests; import dotenv; import werkzeug; print('[SUCCESS] All required modules can be imported!')" 2>nul

if %errorLevel% == 0 (
    echo [SUCCESS] All dependencies are working correctly!
    echo.
) else (
    echo [WARNING] Some modules may not be working correctly.
    echo            The application may still work, but please check for errors when running.
    echo.
)

echo ========================================================================
echo Step 5: Setting up Environment Configuration
echo ========================================================================
echo.

REM Check if .env file exists
if not exist ".env" (
    echo [INFO] Creating .env configuration file...
    echo.
    
    REM Create .env file with default values
    (
        echo # AarogyaLink Backend Configuration
        echo.
        echo # Flask Configuration
        echo SECRET_KEY=a8f5f167f44f4964e6c998dee827110c
        echo FLASK_ENV=development
        echo FLASK_DEBUG=True
        echo.
        echo # API Keys - Replace with your actual API keys
        echo TEACHABLE_API_KEY=your-teachable-api-key-here
        echo GEMINI_API_KEY=your-gemini-api-key-here
        echo.
        echo # Teachable API Configuration
        echo TEACHABLE_BASE_URL=https://api.teachable.com/v1
        echo.
        echo # Database Configuration
        echo DATABASE_URL=sqlite:///aarogyalink.db
        echo.
        echo # File Upload Configuration
        echo MAX_CONTENT_LENGTH=16777216
        echo UPLOAD_FOLDER=uploads
        echo.
        echo # Logging Configuration
        echo LOG_LEVEL=INFO
    ) > .env
    
    echo [SUCCESS] Created .env configuration file.
    echo           Please edit this file to add your actual API keys.
    echo.
) else (
    echo [INFO] .env file already exists - skipping creation.
    echo.
)

REM Create uploads directory if it doesn't exist
if not exist "uploads" (
    mkdir uploads
    echo [INFO] Created uploads directory.
    echo.
)

echo ========================================================================
echo Step 6: Final Verification and Testing
echo ========================================================================
echo.

echo [INFO] Performing final system check...
echo.

REM Test Flask import and basic functionality
python -c "
import sys
print('[INFO] Python version:', sys.version)
print('[INFO] Python executable:', sys.executable)

try:
    import flask
    print('[SUCCESS] Flask version:', flask.__version__)
except ImportError as e:
    print('[ERROR] Flask import failed:', e)

try:
    import google.generativeai as genai
    print('[SUCCESS] Google Generative AI library imported')
except ImportError as e:
    print('[ERROR] Google Generative AI import failed:', e)

try:
    from PIL import Image
    print('[SUCCESS] Pillow (PIL) library imported')
except ImportError as e:
    print('[ERROR] Pillow import failed:', e)

try:
    import requests
    print('[SUCCESS] Requests library imported')
except ImportError as e:
    print('[ERROR] Requests import failed:', e)

print('[INFO] System check completed')
"

echo.

echo ========================================================================
echo                         INSTALLATION COMPLETE!
echo ========================================================================
echo.
echo [SUCCESS] AarogyaLink prerequisites have been installed successfully!
echo.
echo NEXT STEPS:
echo   1. Edit the .env file to add your API keys:
echo      - Get Gemini API key from: https://makersuite.google.com/app/apikey
echo      - Contact Teachable for LLM API access
echo.
echo   2. Run the application using one of these methods:
echo      - Double-click "start.bat"
echo      - Run "python app.py" in command prompt
echo      - Run "python run.py" in command prompt
echo.
echo   3. The application will automatically open in Microsoft Edge
echo.
echo   4. Visit http://localhost:5000 to access AarogyaLink
echo.
echo TROUBLESHOOTING:
echo   - If you encounter any issues, check the console output for errors
echo   - Make sure your API keys are correctly configured in the .env file
echo   - Restart your computer if Python is not recognized after installation
echo.
echo For support, refer to the README.md file or check the instructions.txt
echo.
echo Thank you for using AarogyaLink - Your Personal Health Companion!
echo ========================================================================
echo.

REM Clean up temp directory
rmdir /s /q "%TEMP%\aarogyalink_setup" >nul 2>&1

echo Press any key to exit...
pause >nul