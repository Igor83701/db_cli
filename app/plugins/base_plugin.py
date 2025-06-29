from typing import Protocol
from app.config import Config

class BasePlugin(Protocol):
    name: str
    def initialize(self, config: Config) -> None:
        ...
    def register(self, registry) -> None:
        ...
    def cleanup(self) -> None:
        ... 