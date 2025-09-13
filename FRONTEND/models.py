"""
AarogyaLink Database Models
SQLAlchemy models for health companion application
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid
import json

# Try to import PostgreSQL-specific types, fallback to standard types for SQLite
try:
    from sqlalchemy.dialects.postgresql import UUID, JSONB
    use_postgresql = True
except ImportError:
    from sqlalchemy import String as UUID
    from sqlalchemy import Text as JSONB
    use_postgresql = False

db = SQLAlchemy()

# Helper function for UUID generation
def generate_uuid():
    return str(uuid.uuid4()) if not use_postgresql else uuid.uuid4()

class User(db.Model):
    """User model for storing patient information"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36) if not use_postgresql else UUID(as_uuid=True), 
                       unique=True, nullable=False, default=generate_uuid)
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(100))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    date_of_birth = db.Column(db.Date)
    phone_number = db.Column(db.String(20))
    
    # Health information stored as JSON
    medical_conditions = db.Column(db.Text if not use_postgresql else JSONB)
    allergies = db.Column(db.Text if not use_postgresql else JSONB)
    medications = db.Column(db.Text if not use_postgresql else JSONB)
    emergency_contact = db.Column(db.Text if not use_postgresql else JSONB)
    
    # Preferences
    preferred_language = db.Column(db.String(10), default='en')
    
    # Timestamps and status
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    email_verified = db.Column(db.Boolean, default=False)
    
    # Relationships
    chat_sessions = db.relationship('ChatSession', backref='user', lazy=True, cascade='all, delete-orphan')
    health_records = db.relationship('HealthRecord', backref='user', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        """Convert user object to dictionary"""
        return {
            'user_id': str(self.user_id),
            'email': self.email,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'preferred_language': self.preferred_language,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_active': self.is_active
        }

class ChatSession(db.Model):
    """Chat session model for organizing conversations"""
    __tablename__ = 'chat_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(36) if not use_postgresql else UUID(as_uuid=True), 
                          unique=True, nullable=False, default=generate_uuid)
    user_id = db.Column(db.String(36) if not use_postgresql else UUID(as_uuid=True), 
                       db.ForeignKey('users.user_id'), nullable=True)  # Allow anonymous sessions
    
    # Session metadata
    session_name = db.Column(db.String(255))
    symptoms_summary = db.Column(db.Text)
    diagnosis_suggestions = db.Column(db.Text if not use_postgresql else JSONB)
    severity_level = db.Column(db.Integer)  # 1-10 scale
    session_language = db.Column(db.String(10), default='en')
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    ended_at = db.Column(db.DateTime)
    
    # Flags
    is_emergency = db.Column(db.Boolean, default=False)
    follow_up_required = db.Column(db.Boolean, default=False)
    
    # Relationships
    messages = db.relationship('Message', backref='session', lazy=True, cascade='all, delete-orphan')
    health_records = db.relationship('HealthRecord', backref='session', lazy=True)

    def to_dict(self):
        """Convert session object to dictionary"""
        return {
            'session_id': str(self.session_id),
            'user_id': str(self.user_id) if self.user_id else None,
            'session_name': self.session_name,
            'symptoms_summary': self.symptoms_summary,
            'severity_level': self.severity_level,
            'session_language': self.session_language,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'ended_at': self.ended_at.isoformat() if self.ended_at else None,
            'is_emergency': self.is_emergency,
            'follow_up_required': self.follow_up_required,
            'message_count': len(self.messages) if self.messages else 0
        }

