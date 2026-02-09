import cv2
import os
import sys
sys.path.append(os.path.join(os.getcwd(), 'src'))
from src.face_recognition_module import FaceRecognitionModule
from src.config import STUDENT_DATASET_DIR, FACE_DETECTOR_BACKEND, SIMILARITY_THRESHOLD

print("=" * 60)
print("GROUP PHOTO DEBUG SCRIPT")
print("=" * 60)
print(f"Detector Backend: {FACE_DETECTOR_BACKEND}")
print(f"Similarity Threshold: {SIMILARITY_THRESHOLD}")
print(f"Dataset: {STUDENT_DATASET_DIR}")
print("=" * 60)

# Initialize
print("\nInitializing FaceRecognitionModule...")
fr = FaceRecognitionModule()

# Check dataset
if os.path.exists(STUDENT_DATASET_DIR):
    students = [d for d in os.listdir(STUDENT_DATASET_DIR) if os.path.isdir(os.path.join(STUDENT_DATASET_DIR, d))]
    print(f"Found {len(students)} students in database:")
    for s in students:
        print(f"  - {s}")
else:
    print("ERROR: Dataset directory not found!")
    sys.exit(1)

print("\n" + "=" * 60)
print("PLEASE PROVIDE A GROUP PHOTO PATH")
print("=" * 60)
print("Example: C:/Users/ombha/Downloads/group.jpeg")
photo_path = input("Enter path: ").strip().strip('"')

if not os.path.exists(photo_path):
    print(f"ERROR: File not found: {photo_path}")
    sys.exit(1)

print(f"\nAnalyzing: {photo_path}")
print("=" * 60)

# Run recognition with detailed output
try:
    attendance = fr.recognize_faces(photo_path)
    
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    
    present = [name for name, status in attendance.items() if status == "Present"]
    absent = [name for name, status in attendance.items() if status == "Absent"]
    
    print(f"\nPresent ({len(present)}):")
    for name in present:
        print(f"  ✓ {name}")
    
    print(f"\nAbsent ({len(absent)}):")
    for name in absent:
        print(f"  ✗ {name}")
    
    print("\n" + "=" * 60)
    
except Exception as e:
    print(f"\nERROR during recognition: {e}")
    import traceback
    traceback.print_exc()

print("\nDone.")
