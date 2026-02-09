#!/usr/bin/env python3
"""
Emotion Overlay Window
Always-on-top floating window for real-time emotions
"""

import tkinter as tk
from tkinter import ttk
import logging
from config import *

logger = logging.getLogger(__name__)


class EmotionOverlay:
    """Floating overlay window jo emotions dikhata hai"""
    
    def __init__(self, emotion_monitor):
        self.monitor = emotion_monitor
        self.window = None
        self.is_visible = False
        self.update_job = None
        
        # Drag functionality ke liye
        self.drag_start_x = 0
        self.drag_start_y = 0
        
    def create_window(self):
        """Overlay window banate hai"""
        if self.window is not None:
            logger.warning("Window pehle se hai")
            return
        
        # Main window
        self.window = tk.Toplevel()
        self.window.title("Class Mood Monitor")
        self.window.geometry("220x200+100+100")  # Width x Height + X + Y
        
        # Always on top
        self.window.wm_attributes('-topmost', True)
        
        # Transparency
        self.window.attributes('-alpha', OVERLAY_TRANSPARENCY)
        
        # Dark theme colors
        bg_color = "#1a1a2e"
        fg_color = "#eee"
        accent_color = "#16213e"
        
        self.window.configure(bg=bg_color)
        
        # Title bar (custom - draggable)
        title_frame = tk.Frame(self.window, bg=accent_color, cursor="fleur")
        title_frame.pack(fill=tk.X, padx=2, pady=2)
        
        title_label = tk.Label(
            title_frame,
            text="📊 Class Mood",
            bg=accent_color,
            fg=fg_color,
            font=("Segoe UI", 10, "bold"),
            pady=4
        )
        title_label.pack()
        
        # Bind karte hai dragging events
        title_frame.bind('<Button-1>', self._start_drag)
        title_frame.bind('<B1-Motion>', self._on_drag)
        title_label.bind('<Button-1>', self._start_drag)
        title_label.bind('<B1-Motion>', self._on_drag)
        
        # Separator
        separator1 = tk.Frame(self.window, bg="#444", height=2)
        separator1.pack(fill=tk.X, padx=10, pady=2)
        
        # Emotions display frame
        self.emotions_frame = tk.Frame(self.window, bg=bg_color)
        self.emotions_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Placeholder label
        self.emotion_labels = []
        for i in range(4):  # Top 4 emotions
            label = tk.Label(
                self.emotions_frame,
                text="",
                bg=bg_color,
                fg=fg_color,
                font=("Segoe UI", 9),
                anchor='w'
            )
            label.pack(fill=tk.X, pady=2)
            self.emotion_labels.append(label)
        
        # Separator
        separator2 = tk.Frame(self.window, bg="#444", height=2)
        separator2.pack(fill=tk.X, padx=10, pady=2)
        
        # Face count
        self.face_count_label = tk.Label(
            self.window,
            text="👥 Faces: 0",
            bg=bg_color,
            fg=fg_color,
            font=("Segoe UI", 9),
            pady=3
        )
        self.face_count_label.pack()
        
        # Insight text
        self.insight_label = tk.Label(
            self.window,
            text="",
            bg=bg_color,
            fg="#aaf",
            font=("Segoe UI", 8, "italic"),
            wraplength=180,
            pady=2
        )
        self.insight_label.pack()
        
        # Right-click menu
        self._create_context_menu()
        
        # Close protocol
        self.window.protocol("WM_DELETE_WINDOW", self.hide_window)
        
        self.is_visible = True
        logger.info("Overlay window ban gaya")
        
        # Updates chalu karte hai
        self._schedule_update()
    
    def _create_context_menu(self):
        """Right-click menu banate hai"""
        self.context_menu = tk.Menu(self.window, tearoff=0)
        self.context_menu.add_command(label="Pause", command=self._toggle_pause)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Close", command=self.hide_window)
        
        self.window.bind('<Button-3>', self._show_context_menu)
    
    def _show_context_menu(self, event):
        """Context menu dikhate hai"""
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()
    
    def _toggle_pause(self):
        """Monitoring pause/resume karte hai"""
        if self.monitor.is_monitoring():
            self.monitor.stop_monitoring()
            logger.info("Monitoring paused")
        else:
            self.monitor.start_monitoring()
            logger.info("Monitoring resumed")
    
    def _start_drag(self, event):
        """Drag start karte hai"""
        self.drag_start_x = event.x
        self.drag_start_y = event.y
    
    def _on_drag(self, event):
        """Window drag karte hai"""
        x = self.window.winfo_x() + (event.x - self.drag_start_x)
        y = self.window.winfo_y() + (event.y - self.drag_start_y)
        self.window.geometry(f"+{x}+{y}")
    
    def _schedule_update(self):
        """Regular updates schedule karte hai"""
        if self.window and self.is_visible:
            self.update_display()
            # Next update
            self.update_job = self.window.after(2000, self._schedule_update)
    
    def update_display(self):
        """Emotion data ko UI me update karte hai"""
        try:
            # Monitor se latest data lete hai
            summary = self.monitor.get_emotion_summary()
            
            emotions = summary.get('emotions', {})
            face_count = summary.get('face_count', 0)
            insight = summary.get('insight', '')
            
            # Emotions display karte hai (top 4)
            emotion_items = list(emotions.items())[:4]
            
            for i, label in enumerate(self.emotion_labels):
                if i < len(emotion_items):
                    emotion, percentage = emotion_items[i]
                    emoji = self.monitor.get_emoji(emotion)
                    
                    # Color decide karte hai
                    color = self._get_emotion_color(emotion)
                    
                    label.config(
                        text=f"{emoji} {emotion.capitalize():8} {percentage:5.1f}%",
                        fg=color
                    )
                else:
                    label.config(text="")
            
            # Face count update
            self.face_count_label.config(text=f"👥 Faces: {face_count}")
            
            # Insight update
            self.insight_label.config(text=insight if insight else "Analyzing...")
            
        except Exception as e:
            logger.error(f"Display update me error: {e}")
    
    def _get_emotion_color(self, emotion):
        """Emotion ke liye color return karte hai"""
        positive = ['happy', 'surprise']
        neutral = ['neutral']
        negative = ['sad', 'angry', 'fear', 'disgust']
        
        if emotion in positive:
            return "#4ade80"  # Green
        elif emotion in neutral:
            return "#fbbf24"  # Yellow
        elif emotion in negative:
            return "#f87171"  # Red
        else:
            return "#d1d5db"  # Gray
    
    def show_window(self):
        """Window dikhate hai"""
        if self.window is None:
            self.create_window()
        else:
            self.window.deiconify()
            self.is_visible = True
            self._schedule_update()
    
    def hide_window(self):
        """Window chhupate hai"""
        if self.window:
            if self.update_job:
                self.window.after_cancel(self.update_job)
                self.update_job = None
            self.window.withdraw()
            self.is_visible = False
    
    def destroy_window(self):
        """Window completely destroy karte hai"""
        if self.window:
            if self.update_job:
                self.window.after_cancel(self.update_job)
            self.window.destroy()
            self.window = None
            self.is_visible = False
    
    def toggle_visibility(self):
        """Window show/hide toggle karte hai"""
        if self.is_visible:
            self.hide_window()
        else:
            self.show_window()
