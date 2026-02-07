#!/usr/bin/env python3
"""
Image Capture Module
Handles webcam interface and image capture
"""

import cv2
import os
import threading
from datetime import datetime
import logging
from config import *

logger = logging.getLogger(__name__)


class ImageCapture:
    """Handles image capture from webcam"""
    
    def __init__(self, camera_index=CAMERA_INDEX):
        self.camera_index = camera_index
        self.camera = None
        self.is_camera_active = False
        self.lock = threading.Lock()
        
    def initialize_camera(self):
        """Initialize the camera with fallback"""
        # Try configured index first, then others
        indices_to_try = [self.camera_index] + [i for i in range(3) if i != self.camera_index]
        
        for index in indices_to_try:
            try:
                logger.info(f"Trying to open camera index {index}...")
                cap = cv2.VideoCapture(index, cv2.CAP_DSHOW) # standard backend on Windows
                
                if not cap.isOpened():
                    # Try without CAP_DSHOW
                    cap = cv2.VideoCapture(index)
                
                if cap.isOpened():
                    # Test reading a frame
                    ret, _ = cap.read()
                    if ret:
                        self.camera = cap
                        self.camera_index = index # Update to working index
                        
                        # Set camera properties
                        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
                        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
                        self.camera.set(cv2.CAP_PROP_FPS, CAMERA_FPS)
                        
                        self.is_camera_active = True
                        logger.info(f"Camera {index} initialized successfully")
                        return True
                    else:
                        cap.release()
                        logger.warning(f"Camera {index} opened but returned no frame")
            except Exception as e:
                logger.error(f"Error trying camera {index}: {e}")
        
        logger.error("Failed to initialize any camera")
        return False
    
    def capture_image(self, class_id=""):
        """
        Capture a single image
        
        Args:
            class_id: Optional class/subject identifier
            
        Returns:
            str: Path to saved image, or None if failed
        """
        if not self.is_camera_active:
            if not self.initialize_camera():
                return None
        
        try:
            # Read frame
            with self.lock:
                if self.camera is None or not self.camera.isOpened():
                     return None
                ret, frame = self.camera.read()
            
            if not ret:
                logger.error("Failed to capture frame")
                return None
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"{class_id}_{timestamp}.{IMAGE_FORMAT}" if class_id else f"{timestamp}.{IMAGE_FORMAT}"
            filepath = os.path.join(IMAGES_DIR, filename)
            
            # Save image
            cv2.imwrite(filepath, frame, [cv2.IMWRITE_JPEG_QUALITY, IMAGE_QUALITY])
            logger.info(f"Image saved: {filepath}")
            
            return filepath
            
        except Exception as e:
            logger.error(f"Error capturing image: {e}")
            return None
    
    def capture_multiple_images(self, count=3, interval=2, class_id=""):
        """
        Capture multiple images with interval
        
        Args:
            count: Number of images to capture
            interval: Seconds between captures
            class_id: Optional class identifier
            
        Returns:
            list: Paths to saved images
        """
        images = []
        
        for i in range(count):
            filepath = self.capture_image(class_id)
            
            if filepath:
                images.append(filepath)
                logger.info(f"Captured image {i+1}/{count}")
            
            # Wait between captures (except for last image)
            if i < count - 1:
                import time
                time.sleep(interval)
        
        return images
    
    def get_frame(self):
        """
        Get current camera frame (for live preview)
        
        Returns:
            numpy.ndarray: Current frame, or None if failed
        """
        if not self.is_camera_active:
            if not self.initialize_camera():
                return None
        
        try:
            with self.lock:
                if self.camera is None or not self.camera.isOpened():
                    return None
                ret, frame = self.camera.read()
            return frame if ret else None
            
        except Exception as e:
            logger.error(f"Error getting frame: {e}")
            return None
    
    def release_camera(self):
        """Release the camera"""
        if self.camera is not None:
            self.camera.release()
            self.is_camera_active = False
            logger.info("Camera released")
    
    def __del__(self):
        """Cleanup when object is destroyed"""
        self.release_camera()