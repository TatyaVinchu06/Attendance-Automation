#!/usr/bin/env python3
"""
Email Automation Module
Attendance ki report email karte hai
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import logging
from datetime import datetime
from config import *

logger = logging.getLogger(__name__)


class EmailAutomation:
    """Email bhejne ke liye class"""
    
    def __init__(self, settings_manager=None):
        self.smtp_server = SMTP_SERVER
        self.smtp_port = SMTP_PORT
        self.settings_manager = settings_manager
        
        # Settings se load karte hai agar hai toh
        if settings_manager:
            self.sender_email = settings_manager.get("sender_email") or SENDER_EMAIL
            self.sender_password = settings_manager.get("sender_password") or SENDER_PASSWORD
        else:
            self.sender_email = SENDER_EMAIL
            self.sender_password = SENDER_PASSWORD
    
    def test_email_connection(self):
        """Check karte hai email connect ho raha hai kya"""
        try:
            # Server se connect karte hai
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.quit()
            
            logger.info("Email connection mast chal raha hai")
            return True
            
        except Exception as e:
            logger.error(f"Email connect nahi hua: {e}")
            return False
    
    def update_credentials(self, email, password):
        """Runtime pe email/password change karte hai"""
        self.sender_email = email
        self.sender_password = password
        
        # Save bhi kar lete hai future ke liye
        if self.settings_manager:
            self.settings_manager.set("sender_email", email)
            self.settings_manager.set("sender_password", password)
            logger.info("Email credentials update ho gaye")
        else:
            logger.info("Bas abhi ke liye change kiya hai")

    def is_configured(self):
        """Email set hai ya nahi?"""
        return (self.sender_email != "your.email@gmail.com" and 
                self.sender_password != "your_app_password")

    def send_attendance_report(self, subject, report_files, recipient_email=None):
        """
        Attendance ki report email karte hai
        """
        if not EMAIL_ENABLED:
            logger.info("Email band hai abhi")
            return False
        
        if not self.is_configured():
            logger.error("Email configure nahi kiya hai")
            return False
        
        try:
            # Kisko bhejna hai?
            if recipient_email is None:
                # Timetable se nikalte hai
                recipient_email = get_faculty_email(subject)
            
            # Content ready karte hai
            date_str = datetime.now().strftime("%Y-%m-%d")
            
            # Message banate hai
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = recipient_email
            msg['Subject'] = EMAIL_SUBJECT_TEMPLATE.format(
                subject=subject,
                date=date_str
            )
            
            # Body (Thoda formal hi rakhte hai email me)
            body = f"""
Dear Faculty,

Please find attached the attendance report for {subject} on {date_str}.

This is an automated email from the Smart System by Om Bhamare.

Best regards,
Smart System
"""
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Report attach karte hai
            # Report attach karte hai (list ho ya string)
            if isinstance(report_files, str):
                report_files = [report_files]

            for report_file in report_files:
                if report_file and os.path.exists(report_file):
                    with open(report_file, 'rb') as f:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(f.read())
                        encoders.encode_base64(part)
                        part.add_header(
                            'Content-Disposition',
                            f'attachment; filename= {os.path.basename(report_file)}'
                        )
                        msg.attach(part)
                        logger.debug(f"Attach kiya: {os.path.basename(report_file)}")
            
            # Bhejte hai
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.send_message(msg)
            server.quit()
            
            logger.info(f"Email bhej diya {recipient_email} ko")
            return True
            
        except Exception as e:
            logger.error(f"Email bhejne me error: {e}")
            return False
    
    def send_custom_email(self, recipient_email, subject_line, body, attachments=None):
        """
        Custom email bhejne ke liye
        """
        if not self.is_configured():
            logger.error("Email configure nahi hai")
            return False
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject_line
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Attachments
            if attachments:
                for filepath in attachments:
                    if os.path.exists(filepath):
                        with open(filepath, 'rb') as f:
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(f.read())
                            encoders.encode_base64(part)
                            part.add_header(
                                'Content-Disposition',
                                f'attachment; filename= {os.path.basename(filepath)}'
                            )
                            msg.attach(part)
            
            # Send
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.send_message(msg)
            server.quit()
            
            logger.info(f"Custom email gaya {recipient_email} ko")
            return True
            
        except Exception as e:
            logger.error(f"Custom email error: {e}")
            return False