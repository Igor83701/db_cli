import pytest
from app.commands import CommandRegistry
from app.db import InMemoryDB
from app.transaction_manager import TransactionManager
from app.logger import ConsoleLogger

class TestCommandRegistry:
    def setup_method(self):
        """Create test dependencies before each test"""
        self.logger = ConsoleLogger()
        self.transaction_manager = TransactionManager(self.logger)
        self.database = InMemoryDB(self.transaction_manager, self.logger)  # type: ignore
        self.registry = CommandRegistry(self.database, self.logger)

    def test_command_registration(self):
        """Test that commands are properly registered"""
        commands = self.registry.list_commands()
        expected_commands = ['set', 'get', 'unset', 'counts', 'find', 'begin', 'rollback', 'commit', 'status']
        
        for cmd in expected_commands:
            assert cmd in commands
    
    def test_set_command(self):
        """Test SET command execution"""
        self.registry.execute('set', 'A', '10')
        assert self.database.get('A') == '10'

    def test_get_command(self):
        """Test GET command execution"""
        self.database.set('A', '10')
        result = self.registry.execute('get', 'A')
        assert result == '10'

    def test_get_nonexistent_key(self):
        """Test GET command with non-existent key"""
        result = self.registry.execute('get', 'nonexistent')
        assert result is None

    def test_unset_command(self):
        """Test UNSET command execution"""
        self.database.set('A', '10')
        self.registry.execute('unset', 'A')
        assert self.database.get('A') is None

    def test_counts_command(self):
        """Test COUNTS command execution"""
        self.database.set('A', '10')
        self.database.set('B', '20')
        self.database.set('C', '10')
        
        result = self.registry.execute('counts', '10')
        assert result == 2
        
        result = self.registry.execute('counts', '20')
        assert result == 1

    def test_find_command(self):
        """Test FIND command execution"""
        self.database.set('A', '10')
        self.database.set('B', '20')
        self.database.set('C', '10')
        
        result = self.registry.execute('find', '10')
        assert 'A' in result
        assert 'C' in result
        assert len(result) == 2

    def test_transaction_commands(self):
        """Test transaction commands"""
        self.database.set('A', '10')
        
        # Test BEGIN
        self.registry.execute('begin')
        assert self.database.get_transaction_depth() == 1
        
        # Test SET in transaction
        self.registry.execute('set', 'A', '20')
        assert self.database.get('A') == '20'
        
        # Test ROLLBACK
        result = self.registry.execute('rollback')
        assert result is True
        assert self.database.get('A') == '10'
        assert self.database.get_transaction_depth() == 0

    def test_status_command(self):
        """Test STATUS command execution"""
        result = self.registry.execute('status')
        assert result == 0
        
        self.database.begin()
        result = self.registry.execute('status')
        assert result == 1

    def test_unknown_command(self):
        """Test handling of unknown commands"""
        with pytest.raises(ValueError, match="Unknown command: unknown"):
            self.registry.execute('unknown')

    def test_help_text(self):
        """Test help text generation"""
        help_text = self.registry.get_help()
        assert 'Available commands:' in help_text
        assert 'set' in help_text.lower()
        assert 'get' in help_text.lower()

    def test_specific_help(self):
        """Test help text for specific command"""
        help_text = self.registry.get_help('set')
        assert 'Set a key-value pair' in help_text

    def test_unknown_command_help(self):
        """Test help text for unknown command"""
        help_text = self.registry.get_help('unknown')
        assert 'Unknown command: unknown' in help_text

    def test_custom_command_registration(self):
        """Test registering custom commands"""
        def custom_handler(value):
            return f"Custom: {value}"
        
        self.registry.register('custom', custom_handler, 'Custom command')
        
        assert 'custom' in self.registry.list_commands()
        result = self.registry.execute('custom', 'test')
        assert result == 'Custom: test' 