class Message(db.Model):
    """Message model for storing chat interactions"""
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.String(36) if not use_postgresql else UUID(as_uuid=True), 
                          unique=True, nullable=False, default=generate_uuid)
    session_id = db.Column(db.String(36) if not use_postgresql else UUID(as_uuid=True), 
                          db.ForeignKey('chat_sessions.session_id'), nullable=False)
    
    # Message details
    sender_type = db.Column(db.String(10))  # 'user', 'ai', 'system'
    message_type = db.Column(db.String(20))  # 'text', 'image', 'audio', 'ai_analysis'
    content = db.Column(db.Text)
    
    # AI-specific fields
    ai_source = db.Column(db.String(50))  # 'gemini', 'teachable_machine', 'teachable_llm'
    confidence_score = db.Column(db.Float)
    metadata = db.Column(db.Text if not use_postgresql else JSONB)  # File info, predictions, etc.
    
    # Language and sensitivity
    language = db.Column(db.String(10), default='en')
    is_sensitive = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Parent-child relationship for threaded conversations
    parent_message_id = db.Column(db.String(36) if not use_postgresql else UUID(as_uuid=True), 
                                 db.ForeignKey('messages.message_id'))
    
    # Relationships
    file_uploads = db.relationship('FileUpload', backref='message', lazy=True)
    replies = db.relationship('Message', backref=db.backref('parent', remote_side=[message_id]))

    def to_dict(self):
        """Convert message object to dictionary"""
        return {
            'message_id': str(self.message_id),
            'session_id': str(self.session_id),
            'sender_type': self.sender_type,
            'message_type': self.message_type,
            'content': self.content,
            'ai_source': self.ai_source,
            'confidence_score': self.confidence_score,
            'metadata': json.loads(self.metadata) if self.metadata and isinstance(self.metadata, str) else self.metadata,
            'language': self.language,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'parent_message_id': str(self.parent_message_id) if self.parent_message_id else None
        }

class FileUpload(db.Model):
    """File upload model for storing uploaded files metadata"""
    __tablename__ = 'file_uploads'
    
    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.String(36) if not use_postgresql else UUID(as_uuid=True), 
                       unique=True, nullable=False, default=generate_uuid)
    message_id = db.Column(db.String(36) if not use_postgresql else UUID(as_uuid=True), 
                          db.ForeignKey('messages.message_id'))
    user_id = db.Column(db.String(36) if not use_postgresql else UUID(as_uuid=True), 
                       db.ForeignKey('users.user_id'))
    
    # File details
    original_filename = db.Column(db.String(255))
    stored_filename = db.Column(db.String(255))
    file_type = db.Column(db.String(50))  # 'image', 'audio'
    file_size = db.Column(db.Integer)
    mime_type = db.Column(db.String(100))
    upload_path = db.Column(db.Text)
    
    # Analysis results
    analysis_results = db.Column(db.Text if not use_postgresql else JSONB)
    is_processed = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)  # For automatic cleanup

    def to_dict(self):
        """Convert file upload object to dictionary"""
        return {
            'file_id': str(self.file_id),
            'message_id': str(self.message_id) if self.message_id else None,
            'original_filename': self.original_filename,
            'file_type': self.file_type,
            'file_size': self.file_size,
            'mime_type': self.mime_type,
            'is_processed': self.is_processed,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'analysis_results': json.loads(self.analysis_results) if self.analysis_results and isinstance(self.analysis_results, str) else self.analysis_results
        }

