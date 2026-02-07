#!/usr/bin/env python3
"""
Email Automation Module
Handles automated email sending with timetable integration
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
    """Email automation for attendance reports"""
    
    def __init__(self):
        self.smtp_server = SMTP_SERVER
        self.smtp_port = SMTP_PORT
        self.sender_email = SENDER_EMAIL
        self.sender_password = SENDER_PASSWORD
    
    def test_email_connection(self):
        """Test email configuration"""
        if not self.is_configured():
            logger.error("Email not configured properly")
            return False
        
        try:
            # Connect to server
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.quit()
            
            logger.info("Email configuration test successful")
            return True
            
        except Exception as e:
            logger.error(f"Email configuration test failed: {e}")
            return False
    
    def update_credentials(self, email, password):
        """Update sender credentials at runtime"""
        self.sender_email = email
        self.sender_password = password
        logger.info("Email credentials updated at runtime")

    def is_configured(self):
        """Check if email is configured"""
        return (self.sender_email != "your.email@gmail.com" and 
                self.sender_password != "your_app_password")

    def send_attendance_report(self, subject, report_files, recipient_email=None):
        """
        Send attendance report via email
        
        Args:
            subject: Subject name (e.g., "DBMS")
            report_files: List of report file paths to attach
            recipient_email: Optional recipient email (overrides timetable)
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not EMAIL_ENABLED:
            logger.info("Email sending is disabled")
            return False
        
        if not self.is_configured():
            logger.error("Email not configured")
            return False
        
        try:
            # Get recipient email
            if recipient_email is None:
                # Try to get from arguments first, then config (fallback)
                recipient_email = get_faculty_email(subject)
            
            # Prepare email content
            date_str = datetime.now().strftime("%Y-%m-%d")
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = recipient_email
            msg['Subject'] = EMAIL_SUBJECT_TEMPLATE.format(
                subject=subject,
                date=date_str
            )
            
            # Email body (will be populated from report data)
            body = f"""
Dear Faculty,

Please find attached the attendance report for {subject} on {date_str}.

This is an automated email from the Attendance System.

Best regards,
Attendance System
"""
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Attach report files
            for report_file in report_files:
                if os.path.exists(report_file):
                    with open(report_file, 'rb') as f:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(f.read())
                        encoders.encode_base64(part)
                        part.add_header(
                            'Content-Disposition',
                            f'attachment; filename= {os.path.basename(report_file)}'
                        )
                        msg.attach(part)
                        logger.debug(f"Attached: {os.path.basename(report_file)}")
            
            # Send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.send_message(msg)
            server.quit()
            
            logger.info(f"Email sent to {recipient_email}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return False
    
    def send_custom_email(self, recipient_email, subject_line, body, attachments=None):
        """
        Send custom email
        
        Args:
            recipient_email: Recipient email address
            subject_line: Email subject
            body: Email body text
            attachments: Optional list of file paths to attach
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not is_email_configured():
            logger.error("Email not configured")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject_line
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Attach files
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
            
            # Send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.send_message(msg)
            server.quit()
            
            logger.info(f"Custom email sent to {recipient_email}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending custom email: {e}")
            return False