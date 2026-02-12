
import sys
import os
import cv2
import logging
import traceback
import numpy as np
import pickle

# Setup path: add src to path
sys.path.append(os.path.join(os.getcwd(), "src"))

from face_recognition_module import FaceRecognitionModule
from config import STUDENT_DATASET_DIR, ENCODINGS_FILE

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TRAIN")

def main():
    logger.info("Initializing FaceRecognitionModule (InsightFace)...")
    try:
        fr = FaceRecognitionModule()
    except Exception as e:
        logger.error(f"Initialization Failed: {e}")
        return

    logger.info("Starting training process...")
    # This will regenerate embeddings from STUDENT_DATASET_DIR
    fr.train_face_encodings()
    
    # Verify
    students = fr.get_all_students()
    logger.info(f"Training Complete. Students enrolled: {len(students)}")
    logger.info(f"Student List: {students}")
    
    if len(students) > 0:
        logger.info("SUCCESS: Model re-trained and database updated.")
    else:
        logger.warning("WARNING: No students enrolled. Check data/student_dataset folder.")

if __name__ == "__main__":
    main()
