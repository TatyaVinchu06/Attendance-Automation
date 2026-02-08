# Smart Attendance & Classroom Analytics System

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)](https://www.microsoft.com/windows)

**Made by Om Bhamare**

A comprehensive smart system for automating classroom attendance using advanced face recognition and analyzing student emotions to provide insights into classroom engagement.

## 🌟 Features

- **✅ Automated Attendance**: Multi-layer face verification with 3-model consensus system
- **😊 Emotion Analytics**: Classroom-level emotion detection and analysis
- **📊 Report Generation**: Automatic generation of TXT and DOCX reports
- **📧 Email Automation**: Timetable-based automatic email delivery to faculty
- **📈 Monthly Summary**: Comprehensive student attendance reports across all subjects
- **🔒 Privacy-First**: Auto-deletion of data after 7 days
- **🖥️ Modern GUI**: Premium Dark Mode interface with interactive real-time dashboard
- **📸 Live Camera Feed**: Real-time camera preview with manual "Upload Photo" analysis
- **⚙️ Advanced Tools**: Student management (Delete/Retrain) and System Cleanup

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Webcam/Camera
- Windows OS (tested on Windows 10/11)

### Installation

1. **Clone or download this repository**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup student database**:
   - Go to `data/student_dataset/`
   - Create one folder per student
   - Add 3-5 clear face photos per student

4. **Configure email** (optional):
   - Open `src/config.py`
   - Update `SENDER_EMAIL` and `SENDER_PASSWORD`
   - Update `TIMETABLE` with subject-to-faculty email mapping

5. **Launch the application**:
   ```bash
   python src/main.py
   ```

## 📖 User Guide

### 1. Enroll Students

1. Click **"Enrollment"** in the sidebar
2. Enter student Roll No and Name
3. Capture 5 photos using the live camera
4. Click **"Save Student"**
5. System automatically trains the recognition model

### 2. Run Attendance Session

1. Click **"Live Capture"** in the sidebar
2. Select the subject from dropdown
3. Click **"Start Camera"** to preview
4. Click **"Capture & Process"** to:
   - Capture classroom images
   - Recognize student faces using 3-layer verification
   - Detect emotions
   - Generate reports
   - Send email (if configured)

### 3. View Reports

1. Click **"Reports"** in the sidebar
2. Browse generated reports
3. Click **"Generate Monthly Summary"** for comprehensive attendance overview
4. Reports are available in both TXT and DOCX formats

### 4. System Settings

1. Click **"Settings"** in the sidebar
2. Configure email credentials
3. View system information
4. Check configuration status

## 🏗️ System Architecture

The system uses a sophisticated multi-layer verification approach:

### Face Recognition Pipeline
```
📸 Camera Capture
    ↓
🔍 Image Preprocessing (Auto-resize for large images)
    ↓
🧠 3-Layer Verification:
    - Layer 1: VGG-Face (Primary detection)
    - Layer 2: Facenet (Secondary verification)
    - Layer 3: ArcFace (Final validation)
    ↓
✓ Consensus Decision (2/3 models must agree)
    ↓
📊 Attendance Recorded
```

### Key Innovations

1. **Multi-Model Consensus**: Student must be confirmed by at least 2 out of 3 recognition models
2. **Similarity Thresholding**: Strict distance-based matching prevents false positives
3. **Duplicate Prevention**: Advanced tracking ensures no student is marked twice
4. **RetinaFace Detection**: State-of-the-art face detector for group photos

## 📁 Project Structure

```
cam/
├── src/
│   ├── main.py                    # Main GUI application
│   ├── config.py                  # Configuration settings
│   ├── image_capture.py           # Camera and image capture
│   ├── face_recognition_module.py # 3-layer face verification engine
│   ├── emotion_detection.py       # Emotion detection engine
│   ├── report_generator.py        # Report generation (TXT/DOCX)
│   ├── email_automation.py        # Email automation with SMTP
│   └── data_cleanup.py            # Auto-cleanup for privacy
├── data/                          # Data directory
│   ├── student_dataset/           # Student face photos
│   ├── images/                    # Captured classroom images
│   ├── reports/                   # Generated reports
│   └── logs/                      # System logs
└── requirements.txt               # Python dependencies
```

## ⚙️ Configuration

Key settings in `src/config.py`:

```python
# Data retention (privacy)
DATA_RETENTION_DAYS = 7

# Camera settings
CAMERA_INDEX = 0  # 0 = default camera

# Face recognition
SIMILARITY_THRESHOLD = 0.45  # Lower = stricter (0.40-0.50 recommended)

# Email settings
SENDER_EMAIL = "your.email@gmail.com"
SENDER_PASSWORD = "your_app_password"

# Timetable (subject → faculty email)
TIMETABLE = {
    "DBMS": "dbms.faculty@example.com",
    "DSA": "dsa.faculty@example.com",
    # Add more subjects...
}
```

## 🔧 Troubleshooting

### Camera not working
- Check if camera is connected and not used by another application
- Try changing `CAMERA_INDEX` in config.py (0, 1, 2...)
- Restart the application

### Face recognition accuracy issues
- Ensure good lighting when enrolling students
- Add 5+ photos per student from different angles
- Use clear, frontal face photos
- System uses 3-layer verification for maximum accuracy

### Email not sending
- Use Gmail App Password (not regular password)
- Enable "Less secure app access" or use App Passwords
- Check SMTP settings in config.py

### False positives in attendance
- System automatically prevents this with:
  - 3-model consensus (2/3 must agree)
  - Strict similarity thresholding
  - Duplicate detection

## 📚 Technologies Used

- **Face Recognition**: DeepFace (VGG-Face, Facenet, ArcFace), RetinaFace, OpenCV
- **Emotion Detection**: DeepFace, TensorFlow
- **GUI**: CustomTkinter (Modern Dark UI)
- **Reports**: python-docx
- **Email**: smtplib (built-in)

## 🛡️ Privacy & Data Security

- All data is stored locally (no cloud storage)
- Automatic data deletion after 7 days
- No personally identifiable information shared externally
- Only class-level emotion data (not individual emotions)
- Email communication encrypted with TLS

## 🎯 Accuracy Features

### Multi-Layer Verification
- **Layer 1**: VGG-Face model
- **Layer 2**: Facenet model  
- **Layer 3**: ArcFace model
- **Decision**: 2/3 models must agree to confirm presence

### Smart Detection
- RetinaFace detector for better group photo handling
- Automatic image preprocessing
- Distance-based similarity thresholds
- Prevents duplicate marking

## 📝 Author

**Om Bhamare**
- Smart Attendance & Classroom Analytics System
- Advanced Computer Vision & Pattern Recognition

---

**Made by Om Bhamare - Smart System for Automated Attendance**
