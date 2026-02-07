# Quick Start Guide

## 🚀 Get Up and Running in 5 Minutes

### Step 1: Install Dependencies (2 minutes)

Open PowerShell/Command Prompt in the project directory and run:

```bash
pip install -r requirements.txt
```

**Note**: This may take a few minutes. Some packages like `dlib` and `tensorflow` are large.

### Step 2: Setup Demo Students (1 minute)

Run the demo data setup script:

```bash
python create_demo_data.py
```

Type `yes` when prompted. This creates sample student folders.

### Step 3: Add Student Photos (Optional for Demo)

For a proper demonstration, add real student photos:

1. Open `data/student_dataset/` folder
2. For each student folder, add 3-5 clear face photos (JPG/PNG)
3. Photos should show clear faces looking at camera

**Skip this for now** if you want to test the interface first.

### Step 4: Launch the Application

Double-click:
```
run_app.bat
```

Or run manually:
```bash
python app_gui.py
```

### Step 5: Train the System (Only if you added photos)

1. In the app, click **"Student Database"** in sidebar
2. Click **"Train Face Recognition"**
3. Wait for training to complete (~30 seconds)

---

## 📋 First-Time Demonstration Checklist

### Before the Demo:

- [ ] Install dependencies
- [ ] Add at least 3 students with photos
- [ ] Train face recognition
- [ ] Test camera (check dashboard status)
- [ ] (Optional) Configure email settings

### During the Demo:

1. **Show Dashboard**
   - Point out system statistics
   - Show quick actions
   - Demonstrate system status indicators

2. **Show Student Database**
   - Display registered students
   - Explain training process

3. **Run Live Attendance Session**
   - Select subject (e.g., "DBMS")
   - Start camera preview
   - Capture and process attendance
   - Show results popup with attendance and emotions

4. **View Reports**
   - Open generated reports
   - Show both TXT and DOCX formats
   - Explain email automation feature

5. **Show Settings**
   - Explain timetable configuration
   - Show system information

6. **Demonstrate Data Cleanup**
   - Show privacy-first approach
   - Preview cleanup (7-day retention)

---

## ⚠️ Common First-Time Issues

### "ModuleNotFoundError" when launching
**Solution**: Install dependencies again:
```bash
pip install -r requirements.txt
```

### Camera not opening
**Solution**: 
- Close other apps using camera (Zoom, Teams, etc.)
- Check camera privacy settings in Windows
- Try changing `CAMERA_INDEX` in `config.py` to 1 or 2

### "No students registered"
**Solution**: Add photos to `data/student_dataset/` and train the system

### Training fails
**Solution**: 
- Ensure student folders have at least 3 photos each
- Photos should be JPG/PNG with clear faces
- Check logs in `data/logs/` for detailed errors

---

## 🎯 Testing Without Real Photos (Quick Demo)

If you don't have student photos ready:

1. Launch the app
2. Explore the UI pages:
   - Dashboard
   - Student Database
   - Live Capture (shows camera preview)
   - Reports (empty initially)
   - Settings
   - Data Cleanup

3. Test camera functionality:
   - Go to Live Capture
   - Click "Start Camera"
   - Verify camera preview works

4. Add photos later for full functionality

---

## 📧 Email Configuration (Optional)

For email automation to work:

1. Open `config.py`
2. Update these lines:
   ```python
   SENDER_EMAIL = "your.email@gmail.com"
   SENDER_PASSWORD = "your_app_password"  # Use Gmail App Password
   ```

3. Update timetable:
   ```python
   TIMETABLE = {
       "DBMS": "faculty1@example.com",
       "OS": "faculty2@example.com",
   }
   ```

4. Test in app:
   - Dashboard → Test Email button

---

## 🎓 Ready for Full Demo?

Once you have:
- ✅ Dependencies installed
- ✅ Student photos added
- ✅ System trained
- ✅ Camera working

You're ready to demonstrate the complete system!

Simply run `run_app.bat` and follow the demonstration checklist above.

---

**Need help?** Check `README.md` for detailed documentation or `PROJECT_DOCUMENTATION.md` for technical details.