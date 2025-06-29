from typing import List, Dict, Optional
from .logger import Logger

class TransactionManager:
    """Manages database transactions independently from the main database logic."""
    
    def __init__(self, logger: Logger):
        self._layers: List[Dict[str, Optional[str]]] = [{}]
        self._logger = logger
        self._logger.info("TransactionManager initialized")
    
    def begin(self) -> None:
        """Begin a new transaction."""
        self._layers.append({})
        self._logger.info("BEGIN: New transaction started")
    
    def rollback(self) -> bool:
        """Rollback the current transaction.
        
        Returns:
            True if rolled back, False if no transaction.
        """
        if len(self._layers) == 1:
            self._logger.warning("ROLLBACK: No active transaction")
            return False
        self._layers.pop()
        self._logger.info("ROLLBACK: Transaction rolled back")
        return True
    
    def commit(self) -> bool:
        """Commit the current transaction.
        
        Returns:
            True if committed, False if no transaction.
        """
        if len(self._layers) == 1:
            self._logger.warning("COMMIT: No active transaction")
            return False
        
        top = self._layers.pop()
        for k, v in top.items():
            if v is None:
                # Unset - remove from all layers
                for layer in reversed(self._layers):
                    if k in layer:
                        del layer[k]
                        break
            else:
                # Set - update the current layer
                self._layers[-1][k] = v
        
        self._logger.info("COMMIT: Transaction committed")
        return True
    
    def get_transaction_depth(self) -> int:
        """Get current transaction depth.
        
        Returns:
            The number of active transactions.
        """
        return len(self._layers) - 1
    
    def get_current_layer(self) -> Dict[str, Optional[str]]:
        """Get the current transaction layer.
        
        Returns:
            The current layer dictionary.
        """
        return self._layers[-1]
    
    def get_all_layers(self) -> List[Dict[str, Optional[str]]]:
        """Get all transaction layers.
        
        Returns:
            List of all layer dictionaries.
        """
        return self._layers.copy() 