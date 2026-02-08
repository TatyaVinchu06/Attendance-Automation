#!/usr/bin/env python3
"""
Emotion Detection Module
Classroom ke emotions pakadne wala module
"""

import logging
from collections import Counter
from deepface import DeepFace
import cv2
import numpy as np
from config import *

logger = logging.getLogger(__name__)


class EmotionDetection:
    """Classroom analytics ke liye emotion pakadta hai"""
    
    def __init__(self):
        self.emotion_labels = EMOTIONS
    
    def detect_emotions_in_image(self, image_path):
        """
        Ek photo se emotion nikalte hai
        """
        emotions_detected = []
        
        try:
            # Photo analyze kar rahe hai
            results = DeepFace.analyze(
                img_path=image_path,
                actions=['emotion'],
                enforce_detection=False,
                detector_backend=EMOTION_BACKEND,
                silent=True
            )
            
            # Ek ya jyada chehre sambhalte hai
            if isinstance(results, dict):
                results = [results]
            
            # Har chehre ka dominant emotion nikalte hai
            for result in results:
                if 'emotion' in result:
                    emotion_scores = result['emotion']
                    dominant_emotion = max(emotion_scores, key=emotion_scores.get)
                    emotions_detected.append(dominant_emotion)
                    logger.debug(f"Emotion mila: {dominant_emotion}")
            
            logger.info(f"{len(emotions_detected)} emotions mile is photo me")
            return emotions_detected
            
        except Exception as e:
            logger.error(f"Emotion detect karne me dikkat aayi: {e}")
            return []
    
    def analyze_multiple_images(self, image_paths):
        """
        Bohot saari photos ka analysis karte hai
        """
        all_emotions = []
        
        # Saari photos se emotions ikhattha karo
        for image_path in image_paths:
            emotions = self.detect_emotions_in_image(image_path)
            all_emotions.extend(emotions)
        
        if not all_emotions:
            logger.warning("Koi emotion nahi mila bhai")
            return {}
        
        # Percentages nikalte hai
        emotion_counts = Counter(all_emotions)
        total_faces = len(all_emotions)
        
        emotion_summary = {}
        for emotion, count in emotion_counts.items():
            percentage = round((count / total_faces) * 100, 1)
            emotion_summary[emotion.capitalize()] = percentage
        
        # Sort karte hai (jyada se kam)
        emotion_summary = dict(sorted(
            emotion_summary.items(),
            key=lambda x: x[1],
            reverse=True
        ))
        
        logger.info(f"Analysis khatam: {emotion_summary}")
        return emotion_summary
    
    def get_dominant_emotion(self, emotion_summary):
        """
        Sabse jyada jo emotion hai wo batao
        """
        if not emotion_summary:
            return "Unknown"
        
        return max(emotion_summary, key=emotion_summary.get)
    
    def get_class_mood(self, emotion_summary):
        """
        Class ka mood kaisa hai ye dekhte hai
        """
        if not emotion_summary:
            return "Pata nahi chal raha"
        
        # Mood categories banate hai
        positive_emotions = ['happy', 'surprise']
        neutral_emotions = ['neutral']
        negative_emotions = ['sad', 'angry', 'fear', 'disgust']
        
        # Percentages calculate karte hai
        positive_pct = sum(emotion_summary.get(e.capitalize(), 0) for e in positive_emotions)
        neutral_pct = sum(emotion_summary.get(e.capitalize(), 0) for e in neutral_emotions)
        negative_pct = sum(emotion_summary.get(e.capitalize(), 0) for e in negative_emotions)
        
        # Mood decide karte hai
        if positive_pct >= 50:
            return "Positive - Bachhe khush lag rahe hai"
        elif neutral_pct >= 60:
            return "Neutral - Bachhe dhyan de rahe hai"
        elif negative_pct >= 40:
            return "Needs Attention - Shayad samajh nahi aa raha ya boring hai"
        else:
            return "Mixed - Sabka alag alag mood hai"
    
    def format_emotion_summary(self, emotion_summary):
        """
        Dikhane ke liye summary format karte hai
        """
        if not emotion_summary:
            return "Koi emotion detect nahi hua"
        
        lines = []
        for emotion, percentage in emotion_summary.items():
            bar = "█" * int(percentage / 5)  # Visual bar
            lines.append(f"{emotion:10} {percentage:5.1f}% {bar}")
        
        return "\n".join(lines)