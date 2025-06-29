from typing import Protocol
from .logger_config import logger

class Logger(Protocol):
    """Abstract interface for logging operations."""
    
    def info(self, message: str) -> None:
        """Log an info message."""
        ...
    
    def warning(self, message: str) -> None:
        """Log a warning message."""
        ...
    
    def error(self, message: str) -> None:
        """Log an error message."""
        ...
    
    def debug(self, message: str) -> None:
        """Log a debug message."""
        ...

class ConsoleLogger:
    """Simple console logger implementation."""
    
    def info(self, message: str) -> None:
        print(f"[INFO] {message}")
    
    def warning(self, message: str) -> None:
        print(f"[WARNING] {message}")
    
    def error(self, message: str) -> None:
        print(f"[ERROR] {message}")
    
    def debug(self, message: str) -> None:
        print(f"[DEBUG] {message}")

class FileLogger:
    """File-based logger implementation using the existing logger."""
    
    def info(self, message: str) -> None:
        logger.info(message)
    
    def warning(self, message: str) -> None:
        logger.warning(message)
    
    def error(self, message: str) -> None:
        logger.error(message)
    
    def debug(self, message: str) -> None:
        logger.debug(message)

class CompositeLogger:
    """Logger that writes to both console and file."""
    
    def __init__(self, console_logger: Logger, file_logger: Logger):
        self.console_logger = console_logger
        self.file_logger = file_logger
    
    def info(self, message: str) -> None:
        self.console_logger.info(message)
        self.file_logger.info(message)
    
    def warning(self, message: str) -> None:
        self.console_logger.warning(message)
        self.file_logger.warning(message)
    
    def error(self, message: str) -> None:
        self.console_logger.error(message)
        self.file_logger.error(message)
    
    def debug(self, message: str) -> None:
        self.console_logger.debug(message)
        self.file_logger.debug(message)

class NullLogger:
    """Logger-заглушка для тестов: не выводит ничего."""
    def info(self, message: str) -> None:
        pass
    def warning(self, message: str) -> None:
        pass
    def error(self, message: str) -> None:
        pass
    def debug(self, message: str) -> None:
        pass 