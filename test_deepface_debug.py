import sys
import os
import logging
import cv2
import pandas as pd

# Setup logging
logging.basicConfig(level=logging.INFO)

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from face_recognition_module import FaceRecognitionModule
from config import STUDENT_DATASET_DIR, FACE_DETECTOR_BACKEND

from deepface import DeepFace

def test():
    print("--- Deep Face Debug ---")
    
    # 1. Get a real student image
    dirs = [d for d in os.listdir(STUDENT_DATASET_DIR) if os.path.isdir(os.path.join(STUDENT_DATASET_DIR, d))]
    if not dirs:
        print("No students found!")
        return
    student_name = dirs[0] # Just pick first one
    student_dir = os.path.join(STUDENT_DATASET_DIR, student_name)
    images = [f for f in os.listdir(student_dir) if f.endswith(('.jpg', '.png'))]
    if not images:
        print("No images found!")
        return
        
    test_image_path = os.path.join(student_dir, images[0])
    print(f"Testing with image: {test_image_path}")
    
    # 2. Check Face Detection
    print(f"\nChecking Face Detection (Backend: {FACE_DETECTOR_BACKEND})...")
    try:
        faces = DeepFace.extract_faces(
            img_path=test_image_path, 
            detector_backend=FACE_DETECTOR_BACKEND,
            enforce_detection=False
        )
        print(f"Found {len(faces)} face(s).")
        for i, face in enumerate(faces):
            print(f"  Face {i}: Confidence {face.get('confidence', 0)}")
            
        if len(faces) == 0 or (len(faces) > 0 and faces[0]['confidence'] == 0):
             print("[WARN] No confident face detected!")
             
    except Exception as e:
        print(f"[ERROR] Face detection failed: {e}")

    # 3. Check DeepFace.find directly
    print("\nRunning DeepFace.find...")
    try:
        dfs = DeepFace.find(
            img_path=test_image_path,
            db_path=STUDENT_DATASET_DIR,
            model_name="VGG-Face",
            detector_backend=FACE_DETECTOR_BACKEND,
            distance_metric="cosine",
            enforce_detection=False,
            silent=False # Verbose
        )
        
        if len(dfs) > 0:
            print("Result DataFrame:")
            print(dfs[0])
        else:
            print("Result is empty.")
            
    except Exception as e:
        print(f"[ERROR] DeepFace.find failed: {e}")

if __name__ == "__main__":
    test()
