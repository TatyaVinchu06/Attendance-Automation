#!/usr/bin/env python3
"""
Face Recognition Code (New Engine - InsightFace)

Replaces DeepFace with InsightFace (SCRFD + ArcFace) for better accuracy.
Threshold: 0.55
"""

import os
import logging
import cv2
import numpy as np
from typing import Any, Tuple, Dict, List, Optional

from config import (
    STUDENT_DATASET_DIR,
    SIMILARITY_THRESHOLD,
    ENCODINGS_FILE,
)

# Import new core modules (copied from 'New folder/core' to 'cam/src/core')
from core.detector import FaceDetector
from core.embedder import FaceEmbedder
from core.database import FaceDatabase

logger = logging.getLogger(__name__)

class FaceRecognitionModule:
    """
    InsightFace (SCRFD + ArcFace) engine for face recognition.
    """

    def __init__(self):
        self.database_path = str(STUDENT_DATASET_DIR)
        
        # Initialize Core Modules
        # Ensure models are found. The 'core' modules look in './models' by default.
        # Since we run from 'cam' root, and we copied 'models' to 'cam/models', it should work.
        try:
            self.detector = FaceDetector()
            self.embedder = FaceEmbedder()
            # Use the existing ENCODINGS_FILE path structure but adapted for the new Database class if needed.
            # The new Database class uses pickle.
            # We will use the same ENCODINGS_FILE path defined in config.py
            self.db = FaceDatabase(db_path=ENCODINGS_FILE)
            logger.info("Face Recognition Engine Initialized (InsightFace)")
        except Exception as e:
            logger.error(f"Failed to initialize Face Recognition Engine: {e}")
            raise

    def _cosine_distance(self, a: np.ndarray, b: np.ndarray) -> float:
        """
        Compute cosine distance between two embeddings.
        dist = 1 - cos_sim
        """
        a = a.flatten()
        b = b.flatten()
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        if norm_a == 0 or norm_b == 0:
            return 1.0
        return 1.0 - np.dot(a, b) / (norm_a * norm_b)

    # -------------------- TRAIN --------------------
    def train_face_encodings(self):
        """
        Build embeddings for each student image in STUDENT_DATASET_DIR 
        and store them in the database (pickle file).
        """
        logger.info("Starting training/enrollment from %s...", STUDENT_DATASET_DIR)
        
        if not os.path.exists(STUDENT_DATASET_DIR):
            logger.error("Student dataset directory not found: %s", STUDENT_DATASET_DIR)
            return False

        student_folders = [
            d for d in os.listdir(STUDENT_DATASET_DIR)
            if os.path.isdir(os.path.join(STUDENT_DATASET_DIR, d))
        ]

        if not student_folders:
            logger.error("No student folders found in dataset directory.")
            return False
            
        success_count = 0
            
        # Re-initialize/Clear database for fresh training? 
        # The prompt implies "replace ours with this", usually implies a full rebuild or ensuring it works.
        # If we want to fully retrain, we might want to clear existing. 
        # But FaceDatabase loads existing. Let's assume we update/overwrite.
        # Actually existing 'cam' logic was a full retrain usually.
        
        # NOTE: The new FaceDatabase calculates embeddings on the fly if we use add_student.
        # But here we are processing raw images to embeddings.
        
        for student_name in student_folders:
            student_path = os.path.join(STUDENT_DATASET_DIR, student_name)
            image_files = [
                f for f in os.listdir(student_path)
                if f.lower().endswith((".jpg", ".jpeg", ".png"))
            ]
            
            if not image_files:
                logger.warning(f"No images found for student: {student_name}")
                continue
                
            logger.info(f"Processing student: {student_name} ({len(image_files)} images)")
            
            # We will take the best/first valid face embedding for the student
            # Or average them? The new system's 'train' logic isn't explicitly in 'New folder', 
            # but 'FaceDatabase' stores one embedding per key (implied by add_student).
            # We will try to find the best quality face.
            
            best_embedding = None
            max_conf = -1.0
            
            for img_file in image_files:
                img_path = os.path.join(student_path, img_file)
                try:
                    # Read image
                    # FaceDetector expects RGB or BGR? 
                    # Core detector.py: "SCRFD expects BGR", "Input image (numpy array or PIL Image)"
                    # converting to RGB inside.
                    
                    img = cv2.imread(img_path)
                    if img is None:
                        continue
                        
                    # Detect faces
                    # detect_faces returns [(bbox, face_crop), ...]
                    faces = self.detector.detect_faces(img)
                    
                    if not faces:
                        continue
                        
                    # Take the largest face or most confident?
                    # detect_faces output doesn't sort by default but returns list.
                    # Usually largest is best for enrollment.
                    # Let's pick the one with largest area.
                    
                    best_face = None
                    max_area = 0
                    
                    for (bbox, face_crop) in faces:
                        x1, y1, x2, y2, score = bbox
                        area = (x2 - x1) * (y2 - y1)
                        if area > max_area:
                            max_area = area
                            best_face = face_crop
                            
                    if best_face is not None:
                         # Convert RGB crop (from detector) to BGR for Embedder
                         # Detector returns RGB crop when input is BGR (due to internal swap).
                         # Embedder expects BGR (internal swap to RGB).
                         if len(best_face.shape) == 3:
                             best_face = cv2.cvtColor(best_face, cv2.COLOR_RGB2BGR)

                         # Get embedding
                         emb = self.embedder.get_embedding(best_face)
                         
                         # Store this. If we process multiple images, maybe we can average?
                         # For now, let's just stick to the simplest robust strategy:
                         # Use the first good one, or average if we want to be fancy.
                         # The prompt said "no ui/ux change", keeping logic simple and robust is best.
                         # Let's use the first valid one we find, or overwrite if we find another? 
                         # Actually, let's just use the last one successfully processed, or average.
                         # Averaging is better for stability.
                         
                         if best_embedding is None:
                             best_embedding = emb
                         else:
                             best_embedding = (best_embedding + emb) / 2.0
                             
                except Exception as e:
                    logger.warning(f"Error processing image {img_file} for {student_name}: {e}")
                    
            if best_embedding is not None:
                # Normalize again after averaging
                best_embedding = best_embedding / np.linalg.norm(best_embedding)
                
                # Store in DB
                # DB expects roll, name. We only have folder name which is usually "Name" or "Roll_Name".
                # Existing system seems to use just "student_name" as data.
                # We will treat 'roll' as empty or part of name.
                self.db.add_student(name=student_name, roll="", embedding=best_embedding)
                success_count += 1
                
        self.db.save_database()
        logger.info(f"Training complete. Enrolled {success_count} students.")
        return True

    # -------------------- SAVE/LOAD --------------------
    def save_encodings(self):
        """
        Delegates to FaceDatabase save.
        """
        self.db.save_database()
        return True

    def load_encodings(self):
        """
        Delegates to FaceDatabase load.
        """
        self.db.load_database()
        return True

    # -------------------- RECOGNITION --------------------
    def recognize_faces(self, image_path: str, return_annotated: bool = False) -> Any:
        """
        Recognize faces in the given image path.
        Returns:
            attendance (dict): {student_name: "Present"|"Absent", ...}
            annotated_img (np.ndarray|None): Image with boxes if requested
        """
        # Load DB if empty?
        if self.db.get_student_count() == 0:
            self.load_encodings()

        all_students = self.db.get_all_students() 
        # The key in DB is f"{roll}_{name}" or just name if roll empty.
        # We need to map back to simple names for the attendance dict if possible, 
        # or use the keys as names.
        
        # Initialize attendance dict
        attendance = {name: "Absent" for name in all_students.keys()}
        
        annotated_img = None
        if return_annotated:
            annotated_img = cv2.imread(image_path)

        try:
            logger.info("Recognizing faces in %s", image_path)
            img = cv2.imread(image_path)
            if img is None:
                logger.error("Could not read image: %s", image_path)
                return (attendance, annotated_img) if return_annotated else attendance

            # Detect Faces
            faces = self.detector.detect_faces(img)
            
            if not faces:
                logger.info("No faces detected.")
                return (attendance, annotated_img) if return_annotated else attendance

            logger.info("Detected %d faces.", len(faces))

            for (bbox, face_crop) in faces:
                # Convert RGB crop (from detector) to BGR for Embedder
                if len(face_crop.shape) == 3:
                     face_crop = cv2.cvtColor(face_crop, cv2.COLOR_RGB2BGR)

                # Get Embedding
                query_emb = self.embedder.get_embedding(face_crop)
                
                # Find Best Match
                best_name = None
                best_sim = -1.0
                
                # Manual search vs DB search (DB doesn't have search with threshold exposed widely in the snippet I saw, 
                # but 'recognize.py' implemented 'find_best_match'. I will replicate logic here.)
                
                for name, db_emb in all_students.items():
                    # Cosine Similarity
                    # sim = dot(u, v) / (norm(u)*norm(v))
                    # My embedder returns normalized vectors, but let's be safe.
                    sim = np.dot(query_emb, db_emb) / (np.linalg.norm(query_emb) * np.linalg.norm(db_emb) + 1e-10)
                    
                    if sim > best_sim:
                        best_sim = sim
                        best_name = name
                        
                # Check Threshold
                matched = False
                final_name = "Unknown"
                
                if best_sim >= SIMILARITY_THRESHOLD:
                    attendance[best_name] = "Present"
                    final_name = best_name
                    matched = True
                    logger.info(f"Match found: {best_name} ({best_sim:.4f})")
                else:
                    logger.info(f"Unknown face. Best match: {best_name} ({best_sim:.4f}) < {SIMILARITY_THRESHOLD}")

                # Annotation
                if return_annotated and annotated_img is not None:
                    x1, y1, x2, y2, score = bbox
                    color = (0, 255, 0) if matched else (0, 0, 255)
                    cv2.rectangle(annotated_img, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
                    
                    label = f"{final_name} ({best_sim:.2f})"
                    cv2.putText(annotated_img, label, (int(x1), int(y1)-10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            return (attendance, annotated_img) if return_annotated else attendance

        except Exception as e:
            logger.error(f"Error during recognition: {e}")
            return ({}, None) if return_annotated else {}

    def get_all_students(self):
        """Return list of student names/keys."""
        return list(self.db.get_all_students().keys())

    def is_trained(self):
        """Check if we have embeddings."""
        return self.db.get_student_count() > 0

    def refresh_from_disk(self):
        """Force retrain/refresh."""
        return self.train_face_encodings()

