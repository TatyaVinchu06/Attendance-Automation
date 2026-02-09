#!/usr/bin/env python3
"""
Real-time Emotion Monitor
Live emotions track karta hai bina images save kiye
"""

import cv2
import numpy as np
import threading
import time
import logging
from collections import deque, Counter
from deepface import DeepFace
from config import *

logger = logging.getLogger(__name__)


class RealtimeEmotionMonitor:
    """Real-time emotion monitoring ke liye class"""
    
    def __init__(self, camera_instance=None):
        self.camera = camera_instance
        self.is_running = False
        self.current_emotions = {}
        self.emotion_history = deque(maxlen=EMOTION_SMOOTHING_FRAMES)
        self.face_count = 0
        self.last_update_time = time.time()
        self.lock = threading.Lock()
        self.monitor_thread = None
        
        # Emotion emojis
        self.emotion_emojis = {
            'happy': '😊',
            'neutral': '😐',
            'sad': '😢',
            'angry': '😠',
            'surprise': '😲',
            'fear': '😨',
            'disgust': '🤢'
        }
        
        # Teaching insights
        self.teaching_insights = {
            'happy': 'Mast chal raha hai!',
            'neutral': 'Students dhyan de rahe hai',
            'sad': 'Mood thoda low hai',
            'angry': 'Students frustrated lag rahe hai',
            'surprise': 'Kuch interesting hua!',
            'fear': 'Students tensed hai',
            'disgust': 'Boring lag raha hai'
        }
    
    def start_monitoring(self):
        """Monitoring chalu karte hai"""
        if self.is_running:
            logger.warning("Monitor pehle se chal raha hai")
            return False
        
        if self.camera is None:
            logger.error("Camera nahi mila")
            return False
        
        self.is_running = True
        self.monitor_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitor_thread.start()
        logger.info("Real-time emotion monitoring chalu ho gaya")
        return True
    
    def stop_monitoring(self):
        """Monitoring band karte hai"""
        self.is_running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2.0)
        logger.info("Emotion monitoring band ho gaya")
    
    def _monitoring_loop(self):
        """Main loop jo continuously emotions detect karta hai"""
        while self.is_running:
            try:
                # Check karte hai ki time ho gaya hai kya
                current_time = time.time()
                if current_time - self.last_update_time < REALTIME_EMOTION_INTERVAL:
                    time.sleep(0.1)
                    continue
                
                # Frame lete hai
                ret, frame = self.camera.read()
                if not ret or frame is None:
                    time.sleep(0.5)
                    continue
                
                # Emotions analyze karte hai
                emotions_data = self._analyze_frame(frame)
                
                # Update karte hai
                with self.lock:
                    self.emotion_history.append(emotions_data)
                    self.current_emotions = self._aggregate_emotions()
                    self.last_update_time = current_time
                
            except Exception as e:
                logger.error(f"Monitoring loop me error: {e}")
                time.sleep(1.0)
    
    def _analyze_frame(self, frame):
        """Ek frame me emotions nikalta hai (in-memory processing)"""
        emotions_list = []
        face_count = 0
        
        try:
            # Frame ko thoda chota karte hai speed ke liye
            small_frame = cv2.resize(frame, (320, 240))
            
            # DeepFace se analyze karte hai
            results = DeepFace.analyze(
                small_frame,
                actions=['emotion'],
                enforce_detection=False,
                detector_backend=EMOTION_BACKEND,
                silent=True
            )
            
            # Single face ya multiple faces
            if isinstance(results, dict):
                results = [results]
            
            # Har face ke liye
            for result in results:
                if 'emotion' in result:
                    emotion_scores = result['emotion']
                    dominant_emotion = max(emotion_scores, key=emotion_scores.get)
                    confidence = emotion_scores[dominant_emotion]
                    
                    # Confidence check karte hai
                    if confidence >= EMOTION_CONFIDENCE_THRESHOLD * 100:
                        emotions_list.append(dominant_emotion.lower())
                        face_count += 1
            
            logger.debug(f"{face_count} faces detect kiye, emotions: {emotions_list}")
            
        except Exception as e:
            logger.debug(f"Frame analysis me error (normal hai agar no face): {e}")
        
        return {
            'emotions': emotions_list,
            'face_count': face_count,
            'timestamp': time.time()
        }
    
    def _aggregate_emotions(self):
        """Multiple frames ka data combine karke final result nikalte hai"""
        if not self.emotion_history:
            return {'emotions': {}, 'face_count': 0, 'dominant': None, 'insight': ''}
        
        # Saare emotions collect karte hai
        all_emotions = []
        total_faces = 0
        
        for data in self.emotion_history:
            all_emotions.extend(data['emotions'])
            total_faces = max(total_faces, data['face_count'])
        
        if not all_emotions:
            return {'emotions': {}, 'face_count': 0, 'dominant': None, 'insight': ''}
        
        # Percentages nikalte hai
        emotion_counts = Counter(all_emotions)
        total_count = len(all_emotions)
        
        emotion_percentages = {}
        for emotion, count in emotion_counts.items():
            percentage = round((count / total_count) * 100, 1)
            emotion_percentages[emotion] = percentage
        
        # Sort karte hai (high to low)
        emotion_percentages = dict(sorted(
            emotion_percentages.items(),
            key=lambda x: x[1],
            reverse=True
        ))
        
        # Dominant emotion
        dominant_emotion = list(emotion_percentages.keys())[0] if emotion_percentages else None
        insight = self.teaching_insights.get(dominant_emotion, '') if dominant_emotion else ''
        
        return {
            'emotions': emotion_percentages,
            'face_count': total_faces,
            'dominant': dominant_emotion,
            'insight': insight
        }
    
    def get_emotion_summary(self):
        """Current emotions ko safely return karte hai"""
        with self.lock:
            return self.current_emotions.copy()
    
    def get_emoji(self, emotion):
        """Emotion ka emoji return karte hai"""
        return self.emotion_emojis.get(emotion.lower(), '❓')
    
    def is_monitoring(self):
        """Check karte hai monitor chal raha hai kya"""
        return self.is_running
