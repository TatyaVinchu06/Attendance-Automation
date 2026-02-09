import sys
import os
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG)

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from face_recognition_module import FaceRecognitionModule
from config import IMAGES_DIR

def test():
    fr = FaceRecognitionModule()
    
    # Try to find an image to test
    # We'll look for the uploaded media artifact if possible, or any image in IMAGES_DIR
    check_path = r"C:\Users\ombha\.gemini\antigravity\brain\6c3cef94-43d2-4319-b977-5a11bde24da1\uploaded_media_1770536486453.png"
    
    if not os.path.exists(check_path):
        print(f"Artifact not found at {check_path}")
        return

    print(f"Testing on image: {check_path}")
    
    # Run recognition
    result = fr.recognize_faces(check_path)
    print("Result:", result)

if __name__ == "__main__":
    test()
