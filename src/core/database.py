"""
Database Module for storing face embeddings.
Uses pickle for simple, efficient storage.
"""
import pickle
import numpy as np
from pathlib import Path
from typing import Dict, Optional

class FaceDatabase:
    """Pickle-based face embedding database."""
    
    def __init__(self, db_path="database/students.pkl"):
        """
        Initialize database.
        
        Args:
            db_path: Path to pickle database file
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.data: Dict[str, np.ndarray] = {}
        self.load_database()
    
    def load_database(self):
        """Load database from pickle file."""
        if self.db_path.exists():
            try:
                with open(self.db_path, 'rb') as f:
                    self.data = pickle.load(f)
                print(f"Loaded database with {len(self.data)} students")
            except Exception as e:
                print(f"Error loading database: {e}")
                self.data = {}
        else:
            self.data = {}
            print("Creating new database")
    
    def save_database(self):
        """Save database to pickle file."""
        try:
            with open(self.db_path, 'wb') as f:
                pickle.dump(self.data, f)
            print(f"Saved database with {len(self.data)} students")
        except Exception as e:
            print(f"Error saving database: {e}")
            raise
    
    def add_student(self, name: str, roll: str, embedding: np.ndarray):
        """
        Add or update a student in the database.
        
        Args:
            name: Student name
            roll: Student roll number
            embedding: Face embedding vector (normalized)
        """
        key = f"{roll}_{name}"
        
        # Ensure embedding is numpy array and normalized
        if not isinstance(embedding, np.ndarray):
            embedding = np.array(embedding)
        
        # Normalize embedding if not already normalized
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm
        
        self.data[key] = embedding
        print(f"Added/Updated student: {key}")
    
    def get_student(self, roll: str, name: str) -> Optional[np.ndarray]:
        """
        Get student embedding.
        
        Args:
            roll: Student roll number
            name: Student name
            
        Returns:
            Embedding vector or None if not found
        """
        key = f"{roll}_{name}"
        return self.data.get(key)
    
    def get_all_students(self) -> Dict[str, np.ndarray]:
        """
        Get all enrolled students.
        
        Returns:
            Dictionary mapping student keys to embeddings
        """
        return self.data.copy()
    
    def delete_student(self, roll: str, name: str) -> bool:
        """
        Delete a student from database.
        
        Args:
            roll: Student roll number
            name: Student name
            
        Returns:
            True if deleted, False if not found
        """
        key = f"{roll}_{name}"
        if key in self.data:
            del self.data[key]
            print(f"Deleted student: {key}")
            return True
        return False
    
    def get_student_count(self) -> int:
        """Get total number of enrolled students."""
        return len(self.data)
    
    def search_by_key(self, key: str) -> Optional[np.ndarray]:
        """
        Search student by full key (ROLL_NAME format).
        
        Args:
            key: Student key in format "ROLL_NAME"
            
        Returns:
            Embedding vector or None if not found
        """
        return self.data.get(key)
    
    def remove_student(self, student_key: str) -> bool:
        """
        Remove a student using their full key (ROLL_NAME format).
        Wrapper for delete_student for convenience.
        
        Args:
            student_key: Full student key (e.g., "10_Om_Bhamare")
            
        Returns:
            True if deleted, False if not found
        """
        if student_key in self.data:
            del self.data[student_key]
            print(f"Removed student: {student_key}")
            return True
        return False
