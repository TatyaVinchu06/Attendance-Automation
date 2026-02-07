#!/usr/bin/env python3
"""
Data Cleanup Module
Handles automatic cleanup of old files (7-day retention policy)
"""

import os
from datetime import datetime, timedelta
import logging
from config import *

logger = logging.getLogger(__name__)


class DataCleanup:
    """Data cleanup and retention management"""
    
    def __init__(self, retention_days=DATA_RETENTION_DAYS):
        self.retention_days = retention_days
        self.cleanup_dirs = CLEANUP_DIRECTORIES
    
    def get_directory_stats(self, directory):
        """
        Get statistics for a directory
        
        Args:
            directory: Path to directory
            
        Returns:
            dict: Directory statistics
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
            cutoff_date = datetime.now() - timedelta(days=self.retention_days)
            
            for filename in os.listdir(directory):
                filepath = os.path.join(directory, filename)
                
                if os.path.isfile(filepath):
                    file_size = os.path.getsize(filepath)
                    file_modified = datetime.fromtimestamp(os.path.getmtime(filepath))
                    
                    stats['total_files'] += 1
                    stats['total_size_bytes'] += file_size
                    
                    if file_modified < cutoff_date:
                        stats['old_files'] += 1
                        stats['old_files_size_bytes'] += file_size
            
            # Convert to MB
            stats['total_size_mb'] = round(stats['total_size_bytes'] / (1024 * 1024), 2)
            stats['old_files_size_mb'] = round(stats['old_files_size_bytes'] / (1024 * 1024), 2)
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting directory stats: {e}")
            return stats
    
    def preview_cleanup(self):
        """
        Preview what files will be deleted
        
        Returns:
            dict: Cleanup preview information
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
        Cleanup old files in a directory
        
        Args:
            directory: Path to directory
            
        Returns:
            dict: Cleanup results
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
                        
                        # Check if file is older than retention period
                        if file_modified < cutoff_date:
                            file_size = os.path.getsize(filepath)
                            os.remove(filepath)
                            
                            result['files_deleted'] += 1
                            result['size_freed_bytes'] += file_size
                            
                            logger.info(f"Deleted: {filename}")
                    
                    except Exception as e:
                        error_msg = f"Error deleting {filename}: {e}"
                        result['errors'].append(error_msg)
                        logger.error(error_msg)
            
            result['size_freed_mb'] = round(result['size_freed_bytes'] / (1024 * 1024), 2)
            
            return result
            
        except Exception as e:
            logger.error(f"Error cleaning directory {directory}: {e}")
            result['errors'].append(str(e))
            return result
    
    def cleanup_all(self):
        """
        Cleanup all configured directories
        
        Returns:
            dict: Overall cleanup summary
        """
        summary = {
            'total_files_deleted': 0,
            'total_size_freed_mb': 0,
            'directories': {},
            'errors': []
        }
        
        for directory in self.cleanup_dirs:
            if not os.path.exists(directory):
                logger.warning(f"Directory does not exist: {directory}")
                continue
            
            logger.info(f"Cleaning directory: {directory}")
            result = self.cleanup_directory(directory)
            
            dir_name = os.path.basename(directory)
            summary['directories'][dir_name] = result
            summary['total_files_deleted'] += result['files_deleted']
            summary['total_size_freed_mb'] += result['size_freed_mb']
            summary['errors'].extend(result['errors'])
        
        summary['total_size_freed_mb'] = round(summary['total_size_freed_mb'], 2)
        
        logger.info(f"Cleanup complete: {summary['total_files_deleted']} files deleted, " +
                   f"{summary['total_size_freed_mb']} MB freed")
        
        return summary
    
    def schedule_cleanup(self):
        """Setup scheduled cleanup (runs daily)"""
        import schedule
        
        def cleanup_job():
            logger.info("Running scheduled cleanup")
            summary = self.cleanup_all()
            logger.info(f"Scheduled cleanup: {summary['total_files_deleted']} files deleted")
        
        # Schedule cleanup at 2 AM daily
        schedule.every().day.at("02:00").do(cleanup_job)
        
        logger.info("Cleanup scheduled for 2:00 AM daily")
        
        return schedule