🗄️ AarogyaLink Database Integration Guide
===========================================

This comprehensive guide will help you integrate a database into your AarogyaLink application for storing user conversations, health data, and application analytics.

## 📋 DATABASE SELECTION

### Recommended: PostgreSQL
Based on your project requirements, **PostgreSQL** is the ideal choice because:

✅ **Health Data Compliance**: HIPAA-ready with proper configuration
✅ **JSON Support**: Native JSON/JSONB for storing complex health records
✅ **Scalability**: Handles millions of records efficiently
✅ **Flask Integration**: Excellent SQLAlchemy support
✅ **Advanced Features**: Full-text search, analytics, time-series data
✅ **Free & Open Source**: No licensing costs

### Alternative Options:
- **SQLite**: Good for development/testing
- **MySQL**: Alternative relational database
- **MongoDB**: If you prefer NoSQL

## 🏗️ DATABASE SCHEMA DESIGN

### Core Tables

```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(20),
    preferred_language VARCHAR(5) DEFAULT 'en',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT true
);

-- Chat Sessions
CREATE TABLE chat_sessions (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) UNIQUE NOT NULL,
    user_id VARCHAR(255) REFERENCES users(user_id),
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP,
    session_type VARCHAR(50) DEFAULT 'health_consultation',
    language VARCHAR(5) DEFAULT 'en'
);

-- Messages (Core conversation storage)
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    message_id VARCHAR(255) UNIQUE NOT NULL,
    session_id VARCHAR(255) REFERENCES chat_sessions(session_id),
    sender_type VARCHAR(20) NOT NULL, -- 'user' or 'ai'
    content TEXT NOT NULL,
    message_type VARCHAR(50) DEFAULT 'text', -- 'text', 'image', 'audio', 'ai_analysis'
    metadata JSONB, -- Store additional data (predictions, file info, etc.)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ai_response_time_ms INTEGER -- Track AI response performance
);

-- Health Records (Optional - for tracking user health over time)
CREATE TABLE health_records (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) REFERENCES users(user_id),
    symptoms JSONB,
    ai_analysis JSONB,
    session_id VARCHAR(255) REFERENCES chat_sessions(session_id),
    severity_level INTEGER, -- 1-10 scale
    requires_attention BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- File Uploads
CREATE TABLE file_uploads (
    id SERIAL PRIMARY KEY,
    file_id VARCHAR(255) UNIQUE NOT NULL,
    message_id VARCHAR(255) REFERENCES messages(message_id),
    original_filename VARCHAR(255),
    file_type VARCHAR(50), -- 'image', 'audio'
    file_size INTEGER,
    file_path VARCHAR(500),
    mime_type VARCHAR(100),
    analysis_results JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- System Analytics
CREATE TABLE analytics (
    id SERIAL PRIMARY KEY,
    event_type VARCHAR(100) NOT NULL,
    event_data JSONB,
    user_id VARCHAR(255),
    session_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- API Usage Tracking
CREATE TABLE api_usage (
    id SERIAL PRIMARY KEY,
    api_provider VARCHAR(50), -- 'gemini', 'teachable'
    endpoint VARCHAR(100),
    request_data JSONB,
    response_data JSONB,
    response_time_ms INTEGER,
    status_code INTEGER,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Indexes for Performance
```sql
-- Essential indexes
CREATE INDEX idx_messages_session_id ON messages(session_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);
CREATE INDEX idx_chat_sessions_user_id ON chat_sessions(user_id);
CREATE INDEX idx_health_records_user_id ON health_records(user_id);
CREATE INDEX idx_analytics_event_type ON analytics(event_type);
CREATE INDEX idx_api_usage_created_at ON api_usage(created_at);

-- JSON indexes for fast queries
CREATE INDEX idx_messages_metadata ON messages USING GIN (metadata);
CREATE INDEX idx_health_records_symptoms ON health_records USING GIN (symptoms);
```

## 🔧 FLASK INTEGRATION

### 1. Install Required Packages
```bash
pip install psycopg2-binary SQLAlchemy Flask-SQLAlchemy python-dotenv
```

### 2. Update requirements.txt
Add these to your `requirements.txt`:
```
psycopg2-binary==2.9.7
SQLAlchemy==2.0.23
Flask-SQLAlchemy==3.0.5
```

### 3. Environment Configuration
Update your `.env` file:
```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/aarogyalink
DATABASE_POOL_SIZE=10
DATABASE_POOL_TIMEOUT=30
DATABASE_POOL_RECYCLE=3600

