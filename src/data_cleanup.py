#!/usr/bin/env python3
"""
Data Cleanup Module
Purana data udate hai (7 din ki retention policy hai)
"""

import os
from datetime import datetime, timedelta
import logging
from config import *

logger = logging.getLogger(__name__)


class DataCleanup:
    """Faltu data saaf karne wali class"""
    
    def __init__(self, retention_days=DATA_RETENTION_DAYS):
        self.retention_days = retention_days
        self.cleanup_dirs = CLEANUP_DIRECTORIES
    
    def get_directory_stats(self, directory):
        """
        Directory ka hisaab-kitaab nikalte hai
        """
        stats = {
            'total_files': 0,
            'total_size_bytes': 0,
            'total_size_mb': 0,
            'old_files': 0,
            'old_files_size_bytes': 0,
            'old_files_size_mb': 0
        }
        
        try:
            # Retention period se pehle ki date nikalte hai
            cutoff_date = datetime.now() - timedelta(days=self.retention_days)
            
            for filename in os.listdir(directory):
                filepath = os.path.join(directory, filename)
                
                if os.path.isfile(filepath):
                    file_size = os.path.getsize(filepath)
                    file_modified = datetime.fromtimestamp(os.path.getmtime(filepath))
                    
                    stats['total_files'] += 1
                    stats['total_size_bytes'] += file_size
                    
                    # Agar purana hai
                    if file_modified < cutoff_date:
                        stats['old_files'] += 1
                        stats['old_files_size_bytes'] += file_size
            
            # MB me convert karte hai
            stats['total_size_mb'] = round(stats['total_size_bytes'] / (1024 * 1024), 2)
            stats['old_files_size_mb'] = round(stats['old_files_size_bytes'] / (1024 * 1024), 2)
            
            return stats
            
        except Exception as e:
            logger.error(f"Stats lene me error: {e}")
            return stats
    
    def preview_cleanup(self):
        """
        Dekhte hai kya kya udne wala hai
        """
        preview = {
            'total_files_to_delete': 0,
            'total_size_to_free_mb': 0,
            'directories': {}
        }
        
        for directory in self.cleanup_dirs:
            if not os.path.exists(directory):
                continue
            
            stats = self.get_directory_stats(directory)
            preview['directories'][os.path.basename(directory)] = stats
            preview['total_files_to_delete'] += stats['old_files']
            preview['total_size_to_free_mb'] += stats['old_files_size_mb']
        
        preview['total_size_to_free_mb'] = round(preview['total_size_to_free_mb'], 2)
        
        return preview
    
    def cleanup_directory(self, directory):
        """
        Directory saaf karte hai
        """
        result = {
            'files_deleted': 0,
            'size_freed_bytes': 0,
            'size_freed_mb': 0,
            'errors': []
        }
        
        try:
            cutoff_date = datetime.now() - timedelta(days=self.retention_days)
            
            for filename in os.listdir(directory):
                filepath = os.path.join(directory, filename)
                
                if os.path.isfile(filepath):
                    try:
                        file_modified = datetime.fromtimestamp(os.path.getmtime(filepath))
                        
                        # Agar retention period se purana hai
                        if file_modified < cutoff_date:
                            file_size = os.path.getsize(filepath)
                            os.remove(filepath)
                            
                            result['files_deleted'] += 1
                            result['size_freed_bytes'] += file_size
                            
                            logger.info(f"Uda diya: {filename}")
                    
                    except Exception as e:
                        error_msg = f"{filename} delete nahi hua: {e}"
                        result['errors'].append(error_msg)
                        logger.error(error_msg)
            
            result['size_freed_mb'] = round(result['size_freed_bytes'] / (1024 * 1024), 2)
            
            return result
            
        except Exception as e:
            logger.error(f"{directory} saaf karne me error: {e}")
            result['errors'].append(str(e))
            return result
    
    def cleanup_all(self):
        """
        Sab kuch saaf karte hai (jo config me hai)
        """
        summary = {
            'total_files_deleted': 0,
            'total_size_freed_mb': 0,
            'directories': {},
            'errors': []
        }
        
        for directory in self.cleanup_dirs:
            if not os.path.exists(directory):
                logger.warning(f"Directory nahi mili: {directory}")
                continue
            
            logger.info(f"Safai chalu: {directory}")
            result = self.cleanup_directory(directory)
            
            dir_name = os.path.basename(directory)
            summary['directories'][dir_name] = result
            summary['total_files_deleted'] += result['files_deleted']
            summary['total_size_freed_mb'] += result['size_freed_mb']
            summary['errors'].extend(result['errors'])
        
        summary['total_size_freed_mb'] = round(summary['total_size_freed_mb'], 2)
        
        logger.info(f"Safai abhiyan khatam: {summary['total_files_deleted']} files gayi, " +
                   f"{summary['total_size_freed_mb']} MB khali hua")
        
        return summary
    
    def schedule_cleanup(self):
        """Roz raat ko safai schedule karte hai"""
        import schedule
        
        def cleanup_job():
            logger.info("Scheduled safai shuru...")
            summary = self.cleanup_all()
            logger.info(f"Scheduled safai: {summary['total_files_deleted']} files udi")
        
        # Subah 2 baje
        schedule.every().day.at("02:00").do(cleanup_job)
        
        logger.info("Raat ko 2 baje safai hogi")
        
        return schedule