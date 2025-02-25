"""
Utilities for file and directory handling
"""

import os
import shutil
from typing import List, Optional
import logging

logger = logging.getLogger('devtooling')

def ensure_directory(path: str) -> None:
    """Ensures that a directory exists, creates it if not."""
    try:
        os.makedirs(path, exist_ok=True)
        logger.debug(f"Directory ensured: {path}")
    except Exception as e:
        logger.error(f"Error creating directory {path}: {str(e)}")
        raise

def list_files(
    path: str,
    ignore_patterns: Optional[List[str]] = None,
    recursive: bool = False
) -> List[str]:
    """Lists files in a directory with filters."""
    try:
        files = []
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            
            # Verify patterns to ignore
            if ignore_patterns and any(p in item for p in ignore_patterns):
                continue
                
            if os.path.isfile(item_path):
                files.append(item_path)
            elif recursive and os.path.isdir(item_path):
                files.extend(list_files(item_path, ignore_patterns, recursive))
                
        return files
    except Exception as e:
        logger.error(f"Error listing files in {path}: {str(e)}")
        raise

def get_file_size(path: str) -> int:
    """Gets the size of a file or directory."""
    try:
        if os.path.isfile(path):
            return os.path.getsize(path)
        elif os.path.isdir(path):
            total_size = 0
            for dirpath, _, filenames in os.walk(path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    total_size += os.path.getsize(fp)
            return total_size
    except Exception as e:
        logger.error(f"Error getting size of {path}: {str(e)}")
        raise