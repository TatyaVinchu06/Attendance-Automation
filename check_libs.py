import sys
print(f"Python: {sys.version}")

try:
    import cv2
    print(f"OpenCV: {cv2.__version__}")
    try:
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        print("LBPH Available: Yes")
    except AttributeError:
        print("LBPH Available: No (Need opencv-contrib-python)")
except ImportError:
    print("OpenCV Not Installed")

try:
    import face_recognition
    print("face_recognition Available: Yes")
except ImportError:
    print("face_recognition Available: No")

try:
    import dlib
    print("dlib Available: Yes")
except ImportError:
    print("dlib Available: No")
