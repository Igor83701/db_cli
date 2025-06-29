import click
from typing import Optional
from .commands import CommandRegistry
from .logger import Logger

class InteractiveMode:
    """Handles interactive mode operations following Single Responsibility Principle."""
    
    def __init__(self, command_registry: CommandRegistry, logger: Logger):
        """Initialize interactive mode.
        
        Args:
            command_registry: Registry for command execution.
            logger: Logger for interactive mode logging.
        """
        self._command_registry = command_registry
        self._logger = logger
        self._logger.info("Interactive mode initialized")
    
    def run(self) -> None:
        """Start interactive mode."""
        self._logger.info("Interactive mode started")
        click.echo("Interactive mode started. Type 'help' for available commands or 'end' to exit.")
        
        while True:
            try:
                line = click.prompt('>', prompt_suffix='', type=str).strip()
            except click.Abort:
                self._logger.info("Interactive mode ended by EOF")
                click.echo()
                break
            
            if not line:
                continue
            
            if self._process_command(line):
                break
    
    def _process_command(self, line: str) -> bool:
        """Process a single command line.
        
        Args:
            line: Command line to process.
            
        Returns:
            True if should exit, False otherwise.
        """
        parts = line.split()
        if not parts:
            return False
        
        cmd = parts[0].lower()
        args = parts[1:]
        
        try:
            if cmd == 'end':
                self._logger.info("Interactive mode ended by END command")
                return True
            elif cmd == 'help':
                self._show_help(args)
            else:
                self._execute_command(cmd, args)
        except Exception as e:
            self._logger.error(f"Error executing command '{cmd}': {e}")
            click.echo(f'ERROR: {e}')
        
        return False
    
    def _show_help(self, args: list[str]) -> None:
        """Show help information.
        
        Args:
            args: Help command arguments.
        """
        if args:
            help_text = self._command_registry.get_help(args[0])
        else:
            help_text = self._command_registry.get_help()
        
        click.echo(help_text)
    
    def _execute_command(self, cmd: str, args: list[str]) -> None:
        """Execute a database command.
        
        Args:
            cmd: Command name.
            args: Command arguments.
        """
        try:
            result = self._command_registry.execute(cmd, *args)
            self._format_and_display_result(cmd, result)
        except ValueError as e:
            self._logger.warning(f"Unknown command: {cmd}")
            click.echo('UNKNOWN COMMAND')
        except TypeError as e:
            self._logger.warning(f"Invalid arguments for command '{cmd}': {e}")
            click.echo('INVALID ARGUMENTS')
    
    def _format_and_display_result(self, cmd: str, result) -> None:
        """Format and display command result.
        
        Args:
            cmd: Command name.
            result: Command result.
        """
        if cmd == 'get':
            click.echo(result if result is not None else 'NULL')
        elif cmd == 'counts':
            click.echo(result)
        elif cmd == 'find':
            click.echo(' '.join(result) if result else 'NULL')
        elif cmd == 'rollback' and not result:
            click.echo('NO TRANSACTION')
        elif cmd == 'commit' and not result:
            click.echo('NO TRANSACTION')
        elif cmd == 'status':
            click.echo(f"Transaction depth: {result}")
        # Other commands (set, unset, begin) don't produce output 