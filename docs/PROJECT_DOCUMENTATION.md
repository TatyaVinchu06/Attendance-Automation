# AI-Based Automated Attendance & Classroom Emotion Analytics System

## Complete Technical Documentation

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Architecture](#architecture)
3. [Modules](#modules)
4. [Configuration](#configuration)
5. [API Reference](#api-reference)
6. [Database Schema](#database-schema)
7. [Privacy & Security](#privacy--security)
8. [Deployment](#deployment)

---

## System Overview

### Purpose

Automate classroom attendance using AI-powered face recognition while analyzing classroom emotions to provide actionable insights for educators.

### Key Capabilities

- **Face Recognition**: Identify and mark attendance for registered students
- **Emotion Detection**: Analyze classroom engagement through emotion analytics
- **Report Generation**: Create detailed attendance and emotion reports
- **Email Automation**: Deliver reports to faculty based on timetable
- **Privacy Compliance**: Auto-delete data after 7 days
- **User Interface**: Modern GUI for demonstrations and daily use

### Technology Stack

| Component | Technology |
|-----------|-----------|
| Face Recognition | `face-recognition`, `dlib`, OpenCV |
| Emotion Detection | DeepFace, TensorFlow, Keras |
| GUI Framework | Tkinter, Pillow |
| Report Generation | python-docx, Matplotlib |
| Email Automation | smtplib (built-in) |
| Task Scheduling | schedule |
| Data Processing | NumPy, Pandas |

---

## Architecture

### System Flow

```
┌─────────────┐
│   Camera    │
│   Capture   │
└──────┬──────┘
       │
       ▼
┌──────────────┐
│ Image Storage│
└──────┬───────┘
       │
       ├────────────┐
       ▼            ▼
┌──────────┐  ┌──────────┐
│   Face   │  │ Emotion  │
│   Recog  │  │ Detection│
└────┬─────┘  └────┬─────┘
     │             │
     └─────┬───────┘
           ▼
    ┌──────────────┐
    │  Attendance  │
    │   Manager    │
    └──────┬───────┘
           ▼
    ┌──────────────┐
    │    Report    │
    │  Generator   │
    └──────┬───────┘
           ▼
    ┌──────────────┐
    │    Email     │
    │  Automation  │
    └──────────────┘
           │
           ▼
    ┌──────────────┐
    │ Data Cleanup │
    │  (7 days)    │
    └──────────────┘
```

### Component Diagram

```
app_gui.py (Main GUI)
    │
    ├── image_capture.py
    │   └── [OpenCV Camera Interface]
    │
    ├── face_recognition_module.py
    │   └── [face-recognition, dlib]
    │
    ├── emotion_detection.py
    │   └── [DeepFace, TensorFlow]
    │
    ├── report_generator.py
    │   └── [python-docx, Text Processing]
    │
    ├── email_automation.py
    │   └── [smtplib, Email Handling]
    │
    └── data_cleanup.py
        └── [File Management, Scheduling]
```

---

## Modules

### 1. Image Capture (`image_capture.py`)

**Purpose**: Interface with camera and capture classroom images

**Key Classes**:
```python
class ImageCapture:
    def initialize_camera() -> bool
    def capture_image(class_id: str) -> str
    def capture_multiple_images(count: int, interval: int) -> List[str]
    def get_frame() -> np.ndarray
    def release_camera() -> None
```

**Configuration**:
- `CAMERA_INDEX`: Camera device index (default: 0)
- `CAMERA_WIDTH`: Frame width (default: 640)
- `CAMERA_HEIGHT`: Frame height (default: 480)
- `IMAGE_FORMAT`: Output format (default: jpg)

### 2. Face Recognition (`face_recognition_module.py`)

**Purpose**: Train and recognize student faces for attendance

**Key Classes**:
```python
class FaceRecognitionModule:
    def train_face_encodings() -> bool
    def save_encodings() -> bool
    def load_encodings() -> bool
    def recognize_faces(image_path: str) -> Dict[str, str]
    def get_all_students() -> List[str]
```

**Training Process**:
1. Load student photos from `data/student_dataset/`
2. Detect faces using HOG/CNN detector
3. Generate 128-dimensional face encodings
4. Save encodings to pickle file
5. Load for inference

**Attendance Logic**:
- All students marked "Absent" by default
- Present in ANY captured image → marked "Present"
- Confidence threshold configurable

### 3. Emotion Detection (`emotion_detection.py`)

**Purpose**: Analyze classroom emotions (privacy-safe, class-level only)

**Key Classes**:
```python
class EmotionDetection:
    def detect_emotions_in_image(image_path: str) -> List[str]
    def analyze_multiple_images(image_paths: List[str]) -> Dict[str, float]
    def get_dominant_emotion(summary: Dict) -> str
    def get_class_mood(summary: Dict) -> str
```

**Supported Emotions**:
- Angry
- Disgust
- Fear
- Happy
- Sad
- Surprise
- Neutral

**Privacy Note**: Individual emotions NOT stored, only class-level aggregates

### 4. Report Generation (`report_generator.py`)

**Purpose**: Generate formatted attendance reports

**Key Classes**:
```python
class ReportGenerator:
    def generate_report(...) -> List[str]
    def _generate_txt_report(...) -> str
    def _generate_docx_report(...) -> str
```

**Report Formats**:
- **TXT**: Plain text, console-friendly
- **DOCX**: Professional Word document with formatting

**Report Contents**:
- Subject, date, time
- Total/present/absent counts
- Attendance rate percentage
- List of present students
- List of absent students
- Class emotion summary

### 5. Email Automation (`email_automation.py`)

**Purpose**: Send reports via email based on timetable

**Key Classes**:
```python
class EmailAutomation:
    def test_email_connection() -> bool
    def send_attendance_report(subject: str, files: List[str]) -> bool
    def send_custom_email(...) -> bool
```

**SMTP Configuration**:
- Server: Gmail (default), configurable
- Port: 587 (TLS)
- Authentication: Required
- Attachments: Multiple file support

**Timetable Integration**:
- Maps subjects to faculty emails
- Automatic recipient selection
- Fallback email for unmapped subjects

### 6. Data Cleanup (`data_cleanup.py`)

**Purpose**: Enforce 7-day data retention policy

**Key Classes**:
```python
class DataCleanup:
    def get_directory_stats(directory: str) -> Dict
    def preview_cleanup() -> Dict
    def cleanup_directory(directory: str) -> Dict
    def cleanup_all() -> Dict
    def schedule_cleanup() -> schedule
```

**Cleanup Process**:
1. Check file modification times
2. Identify files older than threshold
3. Delete old files from configured directories
4. Log cleanup summary

**Scheduled Execution**:
- Runs daily at 2:00 AM
- Configurable via `schedule` library

### 7. GUI Application (`app_gui.py`)

**Purpose**: User-friendly interface for system interaction

**Key Pages**:

1. **Dashboard**
   - System statistics
   - Quick actions
   - Status indicators

2. **Student Database**
   - View registered students
   - Train face recognition
   - Manage dataset

3. **Live Capture**
   - Camera preview
   - Subject selection
   - Capture & process

4. **Reports**
   - List generated reports
   - Open/view reports
   - Access reports folder

5. **Settings**
   - Email configuration
   - System information
   - Configuration management

6. **Data Cleanup**
   - Preview old files
   - Execute cleanup
   - View statistics

---

## Configuration

### File: `config.py`

**Directory Structure**:
```python
BASE_DIR = project_root
DATA_DIR = BASE_DIR / "data"
IMAGES_DIR = DATA_DIR / "images"
STUDENT_DATASET_DIR = DATA_DIR / "student_dataset"
REPORTS_DIR = DATA_DIR / "reports"
LOGS_DIR = DATA_DIR / "logs"
ENCODINGS_DIR = DATA_DIR / "encodings"
```

**Camera Settings**:
```python
CAMERA_INDEX = 0
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CAMERA_FPS = 30
```

**Face Recognition**:
```python
FACE_DETECTION_MODEL = 'hog'  # or 'cnn'
FACE_RECOGNITION_TOLERANCE = 0.6
FACE_ENCODING_JITTERS = 1
```

**Emotion Detection**:
```python
EMOTION_BACKEND = 'opencv'
EMOTION_MODEL = 'VGG-Face'
EMOTIONS = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
```

**Email**:
```python
EMAIL_ENABLED = True
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "your.email@gmail.com"
SENDER_PASSWORD = "your_app_password"
```

**Timetable**:
```python
TIMETABLE = {
    "DBMS": "dbms.faculty@example.com",
    "OS": "os.faculty@example.com",
    # Add subjects...
}
```

**Data Retention**:
```python
DATA_RETENTION_DAYS = 7
```

---

## Privacy & Security

### Data Protection Measures

1. **Local Storage Only**
   - No cloud uploads
   - All data stored on local machine
   - No external API calls for face recognition

2. **Automatic Deletion**
   - 7-day retention policy
   - Scheduled cleanup at 2 AM daily
   - Compliance with privacy regulations

3. **Emotion Privacy**
   - NO individual emotion tracking
   - Only class-level aggregates stored
   - No personally identifiable emotion data

4. **Email Security**
   - TLS encryption for SMTP
   - App passwords recommended (not regular passwords)
   - Credentials stored in config (should be encrypted in production)

5. **Access Control**
   - Local GUI access only
   - No remote access by default
   - User responsible for physical security

### Compliance Considerations

- **GDPR**: Data minimization, retention limits, local storage
- **FERPA**: Student data protection, limited access
- **Informed Consent**: Students should be notified of attendance system

---

## Deployment

### Local Deployment (Recommended)

1. Install Python 3.8+
2. Install dependencies: `pip install -r requirements.txt`
3. Configure `config.py`
4. Add student photos
5. Train system
6. Run `run_app.bat`

### Production Considerations

**For Real Classroom Use**:

1. **Hardware**:
   - Dedicated PC/laptop
   - High-quality webcam
   - Stable internet (for email)

2. **Software**:
   - Windows 10/11 recommended
   - Antivirus exceptions for camera access
   - Scheduled startup script

3. **Configuration**:
   - Real faculty emails in timetable
   - Secure credential storage
   - Regular backup of encodings

4. **Maintenance**:
   - Weekly review of logs
   - Monthly re-training if students change
   - Regular cleanup verification

### Future Enhancements

- [ ] Multi-camera support
- [ ] Database integration (SQLite/PostgreSQL)
- [ ] Web-based interface
- [ ] Mobile app for faculty
- [ ] Advanced analytics dashboard
- [ ] Integration with LMS
- [ ] RESTful API
- [ ] Cloud deployment option

---

## Troubleshooting

### Common Issues

1. **Camera Not Detected**
   - Check camera connections
   - Verify camera index in config
   - Close other apps using camera
   - Check Windows privacy settings

2. **Face Recognition Fails**
   - Ensure good lighting
   - Add more training photos
   - Adjust tolerance in config
   - Retrain system

3. **Emotion Detection Slow**
   - Use GPU if available (`USE_GPU = True`)
   - Reduce image resolution
   - Use faster backend (opencv vs. mtcnn)

4. **Email Not Sending**
   - Verify SMTP credentials
   - Use Gmail App Password
   - Check firewall settings
   - Test with test_email_connection()

---

## Version History

- **v1.0.0** (2026-02-06): Initial release
  - Core attendance and emotion features
  - GUI application
  - Email automation
  - Data cleanup

---

## Credits

**Developed by**: Your Name
**Institution**: Your College/University
**Purpose**: Academic Project / Demonstration

**Libraries Used**:
- face-recognition by Adam Geitgey
- DeepFace by Sefik Ilkin Serengil
- OpenCV
- TensorFlow
- Python standard library

---

**For support, refer to README.md or contact the development team.**