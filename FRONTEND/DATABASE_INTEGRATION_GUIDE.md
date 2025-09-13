# AarogyaLink Database Integration Guide

## 📋 Database Selection & Architecture

### Recommended Database: PostgreSQL

**Why PostgreSQL?**
- **HIPAA Compliance Ready**: Robust security features for healthcare data
- **JSON Support**: Native JSON/JSONB columns for flexible health data storage
- **ACID Compliance**: Ensures data integrity for critical health information
- **Scalability**: Handles large volumes of health records efficiently
- **Rich Ecosystem**: Excellent Flask integration with SQLAlchemy

### Alternative Options:
1. **MySQL** - Good performance, widely supported
2. **SQLite** - Development/testing (already partially configured)
3. **MongoDB** - NoSQL option for flexible document storage

---

## 🏗️ Database Schema Design

### Core Tables Structure:

#### 1. Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    user_id UUID UNIQUE NOT NULL DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE,
    username VARCHAR(100),
    password_hash VARCHAR(255),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    date_of_birth DATE,
    phone_number VARCHAR(20),
    emergency_contact JSONB,
    medical_conditions JSONB,
    allergies JSONB,
    medications JSONB,
    preferred_language VARCHAR(10) DEFAULT 'en',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT true,
    email_verified BOOLEAN DEFAULT false,
    last_login TIMESTAMP
);
```

#### 2. Chat Sessions Table
```sql
CREATE TABLE chat_sessions (
    id SERIAL PRIMARY KEY,
    session_id UUID UNIQUE NOT NULL DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id),
    session_name VARCHAR(255),
    symptoms_summary TEXT,
    diagnosis_suggestions JSONB,
    severity_level INTEGER CHECK (severity_level BETWEEN 1 AND 10),
    session_language VARCHAR(10) DEFAULT 'en',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP,
    is_emergency BOOLEAN DEFAULT false,
    follow_up_required BOOLEAN DEFAULT false
);
```

#### 3. Messages Table
```sql
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    message_id UUID UNIQUE NOT NULL DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES chat_sessions(session_id),
    sender_type VARCHAR(10) CHECK (sender_type IN ('user', 'ai', 'system')),
    message_type VARCHAR(20) CHECK (message_type IN ('text', 'image', 'audio', 'ai_analysis')),
    content TEXT,
    metadata JSONB, -- Store file info, AI predictions, etc.
    ai_source VARCHAR(50), -- 'gemini', 'teachable', etc.
    confidence_score DECIMAL(3,2),
    language VARCHAR(10) DEFAULT 'en',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_sensitive BOOLEAN DEFAULT false,
    parent_message_id UUID REFERENCES messages(message_id)
);
```

#### 4. File Uploads Table
```sql
CREATE TABLE file_uploads (
    id SERIAL PRIMARY KEY,
    file_id UUID UNIQUE NOT NULL DEFAULT gen_random_uuid(),
    message_id UUID REFERENCES messages(message_id),
    user_id UUID REFERENCES users(user_id),
    original_filename VARCHAR(255),
    stored_filename VARCHAR(255),
    file_type VARCHAR(50),
    file_size INTEGER,
    mime_type VARCHAR(100),
    upload_path TEXT,
    analysis_results JSONB,
    is_processed BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP
);
```

#### 5. Health Records Table
```sql
CREATE TABLE health_records (
    id SERIAL PRIMARY KEY,
    record_id UUID UNIQUE NOT NULL DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id),
    session_id UUID REFERENCES chat_sessions(session_id),
    record_type VARCHAR(50), -- 'symptom', 'diagnosis', 'medication', 'vital_signs'
    record_data JSONB,
    severity INTEGER CHECK (severity BETWEEN 1 AND 10),
    date_recorded TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source VARCHAR(50), -- 'ai_analysis', 'user_input', 'manual'
    confidence_score DECIMAL(3,2),
    is_verified BOOLEAN DEFAULT false,
    notes TEXT
);
```

#### 6. AI Analysis Log Table
```sql
CREATE TABLE ai_analysis_log (
    id SERIAL PRIMARY KEY,
    analysis_id UUID UNIQUE NOT NULL DEFAULT gen_random_uuid(),
    message_id UUID REFERENCES messages(message_id),
    ai_service VARCHAR(50), -- 'gemini', 'teachable_machine', 'teachable_llm'
    input_data JSONB,
    output_data JSONB,
    processing_time_ms INTEGER,
    tokens_used INTEGER,
    cost_usd DECIMAL(10,4),
    success BOOLEAN DEFAULT true,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🔧 Implementation Steps

### Step 1: Install Required Packages

```bash
pip install psycopg2-binary sqlalchemy flask-sqlalchemy flask-migrate alembic
```

Update `requirements.txt`:
```txt
flask==2.3.3
flask-cors==4.0.0
flask-sqlalchemy==3.1.1
flask-migrate==4.0.5
psycopg2-binary==2.9.7
sqlalchemy==2.0.23
alembic==1.12.1
google-generativeai==0.3.2
Pillow==10.1.0
requests==2.31.0
python-dotenv==1.0.0
werkzeug==2.3.7
```

### Step 2: Database Configuration

Update `.env` file:
```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/aarogyalink_db
DATABASE_URL_DEV=sqlite:///aarogyalink_dev.db
DATABASE_URL_TEST=sqlite:///aarogyalink_test.db

# Database Pool Settings
DB_POOL_SIZE=20
DB_MAX_OVERFLOW=30
DB_POOL_TIMEOUT=30
DB_POOL_RECYCLE=1800
```

### Step 3: SQLAlchemy Models

Create `models.py`:
```python
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID, JSONB
from datetime import datetime
import uuid

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4)
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(100))
    password_hash = db.Column(db.String(255))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    date_of_birth = db.Column(db.Date)
    phone_number = db.Column(db.String(20))
    emergency_contact = db.Column(JSONB)
    medical_conditions = db.Column(JSONB)
    allergies = db.Column(JSONB)
    medications = db.Column(JSONB)
    preferred_language = db.Column(db.String(10), default='en')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    email_verified = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    chat_sessions = db.relationship('ChatSession', backref='user', lazy=True)
    health_records = db.relationship('HealthRecord', backref='user', lazy=True)

class ChatSession(db.Model):
    __tablename__ = 'chat_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.user_id'))
    session_name = db.Column(db.String(255))
    symptoms_summary = db.Column(db.Text)
    diagnosis_suggestions = db.Column(JSONB)
    severity_level = db.Column(db.Integer)
    session_language = db.Column(db.String(10), default='en')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    ended_at = db.Column(db.DateTime)
    is_emergency = db.Column(db.Boolean, default=False)
    follow_up_required = db.Column(db.Boolean, default=False)
    
    # Relationships
    messages = db.relationship('Message', backref='session', lazy=True)
    health_records = db.relationship('HealthRecord', backref='session', lazy=True)

class Message(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4)
    session_id = db.Column(UUID(as_uuid=True), db.ForeignKey('chat_sessions.session_id'))
    sender_type = db.Column(db.Enum('user', 'ai', 'system', name='sender_types'))
    message_type = db.Column(db.Enum('text', 'image', 'audio', 'ai_analysis', name='message_types'))
    content = db.Column(db.Text)
    metadata = db.Column(JSONB)
    ai_source = db.Column(db.String(50))
    confidence_score = db.Column(db.Numeric(3, 2))
    language = db.Column(db.String(10), default='en')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_sensitive = db.Column(db.Boolean, default=False)
    parent_message_id = db.Column(UUID(as_uuid=True), db.ForeignKey('messages.message_id'))
    
    # Relationships
    file_uploads = db.relationship('FileUpload', backref='message', lazy=True)

# ... Continue with other models
```

### Step 4: Database Integration in Flask App

Update `app.py`:
```python
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, User, ChatSession, Message, HealthRecord

# Add to your Flask app configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///aarogyalink.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': int(os.environ.get('DB_POOL_SIZE', 20)),
    'max_overflow': int(os.environ.get('DB_MAX_OVERFLOW', 30)),
    'pool_timeout': int(os.environ.get('DB_POOL_TIMEOUT', 30)),
    'pool_recycle': int(os.environ.get('DB_POOL_RECYCLE', 1800))
}

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)

# Updated chat endpoint with database integration
@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        message = data['message']
        session_id = data.get('session_id')  # Get existing session or create new
        user_id = data.get('user_id')  # In production, get from JWT/session
        
        # Create or get chat session
        if session_id:
            chat_session = ChatSession.query.filter_by(session_id=session_id).first()
        else:
            chat_session = ChatSession(
                user_id=user_id,
                session_name=f\"Health Chat {datetime.now().strftime('%Y-%m-%d %H:%M')}\"
            )
            db.session.add(chat_session)
            db.session.commit()
        
        # Save user message
        user_message = Message(
            session_id=chat_session.session_id,
            sender_type='user',
            message_type='text',
            content=message,
            language=data.get('language', 'en')
        )
        db.session.add(user_message)
        
        # Process with AI
        response = health_api.process_health_query(\"text\", message)
        
        # Save AI response
        ai_message = Message(
            session_id=chat_session.session_id,
            sender_type='ai',
            message_type='text',
            content=response['primary_response'],
            ai_source=response['source'],
            language=data.get('language', 'en'),
            parent_message_id=user_message.message_id
        )
        db.session.add(ai_message)
        db.session.commit()
        
        return jsonify({
            \"success\": True,
            \"response\": response['primary_response'],
            \"session_id\": str(chat_session.session_id),
            \"message_id\": str(ai_message.message_id)
        })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f\"Error in chat endpoint: {e}\")
        return jsonify({\"error\": \"Internal server error\"}), 500
```

---

## 🔐 Security & Privacy Considerations

### 1. Data Encryption
```python
from cryptography.fernet import Fernet

class EncryptedField:
    def __init__(self, key=None):
        self.key = key or os.environ.get('ENCRYPTION_KEY')
        self.cipher = Fernet(self.key)
    
    def encrypt(self, data):
        return self.cipher.encrypt(data.encode()).decode()
    
    def decrypt(self, data):
        return self.cipher.decrypt(data.encode()).decode()
```

### 2. HIPAA Compliance Features
- **Audit Logging**: Track all data access and modifications
- **Data Retention**: Automatic data purging after retention period
- **Access Controls**: Role-based permissions
- **Encryption**: At-rest and in-transit encryption

### 3. Privacy Settings
```python
class PrivacySettings(db.Model):
    user_id = db.Column(UUID, db.ForeignKey('users.user_id'), primary_key=True)
    data_retention_days = db.Column(db.Integer, default=730)  # 2 years
    allow_analytics = db.Column(db.Boolean, default=False)
    allow_research = db.Column(db.Boolean, default=False)
    anonymize_data = db.Column(db.Boolean, default=True)
```

---

## 📊 Performance Optimization

### 1. Database Indexing
```sql
-- Essential indexes for performance
CREATE INDEX idx_users_user_id ON users(user_id);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_chat_sessions_user_id ON chat_sessions(user_id);
CREATE INDEX idx_chat_sessions_created_at ON chat_sessions(created_at);
CREATE INDEX idx_messages_session_id ON messages(session_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);
CREATE INDEX idx_health_records_user_id ON health_records(user_id);
```

### 2. Query Optimization
```python
# Efficient pagination
def get_chat_history(session_id, page=1, per_page=20):
    return Message.query.filter_by(session_id=session_id)\\n                  .order_by(Message.created_at.desc())\\n                  .paginate(page=page, per_page=per_page, error_out=False)

# Efficient data loading with relationships
def get_user_sessions(user_id):
    return ChatSession.query.filter_by(user_id=user_id)\\n                      .options(db.joinedload(ChatSession.messages))\\n                      .order_by(ChatSession.created_at.desc())\\n                      .all()
```

---

## 🚀 Deployment Guide

### 1. PostgreSQL Setup (Production)
```bash
# Install PostgreSQL
sudo apt update
sudo apt install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
CREATE DATABASE aarogyalink_db;
CREATE USER aarogyalink_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE aarogyalink_db TO aarogyalink_user;
```

### 2. Migration Commands
```bash
# Initialize migrations
flask db init

# Create migration
flask db migrate -m \"Initial migration\"

# Apply migration
flask db upgrade

# Seed initial data
python seed_data.py
```

### 3. Backup Strategy
```bash
#!/bin/bash
# backup_db.sh
DB_NAME=\"aarogyalink_db\"
BACKUP_DIR=\"/path/to/backups\"
DATE=$(date +\"%Y%m%d_%H%M%S\")

pg_dump $DB_NAME | gzip > $BACKUP_DIR/aarogyalink_backup_$DATE.sql.gz

# Keep only last 30 days of backups
find $BACKUP_DIR -name \"aarogyalink_backup_*.sql.gz\" -mtime +30 -delete
```

---

## 📈 Analytics & Monitoring

### 1. Health Metrics Dashboard
```python
def get_analytics_data():
    return {
        'total_users': User.query.count(),
        'active_sessions': ChatSession.query.filter_by(ended_at=None).count(),
        'messages_today': Message.query.filter(
            Message.created_at >= datetime.utcnow().date()
        ).count(),
        'ai_accuracy': calculate_ai_accuracy(),
        'popular_symptoms': get_popular_symptoms()
    }
```

### 2. Database Monitoring
```python
import psutil
from sqlalchemy import text

def check_db_health():
    try:
        # Check connection
        db.session.execute(text('SELECT 1'))
        
        # Check table sizes
        result = db.session.execute(text(\"\"\"
            SELECT schemaname, tablename, 
                   pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
            FROM pg_tables WHERE schemaname = 'public'
            ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
        \"\"\"))
        
        return {'status': 'healthy', 'tables': result.fetchall()}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}
```

---

## 🔧 Next Steps

1. **Immediate Implementation**:
   - Set up PostgreSQL database
   - Create and run initial migrations
   - Implement user session management
   - Add basic chat history storage

2. **Phase 2 Enhancements**:
   - User authentication and authorization
   - Advanced health record management
   - AI analysis tracking and improvement
   - Data export/import functionality

3. **Phase 3 Advanced Features**:
   - Multi-tenant support for healthcare providers
   - Advanced analytics and reporting
   - Integration with electronic health records (EHR)
   - Telemedicine scheduling and management

This comprehensive database integration will provide a solid foundation for AarogyaLink's growth while ensuring data security, performance, and compliance with healthcare regulations."