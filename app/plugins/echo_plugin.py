from app.plugins.base_plugin import BasePlugin
from app.config import Config

class EchoPlugin:
    name = "echo"
    def initialize(self, config: Config) -> None:
        pass
    def register(self, registry):
        registry.register('echo', self.echo, 'Echo input')
    def cleanup(self) -> None:
        pass
    def echo(self, *args):
        return ' '.join(args) 