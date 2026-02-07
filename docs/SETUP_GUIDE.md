# Python 3.11 Setup Guide

## Quick Start (Recommended)

### 1. Download and Install Python 3.11.9

**Download URL**: https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe

**Installation Steps**:
1. Run the installer
2. ✅ **Check "Add Python 3.11 to PATH"**
3. Click "Install Now"
4. Wait for installation to complete

### 2. Create Virtual Environment and Install Dependencies

Open PowerShell or Command Prompt in the project folder and run:

```bash
py -3.11 setup_venv.py
```

This automated script will:
- Create a Python 3.11 virtual environment
- Install all required dependencies
- Verify the installation

### 3. Run the Application

Double-click `run_app.bat` or run:

```bash
run_app.bat
```

---

## Manual Setup (Alternative)

If you prefer to set up manually:

### 1. Create Virtual Environment

```bash
py -3.11 -m venv venv
```

### 2. Activate Virtual Environment

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Application

```bash
python app_gui.py
```

---

## Verification

To verify everything is working:

```bash
# Activate venv
venv\Scripts\activate

# Check Python version (should show 3.11.x)
python --version

# Test imports
python -c "import cv2, face_recognition, deepface; print('All imports successful!')"
```

---

## Troubleshooting

### Issue: `py -3.11` not recognized

**Solution**: Python 3.11 is not installed or not in PATH. Reinstall Python 3.11 with "Add to PATH" checked.

### Issue: face-recognition installation fails

**Solution**: 
1. Make sure you're using Python 3.11 (not 3.14)
2. Install Visual C++ Build Tools if on Windows:
   https://visualstudio.microsoft.com/visual-cpp-build-tools/

### Issue: deepface/tensorflow installation fails

**Solution**: These packages don't support Python 3.14+. Use Python 3.11 as recommended.

---

## Notes

- Your Python 3.14 installation remains untouched
- The virtual environment is isolated to this project folder
- You must activate the venv each time before running the app
- `run_app.bat` handles activation automatically