# Optional: Separate read/write databases for scaling
DATABASE_READ_URL=postgresql://readonly_user:password@localhost:5432/aarogyalink
```

### 4. Database Models (models.py)
```python
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid
import json

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(255), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    preferred_language = db.Column(db.String(5), default='en')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    chat_sessions = db.relationship('ChatSession', backref='user', lazy='dynamic')
    health_records = db.relationship('HealthRecord', backref='user', lazy='dynamic')

class ChatSession(db.Model):
    __tablename__ = 'chat_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(255), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(255), db.ForeignKey('users.user_id'))
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    ended_at = db.Column(db.DateTime)
    session_type = db.Column(db.String(50), default='health_consultation')
    language = db.Column(db.String(5), default='en')
    
    # Relationships
    messages = db.relationship('Message', backref='session', lazy='dynamic')

class Message(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.String(255), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    session_id = db.Column(db.String(255), db.ForeignKey('chat_sessions.session_id'))
    sender_type = db.Column(db.String(20), nullable=False)  # 'user' or 'ai'
    content = db.Column(db.Text, nullable=False)
    message_type = db.Column(db.String(50), default='text')
    metadata = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    ai_response_time_ms = db.Column(db.Integer)
    
    # Relationships
    file_uploads = db.relationship('FileUpload', backref='message', lazy='dynamic')

class HealthRecord(db.Model):
    __tablename__ = 'health_records'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(255), db.ForeignKey('users.user_id'))
    symptoms = db.Column(db.JSON)
    ai_analysis = db.Column(db.JSON)
    session_id = db.Column(db.String(255), db.ForeignKey('chat_sessions.session_id'))
    severity_level = db.Column(db.Integer)
    requires_attention = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class FileUpload(db.Model):
    __tablename__ = 'file_uploads'
    
    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.String(255), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    message_id = db.Column(db.String(255), db.ForeignKey('messages.message_id'))
    original_filename = db.Column(db.String(255))
    file_type = db.Column(db.String(50))
    file_size = db.Column(db.Integer)
    file_path = db.Column(db.String(500))
    mime_type = db.Column(db.String(100))
    analysis_results = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Analytics(db.Model):
    __tablename__ = 'analytics'
    
    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(100), nullable=False)
    event_data = db.Column(db.JSON)
    user_id = db.Column(db.String(255))
    session_id = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class APIUsage(db.Model):
    __tablename__ = 'api_usage'
    
    id = db.Column(db.Integer, primary_key=True)
    api_provider = db.Column(db.String(50))
    endpoint = db.Column(db.String(100))
    request_data = db.Column(db.JSON)
    response_data = db.Column(db.JSON)
    response_time_ms = db.Column(db.Integer)
    status_code = db.Column(db.Integer)
    error_message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

