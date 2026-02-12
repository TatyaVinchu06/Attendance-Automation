"""
Face Detection Module
Detects faces in images using insightface (includes SCRFD face detector).
"""
import cv2
import numpy as np
import insightface
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class FaceDetector:
    """Face detector using insightface (SCRFD)."""
    
    def __init__(self, model_path=None):
        """
        Initialize face detector.
        
        Args:
            model_path: Path to model (not used, insightface handles it)
        """
        self.model = None
        
    def _load_model(self):
        """Load face detection model."""
        if self.model is None:
            try:
                model_path = './models/buffalo_l/det_10g.onnx'
                if not Path(model_path).exists():
                     # Try finding it in current directory or user home as fallback (though we should have it in models/buffalo_l now)
                     pass
                     
                logger.info(f"Loading detector from {model_path}")
                # Load SCRFD model directly
                self.model = insightface.model_zoo.get_model(model_path)
                # Prepare with context_id 0 (which usually means GPU 0, or CPU if providers set? 
                # actually get_model returns a model that needs prepare.
                # If we want to use CPU, we might need to specify it.
                # SCRFD prepare matches input size.
                self.model.prepare(ctx_id=0, input_size=(640, 640), det_thresh=0.5)
            except Exception as e:
                logger.error(f"Failed to load face detector: {e}", exc_info=True)
                raise Exception(f"Failed to load face detector: {e}")
    
    def detect_faces(self, image):
        """
        Detect faces in an image.
        
        Args:
            image: Input image (numpy array or PIL Image)
            
        Returns:
            List of tuples: [(bbox, face_crop), ...]
            bbox format: [x1, y1, x2, y2, confidence]
        """
        self._load_model()
        
        # Convert PIL to numpy if needed
        if hasattr(image, 'mode'):
            pil_image = image
            if pil_image.mode == 'RGBA':
                pil_image = pil_image.convert('RGB')
            elif pil_image.mode != 'RGB':
                pil_image = pil_image.convert('RGB')
            image = np.array(pil_image)
        
        # Ensure RGB format
        if len(image.shape) == 3:
            # Check if BGR and convert to RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) if image.shape[2] == 3 else image
        else:
            image_rgb = image
        
        # Run face detection
        # SCRFD expects BGR
        image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
        
        logger.debug(f"Detecting faces in image of shape {image_bgr.shape}")
        try:
            # SCRFD detect returns (bboxes, kpss)
            # bboxes is list of [x1, y1, x2, y2, score]
            bboxes, kpss = self.model.detect(image_bgr, max_num=0, metric='default')
            logger.debug(f"Found {len(bboxes)} faces")
        except Exception as e:
            logger.error(f"Error in face detection: {e}", exc_info=True)
            bboxes = []
        
        faces = []
        h, w = image_rgb.shape[:2]
        
        for bbox in bboxes:
            # Get bounding box
            x1, y1, x2, y2, score = bbox
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            
            # Ensure coordinates are within image bounds
            x1 = max(0, x1)
            y1 = max(0, y1)
            x2 = min(w, x2)
            y2 = min(h, y2)
            
            # Crop face (from RGB image for consistency with other parts of app)
            face_crop = image_rgb[y1:y2, x1:x2]
            
            if face_crop.size > 0 and (x2 - x1) > 10 and (y2 - y1) > 10:
                bbox_with_conf = [x1, y1, x2, y2, score]
                faces.append((bbox_with_conf, face_crop))
        
        return faces
