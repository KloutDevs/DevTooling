import logging
import os
from datetime import datetime
from rich.logging import RichHandler
from typing import Optional

class Logger:
    _instance: Optional['Logger'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'logger'):
            self.setup_logger()
    
    def setup_logger(self):
        # Create logs directory if not exists
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Configure logger
        self.logger = logging.getLogger('devtooling')
        self.logger.setLevel(logging.DEBUG)
        
        # Avoid duplicate handlers
        if self.logger.handlers:
            return
        
        # Console handler using Rich
        console_handler = RichHandler(
            rich_tracebacks=True,
            markup=True,
            show_time=False
        )
        console_handler.setLevel(logging.INFO)
        
        # File handler
        log_file = os.path.join(log_dir, f'devtooling_{datetime.now().strftime("%Y%m%d")}.log')
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        # Format for logs
        file_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_format)
        
        # Add handlers
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
    
    @classmethod
    def get_logger(cls):
        if cls._instance is None:
            cls()
        return cls._instance.logger

def setup_logging():
    return Logger.get_logger()