from typing import Optional
from .base import BaseDB, Database
from .db import InMemoryDB
from .transaction_manager import TransactionManager
from .logger import Logger, FileLogger, ConsoleLogger, CompositeLogger
from .config import Config

class DatabaseFactory:
    """Factory for creating database instances with proper dependency injection."""
    
    @staticmethod
    def create_logger(config: Config) -> Logger:
        """Create a logger instance based on configuration.
        
        Args:
            config: Application configuration.
            
        Returns:
            Configured logger instance.
        """
        logger_type = config.get('logging.type', 'composite')
        
        if logger_type == 'console':
            return ConsoleLogger()
        elif logger_type == 'file':
            return FileLogger()
        elif logger_type == 'composite':
            return CompositeLogger(ConsoleLogger(), FileLogger())
        else:
            # Default to composite logger
            return CompositeLogger(ConsoleLogger(), FileLogger())
    
    @staticmethod
    def create_transaction_manager(logger: Logger) -> TransactionManager:
        """Create a transaction manager instance.
        
        Args:
            logger: Logger instance for transaction logging.
            
        Returns:
            Configured transaction manager.
        """
        return TransactionManager(logger)
    
    @staticmethod
    def create_database(config: Config, logger: Optional[Logger] = None) -> Database:
        """Create a database instance based on configuration.
        
        Args:
            config: Application configuration.
            logger: Optional logger instance. If not provided, one will be created.
            
        Returns:
            Configured database instance.
        """
        if logger is None:
            logger = DatabaseFactory.create_logger(config)
        
        db_type = config.get('database.type', 'inmemory')
        
        if db_type == 'inmemory':
            transaction_manager = DatabaseFactory.create_transaction_manager(logger)
            return InMemoryDB(transaction_manager, logger)  # type: ignore
        else:
            # Default to in-memory database
            transaction_manager = DatabaseFactory.create_transaction_manager(logger)
            return InMemoryDB(transaction_manager, logger)  # type: ignore
    
    @staticmethod
    def create_with_dependencies(config: Config) -> tuple[Database, Logger, TransactionManager]:
        """Create all database-related dependencies.
        
        Args:
            config: Application configuration.
            
        Returns:
            Tuple of (database, logger, transaction_manager).
        """
        logger = DatabaseFactory.create_logger(config)
        transaction_manager = DatabaseFactory.create_transaction_manager(logger)
        database = DatabaseFactory.create_database(config, logger)
        
        return database, logger, transaction_manager 