### 5. Update app.py with Database Support
```python
from flask import Flask, request, jsonify, render_template, session
from flask_sqlalchemy import SQLAlchemy
from models import db, User, ChatSession, Message, HealthRecord, FileUpload, Analytics
import os
from datetime import datetime
import uuid

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': int(os.environ.get('DATABASE_POOL_SIZE', 10)),
    'pool_timeout': int(os.environ.get('DATABASE_POOL_TIMEOUT', 30)),
    'pool_recycle': int(os.environ.get('DATABASE_POOL_RECYCLE', 3600)),
}

# Initialize database
db.init_app(app)

# Database helper functions
def get_or_create_user(user_identifier=None):
    """Get existing user or create new anonymous user"""
    if user_identifier:
        user = User.query.filter_by(user_id=user_identifier).first()
        if user:
            return user
    
    # Create new anonymous user
    user = User()
    db.session.add(user)
    db.session.commit()
    return user

def get_or_create_session(user_id, language='en'):
    """Get or create chat session for user"""
    # Check for existing active session
    session = ChatSession.query.filter_by(
        user_id=user_id,
        ended_at=None
    ).first()
    
    if not session:
        session = ChatSession(
            user_id=user_id,
            language=language
        )
        db.session.add(session)
        db.session.commit()
    
    return session

def save_message(session_id, sender_type, content, message_type='text', metadata=None, response_time=None):
    """Save message to database"""
    message = Message(
        session_id=session_id,
        sender_type=sender_type,
        content=content,
        message_type=message_type,
        metadata=metadata,
        ai_response_time_ms=response_time
    )
    db.session.add(message)
    db.session.commit()
    return message

def log_analytics(event_type, event_data=None, user_id=None, session_id=None):
    """Log analytics event"""
    analytics = Analytics(
        event_type=event_type,
        event_data=event_data,
        user_id=user_id,
        session_id=session_id
    )
    db.session.add(analytics)
    db.session.commit()

# Updated chat endpoint with database storage
@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        message = data['message']
        user_id = session.get('user_id')
        language = data.get('language', 'en')
        
        # Get or create user and session
        if not user_id:
            user = get_or_create_user()
            session['user_id'] = user.user_id
            user_id = user.user_id
        
        chat_session = get_or_create_session(user_id, language)
        
        # Save user message
        user_message = save_message(
            session_id=chat_session.session_id,
            sender_type='user',
            content=message,
            message_type=data.get('type', 'text'),
            metadata=data.get('metadata')
        )
        
        # Process AI response (existing logic)
        start_time = datetime.now()
        response = health_api.process_health_query("text", message)
        response_time = int((datetime.now() - start_time).total_seconds() * 1000)
        
        if response['primary_response']:
            # Save AI response
            ai_message = save_message(
                session_id=chat_session.session_id,
                sender_type='ai',
                content=response['primary_response'],
                response_time=response_time,
                metadata={
                    'source': response['source'],
                    'timestamp': response['timestamp']
                }
            )
            
            # Log analytics
            log_analytics(
                event_type='chat_interaction',
                event_data={
                    'message_length': len(message),
                    'response_time_ms': response_time,
                    'ai_source': response['source']
                },
                user_id=user_id,
                session_id=chat_session.session_id
            )
            
            return jsonify({
                "success": True,
                "response": response['primary_response'],
                "source": response['source'],
                "session_id": chat_session.session_id,
                "message_id": ai_message.message_id
            })
        else:
            return jsonify({"error": "Unable to process your query"}), 500
            
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        return jsonify({"error": "Internal server error"}), 500

# Get chat history endpoint
@app.route('/api/chat/history/<session_id>')
def get_chat_history(session_id):
    """Get chat history for a session"""
    try:
        messages = Message.query.filter_by(session_id=session_id).order_by(Message.created_at).all()
        
        history = []
        for msg in messages:
            history.append({
                'id': msg.message_id,
                'sender': msg.sender_type,
                'content': msg.content,
                'type': msg.message_type,
                'timestamp': msg.created_at.isoformat(),
                'metadata': msg.metadata
            })
        
        return jsonify({
            "success": True,
            "history": history,
            "session_id": session_id
        })
        
    except Exception as e:
        logger.error(f"Error getting chat history: {e}")
        return jsonify({"error": "Failed to retrieve chat history"}), 500

# Create database tables
@app.before_first_request
def create_tables():
    db.create_all()
    logger.info("Database tables created successfully")

if __name__ == '__main__':
    app.run(debug=True)
```

## 🚀 DEPLOYMENT SETUP

### 1. PostgreSQL Installation

#### Ubuntu/Debian:
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

#### macOS:
```bash
brew install postgresql
brew services start postgresql
```

#### Windows:
Download from: https://www.postgresql.org/download/windows/

### 2. Database Setup
```sql
-- Create database
CREATE DATABASE aarogyalink;

-- Create user
CREATE USER aarogyalink_user WITH PASSWORD 'secure_password_here';

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE aarogyalink TO aarogyalink_user;
```

### 3. Initialize Database
```python
# create_db.py
from app import app, db

with app.app_context():
    db.create_all()
    print("Database tables created successfully!")
```

Run: `python create_db.py`

## 📊 ANALYTICS & INSIGHTS

### Query Examples

#### 1. Most Common Health Concerns
```sql
SELECT 
    COUNT(*) as frequency,
    REGEXP_REPLACE(LOWER(content), '[^a-z ]+', '', 'g') as symptoms
FROM messages 
WHERE sender_type = 'user' 
    AND message_type = 'text'
    AND content ILIKE '%pain%'
GROUP BY symptoms
ORDER BY frequency DESC
LIMIT 10;
```

#### 2. AI Performance Metrics
```sql
SELECT 
    DATE(created_at) as date,
    AVG(ai_response_time_ms) as avg_response_time,
    COUNT(*) as total_responses,
    COUNT(CASE WHEN ai_response_time_ms > 5000 THEN 1 END) as slow_responses
FROM messages 
WHERE sender_type = 'ai' 
    AND created_at >= NOW() - INTERVAL '30 days'
GROUP BY DATE(created_at)
ORDER BY date DESC;
```

#### 3. User Engagement
```sql
SELECT 
    u.preferred_language,
    COUNT(DISTINCT cs.session_id) as total_sessions,
    AVG(msg_count.message_count) as avg_messages_per_session
FROM users u
JOIN chat_sessions cs ON u.user_id = cs.user_id
JOIN (
    SELECT session_id, COUNT(*) as message_count
    FROM messages
    GROUP BY session_id
) msg_count ON cs.session_id = msg_count.session_id
GROUP BY u.preferred_language;
```

