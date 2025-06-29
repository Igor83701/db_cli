from typing import Dict
from .base_plugin import BasePlugin
from app.config import Config
from app.commands import CommandRegistry

class PluginManager:
    def __init__(self):
        self._plugins: Dict[str, BasePlugin] = {}

    def register(self, plugin: BasePlugin):
        self._plugins[plugin.name] = plugin

    def initialize_all(self, config: Config, registry: CommandRegistry):
        for plugin in self._plugins.values():
            plugin.initialize(config)
            plugin.register(registry)

    def cleanup_all(self):
        for plugin in self._plugins.values():
            plugin.cleanup() 