#!/usr/bin/env python3
"""
Configuration file
Yaha saari settings change kar sakte hai
"""

import os
from pathlib import Path

# ====================================================================
# FOLDER STRUCTURE
# ====================================================================

# Base directory (project root)
# config.py src/ me hai, toh parent uske bahar hai
BASE_DIR = Path(__file__).parent.parent.absolute()

# Data directories
DATA_DIR = BASE_DIR / "data"
IMAGES_DIR = DATA_DIR / "images"
STUDENT_DATASET_DIR = DATA_DIR / "student_dataset"
REPORTS_DIR = DATA_DIR / "reports"
LOGS_DIR = DATA_DIR / "logs"
ENCODINGS_DIR = DATA_DIR / "encodings"

# Ensure directories exist
for directory in [DATA_DIR, IMAGES_DIR, STUDENT_DATASET_DIR, REPORTS_DIR, LOGS_DIR, ENCODINGS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# File paths
ENCODINGS_FILE = ENCODINGS_DIR / "face_encodings.pkl"

# ====================================================================
# CAMERA KI SETTING
# ====================================================================

CAMERA_INDEX = 0  # 0 matlab laptop ka webcam
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CAMERA_FPS = 30

# Image capture settings
IMAGE_FORMAT = "jpg"
IMAGE_QUALITY = 95  # Quality mast honi chahiye

# ====================================================================
# FACE RECOGNITION KI SETTING
# ====================================================================

# Face detection model: 'hog' (fast hai) ya 'cnn' (bhaari hai)
FACE_DETECTION_MODEL = 'hog'

# Face recognition tolerance (jitna kam, utna strict, default: 0.6)
FACE_RECOGNITION_TOLERANCE = 0.6

# Similarity threshold for DeepFace
# Kam matlab strict checking
SIMILARITY_THRESHOLD = 0.45

# Face encoding jitters
FACE_ENCODING_JITTERS = 1

# Minimum face size (pixels me)
MIN_FACE_SIZE = 50

# ====================================================================
# EMOTION DETECTION KA JUGAD
# ====================================================================

# Emotion backend
EMOTION_BACKEND = 'opencv'

# Emotion model
EMOTION_MODEL = 'VGG-Face'

# Emotions jo detect karne hai
EMOTIONS = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']

# Confidence threshold (0-100)
EMOTION_CONFIDENCE_THRESHOLD = 60

# ====================================================================
# REPORT GENERATION SETTINGS
# ====================================================================

# Report format: 'txt', 'docx', ya 'both'
REPORT_FORMAT = 'both'

# Report naming convention
REPORT_TIMESTAMP_FORMAT = "%Y-%m-%d_%H-%M-%S"

# Charts chahiye report me?
INCLUDE_EMOTION_CHARTS = True

# ====================================================================
# EMAIL AUTOMATION SETTINGS
# ====================================================================

# Email configuration
EMAIL_ENABLED = True  # False kardo agar email nahi bhejna

# SMTP settings (Gmail ke liye)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USE_TLS = True

# Sender credentials (IMP: Apna email daalna yaha)
SENDER_EMAIL = "your.email@gmail.com"  # Change this
SENDER_PASSWORD = "your_app_password"  # Change this (App Password use karna)

# Email subject template
EMAIL_SUBJECT_TEMPLATE = "Attendance Report - {subject} - {date}"

# Email body template
EMAIL_BODY_TEMPLATE = """
Dear Faculty,

Please find attached the attendance report for {subject} on {date}.

Session Details:
- Subject: {subject}
- Date: {date}
- Time: {time}
- Total Students: {total}
- Present: {present}
- Absent: {absent}
- Attendance Rate: {rate}%

Class Emotion Summary:
{emotion_summary}

This is a smart system generated email.

Best regards,
Om Bhamare System
"""

# ====================================================================
# TIMETABLE CONFIGURATION
# ====================================================================

# Subject aur teacher ka email mapping
TIMETABLE = {
    "DBMS": "",
    "MP": "",
    "DAA": "",
    "DTS": "",
    "ED": "",
    "OE": "",
    "ADPL": "",
    "DBMSL": ""
}

# Default email agar subject nahi mila
DEFAULT_FACULTY_EMAIL = "ombhamer06@gmail.com"

# ====================================================================
# DATA CLEANUP SETTINGS
# ====================================================================

# Kitne din ka data rakhna hai
DATA_RETENTION_DAYS = 7

# Directories to cleanup
CLEANUP_DIRECTORIES = [IMAGES_DIR, LOGS_DIR, REPORTS_DIR]

# File extensions to cleanup
CLEANUP_FILE_EXTENSIONS = ['.jpg', '.png', '.log', '.txt', '.docx']

# ====================================================================
# SYSTEM SETTINGS
# ====================================================================

# Logging level
LOG_LEVEL = "INFO"

# Maximum concurrent processes
MAX_WORKERS = 4

# Session timeout (seconds)
SESSION_TIMEOUT = 300

# Auto-save interval (seconds)
AUTO_SAVE_INTERVAL = 60

# ====================================================================
# GUI SETTINGS
# ====================================================================

# Window settings
WINDOW_TITLE = "Attendance & Emotion Analytics System"
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
WINDOW_RESIZABLE = True

# Theme colors (Dark Mode FTW)
THEME_COLORS = {
    'background': '#0f172a',    # Slate-900 
    'surface': '#1e293b',       # Slate-800
    'primary': '#6366f1',       # Indigo-500
    'primary_dark': '#4338ca',  # Indigo-700
    'secondary': '#a855f7',     # Purple-500
    'accent': '#06b6d4',        # Cyan-500
    'success': '#10b981',       # Emerald-500
    'danger': '#ef4444',        # Red-500
    'warning': '#f59e0b',       # Amber-500
    'info': '#3b82f6',          # Blue-500
    'text': '#f8fafc',          # Slate-50
    'text_dim': '#94a3b8',      # Slate-400
    'border': '#334155'         # Slate-700
}

# Font settings
FONT_FAMILY = "Segoe UI"  # Clean font
FONT_SIZE_SMALL = 11
FONT_SIZE_NORMAL = 13
FONT_SIZE_LARGE = 16
FONT_SIZE_HEADING = 20
FONT_SIZE_TITLE = 28
FONT_SIZE_HERO = 36

# ====================================================================
# ADVANCED SETTINGS
# ====================================================================

# Performance stuff
USE_GPU = False  # GPU hai toh True karo
PARALLEL_PROCESSING = True

# Debug mode
DEBUG_MODE = False  # Sab kuch print hoga agar True kiya

# Feature flags
ENABLE_LIVE_PREVIEW = True
ENABLE_EMOTION_TRACKING = True
ENABLE_AUTO_CLEANUP = True
ENABLE_NOTIFICATIONS = True

# ====================================================================
# HELPER FUNCTIONS
# ====================================================================

def get_faculty_email(subject):
    """Teacher ka email nikalte hai"""
    return TIMETABLE.get(subject, DEFAULT_FACULTY_EMAIL)

def get_all_subjects():
    """Saare subjects ki list"""
    return list(TIMETABLE.keys())

def is_email_configured():
    """Check karte hai email set hai ya nahi"""
    return (EMAIL_ENABLED and 
            SENDER_EMAIL != "your.email@gmail.com" and 
            SENDER_PASSWORD != "your_app_password")

# ====================================================================
# CONSTANTS
# ====================================================================

APP_NAME = "Smart Attendance System"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Om Bhamare"
APP_DESCRIPTION = "Automated Attendance & Classroom Emotion Analytics System"

# Status messages
STATUS_READY = "Ready"
STATUS_PROCESSING = "Kaam chalu hai..."
STATUS_COMPLETE = "Ho gaya"
STATUS_ERROR = "Lagg gaye (Error)"

# ====================================================================
# EXPORT ALL
# ====================================================================

__all__ = [
    # Directories
    'BASE_DIR', 'DATA_DIR', 'IMAGES_DIR', 'STUDENT_DATASET_DIR',
    'REPORTS_DIR', 'LOGS_DIR', 'ENCODINGS_DIR', 'ENCODINGS_FILE',
    
    # Camera
    'CAMERA_INDEX', 'CAMERA_WIDTH', 'CAMERA_HEIGHT', 'CAMERA_FPS',
    'IMAGE_FORMAT', 'IMAGE_QUALITY',
    
    # Face Recognition
    'FACE_DETECTION_MODEL', 'FACE_RECOGNITION_TOLERANCE',
    'FACE_ENCODING_JITTERS', 'MIN_FACE_SIZE',
    
    # Emotion Detection
    'EMOTION_BACKEND', 'EMOTION_MODEL', 'EMOTIONS',
    'EMOTION_CONFIDENCE_THRESHOLD',
    
    # Reports
    'REPORT_FORMAT', 'REPORT_TIMESTAMP_FORMAT', 'INCLUDE_EMOTION_CHARTS',
    
    # Email
    'EMAIL_ENABLED', 'SMTP_SERVER', 'SMTP_PORT', 'SMTP_USE_TLS',
    'SENDER_EMAIL', 'SENDER_PASSWORD', 'EMAIL_SUBJECT_TEMPLATE',
    'EMAIL_BODY_TEMPLATE', 'TIMETABLE', 'DEFAULT_FACULTY_EMAIL',
    
    # Data Cleanup
    'DATA_RETENTION_DAYS', 'CLEANUP_DIRECTORIES', 'CLEANUP_FILE_EXTENSIONS',
    
    # System
    'LOG_LEVEL', 'MAX_WORKERS', 'SESSION_TIMEOUT', 'AUTO_SAVE_INTERVAL',
    
    # GUI
    'WINDOW_TITLE', 'WINDOW_WIDTH', 'WINDOW_HEIGHT', 'WINDOW_RESIZABLE',
    'THEME_COLORS', 'FONT_FAMILY', 'FONT_SIZE_NORMAL', 'FONT_SIZE_LARGE',
    'FONT_SIZE_HEADING', 'FONT_SIZE_TITLE',
    
    # Advanced
    'USE_GPU', 'PARALLEL_PROCESSING', 'DEBUG_MODE',
    'ENABLE_LIVE_PREVIEW', 'ENABLE_EMOTION_TRACKING',
    'ENABLE_AUTO_CLEANUP', 'ENABLE_NOTIFICATIONS',
    
    # Helpers
    'get_faculty_email', 'get_all_subjects', 'is_email_configured',
    
    # Constants
    'APP_NAME', 'APP_VERSION', 'APP_AUTHOR', 'APP_DESCRIPTION',
    'STATUS_READY', 'STATUS_PROCESSING', 'STATUS_COMPLETE', 'STATUS_ERROR',
]   
 