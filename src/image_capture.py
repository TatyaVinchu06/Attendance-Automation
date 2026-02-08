#!/usr/bin/env python3
"""
Image Capture Module
Camera handle karne wala module
"""

import cv2
import os
import threading
from datetime import datetime
import logging
from config import *

logger = logging.getLogger(__name__)


class ImageCapture:
    """Webcam se photo khinchne wali class"""
    
    def __init__(self, camera_index=CAMERA_INDEX):
        self.camera_index = camera_index
        self.camera = None
        self.is_camera_active = False
        self.lock = threading.Lock()
        
    def initialize_camera(self):
        """Camera chalu karte hai (jo bhi mile)"""
        # Pehle user wala index try karenge, fir baaki
        indices_to_try = [self.camera_index] + [i for i in range(3) if i != self.camera_index]
        
        for index in indices_to_try:
            try:
                logger.info(f"Camera index {index} try kar rahe hai...")
                cap = cv2.VideoCapture(index, cv2.CAP_DSHOW) # Windows ke liye best hai
                
                if not cap.isOpened():
                    # Agar DSHOW nahi chala toh simple wala
                    cap = cv2.VideoCapture(index)
                
                if cap.isOpened():
                    # Check karte hai frame aa raha hai kya
                    ret, _ = cap.read()
                    if ret:
                        self.camera = cap
                        self.camera_index = index # Ye wala index chal gaya
                        
                        # Camera settings set karte hai
                        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
                        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
                        self.camera.set(cv2.CAP_PROP_FPS, CAMERA_FPS)
                        
                        self.is_camera_active = True
                        logger.info(f"Camera {index} mast chal gaya")
                        return True
                    else:
                        cap.release()
                        logger.warning(f"Camera {index} khula to sahi par frame nahi diya")
            except Exception as e:
                logger.error(f"Camera {index} me dikkat aayi: {e}")
        
        logger.error("Koi bhi camera nahi chala bhai")
        return False
    
    def capture_image(self, class_id=""):
        """
        Ek photo khichte hai
        """
        if not self.is_camera_active:
            if not self.initialize_camera():
                return None
        
        try:
            # Frame capture karte hai
            with self.lock:
                if self.camera is None or not self.camera.isOpened():
                     return None
                ret, frame = self.camera.read()
            
            if not ret:
                logger.error("Frame capture nahi hua")
                return None
            
            # Filename banate hai timestamp ke saath
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"{class_id}_{timestamp}.{IMAGE_FORMAT}" if class_id else f"{timestamp}.{IMAGE_FORMAT}"
            filepath = os.path.join(IMAGES_DIR, filename)
            
            # Save karte hai
            cv2.imwrite(filepath, frame, [cv2.IMWRITE_JPEG_QUALITY, IMAGE_QUALITY])
            logger.info(f"Photo save ho gayi: {filepath}")
            
            return filepath
            
        except Exception as e:
            logger.error(f"Photo khinchne me error: {e}")
            return None
    
    def capture_multiple_images(self, count=3, interval=2, class_id=""):
        """
        Dhadadhan photos khenchna (interval ke saath)
        """
        images = []
        
        for i in range(count):
            filepath = self.capture_image(class_id)
            
            if filepath:
                images.append(filepath)
                logger.info(f"Photo {i+1}/{count} khinch li")
            
            # Agli photo se pehle thoda rukte hai
            if i < count - 1:
                import time
                time.sleep(interval)
        
        return images
    
    def get_frame(self):
        """
        Live preview ke liye frame chahiye
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
            logger.error(f"Frame lene me error: {e}")
            return None
    
    def release_camera(self):
        """Camera band karte hai"""
        if self.camera is not None:
            self.camera.release()
            self.is_camera_active = False
            logger.info("Camera band kar diya")
    
    def __del__(self):
        """Agar object delete hua toh camera bhi band"""
        self.release_camera()