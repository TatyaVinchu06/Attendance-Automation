#!/usr/bin/env python3
"""
Emotion Detection Module (Mock)
Classroom ke emotions pakadne wala module (Currently Disabled)
"""

import logging
from collections import Counter
# from deepface import DeepFace  # Disabled as it causes issues without dependency
import cv2
import numpy as np
from config import *

logger = logging.getLogger(__name__)


class EmotionDetection:
    """Classroom analytics ke liye emotion pakadta hai (Mock Version)"""
    
    def __init__(self):
        self.emotion_labels = EMOTIONS
        logger.warning("Emotion Detection is running in MOCK mode (DeepFace disabled).")
    
    def detect_emotions_in_image(self, image_path):
        """
        Ek photo se emotion nikalte hai (Mock: Returns Neutral)
        """
        logger.debug("Mocking emotion detection: returning 'neutral'")
        return ['neutral']
            
    def analyze_multiple_images(self, image_paths):
        """
        Bohot saari photos ka analysis karte hai (Mock: Returns Neutral 100%)
        """
        return {'Neutral': 100.0}
    
    def get_dominant_emotion(self, emotion_summary):
        """
        Sabse jyada jo emotion hai wo batao (Mock)
        """
        return "neutral"
    
    def get_class_mood(self, emotion_summary):
        """
        Class ka mood kaisa hai ye dekhte hai (Mock)
        """
        return "Neutral - System running in lightweight mode"
    
    def format_emotion_summary(self, emotion_summary):
        """
        Dikhane ke liye summary format karte hai (Mock)
        """
        return "Emotion detection unavailable (DeepFace disabled)"
