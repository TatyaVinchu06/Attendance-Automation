# Automated Attendance & Classroom Emotion Analytics System

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)](https://www.microsoft.com/windows)

A comprehensive AI-powered system for automating classroom attendance using face recognition and analyzing student emotions to provide insights into classroom engagement.

## 🌟 Features

- **✅ Automated Attendance**: Face recognition-based attendance marking with configurable intervals
- **😊 Emotion Analytics**: Classroom-level emotion detection and analysis
- **📊 Report Generation**: Automatic generation of TXT and DOCX reports
- **📧 Email Automation**: Timetable-based automatic email delivery to faculty
- **🔒 Privacy-First**: Auto-deletion of data after 7 days
- **🖥️ Modern GUI**: Premium Dark Mode interface with interactive dashboard
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
   ```bash
   python create_demo_data.py
   ```
   
   Then add student photos:
   - Go to `data/student_dataset/`
   - Create one folder per student
   - Add 3-5 clear face photos per student

4. **Configure email** (optional):
   - Open `config.py`
   - Update `SENDER_EMAIL` and `SENDER_PASSWORD`
   - Update `TIMETABLE` with subject-to-faculty email mapping

5. **Launch the application**:
   ```bash
   # Double-click this file:
   run_app.bat
   ```

## 📖 User Guide

### 1. Setup Student Database

1. Launch the application
2. Click **"Student Database"** in the sidebar
3. Click **"Open Student Dataset Folder"**
4. Add student photos (3-5 per student in separate folders)
5. Click **"Train Face Recognition"**
6. Wait for training to complete

### 2. Run Attendance Session

1. Click **"Live Capture"** in the sidebar
2. Select the subject from dropdown
3. Click **"Start Camera"** to preview
4. Click **"Capture & Process"** to:
   - Capture classroom images
   - Recognize student faces
   - Detect emotions
   - Generate reports
   - Send email (if configured)

### 3. View Reports

1. Click **"Reports"** in the sidebar
2. Select a report from the list
3. Click **"Open Report"** to view
4. Reports are available in both TXT and DOCX formats

### 4. System Settings

1. Click **"Settings"** in the sidebar
2. Configure:
   - Email credentials
   - View system information
   - Check configuration status

### 5. Advanced Management & Cleanup

1.  **Student Management**:
    - Go to **Student Database**.
    - Use the **Delete (🗑)** button to remove a student and auto-retrain.
    - Use **"Re-Train Model"** if you manually add photos.

2.  **Manual Upload**:
    - Go to **Live Capture** -> **Upload Photo to Analyze**.
    - Select a group photo to mark attendance without the camera.

3.  **Data Cleanup**:
    - Click **"Data Cleanup"** -> **"Run Cleanup"** to free up space.

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    GUI Application                      │
│                     (app_gui.py)                        │
└────────────┬────────────────────────────────────────────┘
             │
    ┌────────┴────────┐
    │                 │
┌───▼────┐      ┌────▼─────┐
│ Camera │      │   Face   │
│Capture │      │   Recog  │
└───┬────┘      └────┬─────┘
    │                │
    │           ┌────▼─────┐
    │           │ Emotion  │
    │           │ Detection│
    │           └────┬─────┘
    │                │
    └────────┬───────┘
             │
    ┌────────▼────────┐
    │     Report      │
    │   Generation    │
    └────────┬────────┘
             │
    ┌────────▼────────┐
    │      Email      │
    │   Automation    │
    └─────────────────┘
```

## 📁 Project Structure

```
cam/
├── app_gui.py                 # Main GUI application
├── config.py                  # Configuration settings
├── main.py                    # Console-based interface
├── image_capture.py           # Camera and image capture
├── face_recognition_module.py # Face recognition engine
├── emotion_detection.py       # Emotion detection engine
├── report_generator.py        # Report generation (TXT/DOCX)
├── email_automation.py        # Email automation with SMTP
├── data_cleanup.py            # Auto-cleanup for privacy
├── create_demo_data.py        # Demo data setup script
├── requirements.txt           # Python dependencies
├── run_app.bat                # Windows launch script
├── README.md                  # This file
├── PROJECT_DOCUMENTATION.md   # Detailed documentation
└── data/                      # Data directory
    ├── student_dataset/       # Student face photos
    ├── images/                # Captured classroom images
    ├── reports/               # Generated reports
    ├── logs/                  # System logs
    └── encodings/             # Face encodings (trained data)
```

## ⚙️ Configuration

Key settings in `config.py`:

```python
# Data retention (privacy)
DATA_RETENTION_DAYS = 7

# Camera settings
CAMERA_INDEX = 0  # 0 = default camera

# Face recognition
FACE_DETECTION_MODEL = 'hog'  # 'hog' (fast) or 'cnn' (accurate)
FACE_RECOGNITION_TOLERANCE = 0.6  # Lower = stricter

# Email settings
SENDER_EMAIL = "your.email@gmail.com"
SENDER_PASSWORD = "your_app_password"

# Timetable (subject → faculty email)
TIMETABLE = {
    "DBMS": "dbms.faculty@example.com",
    "OS": "os.faculty@example.com",
    # Add more subjects...
}
```

## 🔧 Troubleshooting

### Camera not working
- Check if camera is connected and not used by another application
- Try changing `CAMERA_INDEX` in config.py (0, 1, 2...)
- Restart the application

### Face recognition not accurate
- Ensure good lighting when adding student photos
- Add more photos per student (5+ recommended)
- Use clear, frontal face photos
- Adjust `FACE_RECOGNITION_TOLERANCE` in config.py

### Email not sending
- Use Gmail App Password (not regular password)
- Enable "Less secure app access" or use App Passwords
- Check SMTP settings in config.py
- Test with "Test Email" button in dashboard

### Dependencies installation fails
- Install Visual C++ Build Tools (for dlib/cmake)
- Use Python 3.8-3.10 (better compatibility)
- Install packages one by one if batch install fails

## 📚 Technologies Used

- **Face Recognition**: `face-recognition`, `dlib`, `OpenCV`
- **Emotion Detection**: `DeepFace`, `TensorFlow`
- **GUI**: `Tkinter`, `Pillow`
- **Reports**: `python-docx`, `matplotlib`
- **Email**: `smtplib` (built-in)
- **Scheduling**: `schedule`

## 🛡️ Privacy & Data Security

- All data is stored locally (no cloud storage)
- Automatic data deletion after 7 days
- No personally identifiable information shared
- Only class-level emotion data (not individual emotions)
- Email communication encrypted with TLS

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Your Name**
- Email: your.email@example.com
- GitHub: [@yourusername](https://github.com/yourusername)

## 🙏 Acknowledgments

- Face recognition powered by [face-recognition](https://github.com/ageitgey/face_recognition)
- Emotion detection using [DeepFace](https://github.com/serengil/deepface)
- Built for academic demonstration purposes

## 📞 Support

For issues, questions, or contributions:
1. Check the troubleshooting section above
2. Review `PROJECT_DOCUMENTATION.md`
3. Create an issue on GitHub
4. Contact the development team

---

**Made with ❤️ for automated attendance and classroom analytics**
