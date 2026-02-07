#!/usr/bin/env python3
"""
Face Recognition Module (DeepFace Implementation)
Handles student face recognition for attendance using DeepFace
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
    """Face recognition for attendance marking using DeepFace"""
    
    def __init__(self):
        self.database_path = str(STUDENT_DATASET_DIR)
        self.all_students = []
        self.encodings_ready = False
        
        # Check if student database exists and is ready
        if os.path.exists(STUDENT_DATASET_DIR):
            self._update_student_list()
    
    def _update_student_list(self):
        """Update the list of all registered students"""
        try:
            student_folders = [d for d in os.listdir(STUDENT_DATASET_DIR) 
                             if os.path.isdir(os.path.join(STUDENT_DATASET_DIR, d))]
            self.all_students = sorted(student_folders)
            logger.info(f"Found {len(self.all_students)} students")
        except Exception as e:
            logger.error(f"Error updating student list: {e}")
            self.all_students = []
    
    def train_face_encodings(self):
        """
        Prepare face recognition database with student dataset
        
        Returns:
            bool: True if successful, False otherwise
        """
        logger.info("Preparing face recognition database")
        
        try:
            # Check if student dataset exists
            if not os.path.exists(STUDENT_DATASET_DIR):
                logger.error(f"Student dataset directory not found: {STUDENT_DATASET_DIR}")
                return False
            
            # Update student list
            self._update_student_list()
            
            if not self.all_students:
                logger.error("No student folders found in dataset")
                return False
            
            # Verify each student has at least one image
            valid_students = 0
            for student_name in self.all_students:
                student_path = os.path.join(STUDENT_DATASET_DIR, student_name)
                image_files = [f for f in os.listdir(student_path) 
                             if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
                
                if image_files:
                    valid_students += 1
                    logger.info(f"Student '{student_name}': {len(image_files)} images")
                else:
                    logger.warning(f"Student '{student_name}': No images found")
            
            if valid_students == 0:
                logger.error("No valid student images found")
                return False
            
            # DeepFace will build representations on first use
            # Mark as ready
            self.encodings_ready = True
            
            logger.info(f"Database ready with {valid_students} students")
            return True
            
        except Exception as e:
            logger.error(f"Error during training: {e}")
            return False
    
    def save_encodings(self):
        """Save metadata (compatibility method)"""
        try:
            data = {
                'students': self.all_students,
                'encodings_ready': self.encodings_ready
            }
            
            with open(ENCODINGS_FILE, 'wb') as f:
                pickle.dump(data, f)
            
            logger.info(f"Metadata saved to {ENCODINGS_FILE}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving metadata: {e}")
            return False
    
    def load_encodings(self):
        """Load metadata (compatibility method)"""
        try:
            with open(ENCODINGS_FILE, 'rb') as f:
                data = pickle.load(f)
            
            self.all_students = data.get('students', [])
            self.encodings_ready = data.get('encodings_ready', False)
            
            logger.info(f"Loaded metadata for {len(self.all_students)} students")
            return True
            
        except Exception as e:
            logger.error(f"Error loading metadata: {e}")
            return False
    
    def recognize_faces(self, image_path, return_annotated=False):
        """
        Recognize faces in an image and mark attendance
        
        Args:
            image_path: Path to image file
            return_annotated: If True, returns (attendance, annotated_image_numpy)
            
        Returns:
            dict: Attendance dictionary {student_name: status}
            OR tuple: (attendance, annotated_image) if return_annotated=True
        """
        if not self.all_students:
            logger.error("No students registered. Please train the system first.")
            return ({}, None) if return_annotated else {}
        
        try:
            # Initialize attendance (all absent by default)
            attendance = {student: "Absent" for student in self.all_students}
            annotated_img = None
            if return_annotated:
                annotated_img = cv2.imread(image_path)
            
            # Find matching faces using DeepFace
            logger.info(f"Analyzing image: {image_path}")
            
            # Use DeepFace.find to search for matches in the database
            try:
                dfs = DeepFace.find(
                    img_path=image_path,
                    db_path=self.database_path,
                    model_name="VGG-Face",
                    detector_backend="opencv",
                    enforce_detection=False,
                    silent=True
                )
                
                # Process results
                if dfs and len(dfs) > 0:
                    for df in dfs:
                        if not df.empty:
                            # Iterate through matches
                            for index, row in df.iterrows():
                                identity_path = row['identity']
                                
                                # Parse student name with robust separator handling
                                identity_path = str(row['identity'])
                                
                                # Normalize all separators to forward slashes for splitting
                                normalized_path = identity_path.replace('\\', '/')
                                parts = normalized_path.split('/')
                                
                                if 'student_dataset' in parts:
                                    idx = parts.index('student_dataset')
                                    if idx + 1 < len(parts):
                                        student_name = parts[idx + 1]
                                        if student_name in attendance:
                                            attendance[student_name] = "Present"
                                            logger.info(f"Recognized: {student_name}")
                                            
                                            # Draw Green Box if requested
                                            if return_annotated and annotated_img is not None:
                                                x = int(row['source_x'])
                                                y = int(row['source_y'])
                                                w = int(row['source_w'])
                                                h = int(row['source_h'])
                                                
                                                # Draw Rectangle
                                                cv2.rectangle(annotated_img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                                                # Draw Name
                                                cv2.putText(annotated_img, student_name, (x, y-10), 
                                                           cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                
            except ValueError as e:
                logger.warning(f"No faces detected in image: {e}")
            except Exception as e:
                logger.error(f"Error during face recognition: {e}")
            
            present_count = sum(1 for status in attendance.values() if status == "Present")
            logger.info(f"Attendance marked: {present_count}/{len(attendance)} present")
            
            if return_annotated:
                return attendance, annotated_img
            return attendance
            
        except Exception as e:
            logger.error(f"Error recognizing faces: {e}")
            return ({}, None) if return_annotated else {}
    
    def get_all_students(self):
        """Get list of all registered students"""
        return self.all_students.copy()
    
    def is_trained(self):
        """Check if system is trained"""
        return len(self.all_students) > 0
