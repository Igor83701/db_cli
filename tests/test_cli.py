import pytest
from click.testing import CliRunner
from app.cli import cli
from app.database_factory import DatabaseFactory
from app.logger import NullLogger

@pytest.fixture(autouse=True)
def patch_logger(monkeypatch):
    monkeypatch.setattr(DatabaseFactory, "create_logger", staticmethod(lambda config: NullLogger()))
    yield

class TestCLI:
    def setup_method(self):
        """Create CLI runner before each test"""
        self.runner = CliRunner()

    def test_set_command(self):
        """Test CLI SET command"""
        result = self.runner.invoke(cli, ['set', 'A', '10'])
        assert result.exit_code == 0

    def test_get_command(self):
        """Test CLI GET command"""
        self.runner.invoke(cli, ['set', 'A', '10'])
        result = self.runner.invoke(cli, ['get', 'A'])
        assert result.exit_code == 0
        assert result.output.strip() == '10'

    def test_get_nonexistent_key(self):
        """Test GET for a non-existent key"""
        result = self.runner.invoke(cli, ['get', 'nonexistent'])
        assert result.exit_code == 0
        assert result.output.strip() == 'NULL'

    def test_unset_command(self):
        """Test CLI UNSET command"""
        self.runner.invoke(cli, ['set', 'A', '10'])
        result = self.runner.invoke(cli, ['get', 'A'])
        assert result.output.strip() == '10'
        self.runner.invoke(cli, ['unset', 'A'])
        result = self.runner.invoke(cli, ['get', 'A'])
        assert result.output.strip() == 'NULL'

    def test_counts_command(self):
        """Test CLI COUNTS command"""
        self.runner.invoke(cli, ['set', 'A', '10'])
        self.runner.invoke(cli, ['set', 'B', '20'])
        self.runner.invoke(cli, ['set', 'C', '10'])
        result = self.runner.invoke(cli, ['counts', '10'])
        assert result.exit_code == 0
        assert result.output.strip() == '2'

    def test_find_command(self):
        """Test CLI FIND command"""
        self.runner.invoke(cli, ['set', 'A', '10'])
        self.runner.invoke(cli, ['set', 'B', '20'])
        self.runner.invoke(cli, ['set', 'C', '10'])
        result = self.runner.invoke(cli, ['find', '10'])
        assert result.exit_code == 0
        output = result.output.strip()
        assert 'A' in output
        assert 'C' in output

    def test_transaction_commands(self):
        """Test CLI transaction commands"""
        self.runner.invoke(cli, ['set', 'A', '10'])
        result = self.runner.invoke(cli, ['begin'])
        assert result.exit_code == 0
        self.runner.invoke(cli, ['set', 'A', '20'])
        result = self.runner.invoke(cli, ['get', 'A'])
        assert result.output.strip() == '20'
        result = self.runner.invoke(cli, ['rollback'])
        assert result.exit_code == 0
        result = self.runner.invoke(cli, ['get', 'A'])
        assert result.output.strip() == '10'

    def test_rollback_without_transaction(self):
        """Test ROLLBACK without an active transaction"""
        result = self.runner.invoke(cli, ['rollback'])
        assert result.exit_code == 0
        assert result.output.strip() == 'NO TRANSACTION'

    def test_commit_without_transaction(self):
        """Test COMMIT without an active transaction"""
        result = self.runner.invoke(cli, ['commit'])
        assert result.exit_code == 0
        assert result.output.strip() == 'NO TRANSACTION'

    def test_end_command(self):
        """Test END command"""
        result = self.runner.invoke(cli, ['end'])
        assert result.exit_code == 0

    def test_status_command(self):
        """Test STATUS command"""
        result = self.runner.invoke(cli, ['status'])
        assert result.exit_code == 0
        assert 'Transaction depth: 0' in result.output

    def test_help_command(self):
        """Test help command"""
        result = self.runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert 'In-Memory Database CLI Application' in result.output

    def test_interactive_command(self):
        """Test interactive command exists"""
        result = self.runner.invoke(cli, ['interactive', '--help'])
        assert result.exit_code == 0 