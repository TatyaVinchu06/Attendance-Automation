#!/usr/bin/env python3
"""
Emotion Detection Module
Analyzes classroom emotions from face images
"""

import logging
from collections import Counter
from deepface import DeepFace
import cv2
import numpy as np
from config import *

logger = logging.getLogger(__name__)


class EmotionDetection:
    """Emotion detection for classroom analytics"""
    
    def __init__(self):
        self.emotion_labels = EMOTIONS
    
    def detect_emotions_in_image(self, image_path):
        """
        Detect emotions in a single image
        
        Args:
            image_path: Path to image file
            
        Returns:
            list: List of detected emotions
        """
        emotions_detected = []
        
        try:
            # Analyze image
            results = DeepFace.analyze(
                img_path=image_path,
                actions=['emotion'],
                enforce_detection=False,
                detector_backend=EMOTION_BACKEND,
                silent=True
            )
            
            # Handle single face or multiple faces
            if isinstance(results, dict):
                results = [results]
            
            # Extract dominant emotion from each face
            for result in results:
                if 'emotion' in result:
                    emotion_scores = result['emotion']
                    dominant_emotion = max(emotion_scores, key=emotion_scores.get)
                    emotions_detected.append(dominant_emotion)
                    logger.debug(f"Detected emotion: {dominant_emotion}")
            
            logger.info(f"Detected {len(emotions_detected)} emotions in image")
            return emotions_detected
            
        except Exception as e:
            logger.error(f"Error detecting emotions: {e}")
            return []
    
    def analyze_multiple_images(self, image_paths):
        """
        Analyze emotions across multiple images
        
        Args:
            image_paths: List of image file paths
            
        Returns:
            dict: Emotion summary with percentages
        """
        all_emotions = []
        
        # Collect emotions from all images
        for image_path in image_paths:
            emotions = self.detect_emotions_in_image(image_path)
            all_emotions.extend(emotions)
        
        if not all_emotions:
            logger.warning("No emotions detected")
            return {}
        
        # Calculate percentages
        emotion_counts = Counter(all_emotions)
        total_faces = len(all_emotions)
        
        emotion_summary = {}
        for emotion, count in emotion_counts.items():
            percentage = round((count / total_faces) * 100, 1)
            emotion_summary[emotion.capitalize()] = percentage
        
        # Sort by percentage (descending)
        emotion_summary = dict(sorted(
            emotion_summary.items(),
            key=lambda x: x[1],
            reverse=True
        ))
        
        logger.info(f"Emotion analysis complete: {emotion_summary}")
        return emotion_summary
    
    def get_dominant_emotion(self, emotion_summary):
        """
        Get the most dominant emotion
        
        Args:
            emotion_summary: Emotion summary dict
            
        Returns:
            str: Dominant emotion name
        """
        if not emotion_summary:
            return "Unknown"
        
        return max(emotion_summary, key=emotion_summary.get)
    
    def get_class_mood(self, emotion_summary):
        """
        Determine overall class mood
        
        Args:
            emotion_summary: Emotion summary dict
            
        Returns:
            str: Class mood description
        """
        if not emotion_summary:
            return "Unable to determine"
        
        # Define mood categories
        positive_emotions = ['happy', 'surprise']
        neutral_emotions = ['neutral']
        negative_emotions = ['sad', 'angry', 'fear', 'disgust']
        
        # Calculate percentages
        positive_pct = sum(emotion_summary.get(e.capitalize(), 0) for e in positive_emotions)
        neutral_pct = sum(emotion_summary.get(e.capitalize(), 0) for e in neutral_emotions)
        negative_pct = sum(emotion_summary.get(e.capitalize(), 0) for e in negative_emotions)
        
        # Determine mood
        if positive_pct >= 50:
            return "Positive - Students are engaged and happy"
        elif neutral_pct >= 60:
            return "Neutral - Students are attentive"
        elif negative_pct >= 40:
            return "Needs Attention - Students may be struggling"
        else:
            return "Mixed - Varied emotional responses"
    
    def format_emotion_summary(self, emotion_summary):
        """
        Format emotion summary for display
        
        Args:
            emotion_summary: Emotion summary dict
            
        Returns:
            str: Formatted string
        """
        if not emotion_summary:
            return "No emotions detected"
        
        lines = []
        for emotion, percentage in emotion_summary.items():
            bar = "█" * int(percentage / 5)  # Visual bar
            lines.append(f"{emotion:10} {percentage:5.1f}% {bar}")
        
        return "\n".join(lines)