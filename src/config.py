#!/usr/bin/env python3
"""
Configuration file for AI-Based Attendance & Emotion Analytics System
"""

import os
from pathlib import Path

# ====================================================================
# DIRECTORY STRUCTURE
# ====================================================================

# Base directory (project root)
# Base directory (project root)
# config.py is in src/, so project root is parent directory
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
# CAMERA SETTINGS
# ====================================================================

CAMERA_INDEX = 0  # Default webcam (0 = primary camera)
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CAMERA_FPS = 30

# Image capture settings
IMAGE_FORMAT = "jpg"
IMAGE_QUALITY = 95  # JPEG quality (0-100)

# ====================================================================
# FACE RECOGNITION SETTINGS
# ====================================================================

# Face detection model: 'hog' (faster, CPU) or 'cnn' (accurate, GPU)
FACE_DETECTION_MODEL = 'hog'

# Face recognition tolerance (lower = more strict, default: 0.6)
FACE_RECOGNITION_TOLERANCE = 0.6

# Number of times to re-sample when encoding faces
FACE_ENCODING_JITTERS = 1

# Minimum face size to detect (in pixels)
MIN_FACE_SIZE = 50

# ====================================================================
# EMOTION DETECTION SETTINGS
# ====================================================================

# Emotion detection backend: 'opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface'
EMOTION_BACKEND = 'opencv'

# Emotion model: 'VGGFace', 'Facenet', 'OpenFace', 'DeepFace', 'DeepID', 'ArcFace', 'Dlib'
EMOTION_MODEL = 'VGG-Face'

# Emotions to detect
EMOTIONS = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']

# Confidence threshold for emotion detection (0-100)
EMOTION_CONFIDENCE_THRESHOLD = 60

# ====================================================================
# REPORT GENERATION SETTINGS
# ====================================================================

# Report format: 'txt', 'docx', or 'both'
REPORT_FORMAT = 'both'

# Report naming convention: timestamp format
REPORT_TIMESTAMP_FORMAT = "%Y-%m-%d_%H-%M-%S"

# Include emotion charts in reports
INCLUDE_EMOTION_CHARTS = True

# ====================================================================
# EMAIL AUTOMATION SETTINGS
# ====================================================================

# Email configuration
EMAIL_ENABLED = True  # Set to False to disable email sending

# SMTP settings (Gmail example)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USE_TLS = True

# Sender credentials (IMPORTANT: Update these with your actual credentials)
SENDER_EMAIL = "your.email@gmail.com"  # Change this
SENDER_PASSWORD = "your_app_password"  # Change this (use App Password for Gmail)

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

This is an automated email from the Attendance System.

Best regards,
Attendance System
"""

# ====================================================================
# TIMETABLE CONFIGURATION
# ====================================================================

# Subject to faculty email mapping
# Subject to faculty email mapping
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

# Default fallback email (if subject not in timetable)
DEFAULT_FACULTY_EMAIL = "ombhamer06@gmail.com"

# ====================================================================
# DATA CLEANUP SETTINGS
# ====================================================================

# Data retention period (days)
DATA_RETENTION_DAYS = 7

# Directories to cleanup
CLEANUP_DIRECTORIES = [IMAGES_DIR, LOGS_DIR, REPORTS_DIR]

# File extensions to cleanup
CLEANUP_FILE_EXTENSIONS = ['.jpg', '.png', '.log', '.txt', '.docx']

# ====================================================================
# SYSTEM SETTINGS
# ====================================================================

# Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL
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

# Theme colors
# Theme colors (Modern Dark / Glassmorphism)
THEME_COLORS = {
    'background': '#0f172a',    # Slate-900 (Main App Background)
    'surface': '#1e293b',       # Slate-800 (Cards/Sidebar)
    'primary': '#6366f1',       # Indigo-500 (Primary Actions)
    'primary_dark': '#4338ca',  # Indigo-700
    'secondary': '#a855f7',     # Purple-500 (Accents)
    'accent': '#06b6d4',        # Cyan-500 (Highlights)
    'success': '#10b981',       # Emerald-500
    'danger': '#ef4444',        # Red-500
    'warning': '#f59e0b',       # Amber-500
    'info': '#3b82f6',          # Blue-500
    'text': '#f8fafc',          # Slate-50 (Primary Text)
    'text_dim': '#94a3b8',      # Slate-400 (Secondary Text)
    'border': '#334155'         # Slate-700
}

# Font settings
FONT_FAMILY = "Segoe UI"  # Clean, modern system font
FONT_SIZE_SMALL = 11
FONT_SIZE_NORMAL = 13
FONT_SIZE_LARGE = 16
FONT_SIZE_HEADING = 20
FONT_SIZE_TITLE = 28
FONT_SIZE_HERO = 36

# ====================================================================
# ADVANCED SETTINGS
# ====================================================================

# Performance optimization
USE_GPU = False  # Set to True if GPU is available
PARALLEL_PROCESSING = True

# Debug mode
DEBUG_MODE = False  # Set to True for verbose logging

# Feature flags
ENABLE_LIVE_PREVIEW = True
ENABLE_EMOTION_TRACKING = True
ENABLE_AUTO_CLEANUP = True
ENABLE_NOTIFICATIONS = True

# ====================================================================
# HELPER FUNCTIONS
# ====================================================================

def get_faculty_email(subject):
    """Get faculty email for a subject"""
    return TIMETABLE.get(subject, DEFAULT_FACULTY_EMAIL)

def get_all_subjects():
    """Get list of all configured subjects"""
    return list(TIMETABLE.keys())

def is_email_configured():
    """Check if email is properly configured"""
    return (EMAIL_ENABLED and 
            SENDER_EMAIL != "your.email@gmail.com" and 
            SENDER_PASSWORD != "your_app_password")

# ====================================================================
# CONSTANTS
# ====================================================================

APP_NAME = "AI Attendance System"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Your Name"
APP_DESCRIPTION = "Automated Attendance & Classroom Emotion Analytics System"

# Status messages
STATUS_READY = "Ready"
STATUS_PROCESSING = "Processing..."
STATUS_COMPLETE = "Complete"
STATUS_ERROR = "Error"

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
]