class HealthRecord(db.Model):
    """Health record model for storing structured health data"""
    __tablename__ = 'health_records'
    
    id = db.Column(db.Integer, primary_key=True)
    record_id = db.Column(db.String(36) if not use_postgresql else UUID(as_uuid=True), 
                         unique=True, nullable=False, default=generate_uuid)
    user_id = db.Column(db.String(36) if not use_postgresql else UUID(as_uuid=True), 
                       db.ForeignKey('users.user_id'))
    session_id = db.Column(db.String(36) if not use_postgresql else UUID(as_uuid=True), 
                          db.ForeignKey('chat_sessions.session_id'))
    
    # Record details
    record_type = db.Column(db.String(50))  # 'symptom', 'diagnosis', 'medication', 'vital_signs'
    record_data = db.Column(db.Text if not use_postgresql else JSONB)
    severity = db.Column(db.Integer)  # 1-10 scale
    
    # Source and verification
    source = db.Column(db.String(50))  # 'ai_analysis', 'user_input', 'manual'
    confidence_score = db.Column(db.Float)
    is_verified = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text)
    
    # Timestamps
    date_recorded = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Convert health record object to dictionary"""
        return {
            'record_id': str(self.record_id),
            'user_id': str(self.user_id) if self.user_id else None,
            'session_id': str(self.session_id) if self.session_id else None,
            'record_type': self.record_type,
            'record_data': json.loads(self.record_data) if self.record_data and isinstance(self.record_data, str) else self.record_data,
            'severity': self.severity,
            'source': self.source,
            'confidence_score': self.confidence_score,
            'is_verified': self.is_verified,
            'notes': self.notes,
            'date_recorded': self.date_recorded.isoformat() if self.date_recorded else None
        }

class AIAnalysisLog(db.Model):
    """AI analysis log model for tracking AI service usage"""
    __tablename__ = 'ai_analysis_log'
    
    id = db.Column(db.Integer, primary_key=True)
    analysis_id = db.Column(db.String(36) if not use_postgresql else UUID(as_uuid=True), 
                           unique=True, nullable=False, default=generate_uuid)
    message_id = db.Column(db.String(36) if not use_postgresql else UUID(as_uuid=True), 
                          db.ForeignKey('messages.message_id'))
    
    # AI service details
    ai_service = db.Column(db.String(50))  # 'gemini', 'teachable_machine', 'teachable_llm'
    input_data = db.Column(db.Text if not use_postgresql else JSONB)
    output_data = db.Column(db.Text if not use_postgresql else JSONB)
    
    # Performance metrics
    processing_time_ms = db.Column(db.Integer)
    tokens_used = db.Column(db.Integer)
    cost_usd = db.Column(db.Float)
    
    # Status
    success = db.Column(db.Boolean, default=True)
    error_message = db.Column(db.Text)
    
    # Timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Convert AI analysis log object to dictionary"""
        return {
            'analysis_id': str(self.analysis_id),
            'message_id': str(self.message_id) if self.message_id else None,
            'ai_service': self.ai_service,
            'processing_time_ms': self.processing_time_ms,
            'tokens_used': self.tokens_used,
            'cost_usd': self.cost_usd,
            'success': self.success,
            'error_message': self.error_message,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# Database utility functions
def init_db(app):
    """Initialize database with Flask app"""
    db.init_app(app)
    
def create_tables(app):
    """Create all database tables"""
    with app.app_context():
        db.create_all()
        
def drop_tables(app):
    """Drop all database tables (use with caution!)"""
    with app.app_context():
        db.drop_all()

# Helper functions for common queries
def get_or_create_session(user_id=None, session_name=None):
    """Get existing session or create new one"""
    session = ChatSession(
        user_id=user_id,
        session_name=session_name or f"Health Chat {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    )
    db.session.add(session)
    db.session.commit()
    return session

def save_message(session_id, sender_type, message_type, content, ai_source=None, metadata=None, language='en'):
    """Save a message to the database"""
    message = Message(
        session_id=session_id,
        sender_type=sender_type,
        message_type=message_type,
        content=content,
        ai_source=ai_source,
        metadata=json.dumps(metadata) if metadata and not isinstance(metadata, str) else metadata,
        language=language
    )
    db.session.add(message)
    db.session.commit()
    return message

def get_chat_history(session_id, limit=50):
    """Get chat history for a session"""
    return Message.query.filter_by(session_id=session_id)\
                  .order_by(Message.created_at.asc())\
                  .limit(limit).all()

def get_user_sessions(user_id, limit=20):
    """Get user's recent chat sessions"""
    return ChatSession.query.filter_by(user_id=user_id)\
                      .order_by(ChatSession.created_at.desc())\
                      .limit(limit).all()