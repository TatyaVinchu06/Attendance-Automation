import sys
import os
import logging

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from face_recognition_module import FaceRecognitionModule

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup():
    print("--- Setting up Student Database ---")
    
    fr = FaceRecognitionModule()
    
    # 1. Force update list from disk
    print("Scanning student_dataset folder...")
    fr._update_student_list()
    
    if not fr.all_students:
        print("[ERROR] No students found in data/student_dataset!")
        print("Please add folders with images first.")
        return
        
    print(f"Found {len(fr.all_students)} students: {fr.all_students}")
    
    # 2. Train (Validate images)
    print("Validating images...")
    if fr.train_face_encodings():
        print("Validation Successful.")
        
        # 3. Save to pickle
        print("Saving configuration to config.pkl...")
        if fr.save_encodings():
            print("[SUCCESS] Database setup complete!")
        else:
            print("[FAIL] Could not save encodings file.")
    else:
        print("[FAIL] Image validation failed.")

if __name__ == "__main__":
    setup()
