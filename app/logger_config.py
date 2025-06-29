import logging
import os
from datetime import datetime
from .config import config

def setup_logging():
    """Setup logging configuration with file and console handlers."""
    logging_config = config.get_logging_config()
    
    # Create logs directory if it doesn't exist
    log_path = logging_config.get('file', {}).get('path', 'logs')
    os.makedirs(log_path, exist_ok=True)
    
    # Create logger
    logger = logging.getLogger('inmemory_db')
    logger.setLevel(getattr(logging, logging_config.get('level', 'INFO')))
    
    # Prevent duplicate handlers
    if logger.handlers:
        return logger
    
    # Create formatters
    file_formatter = logging.Formatter(
        logging_config.get('format', {}).get('file', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    )
    console_formatter = logging.Formatter(
        logging_config.get('format', {}).get('console', '%(levelname)s: %(message)s')
    )
    
    # File handler - daily rotation
    if logging_config.get('file', {}).get('enabled', True):
        today = datetime.now().strftime('%Y-%m-%d')
        filename_pattern = logging_config.get('file', {}).get('filename_pattern', 'db_{date}.log')
        filename = filename_pattern.format(date=today)
        file_path = os.path.join(log_path, filename)
        
        file_handler = logging.FileHandler(file_path)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    # Console handler
    if logging_config.get('console', {}).get('enabled', True):
        console_handler = logging.StreamHandler()
        console_level = logging_config.get('console', {}).get('level', 'INFO')
        console_handler.setLevel(getattr(logging, console_level))
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
    
    return logger

logger = setup_logging() 