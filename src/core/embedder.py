"""
ArcFace Embedding Generation Module
Generates face embeddings using ArcFace model.
"""
import cv2
import numpy as np
import onnxruntime as ort
from pathlib import Path
import insightface

class FaceEmbedder:
    """ArcFace-based face embedder."""
    
    def __init__(self, model_path=None):
        """
        Initialize face embedder.
        
        Args:
            model_path: Path to ArcFace ONNX model. If None, uses insightface default.
        """
        self.model = None
        self.model_path = model_path
        self.input_size = (112, 112)  # Standard ArcFace input size
        
    def _load_model(self):
        """Load ArcFace model."""
        if self.model is None:
            try:
                # Prefer local ONNX model
                model_path = './models/buffalo_l/w600k_r50.onnx'
                if self.model_path:
                    model_path = self.model_path
                    
                if Path(model_path).exists():
                    try:
                        import logging
                        logger = logging.getLogger(__name__)
                        logger.info(f"Loading embedder from {model_path}")
                        self.model = ort.InferenceSession(model_path, providers=['CPUExecutionProvider'])
                    except Exception as e:
                         # Try fallback
                         raise e
                else:
                    # Fallback to insightface if local not found (unlikely now)
                    # But we prefer explicit ONNX loading
                    raise FileNotFoundError(f"Model not found at {model_path}")

            except Exception as e:
                # Fallback to ONNX runtime if insightface fails
                if self.model_path and Path(self.model_path).exists():
                    self.model = ort.InferenceSession(self.model_path)
                else:
                    raise Exception(f"Failed to load ArcFace model: {e}")
    
    def get_embedding(self, face_image):
        """
        Generate embedding for a face image.
        
        Args:
            face_image: Face crop (numpy array)
            
        Returns:
            Normalized 512-dimensional embedding vector
        """
        self._load_model()
        
        # Convert PIL to numpy if needed
        if hasattr(face_image, 'mode'):
            face_image = np.array(face_image)
            if len(face_image.shape) == 3 and face_image.shape[2] == 4:  # RGBA
                face_image = cv2.cvtColor(face_image, cv2.COLOR_RGBA2RGB)
        
        # Preprocess for ArcFace ONNX
        face_processed = self._preprocess_face(face_image)
        
        # Get input and output names
        input_name = self.model.get_inputs()[0].name
        
        # Run inference
        outputs = self.model.run(None, {input_name: face_processed})
        embedding = outputs[0][0]
        
        # Normalize embedding
        embedding = embedding / np.linalg.norm(embedding)
        
        return embedding
    
    def _preprocess_face(self, face_image):
        """
        Preprocess face image for ArcFace model.
        
        Args:
            face_image: Face crop (numpy array)
            
        Returns:
            Preprocessed image ready for model input
        """
        # Resize to model input size
        face_resized = cv2.resize(face_image, self.input_size)
        
        # Convert BGR to RGB if needed
        if len(face_resized.shape) == 3:
            face_resized = cv2.cvtColor(face_resized, cv2.COLOR_BGR2RGB)
        
        # Normalize to [-1, 1] range (common for ArcFace)
        face_normalized = (face_resized.astype(np.float32) / 127.5) - 1.0
        
        # Transpose to CHW format and add batch dimension
        face_transposed = np.transpose(face_normalized, (2, 0, 1))
        face_batch = np.expand_dims(face_transposed, axis=0)
        
        return face_batch.astype(np.float32)
    
    def get_embeddings_batch(self, face_images):
        """
        Generate embeddings for multiple face images.
        
        Args:
            face_images: List of face crops
            
        Returns:
            List of normalized embedding vectors
        """
        embeddings = []
        for face_image in face_images:
            try:
                embedding = self.get_embedding(face_image)
                embeddings.append(embedding)
            except Exception as e:
                print(f"Error processing face: {e}")
                continue
        return embeddings
