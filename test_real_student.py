import sys
import os
import logging
import cv2

# Setup logging
logging.basicConfig(level=logging.INFO)

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from face_recognition_module import FaceRecognitionModule
from config import STUDENT_DATASET_DIR

def test():
    print("--- Face Recognition Test ---")
    fr = FaceRecognitionModule()
    fr.load_encodings()
    
    # 1. Get a real student image
    # We saw '10_Om_Bhamare' in the dataset
    student_name = "10_Om_Bhamare"
    student_dir = os.path.join(STUDENT_DATASET_DIR, student_name)
    
    if not os.path.exists(student_dir):
        # Fallback to any directory
        dirs = [d for d in os.listdir(STUDENT_DATASET_DIR) if os.path.isdir(os.path.join(STUDENT_DATASET_DIR, d))]
        if not dirs:
            print("No students found!")
            return
        student_name = dirs[0]
        student_dir = os.path.join(STUDENT_DATASET_DIR, student_name)

    print(f"Testing with student: {student_name}")
    
    images = [f for f in os.listdir(student_dir) if f.endswith(('.jpg', '.png'))]
    if not images:
        print("No images found for student!")
        return
        
    test_image_path = os.path.join(student_dir, images[0])
    print(f"Input Image: {test_image_path}")
    
    # 2. Recognize
    result = fr.recognize_faces(test_image_path)
    print("\nRecognition Result:")
    print(result)
    
    # Check if correct student is detected
    if student_name in result and result[student_name] == "Present":
        print(f"\n[PASS] Correctly identified {student_name}")
    else:
        print(f"\n[FAIL] Could not identify {student_name}")
        print(f"Detected: {result}")

if __name__ == "__main__":
    test()
