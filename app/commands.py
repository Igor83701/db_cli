from typing import Callable, Dict, Any, Optional
from .base import Database
from .logger import Logger

class CommandRegistry:
    """Registry for database commands following Single Responsibility Principle."""
    
    def __init__(self, database: Database, logger: Logger):
        """Initialize command registry with database and logger.
        
        Args:
            database: Database instance for operations.
            logger: Logger for command logging.
        """
        self._database = database
        self._logger = logger
        self._commands: Dict[str, Dict[str, Any]] = {}
        self._register_default_commands()
    
    def _register_default_commands(self) -> None:
        """Register all default database commands."""
        self.register('set', self._cmd_set, 'Set a key-value pair')
        self.register('get', self._cmd_get, 'Get value by key')
        self.register('unset', self._cmd_unset, 'Remove a key')
        self.register('counts', self._cmd_counts, 'Count occurrences of value')
        self.register('find', self._cmd_find, 'Find keys with value')
        self.register('begin', self._cmd_begin, 'Start transaction')
        self.register('rollback', self._cmd_rollback, 'Rollback transaction')
        self.register('commit', self._cmd_commit, 'Commit transaction')
        self.register('status', self._cmd_status, 'Show database status')
    
    def register(self, name: str, handler: Callable, help_text: str = "") -> None:
        """Register a new command.
        
        Args:
            name: Command name.
            handler: Command handler function.
            help_text: Help text for the command.
        """
        self._commands[name] = {
            'handler': handler,
            'help': help_text
        }
        self._logger.debug(f"Registered command: {name}")
    
    def execute(self, name: str, *args, **kwargs) -> Any:
        """Execute a command by name.
        
        Args:
            name: Command name.
            *args: Command arguments.
            **kwargs: Command keyword arguments.
            
        Returns:
            Command result.
            
        Raises:
            ValueError: If command not found.
        """
        if name not in self._commands:
            raise ValueError(f"Unknown command: {name}")
        
        command = self._commands[name]
        self._logger.debug(f"Executing command: {name} with args: {args}")
        return command['handler'](*args, **kwargs)
    
    def get_help(self, name: Optional[str] = None) -> str:
        """Get help text for commands.
        
        Args:
            name: Specific command name, or None for all commands.
            
        Returns:
            Help text.
        """
        if name:
            if name in self._commands:
                return self._commands[name]['help']
            return f"Unknown command: {name}"
        
        help_text = "Available commands:\n"
        for cmd_name, cmd_info in sorted(self._commands.items()):
            help_text += f"  {cmd_name.upper():<12} - {cmd_info['help']}\n"
        return help_text
    
    def list_commands(self) -> list[str]:
        """Get list of available command names.
        
        Returns:
            List of command names.
        """
        return list(self._commands.keys())
    
    # Command handlers
    def _cmd_set(self, key: str, value: str) -> None:
        """Set command handler."""
        self._database.set(key, value)
    
    def _cmd_get(self, key: str) -> Optional[str]:
        """Get command handler."""
        return self._database.get(key)
    
    def _cmd_unset(self, key: str) -> None:
        """Unset command handler."""
        self._database.unset(key)
    
    def _cmd_counts(self, value: str) -> int:
        """Counts command handler."""
        return self._database.counts(value)
    
    def _cmd_find(self, value: str) -> list[str]:
        """Find command handler."""
        return self._database.find(value)
    
    def _cmd_begin(self) -> None:
        """Begin command handler."""
        self._database.begin()
    
    def _cmd_rollback(self) -> bool:
        """Rollback command handler."""
        return self._database.rollback()
    
    def _cmd_commit(self) -> bool:
        """Commit command handler."""
        return self._database.commit()
    
    def _cmd_status(self) -> int:
        """Status command handler."""
        return self._database.get_transaction_depth() 