import os
import yaml
from typing import Dict, Any, Optional

class Config:
    """Configuration manager for the application."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration.
        
        Args:
            config_path: Path to configuration file. Defaults to 'config.yaml'.
        """
        self.config_path = config_path or 'config.yaml'
        self._config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file."""
        if not os.path.exists(self.config_path):
            return self._get_default_config()
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Warning: Could not load config from {self.config_path}: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            'app': {
                'name': 'In-Memory Database CLI',
                'version': '1.0.0',
                'description': 'A command-line interface for an in-memory database with transaction support'
            },
            'logging': {
                'level': 'INFO',
                'file': {
                    'enabled': True,
                    'path': 'logs',
                    'filename_pattern': 'db_{date}.log',
                    'max_size': '10MB',
                    'backup_count': 7
                },
                'console': {
                    'enabled': True,
                    'level': 'INFO'
                },
                'format': {
                    'file': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    'console': '%(levelname)s: %(message)s'
                }
            },
            'database': {
                'type': 'inmemory',
                'transaction': {
                    'max_depth': 100,
                    'auto_commit': False
                },
                'storage': {
                    'persistence': False,
                    'backup_interval': 300
                }
            },
            'cli': {
                'prompt': '>',
                'history_file': '.db_history',
                'auto_complete': True,
                'colors': True
            },
            'development': {
                'debug': False,
                'test_mode': False,
                'mock_logger': False
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key.
        
        Args:
            key: Configuration key (dot-separated for nested keys).
            default: Default value if key not found.
            
        Returns:
            Configuration value.
        """
        keys = key.split('.')
        value = self._config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def get_logging_config(self) -> Dict[str, Any]:
        """Get logging configuration."""
        return self._config.get('logging', {})
    
    def get_database_config(self) -> Dict[str, Any]:
        """Get database configuration."""
        return self._config.get('database', {})
    
    def get_cli_config(self) -> Dict[str, Any]:
        """Get CLI configuration."""
        return self._config.get('cli', {})
    
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.get('development.debug', False)
    
    def is_test_mode(self) -> bool:
        """Check if running in test mode."""
        return self.get('development.test_mode', False)

# Global configuration instance
config = Config() 