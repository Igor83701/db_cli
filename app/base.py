from abc import ABC, abstractmethod
from typing import Optional, List, Protocol

class KeyValueStore(Protocol):
    """Interface for basic key-value operations."""
    
    def set(self, key: str, value: str) -> None:
        """Set a key-value pair."""
        ...
    
    def get(self, key: str) -> Optional[str]:
        """Get a value by key."""
        ...
    
    def unset(self, key: str) -> None:
        """Remove a key."""
        ...

class SearchableStore(Protocol):
    """Interface for search operations."""
    
    def counts(self, value: str) -> int:
        """Count occurrences of a value."""
        ...
    
    def find(self, value: str) -> List[str]:
        """Find keys with a specific value."""
        ...

class TransactionalStore(Protocol):
    """Interface for transaction operations."""
    
    def begin(self) -> None:
        """Begin a new transaction."""
        ...
    
    def rollback(self) -> bool:
        """Rollback the current transaction."""
        ...
    
    def commit(self) -> bool:
        """Commit the current transaction."""
        ...
    
    def get_transaction_depth(self) -> int:
        """Get current transaction depth."""
        ...

class Database(KeyValueStore, SearchableStore, TransactionalStore):
    """Complete database interface combining all operations."""
    pass

class BaseDB(ABC):
    """Abstract base class for a key-value database.
    
    This class maintains backward compatibility while implementing
    the new interface segregation pattern.
    """
    
    @abstractmethod
    def set(self, key: str, value: str) -> None:
        pass

    @abstractmethod
    def get(self, key: str) -> Optional[str]:
        pass

    @abstractmethod
    def unset(self, key: str) -> None:
        pass

    @abstractmethod
    def counts(self, value: str) -> int:
        pass

    @abstractmethod
    def find(self, value: str) -> List[str]:
        pass

    @abstractmethod
    def begin(self) -> None:
        pass

    @abstractmethod
    def rollback(self) -> bool:
        pass

    @abstractmethod
    def commit(self) -> bool:
        pass

    @abstractmethod
    def get_transaction_depth(self) -> int:
        pass 