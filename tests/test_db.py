import pytest
from app.db import InMemoryDB
from app.base import BaseDB
from app.transaction_manager import TransactionManager
from app.logger import ConsoleLogger

class TestInMemoryDB:
    def setup_method(self):
        """Create a new DB instance before each test"""
        logger = ConsoleLogger()
        transaction_manager = TransactionManager(logger)
        self.db = InMemoryDB(transaction_manager, logger)

    def test_inheritance(self):
        """Test that InMemoryDB inherits from BaseDB"""
        assert isinstance(self.db, BaseDB)

    def test_set_and_get(self):
        """Test SET and GET commands"""
        self.db.set("A", "10")
        assert self.db.get("A") == "10"
        # Test getting a non-existent key
        assert self.db.get("B") is None

    def test_unset(self):
        """Test UNSET command"""
        self.db.set("A", "10")
        assert self.db.get("A") == "10"
        self.db.unset("A")
        assert self.db.get("A") is None
        # UNSET for a non-existent key should not raise an error
        self.db.unset("B")

    def test_counts(self):
        """Test COUNTS command"""
        self.db.set("A", "10")
        self.db.set("B", "20")
        self.db.set("C", "10")
        assert self.db.counts("10") == 2
        assert self.db.counts("20") == 1
        assert self.db.counts("30") == 0

    def test_find(self):
        """Test FIND command"""
        self.db.set("A", "10")
        self.db.set("B", "20")
        self.db.set("C", "10")
        found_10 = self.db.find("10")
        assert "A" in found_10
        assert "C" in found_10
        assert len(found_10) == 2
        found_20 = self.db.find("20")
        assert found_20 == ["B"]
        found_30 = self.db.find("30")
        assert found_30 == []

    def test_simple_transaction(self):
        """Test a simple transaction"""
        self.db.set("A", "10")
        self.db.begin()
        self.db.set("A", "20")
        assert self.db.get("A") == "20"
        self.db.rollback()
        assert self.db.get("A") == "10"

    def test_nested_transactions(self):
        """Test nested transactions"""
        self.db.set("A", "10")
        self.db.begin()
        self.db.set("A", "20")
        assert self.db.get("A") == "20"
        self.db.begin()
        self.db.set("A", "30")
        assert self.db.get("A") == "30"
        self.db.begin()
        self.db.set("A", "40")
        assert self.db.get("A") == "40"
        self.db.rollback()
        assert self.db.get("A") == "30"
        self.db.commit()
        assert self.db.get("A") == "30"
        self.db.rollback()
        assert self.db.get("A") == "10"

    def test_commit_transaction(self):
        """Test transaction commit"""
        self.db.set("A", "10")
        self.db.begin()
        self.db.set("A", "20")
        self.db.set("B", "30")
        self.db.commit()
        assert self.db.get("A") == "20"
        assert self.db.get("B") == "30"

    def test_unset_in_transaction(self):
        """Test UNSET in a transaction"""
        self.db.set("A", "10")
        self.db.set("B", "20")
        self.db.begin()
        self.db.unset("A")
        self.db.set("C", "30")
        # In transaction, A should be None
        assert self.db.get("A") is None
        assert self.db.get("B") == "20"
        assert self.db.get("C") == "30"
        self.db.rollback()
        # After rollback, A should be restored
        assert self.db.get("A") == "10"
        assert self.db.get("B") == "20"
        assert self.db.get("C") is None

    def test_rollback_without_transaction(self):
        """Test ROLLBACK without an active transaction"""
        assert not self.db.rollback()

    def test_commit_without_transaction(self):
        """Test COMMIT without an active transaction"""
        assert not self.db.commit()

    def test_multiple_values_same_key(self):
        """Test multiple changes to the same key"""
        self.db.set("A", "10")
        self.db.set("A", "20")
        self.db.set("A", "30")
        assert self.db.get("A") == "30"
        assert self.db.counts("30") == 1
        assert self.db.counts("10") == 0
        assert self.db.counts("20") == 0

    def test_transaction_depth(self):
        """Test transaction depth tracking"""
        assert self.db.get_transaction_depth() == 0
        self.db.begin()
        assert self.db.get_transaction_depth() == 1
        self.db.begin()
        assert self.db.get_transaction_depth() == 2
        self.db.rollback()
        assert self.db.get_transaction_depth() == 1
        self.db.rollback()
        assert self.db.get_transaction_depth() == 0

    def test_unset_commit_removes_key_completely(self):
        """Unset + commit should remove key completely"""
        self.db.set("A", "1")
        self.db.begin()
        self.db.set("A", "2")
        self.db.begin()
        self.db.unset("A")
        assert self.db.get("A") is None  # A unset in nested transaction
        self.db.commit()  # Commit inner transaction
        assert self.db.get("A") is None  # Should still be None
        self.db.commit()  # Commit outer transaction
        assert self.db.get("A") is None  # Should still be None after all commits 