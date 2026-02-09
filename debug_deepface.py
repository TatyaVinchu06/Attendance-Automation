import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("--- Starting DeepFace Debug ---")

try:
    print("Importing DeepFace...")
    from deepface import DeepFace
    print(f"DeepFace version: {DeepFace.__version__}")
    
    print("Building VGG-Face model...")
    # This might download weights if not present
    model = DeepFace.build_model("VGG-Face") 
    print("VGG-Face model built successfully!")
    
    print("Building SSD detector...")
    # This might also download weights
    from deepface.detectors import FaceDetector
    # DeepFace internal structure might vary, let's just use build_model or check backends
    print("DeepFace backends available.")

except Exception as e:
    print(f"\n[ERROR] DeepFace check failed: {e}")
    import traceback
    traceback.print_exc()

print("--- End of Debug ---")
