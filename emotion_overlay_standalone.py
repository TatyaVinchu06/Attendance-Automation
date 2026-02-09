#!/usr/bin/env python3
"""
Standalone Emotion Overlay Launcher
Sirf emotion overlay run karne ke liye
"""

import sys
import tkinter as tk
from tkinter import messagebox
import logging

# Local imports
from image_capture import ImageCapture
from realtime_emotion_monitor import RealtimeEmotionMonitor
from emotion_overlay import EmotionOverlay
from config import *

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main execution function"""
    logger.info("Emotion Overlay Standalone Mode shuru ho raha hai...")
    
    # Root window (hidden)
    root = tk.Tk()
    root.withdraw()  # Chhupate hai
    
    try:
        # Camera initialize karte hai
        logger.info("Camera initialize kar rahe hai...")
        camera_capture = ImageCapture()
        
        if not camera_capture.initialize_camera():
            messagebox.showerror(
                "Camera Error",
                "Camera nahi khula bhai. Check karo camera connected hai aur kisi aur app me use nahi ho raha."
            )
            return
        
        # Monitor initialize karte hai
        logger.info("Emotion monitor setup kar rahe hai...")
        emotion_monitor = RealtimeEmotionMonitor(camera_instance=camera_capture.camera)
        
        # Overlay banate hai
        logger.info("Overlay window bana rahe hai...")
        overlay = EmotionOverlay(emotion_monitor)
        overlay.create_window()
        
        # Monitoring chalu karte hai
        logger.info("Real-time monitoring chalu kar rahe hai...")
        if not emotion_monitor.start_monitoring():
            messagebox.showerror(
                "Monitor Error",
                "Emotion monitoring chalu nahi hui. Logs check karo."
            )
            return
        
        logger.info("Sab set hai! Overlay chal raha hai.")
        
        # Cleanup function
        def on_closing():
            logger.info("Cleanup kar rahe hai...")
            emotion_monitor.stop_monitoring()
            camera_capture.release_camera()
            overlay.destroy_window()
            root.quit()
        
        # Bind close event
        if overlay.window:
            overlay.window.protocol("WM_DELETE_WINDOW", on_closing)
        
        # Main loop
        root.mainloop()
        
    except KeyboardInterrupt:
        logger.info("Ctrl+C se band kiya gaya")
    except Exception as e:
        logger.error(f"Error aaya: {e}", exc_info=True)
        messagebox.showerror("Error", f"Kuch galat ho gaya:\n{str(e)}")
    finally:
        # Cleanup
        try:
            if 'emotion_monitor' in locals():
                emotion_monitor.stop_monitoring()
            if 'camera_capture' in locals():
                camera_capture.release_camera()
        except:
            pass


if __name__ == "__main__":
    main()
