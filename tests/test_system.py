#!/usr/bin/env python3
"""
System Test Script
Tests all modules to verify installation and setup
"""

import os
import sys

# Add src directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, '..', 'src')
sys.path.append(src_dir)

def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 60)
    print(text)
    print("=" * 60)

def test_imports():
    """Test if all required packages are installed"""
    print_header("Testing Package Imports")
    
    packages = {
        'cv2': 'opencv-python',
        'PIL': 'Pillow',
        'docx': 'python-docx',
        'schedule': 'schedule',
        'deepface': 'deepface',
        'numpy': 'numpy'
    }
    
    all_passed = True
    
    for module, package in packages.items():
        try:
            __import__(module)
            print(f"  [PASS] {package}")
        except ImportError:
            print(f"  [FAIL] {package} - NOT INSTALLED")
            all_passed = False
    
    return all_passed

def test_directory_structure():
    """Test if required directories exist"""
    print_header("Testing Directory Structure")
    
    from config import DATA_DIR, IMAGES_DIR, LOGS_DIR, REPORTS_DIR, STUDENT_DATASET_DIR
    
    directories = {
        'Data Directory': DATA_DIR,
        'Images Directory': IMAGES_DIR,
        'Logs Directory': LOGS_DIR,
        'Reports Directory': REPORTS_DIR,
        'Student Dataset': STUDENT_DATASET_DIR
    }
    
    all_passed = True
    
    for name, path in directories.items():
        if os.path.exists(path):
            print(f"  [PASS] {name}: {path}")
        else:
            print(f"  [FAIL] {name}: {path} - NOT FOUND")
            all_passed = False
    
    return all_passed

def test_camera():
    """Test camera connectivity"""
    print_header("Testing Camera")
    
    try:
        import cv2
        from config import CAMERA_INDEX
        
        cap = cv2.VideoCapture(CAMERA_INDEX)
        
        if cap.isOpened():
            ret, frame = cap.read()
            cap.release()
            
            if ret:
                print(f"  [PASS] Camera {CAMERA_INDEX} is working")
                print(f"    Resolution: {frame.shape[1]}x{frame.shape[0]}")
                return True
            else:
                print(f"  [FAIL] Camera {CAMERA_INDEX} opened but cannot read frames")
                return False
        else:
            print(f"  [FAIL] Cannot open camera {CAMERA_INDEX}")
            print(f"    Try different CAMERA_INDEX in config.py (0, 1, 2...)")
            return False
            
    except Exception as e:
        print(f"  [FAIL] Camera test failed: {e}")
        return False

def test_student_dataset():
    """Test student dataset"""
    print_header("Testing Student Dataset")
    
    from config import STUDENT_DATASET_DIR
    
    try:
        students = [d for d in os.listdir(STUDENT_DATASET_DIR) 
                   if os.path.isdir(os.path.join(STUDENT_DATASET_DIR, d))]
        
        if len(students) == 0:
            print("  [WARN] No students in dataset")
            print(f"    Add student folders to: {STUDENT_DATASET_DIR}")
            return False
        
        print(f"  [PASS] Found {len(students)} student(s):")
        
        for student in students:
            student_path = os.path.join(STUDENT_DATASET_DIR, student)
            images = [f for f in os.listdir(student_path) 
                     if f.endswith(('.jpg', '.jpeg', '.png'))]
            print(f"    - {student}: {len(images)} image(s)")
        
        return True
        
    except Exception as e:
        print(f"  [FAIL] Dataset test failed: {e}")
        return False

def test_face_recognition():
    """Test face recognition module"""
    print_header("Testing Face Recognition")
    
    try:
        from face_recognition_module import FaceRecognitionModule
        from config import ENCODINGS_FILE
        
        fr = FaceRecognitionModule()
        
        if os.path.exists(ENCODINGS_FILE):
            print("  [PASS] Face encodings file exists")
            if fr.load_encodings():
                students = fr.get_all_students()
                print(f"  [PASS] Loaded encodings for {len(students)} students")
                return True
            else:
                print("  [FAIL] Failed to load encodings")
                return False
        else:
            print("  [WARN] No face encodings found")
            print("    Run 'Setup Student Database' in main menu")
            return False
            
    except Exception as e:
        print(f"  [FAIL] Face recognition test failed: {e}")
        return False

def test_email_config():
    """Test email configuration"""
    print_header("Testing Email Configuration")
    
    try:
        from config import SENDER_EMAIL, SENDER_PASSWORD, SMTP_SERVER, SMTP_PORT
        
        print(f"  SMTP Server: {SMTP_SERVER}:{SMTP_PORT}")
        print(f"  Sender Email: {SENDER_EMAIL}")
        
        if SENDER_EMAIL == "your_email@gmail.com":
            print("  [WARN] Email not configured")
            print("    Update SENDER_EMAIL and SENDER_PASSWORD in config.py")
            return False
        
        if SENDER_PASSWORD == "your_app_password":
            print("  [WARN] Email password not configured")
            print("    Update SENDER_PASSWORD in config.py")
            return False
        
        print("  [PASS] Email configuration set")
        print("    Use 'Test Email' option in main menu to verify")
        return True
        
    except Exception as e:
        print(f"  [FAIL] Email config test failed: {e}")
        return False

def test_modules():
    """Test individual modules"""
    print_header("Testing System Modules")
    
    modules = [
        'image_capture',
        'face_recognition_module',
        'emotion_detection',
        'report_generator',
        'email_automation',
        'data_cleanup'
    ]
    
    all_passed = True
    
    for module in modules:
        try:
            __import__(module)
            print(f"  [PASS] {module}.py")
        except Exception as e:
            print(f"  [FAIL] {module}.py - {str(e)[:50]}")
            all_passed = False
    
    return all_passed

def run_all_tests():
    """Run all system tests"""
    print("\n" + "=" * 60)
    print("AI ATTENDANCE SYSTEM - SYSTEM TEST")
    print("=" * 60)
    
    tests = [
        ("Package Imports", test_imports),
        ("Directory Structure", test_directory_structure),
        ("System Modules", test_modules),
        ("Camera", test_camera),
        ("Student Dataset", test_student_dataset),
        ("Face Recognition", test_face_recognition),
        ("Email Configuration", test_email_config)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\nTest '{test_name}' crashed: {e}")
            results[test_name] = False
    
    # Summary
    print_header("TEST SUMMARY")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "[PASS]" if result else "[FAIL]"
        print(f"  {status} - {test_name}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n[PASS] All tests passed! System is ready to use.")
        print("Run: python src/main.py")
    else:
        print("\n[WARN] Some tests failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("  - Install missing packages: pip install -r requirements.txt")
        print("  - Add student photos to data/student_dataset/")
        print("  - Configure email in config.py")
        print("  - Check camera permissions")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)