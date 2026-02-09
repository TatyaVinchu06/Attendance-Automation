import cv2
import os
import sys
sys.path.append(os.path.join(os.getcwd(), 'src'))
from src.face_recognition_module import FaceRecognitionModule
from src.config import STUDENT_DATASET_DIR

# Initializing
print("Initializing FaceRecognitionModule...")
fr = FaceRecognitionModule()

# Check dataset
print(f"Checking dataset at {STUDENT_DATASET_DIR}...")
if os.path.exists(STUDENT_DATASET_DIR):
    students = os.listdir(STUDENT_DATASET_DIR)
    print(f"Found {len(students)} students: {students}")
else:
    print("Dataset directory not found!")

# Capture frame
print("Capturing frame from camera...")
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open camera.")
    sys.exit(1)

ret, frame = cap.read()
cap.release()

if not ret:
    print("Error: Could not read frame.")
    sys.exit(1)

# Save temp frame
temp_path = "debug_frame.jpg"
cv2.imwrite(temp_path, frame)
print(f"Saved frame to {temp_path}")

# Run recognition
print("Running recognize_faces...")
try:
    # Temporarily set threshold very high to see ALL matches if possible, 
    # but DeepFace.find uses the argument. 
    # We will rely on the debug prints inside the module (which we will add/enhance).
    attendance = fr.recognize_faces(temp_path)
    print("Result:", attendance)
except Exception as e:
    print(f"Error during recognition: {e}")
    import traceback
    traceback.print_exc()

print("Done.")
