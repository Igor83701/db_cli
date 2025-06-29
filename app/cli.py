import click
import sys
from .database_factory import DatabaseFactory
from .commands import CommandRegistry
from .interactive import InteractiveMode
from .config import Config
from .base import Database
from .logger import Logger
from .plugins.plugin_manager import PluginManager
from .plugins.echo_plugin import EchoPlugin
from typing import Optional

class CLI:
    """CLI application following SOLID principles with dependency injection."""
    
    def __init__(self, database: Database, command_registry: CommandRegistry, 
                 interactive_mode: InteractiveMode, logger: Logger, plugin_manager: PluginManager):
        """Initialize CLI with dependencies.
        
        Args:
            database: Database instance.
            command_registry: Command registry for operations.
            interactive_mode: Interactive mode handler.
            logger: Logger for CLI operations.
            plugin_manager: Plugin manager for managing plugins.
        """
        self._database = database
        self._command_registry = command_registry
        self._interactive_mode = interactive_mode
        self._logger = logger
        self._plugin_manager = plugin_manager
        self._logger.info("CLI initialized")

@click.group()
def cli():
    """In-Memory Database CLI Application"""
    pass

@cli.command()
@click.argument('key')
@click.argument('value')
def set(key, value):
    """Set a key-value pair in the database"""
    _get_cli_instance()._command_registry.execute('set', key, value)

@cli.command()
@click.argument('key')
def get(key):
    """Get a value by key from the database"""
    val = _get_cli_instance()._command_registry.execute('get', key)
    click.echo(val if val is not None else 'NULL')

@cli.command()
@click.argument('key')
def unset(key):
    """Unset a key from the database"""
    _get_cli_instance()._command_registry.execute('unset', key)

@cli.command()
@click.argument('value')
def counts(value):
    """Count how many times a value appears in the database"""
    result = _get_cli_instance()._command_registry.execute('counts', value)
    click.echo(result)

@cli.command()
@click.argument('value')
def find(value):
    """Find all keys that have the specified value"""
    found = _get_cli_instance()._command_registry.execute('find', value)
    click.echo(' '.join(found) if found else 'NULL')

@cli.command()
def begin():
    """Begin a new transaction"""
    _get_cli_instance()._command_registry.execute('begin')

@cli.command()
def rollback():
    """Rollback the current transaction"""
    if not _get_cli_instance()._command_registry.execute('rollback'):
        click.echo('NO TRANSACTION')

@cli.command()
def commit():
    """Commit the current transaction"""
    if not _get_cli_instance()._command_registry.execute('commit'):
        click.echo('NO TRANSACTION')

@cli.command()
def end():
    """End the application"""
    _get_cli_instance()._logger.info("Application ended by user")
    sys.exit(0)

@cli.command()
def status():
    """Show database status"""
    transaction_depth = _get_cli_instance()._command_registry.execute('status')
    click.echo(f"Transaction depth: {transaction_depth}")
    _get_cli_instance()._logger.info(f"STATUS: Transaction depth = {transaction_depth}")

@cli.command()
def interactive():
    """Start interactive mode"""
    _get_cli_instance()._interactive_mode.run()

# Global CLI instance for Click commands
_cli_instance: Optional[CLI] = None

def _get_cli_instance() -> CLI:
    """Get the global CLI instance, creating it if necessary."""
    global _cli_instance
    if _cli_instance is None:
        _cli_instance = _create_cli_instance()
    return _cli_instance

def _create_cli_instance() -> CLI:
    """Create a new CLI instance with all dependencies."""
    config = Config()
    database, logger, _ = DatabaseFactory.create_with_dependencies(config)
    command_registry = CommandRegistry(database, logger)
    interactive_mode = InteractiveMode(command_registry, logger)
    plugin_manager = PluginManager()
    # Регистрируем плагины
    plugin_manager.register(EchoPlugin())
    plugin_manager.initialize_all(config, command_registry)
    return CLI(database, command_registry, interactive_mode, logger, plugin_manager)

def main():
    """Main entry point for the CLI application."""
    cli() 