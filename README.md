# AI Smart Attendance & Classroom Analytics System

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)](https://www.microsoft.com/windows)
[![Face Recognition](https://img.shields.io/badge/InsightFace-State%20of%20the%20Art-green)](https://github.com/deepinsight/insightface)

**Developed by Om Bhamare**

A comprehensive smart system for automating classroom attendance using advanced face recognition (InsightFace) and analyzing student emotions to provide insights into classroom engagement.

## 🌟 Key Features

- **✅ Automated Attendance**: High-accuracy face recognition using **InsightFace (SCRFD + ArcFace)**.
- **😊 Emotion Analytics**: Classroom-level emotion detection (Currently in maintenance/mock mode).
- **📊 Report Generation**: Automatic generation of Excel/CSV and PDF reports.
- **📧 Email Automation**: Automated email notifications to faculty with attendance summaries.
- **📈 Dashboard**: Interactive modern GUI for real-time monitoring.
- **🔒 Privacy-First**: Local data storage with auto-cleanup policies.
- **🖥️ Modern UI**: Built with CustomTkinter for a premium dark-mode experience.

## 🚀 Quick Start

### Prerequisites
- Python 3.8 to 3.11
- Webcam
- Windows OS (Recommended)
- [Visual Studio C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) (required for some dependencies like `insightface`)

### Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/yourusername/attendance-system.git
    cd attendance-system
    ```

2.  **Create Virtual Environment (Recommended)**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Download Models**
    *   This project uses **InsightFace buffalo_l**.
    *   Download the `buffalo_l.zip` model pack from [InsightFace Model Zoo](https://github.com/deepinsight/insightface/releases).
    *   Extract it to `models/buffalo_l/`.
    *   Ensure the structure is:
        ```
        models/
        └── buffalo_l/
            ├── det_10g.onnx
            └── w600k_r50.onnx
        ```

### Usage

1.  **Enroll Students**
    *   Run the app: `python src/main.py`
    *   Go to **Enrollment** tab.
    *   Enter ID and Name.
    *   Capture photos.
    *   Click **Save**. The system will automatically train embeddings.

2.  **Take Attendance**
    *   Go to **Live Capture** tab.
    *   Select Subject/Class.
    *   Click **Start Camera**.
    *   Click **Capture & Process** to detect faces and mark attendance.

3.  **View Reports**
    *   Check the **Reports** tab for generated attendance sheets.

## 📁 Project Structure

```
cam/
├── src/
│   ├── main.py                    # Application Entry Point
│   ├── config.py                  # Configuration (Thresholds, Paths, Email)
│   ├── face_recognition_module.py # InsightFace Implementation
│   ├── emotion_detection.py       # Emotion Analysis (Mock/DeepFace)
│   ├── core/                      # Core AI Modules (Detector, Embedder)
│   └── ...
├── data/
│   ├── student_dataset/           # Raw Student Images
│   ├── encodings/                 # Generated Face Embeddings (Pickle)
│   └── reports/                   # Output Reports
├── models/                        # AI Models (Not included in repo, download separate)
├── scripts/                       # Utility Scripts (DB Setup, Retraining)
└── requirements.txt               # Dependencies
```

## ⚙️ Configuration

Edit `src/config.py` to customize:
*   `SIMILARITY_THRESHOLD`: Default **0.55**. Adjust for stricter/looser matching.
*   `EMAIL_CONFIG`: SMTP details for email alerts.
*   `DATA_RETENTION`: Days to keep logs/images.

## �️ Data Management

*   **Retraining**: If you add students manually to `data/student_dataset`, run:
    ```bash
    python scripts/fix_and_retrain.py
    ```
*   **Database**: stored in `data/encodings/face_encodings.pkl`.

## 🤝 Credits

*   **InsightFace**: For the state-of-the-art face analysis library.
*   **CustomTkinter**: For the modern GUI components.

---
**Note**: Large model files (>100MB) are excluded from this repository used Git LFS or download instructions above.
