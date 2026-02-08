import json
import os
import logging

SETTINGS_FILE = 'settings.json'

DEFAULT_SETTINGS = {
    "analysis_interval": 30,  # Minutes
    "attendance_interval": 60, # Minutes
    "email_enabled": True,
    "theme": "Dark",
    "faculty_emails": {},
    "sender_email": "",
    "sender_password": ""
}

class SettingsManager:
    """Settings sambhalne wala class"""
    
    def __init__(self):
        self.settings = DEFAULT_SETTINGS.copy()
        self.load_settings()

    def load_settings(self):
        """JSON file se settings uthate hai"""
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, 'r') as f:
                    data = json.load(f)
                    self.settings.update(data)
            except Exception as e:
                logging.error(f"Settings load nahi hui: {e}")

    def save_settings(self):
        """Settings ko JSON me save karte hai"""
        try:
            with open(SETTINGS_FILE, 'w') as f:
                json.dump(self.settings, f, indent=4)
        except Exception as e:
            logging.error(f"Settings save nahi hui: {e}")

    def get(self, key):
        """Value nikalo"""
        return self.settings.get(key, DEFAULT_SETTINGS.get(key))

    def set(self, key, value):
        """Value set karo aur save bhi karo"""
        self.settings[key] = value
        self.save_settings()
