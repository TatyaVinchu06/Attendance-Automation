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
from config import *

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
    
    def _process_layer_results(self, dfs, student_votes, model_name, threshold):
        """Ek model ka result process karte hai"""
        if not dfs or len(dfs) == 0:
            return
        
        for df in dfs:
            if not df.empty:
                for index, row in df.iterrows():
                    distance = row.get('distance', float('inf'))
                    
                    if distance > threshold:
                        continue  # Weak match hai toh chhod do
                    
                    # Student ka naam nikalte hai path se
                    identity_path = str(row['identity'])
                    normalized_path = identity_path.replace('\\', '/')
                    parts = normalized_path.split('/')
                    
                    if 'student_dataset' in parts:
                        idx = parts.index('student_dataset')
                        if idx + 1 < len(parts):
                            student_name = parts[idx + 1]
                            if student_name in self.all_students:
                                student_votes[student_name] = student_votes.get(student_name, 0) + 1
                                logger.debug(f"{model_name}: {student_name} (match pakka hai, dist: {distance:.3f})")
    
    def recognize_faces(self, image_path, return_annotated=False):
        """
        Photo me chehra pehchante hai.
        3 layer security lagayi hai taaki galti na ho.
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
            
            # Agar photo bahut badi hai toh chhota karte hai taaki fast chale
            original_path = image_path
            img = cv2.imread(image_path)
            if img is not None:
                height, width = img.shape[:2]
                # 4K se bada hai toh resize karo
                if width > 3840 or height > 2160:
                    scale = min(1920/width, 1080/height)
                    img_resized = cv2.resize(img, None, fx=scale, fy=scale)
                    temp_path = os.path.join(os.path.dirname(image_path), f"temp_resized_{os.path.basename(image_path)}")
                    cv2.imwrite(temp_path, img_resized)
                    image_path = temp_path
                    logger.info(f"Photo resize kar di speed badhane ke liye")
            
            # 3 LAYER KA SYSTEM LAGAYA HAI
            # Kam se kam 2 models haan bolne chahiye tabhi present lagegi
            logger.info("3 models se check kar rahe hai...")
            
            # Votes count karenge
            student_votes = {}  # {student_name: vote_count}
            
            # LAYER 1: VGG-Face (Sabse main wala)
            logger.debug("Layer 1: VGG-Face check kar raha hai")
            try:
                dfs_vgg = DeepFace.find(
                    img_path=image_path,
                    db_path=self.database_path,
                    model_name="VGG-Face",
                    detector_backend="retinaface",
                    enforce_detection=False,
                    silent=True
                )
                self._process_layer_results(dfs_vgg, student_votes, "VGG-Face", SIMILARITY_THRESHOLD)
            except Exception as e:
                logger.warning(f"Layer 1 (VGG-Face) fail ho gaya: {e}")
            
            # LAYER 2: Facenet (Cross check ke liye)
            logger.debug("Layer 2: Facenet confirm kar raha hai")
            try:
                dfs_facenet = DeepFace.find(
                    img_path=image_path,
                    db_path=self.database_path,
                    model_name="Facenet",
                    detector_backend="retinaface",
                    enforce_detection=False,
                    silent=True
                )
                # Facenet ka scale alag hota hai
                self._process_layer_results(dfs_facenet, student_votes, "Facenet", 10.0)
            except Exception as e:
                logger.warning(f"Layer 2 (Facenet) fail ho gaya: {e}")
            
            # LAYER 3: ArcFace (Final mahr)
            logger.debug("Layer 3: ArcFace final check kar raha hai")
            try:
                dfs_arcface = DeepFace.find(
                    img_path=image_path,
                    db_path=self.database_path,
                    model_name="ArcFace",
                    detector_backend="retinaface",
                    enforce_detection=False,
                    silent=True
                )
                self._process_layer_results(dfs_arcface, student_votes, "ArcFace", 4.0)
            except Exception as e:
                logger.warning(f"Layer 3 (ArcFace) fail ho gaya: {e}")
            
            # DECISION TIME: 2/3 votes chahiye
            logger.info(f"Total votes: {student_votes}")
            
            # Jisko 2 se zyada vote mile wo Present
            marked_students = set()
            for student_name, votes in student_votes.items():
                if votes >= 2 and student_name in attendance:
                    attendance[student_name] = "Present"
                    marked_students.add(student_name)
                    logger.info(f"✓ CONFIRMED: {student_name} (Sahi hai, {votes}/3 models ne haan bola)")
                elif votes == 1:
                    logger.info(f"✗ REJECTED: {student_name} (Bas 1 model bola, doubt hai ispe)")
            
            # Photo pe box aur naam banate hai agar chahiye toh
            if return_annotated and annotated_img is not None and marked_students:
                # Box banane ke liye wapis run karte hai
                try:
                    dfs_final = DeepFace.find(
                        img_path=image_path,
                        db_path=self.database_path,
                        model_name="VGG-Face",
                        detector_backend="retinaface",
                        enforce_detection=False,
                        silent=True
                    )
                    
                    if dfs_final and len(dfs_final) > 0:
                        for df in dfs_final:
                            if not df.empty:
                                for index, row in df.iterrows():
                                    identity_path = str(row['identity'])
                                    normalized_path = identity_path.replace('\\', '/')
                                    parts = normalized_path.split('/')
                                    
                                    if 'student_dataset' in parts:
                                        idx = parts.index('student_dataset')
                                        if idx + 1 < len(parts):
                                            student_name = parts[idx + 1]
                                            
                                            # Sirf confirm walo pe box banayenge
                                            if student_name in marked_students:
                                                x = int(row['source_x'])
                                                y = int(row['source_y'])
                                                w = int(row['source_w'])
                                                h = int(row['source_h'])
                                                votes = student_votes.get(student_name, 0)
                                                
                                                # Hara dibba banate hai
                                                cv2.rectangle(annotated_img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                                                # Naam likhte hai
                                                label = f"{student_name} ({votes}/3)"
                                                cv2.putText(annotated_img, label, (x, y-10), 
                                                           cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                except Exception as e:
                    logger.warning(f"Box banane me galti huyi: {e}")
            
            present_count = sum(1 for status in attendance.values() if status == "Present")
            logger.info(f"Attendance lag gayi: {present_count}/{len(attendance)} present hai")
            
            # Temporary file delete karte hai, kachra saaf
            if image_path != original_path and os.path.exists(image_path):
                try:
                    os.remove(image_path)
                except:
                    pass
            
            if return_annotated:
                return attendance, annotated_img
            return attendance
            
        except Exception as e:
            logger.error(f"Chehra pehchanne me error aaya: {e}")
            # Error aane pe bhi file saaf karte hai
            if 'original_path' in locals() and image_path != original_path and os.path.exists(image_path):
                try:
                    os.remove(image_path)
                except:
                    pass
            return ({}, None) if return_annotated else {}
    
    def get_all_students(self):
        """Saare students ki list chahiye"""
        return self.all_students.copy()
    
    def is_trained(self):
        """Check karte hai ki model trained hai ya nahi"""
        return len(self.all_students) > 0
   
 