from .base import BaseDB, Database
from .transaction_manager import TransactionManager
from .logger import Logger
from typing import Optional, List

class InMemoryDB(BaseDB, Database):
    """In-memory key-value database with transaction support.
    Implements BaseDB interface and follows Dependency Inversion Principle.
    """
    
    def __init__(self, transaction_manager: TransactionManager, logger: Logger) -> None:
        """Initialize the database with dependencies.
        
        Args:
            transaction_manager: Manager for transaction operations.
            logger: Logger for database operations.
        """
        self._transaction_manager = transaction_manager
        self._logger = logger
        self._logger.info("InMemoryDB initialized")

    def _current(self) -> dict[str, Optional[str]]:
        """Return the current transaction layer."""
        return self._transaction_manager.get_current_layer()

    def set(self, key: str, value: str) -> None:
        """Set a key-value pair in the database.

        Args:
            key: The key to set.
            value: The value to assign.
        """
        self._current()[key] = value
        self._logger.info(f"SET: {key} = {value}")

    def get(self, key: str) -> Optional[str]:
        """Get a value by key from the database.

        Args:
            key: The key to retrieve.
        Returns:
            The value if found, else None.
        """
        for layer in reversed(self._transaction_manager.get_all_layers()):
            if key in layer:
                value = layer[key]
                self._logger.info(f"GET: {key} = {value}")
                return value
        self._logger.info(f"GET: {key} = NULL (not found)")
        return None

    def unset(self, key: str) -> None:
        """Unset a key from the database.

        Args:
            key: The key to remove.
        """
        self._current()[key] = None
        self._logger.info(f"UNSET: {key}")

    def counts(self, value: str) -> int:
        """Count how many times a value appears in the database.

        Args:
            value: The value to count.
        Returns:
            The number of keys with the given value.
        """
        result = 0
        seen = set()
        for layer in self._transaction_manager.get_all_layers():
            for k, v in layer.items():
                if k not in seen:
                    seen.add(k)
                    val = self.get(k)
                    if val == value:
                        result += 1
        self._logger.info(f"COUNTS: {value} = {result}")
        return result

    def find(self, value: str) -> List[str]:
        """Find all keys that have the specified value.

        Args:
            value: The value to search for.
        Returns:
            List of keys with the given value.
        """
        found = []
        seen = set()
        for layer in self._transaction_manager.get_all_layers():
            for k in layer:
                if k not in seen:
                    seen.add(k)
                    val = self.get(k)
                    if val == value:
                        found.append(k)
        self._logger.info(f"FIND: {value} = {found}")
        return found

    def begin(self) -> None:
        """Begin a new transaction."""
        self._transaction_manager.begin()

    def rollback(self) -> bool:
        """Rollback the current transaction.

        Returns:
            True if rolled back, False if no transaction.
        """
        return self._transaction_manager.rollback()

    def commit(self) -> bool:
        """Commit the current transaction.

        Returns:
            True if committed, False if no transaction.
        """
        return self._transaction_manager.commit()

    def get_transaction_depth(self) -> int:
        """Get current transaction depth.

        Returns:
            The number of active transactions.
        """
        return self._transaction_manager.get_transaction_depth() 