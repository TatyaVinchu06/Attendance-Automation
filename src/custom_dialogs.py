#!/usr/bin/env python3
"""
Custom Dialog Boxes Module
Modern dark-themed dialogs that match the app's UI
"""

import customtkinter as ctk
from tkinter import messagebox
from config import THEME_COLORS


class CustomDialog(ctk.CTkToplevel):
    """Base class for custom dialogs"""
    
    def __init__(self, parent, title, message, dialog_type="info", buttons=None):
        super().__init__(parent)
        
        self.result = None
        self.title(title)
        self.geometry("480x200")
        self.resizable(False, False)
        
        # Center on parent
        if parent:
            self.transient(parent)
            x = parent.winfo_x() + (parent.winfo_width() // 2) - 240
            y = parent.winfo_y() + (parent.winfo_height() // 2) - 100
            self.geometry(f"+{x}+{y}")
        
        # Main container
        container = ctk.CTkFrame(self, fg_color=THEME_COLORS['background'])
        container.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Icon and message area
        content_frame = ctk.CTkFrame(container, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Icon
        icon_map = {
            "info": "ℹ️",
            "success": "✅",
            "warning": "⚠️",
            "error": "❌",
            "question": "❓"
        }
        icon = icon_map.get(dialog_type, "ℹ️")
        
        icon_label = ctk.CTkLabel(
            content_frame,
            text=icon,
            font=ctk.CTkFont(size=40),
            width=60
        )
        icon_label.pack(side="left", padx=(0, 20))
        
        # Message
        msg_label = ctk.CTkLabel(
            content_frame,
            text=message,
            font=ctk.CTkFont(size=13),
            wraplength=350,
            justify="left"
        )
        msg_label.pack(side="left", fill="both", expand=True)
        
        # Buttons
        button_frame = ctk.CTkFrame(container, fg_color="transparent")
        button_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        if not buttons:
            buttons = [("OK", True)]
        
        for btn_text, btn_value in reversed(buttons):
            btn_color = THEME_COLORS['primary'] if btn_value else THEME_COLORS['surface']
            btn = ctk.CTkButton(
                button_frame,
                text=btn_text,
                width=100,
                height=35,
                fg_color=btn_color,
                command=lambda v=btn_value: self._on_button_click(v)
            )
            btn.pack(side="right", padx=5)
        
        # Make modal
        self.grab_set()
        self.focus_set()
        
        # Bind escape to close
        self.bind("<Escape>", lambda e: self._on_button_click(False))
    
    def _on_button_click(self, value):
        """Handle button click"""
        self.result = value
        self.grab_release()
        self.destroy()
    
    def get_result(self):
        """Wait for dialog and return result"""
        self.wait_window()
        return self.result


def showinfo(title, message, parent=None):
    """Show info dialog"""
    dialog = CustomDialog(parent, title, message, "info", [("OK", True)])
    dialog.get_result()


def showsuccess(title, message, parent=None):
    """Show success dialog"""
    dialog = CustomDialog(parent, title, message, "success", [("OK", True)])
    dialog.get_result()


def showwarning(title, message, parent=None):
    """Show warning dialog"""
    dialog = CustomDialog(parent, title, message, "warning", [("OK", True)])
    dialog.get_result()


def showerror(title, message, parent=None):
    """Show error dialog"""
    dialog = CustomDialog(parent, title, message, "error", [("OK", True)])
    dialog.get_result()


def askyesno(title, message, parent=None):
    """Ask yes/no question"""
    dialog = CustomDialog(parent, title, message, "question", [("No", False), ("Yes", True)])
    return dialog.get_result() or False


def askokcancel(title, message, parent=None):
    """Ask OK/Cancel question"""
    dialog = CustomDialog(parent, title, message, "question", [("Cancel", False), ("OK", True)])
    return dialog.get_result() or False
