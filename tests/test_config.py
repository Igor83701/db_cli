import pytest
import os
import tempfile
import yaml
from app.config import Config

class TestConfig:
    def setup_method(self):
        """Setup test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.temp_dir, 'test_config.yaml')
    
    def teardown_method(self):
        """Cleanup test environment"""
        if os.path.exists(self.temp_dir):
            for file in os.listdir(self.temp_dir):
                os.remove(os.path.join(self.temp_dir, file))
            os.rmdir(self.temp_dir)
    
    def test_default_config(self):
        """Test default configuration loading"""
        config = Config('nonexistent.yaml')
        
        # Test app section
        assert config.get('app.name') == 'In-Memory Database CLI'
        assert config.get('app.version') == '1.0.0'
        
        # Test logging section
        assert config.get('logging.level') == 'INFO'
        assert config.get('logging.file.enabled') is True
        assert config.get('logging.console.enabled') is True
        
        # Test database section
        assert config.get('database.type') == 'inmemory'
        assert config.get('database.transaction.max_depth') == 100
        
        # Test CLI section
        assert config.get('cli.prompt') == '>'
        assert config.get('cli.colors') is True
        
        # Test development section
        assert config.get('development.debug') is False
        assert config.get('development.test_mode') is False
    
    def test_custom_config_file(self):
        """Test loading custom configuration file"""
        custom_config = {
            'app': {
                'name': 'Custom DB CLI',
                'version': '2.0.0'
            },
            'logging': {
                'level': 'DEBUG',
                'file': {
                    'enabled': False
                }
            },
            'database': {
                'type': 'custom',
                'transaction': {
                    'max_depth': 50
                }
            }
        }
        
        with open(self.config_file, 'w') as f:
            yaml.dump(custom_config, f)
        
        config = Config(self.config_file)
        
        assert config.get('app.name') == 'Custom DB CLI'
        assert config.get('app.version') == '2.0.0'
        assert config.get('logging.level') == 'DEBUG'
        assert config.get('logging.file.enabled') is False
        assert config.get('database.type') == 'custom'
        assert config.get('database.transaction.max_depth') == 50
    
    def test_get_with_default(self):
        """Test getting configuration values with defaults"""
        config = Config()
        
        # Test existing key
        assert config.get('app.name') == 'In-Memory Database CLI'
        
        # Test non-existing key with default
        assert config.get('nonexistent.key', 'default_value') == 'default_value'
        assert config.get('nonexistent.key') is None
    
    def test_nested_key_access(self):
        """Test accessing nested configuration keys"""
        config = Config()
        
        # Test deeply nested keys
        assert config.get('logging.file.path') == 'logs'
        assert config.get('database.transaction.auto_commit') is False
        assert config.get('cli.history_file') == '.db_history'
    
    def test_get_logging_config(self):
        """Test getting logging configuration section"""
        config = Config()
        logging_config = config.get_logging_config()
        
        assert isinstance(logging_config, dict)
        assert 'level' in logging_config
        assert 'file' in logging_config
        assert 'console' in logging_config
        assert logging_config['level'] == 'INFO'
    
    def test_get_database_config(self):
        """Test getting database configuration section"""
        config = Config()
        db_config = config.get_database_config()
        
        assert isinstance(db_config, dict)
        assert 'type' in db_config
        assert 'transaction' in db_config
        assert 'storage' in db_config
        assert db_config['type'] == 'inmemory'
    
    def test_get_cli_config(self):
        """Test getting CLI configuration section"""
        config = Config()
        cli_config = config.get_cli_config()
        
        assert isinstance(cli_config, dict)
        assert 'prompt' in cli_config
        assert 'colors' in cli_config
        assert cli_config['prompt'] == '>'
    
    def test_development_mode_flags(self):
        """Test development mode flags"""
        config = Config()
        
        assert config.is_development() is False
        assert config.is_test_mode() is False
    
    def test_invalid_yaml_handling(self):
        """Test handling of invalid YAML file"""
        with open(self.config_file, 'w') as f:
            f.write("invalid: yaml: content: [")
        
        config = Config(self.config_file)
        
        # Should fall back to default config
        assert config.get('app.name') == 'In-Memory Database CLI'
    
    def test_missing_file_handling(self):
        """Test handling of missing configuration file"""
        config = Config('nonexistent_file.yaml')
        
        # Should use default configuration
        assert config.get('app.name') == 'In-Memory Database CLI'
        assert config.get('logging.level') == 'INFO'
    
    def test_global_config_instance(self):
        """Test global configuration instance"""
        from app.config import config
        
        assert isinstance(config, Config)
        assert config.get('app.name') == 'In-Memory Database CLI' 