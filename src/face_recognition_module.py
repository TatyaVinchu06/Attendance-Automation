#!/usr/bin/env python3
"""
Face Recognition Code
Students ka face pehchanne ke liye DeepFace use kiya hai
"""

import pickle
import os
import cv2
import logging
from pathlib import Path
from deepface import DeepFace
import pandas as pd
from config import (
    STUDENT_DATASET_DIR, 
    ENCODINGS_FILE, 
    DEEPFACE_MODEL, 
    FACE_DETECTOR_BACKEND, 
    SIMILARITY_THRESHOLD
)

logger = logging.getLogger(__name__)


class FaceRecognitionModule:
    """Face recognition ka main logic yaha hai"""
    
    def __init__(self):
        # Database path set kar rahe hai
        self.database_path = str(STUDENT_DATASET_DIR)
        self.all_students = []
        self.encodings_ready = False
        
        # Check karte hai agar database ready hai toh list update karo
        if os.path.exists(STUDENT_DATASET_DIR):
            self._update_student_list()
    
    def _update_student_list(self):
        """Folder check karke students ki list banate hai"""
        try:
            student_folders = [d for d in os.listdir(STUDENT_DATASET_DIR) 
                             if os.path.isdir(os.path.join(STUDENT_DATASET_DIR, d))]
            self.all_students = sorted(student_folders)
            logger.info(f"Total {len(self.all_students)} students mile")
        except Exception as e:
            logger.error(f"List update karne me error aaya: {e}")
            self.all_students = []
    
    def train_face_encodings(self):
        """
        Database ready karte hai, check karte hai photos hai ya nahi
        """
        logger.info("Face database ready kar rahe hai bhai")
        
        try:
            # Check karte hai folder hai ya nahi
            if not os.path.exists(STUDENT_DATASET_DIR):
                logger.error(f"Student folder hi gayab hai: {STUDENT_DATASET_DIR}")
                return False
            
            # List update karte hai
            self._update_student_list()
            
            if not self.all_students:
                logger.error("Koi student folder nahi mila")
                return False
            
            # Har student ki photo check karte hai
            valid_students = 0
            for student_name in self.all_students:
                student_path = os.path.join(STUDENT_DATASET_DIR, student_name)
                image_files = [f for f in os.listdir(student_path) 
                             if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
                
                if image_files:
                    valid_students += 1
                    logger.info(f"Student '{student_name}': {len(image_files)} photos mili")
                else:
                    logger.warning(f"Student '{student_name}': Iski photo nahi hai")
            
            if valid_students == 0:
                logger.error("Kisi ki bhi photo nahi mili yaar")
                return False
            
            # DeepFace apne aap handle kar lega
            self.encodings_ready = True
            
            logger.info(f"Database mast ready hai, {valid_students} students ke saath")
            return True
            
        except Exception as e:
            logger.error(f"Training me locha ho gaya: {e}")
            return False
    
    def save_encodings(self):
        """Metadata save karte hai (backup ke liye)"""
        try:
            data = {
                'students': self.all_students,
                'encodings_ready': self.encodings_ready
            }
            
            with open(ENCODINGS_FILE, 'wb') as f:
                pickle.dump(data, f)
            
            logger.info(f"Sab save ho gaya file me: {ENCODINGS_FILE}")
            return True
            
        except Exception as e:
            logger.error(f"Save karne me error: {e}")
            return False
    
    def load_encodings(self):
        """Purana data load karte hai"""
        try:
            with open(ENCODINGS_FILE, 'rb') as f:
                data = pickle.load(f)
            
            self.all_students = data.get('students', [])
            self.encodings_ready = data.get('encodings_ready', False)
            
            logger.info(f"Data load ho gaya, {len(self.all_students)} students hai")
            return True
            
        except Exception as e:
            logger.error(f"Load karne me error: {e}")
            return False
    
    def recognize_faces(self, image_path, return_annotated=False):
        """
        FAST & ACCURATE Face Recognition (Rebuilt)
        Uses DeepFace (VGG-Face) + SSD Detector.
        """
        if not self.all_students:
            logger.error("Bhai pehle students toh add karo database me")
            return ({}, None) if return_annotated else {}
        
        try:
            # Sabko absent mark karte hai pehle
            attendance = {student: "Absent" for student in self.all_students}
            annotated_img = None
            if return_annotated:
                annotated_img = cv2.imread(image_path)
            
            # --- OPTIMIZATION: Resize if 4K ---
            original_path = image_path
            img = cv2.imread(image_path)
            if img is not None:
                print(f"[LIVE DEBUG] Analyzing frame: {image_path} | Size: {img.shape}")
                h, w = img.shape[:2]
                if w > 3840 or h > 2160:
                    scale = 0.5
                    img_resized = cv2.resize(img, None, fx=scale, fy=scale)
                    temp_path = os.path.join(os.path.dirname(image_path), f"temp_fast_{os.path.basename(image_path)}")
                    cv2.imwrite(temp_path, img_resized)
                    image_path = temp_path
            
            # --- CORE LOGIC: DeepFace.find (Single Pass) ---
            # Backend: 'ssd' (Fast & Accurate) | Model: Configured (Facenet512/VGG-Face)
            logger.info(f"⚡ Analyzing face with SSD + {DEEPFACE_MODEL}...")
            
            try:
                dfs = DeepFace.find(
                    img_path=image_path,
                    db_path=self.database_path,
                    model_name=DEEPFACE_MODEL,
                    detector_backend=FACE_DETECTOR_BACKEND,  # Configured (opencv)
                    distance_metric="cosine",
                    enforce_detection=False,
                    silent=True,
                    threshold=SIMILARITY_THRESHOLD # Config se uthaya (0.50)
                )
                
                # --- LIVE DEBUGGING ---
                if len(dfs) > 0:
                    df = dfs[0]
                    if not df.empty:
                         print(f"[LIVE DEBUG] Found matches: {len(df)}")
                         if 'distance' in df.columns:
                             print(f"[LIVE DEBUG] Top match distance: {df.iloc[0]['distance']:.4f}")
                         if 'identity' in df.columns:
                             print(f"[LIVE DEBUG] Top match identity: {df.iloc[0]['identity']}")
                    else:
                         print(f"[LIVE DEBUG] Detected face but NO MATCH found (Threshold: {SIMILARITY_THRESHOLD})")
                else:
                     pass # No face detected



            except ValueError:
                # SSD requires tensorflow/opencv specific setup, fallback to retinaface if fails?
                # No, we assume SSD works. If error, likely no face or library issue.
                logger.warning("SSD detector failed, trying opencv as backup...")
                dfs = DeepFace.find(
                    img_path=image_path,
                    db_path=self.database_path,
                    model_name=DEEPFACE_MODEL,
                    detector_backend="opencv",
                    distance_metric="cosine",
                    enforce_detection=False,
                    silent=True
                )


            # --- DEBUG: Show structure of results ---
            print(f"[DEBUG] DeepFace.find returned {len(dfs)} dataframe(s)")
            for idx, df in enumerate(dfs):
                print(f"[DEBUG] DF[{idx}]: {len(df)} row(s), empty={df.empty}")
                if not df.empty:
                    print(f"[DEBUG] DF[{idx}] columns: {list(df.columns)}")
                    print(f"[DEBUG] DF[{idx}] first row: {df.iloc[0].to_dict()}")
        
            # --- PROCESS RESULTS ---
            detected_students = set()
            
            if len(dfs) > 0:
                for df in dfs:
                    if not df.empty:
                        for index, row in df.iterrows():
                            # Extract Name
                            identity_path = str(row['identity'])
                            # Path logic to get student name
                            normalized_path = identity_path.replace('\\', '/')
                            parts = normalized_path.split('/')
                            
                            # Standard structure: dataset/student_name/image.jpg
                            # We look for folder name that matches our known students
                            for student in self.all_students:
                                if f"/{student}/" in normalized_path or normalized_path.endswith(f"/{student}"):
                                    attendance[student] = "Present"
                                    detected_students.add(student)
                                    logger.info(f"✅ MATCH: {student} (Dist: {row.get('distance', 0):.4f})")
                                    
                                    # Draw Box
                                    if return_annotated and annotated_img is not None:
                                        x, y = int(row.get('source_x', 0)), int(row.get('source_y', 0))
                                        w, h = int(row.get('source_w', 0)), int(row.get('source_h', 0))
                                        cv2.rectangle(annotated_img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                                        cv2.putText(annotated_img, f"{student}", (x, y-10), 
                                                   cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                                    break
            
            if not detected_students:
                logger.info("❌ No matching faces found.")

            # --- CLEANUP ---
            if image_path != original_path and os.path.exists(image_path):
                try: os.remove(image_path)
                except: pass
                
            if return_annotated:
                return attendance, annotated_img
            return attendance

        except Exception as e:
            logger.error(f"Analysis Error: {e}")
            return ({}, None) if return_annotated else {}
    
    def get_all_students(self):
        """Saare students ki list chahiye"""
        return self.all_students.copy()
    
    def is_trained(self):
        """Check karte hai ki model trained hai ya nahi"""
        return len(self.all_students) > 0
