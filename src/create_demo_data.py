#!/usr/bin/env python3
"""
Create demo student data for testing the attendance system
Run this script to set up sample students for demonstration
"""

import os
import cv2
import shutil
from pathlib import Path
from config import STUDENT_DATASET_DIR

# Demo students
DEMO_STUDENTS = [
    "Om_Bhardwaj",
    "Rahul_Sharma",
    "Neha_Patel",
    "Arjun_Singh",
    "Priya_Gupta",
]


def create_demo_student_folders():
    """Create demo student folders with placeholder images"""
    print("Creating demo student dataset...")
    print("=" * 60)
    
    # Create student dataset directory if it doesn't exist
    os.makedirs(STUDENT_DATASET_DIR, exist_ok=True)
    
    for student_name in DEMO_STUDENTS:
        student_dir = os.path.join(STUDENT_DATASET_DIR, student_name)
        os.makedirs(student_dir, exist_ok=True)
        
        print(f"\n✓ Created folder: {student_name}")
        print(f"  Path: {student_dir}")
        print(f"\n  ⚠️  ACTION REQUIRED:")
        print(f"  Add 3-5 clear face photos of {student_name} to this folder")
        print(f"  Photos should be JPG/PNG format, showing clear facial features")
    
    print("\n" + "=" * 60)
    print("Demo folders created successfully!")
    print("\nNEXT STEPS:")
    print("1. Add student photos to each folder")
    print("2. Launch the application: run_app.bat")
    print("3. Go to 'Student Database' page")
    print("4. Click 'Train Face Recognition'")
    print("=" * 60)


def create_readme_in_dataset():
    """Create README in dataset folder with instructions"""
    readme_path = os.path.join(STUDENT_DATASET_DIR, "README.txt")
    
    content = """
AI-BASED ATTENDANCE SYSTEM - STUDENT DATASET
=============================================

This folder contains student face photos for the attendance system.

FOLDER STRUCTURE:
-----------------
student_dataset/
├── Student_Name_1/
│   ├── photo1.jpg
│   ├── photo2.jpg
│   └── photo3.jpg
├── Student_Name_2/
│   ├── photo1.jpg
│   └── photo2.jpg
...

INSTRUCTIONS:
-------------
1. Create one folder for each student
2. Name the folder with the student's name (use underscores for spaces)
3. Add 3-5 clear face photos per student
4. Photos should be:
   - JPG or PNG format
   - Clear, well-lit faces
   - Person looking at camera
   - Different angles/expressions (optional but recommended)

EXAMPLE NAMES:
--------------
- Om_Bhardwaj
- Rahul_Sharma  
- Neha_Patel
- Arjun_Singh
- Priya_Gupta

TRAINING:
---------
After adding photos:
1. Open the application
2. Go to "Student Database" page
3. Click "Train Face Recognition"
4. Wait for training to complete

PRIVACY NOTE:
-------------
All face data is stored locally and will be automatically deleted after 7 days.
No data is sent to external servers.

For support, check the main README.md file.
"""
    
    with open(readme_path, 'w') as f:
        f.write(content)
    
    print(f"\n✓ Created README in {readme_path}")


def main():
    print("\n" + "=" * 60)
    print("DEMO DATA SETUP FOR AI-BASED ATTENDANCE SYSTEM")
    print("=" * 60 + "\n")
    
    response = input("This will create demo student folders. Continue? (yes/no): ").strip().lower()
    
    if response == 'yes':
        create_demo_student_folders()
        create_readme_in_dataset()
        
        print("\nWould you like to open the student dataset folder now? (yes/no): ", end='')
        open_folder = input().strip().lower()
        
        if open_folder == 'yes':
            import subprocess
            subprocess.Popen(f'explorer "{STUDENT_DATASET_DIR}"')
    else:
        print("\nOperation cancelled.")


if __name__ == "__main__":
    main()