## 🔒 SECURITY & PRIVACY

### 1. Data Encryption
```python
from cryptography.fernet import Fernet
import os

# Generate key (store securely)
encryption_key = Fernet.generate_key()
cipher_suite = Fernet(encryption_key)

def encrypt_sensitive_data(data):
    return cipher_suite.encrypt(data.encode()).decode()

def decrypt_sensitive_data(encrypted_data):
    return cipher_suite.decrypt(encrypted_data.encode()).decode()
```

### 2. Data Retention Policy
```sql
-- Delete old analytics data (keep 6 months)
DELETE FROM analytics WHERE created_at < NOW() - INTERVAL '6 months';

-- Archive old messages (keep 2 years)
CREATE TABLE messages_archive AS 
SELECT * FROM messages WHERE created_at < NOW() - INTERVAL '2 years';

DELETE FROM messages WHERE created_at < NOW() - INTERVAL '2 years';
```

### 3. User Data Privacy
```python
@app.route('/api/user/delete', methods=['POST'])
def delete_user_data():
    """GDPR-compliant user data deletion"""
    user_id = request.json.get('user_id')
    
    # Delete in correct order (foreign key constraints)
    FileUpload.query.join(Message).filter(Message.session_id.in_(
        db.session.query(ChatSession.session_id).filter_by(user_id=user_id)
    )).delete(synchronize_session=False)
    
    Message.query.join(ChatSession).filter(ChatSession.user_id == user_id).delete(synchronize_session=False)
    HealthRecord.query.filter_by(user_id=user_id).delete()
    ChatSession.query.filter_by(user_id=user_id).delete()
    Analytics.query.filter_by(user_id=user_id).delete()
    User.query.filter_by(user_id=user_id).delete()
    
    db.session.commit()
    return jsonify({"success": True})
```

## 📈 MONITORING & MAINTENANCE

### 1. Health Checks
```python
@app.route('/health/db')
def db_health_check():
    try:
        # Simple query to test database connection
        db.session.execute('SELECT 1')
        return jsonify({"database": "healthy"})
    except Exception as e:
        return jsonify({"database": "unhealthy", "error": str(e)}), 500
```

### 2. Database Backup Script
```bash
#!/bin/bash
# backup_db.sh
DB_NAME="aarogyalink"
BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)

pg_dump $DB_NAME > $BACKUP_DIR/aarogyalink_backup_$DATE.sql
gzip $BACKUP_DIR/aarogyalink_backup_$DATE.sql

# Keep only last 7 days of backups
find $BACKUP_DIR -name "aarogyalink_backup_*.sql.gz" -mtime +7 -delete
```

### 3. Performance Monitoring
```python
import time
from functools import wraps

def monitor_db_performance(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        duration = (time.time() - start_time) * 1000
        
        # Log slow queries
        if duration > 1000:  # 1 second
            logger.warning(f"Slow query detected: {func.__name__} took {duration:.2f}ms")
        
        return result
    return wrapper
```

## 🎯 NEXT STEPS

1. **Install PostgreSQL** on your system
2. **Create database** and user
3. **Update app.py** with database models
4. **Run migrations** to create tables
5. **Test database integration** with sample data
6. **Set up monitoring** and backup procedures
7. **Implement analytics dashboard** for insights

## 💡 ADVANCED FEATURES

### 1. Real-time Updates with WebSockets
```python
from flask_socketio import SocketIO, emit

socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('join_session')
def on_join(data):
    session_id = data['session_id']
    join_room(session_id)
    emit('status', {'msg': 'Connected to session'})
```

### 2. Health Data Analytics
```python
def generate_health_insights(user_id):
    """Generate personalized health insights"""
    records = HealthRecord.query.filter_by(user_id=user_id).all()
    
    # Analyze patterns
    symptoms_frequency = {}
    for record in records:
        for symptom in record.symptoms:
            symptoms_frequency[symptom] = symptoms_frequency.get(symptom, 0) + 1
    
    return {
        'common_symptoms': sorted(symptoms_frequency.items(), key=lambda x: x[1], reverse=True)[:5],
        'total_consultations': len(records),
        'average_severity': sum(r.severity_level for r in records if r.severity_level) / len(records)
    }
```

This database integration will transform your AarogyaLink application into a comprehensive health platform with persistent data storage, analytics capabilities, and scalable architecture!