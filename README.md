# In-Memory Database CLI

A command-line interface for an in-memory database with transaction support, built with Python and Click.

## Features

- **In-Memory Storage**: Fast key-value storage in memory
- **Transaction Support**: Nested transactions with BEGIN, COMMIT, ROLLBACK
- **CLI Interface**: Both interactive and command-line modes
- **Comprehensive Logging**: All operations logged to daily log files
- **Full Test Coverage**: Unit tests for all functionality

## Commands

| Command | Description | Example |
|---------|-------------|---------|
| `SET <key> <value>` | Set a key-value pair | `SET A 10` |
| `GET <key>` | Get value by key | `GET A` |
| `UNSET <key>` | Remove a key | `UNSET A` |
| `COUNTS <value>` | Count occurrences of value | `COUNTS 10` |
| `FIND <value>` | Find keys with value | `FIND 10` |
| `BEGIN` | Start transaction | `BEGIN` |
| `COMMIT` | Commit transaction | `COMMIT` |
| `ROLLBACK` | Rollback transaction | `ROLLBACK` |
| `STATUS` | Show transaction depth | `STATUS` |
| `END` | Exit application | `END` |

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd in-memory-db
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Interactive Mode

Start the interactive mode:
```bash
python main.py interactive
```

Example session:
```
> SET A 10
> GET A
10
> BEGIN
> SET A 20
> GET A
20
> ROLLBACK
> GET A
10
> END
```

### Command Line Mode

Use individual commands:
```bash
python main.py set A 10
python main.py get A
python main.py counts 10
python main.py begin
python main.py set A 20
python main.py commit
```

### Transaction Examples

Nested transactions:
```bash
python main.py set A 10
python main.py begin
python main.py set A 20
python main.py begin
python main.py set A 30
python main.py get A
30
python main.py rollback
python main.py get A
20
python main.py commit
python main.py get A
20
```

## Logging

The application logs all operations to daily log files in the `logs/` directory:

- **File**: `logs/db_YYYY-MM-DD.log`
- **Console**: INFO level messages
- **File**: DEBUG level with timestamps

Log format:
```
2024-01-15 10:30:45,123 - inmemory_db - INFO - SET: A = 10
2024-01-15 10:30:46,456 - inmemory_db - INFO - GET: A = 10
2024-01-15 10:30:47,789 - inmemory_db - INFO - BEGIN: New transaction started
```

## Testing

Run the test suite:
```bash
pytest test_main.py -v
```

Run with coverage:
```bash
pytest test_main.py --cov=main --cov-report=html
```

## Project Structure

```
.
├── main.py              # Main application with CLI
├── test_main.py         # Test suite
├── requirements.txt     # Python dependencies
├── .gitignore          # Git ignore patterns
├── README.md           # This file
└── logs/               # Log files directory
    └── db_2024-01-15.log
```

## Dependencies

- **click**: CLI framework
- **pytest**: Testing framework

## Development

### Adding New Commands

1. Add method to `InMemoryDB` class
2. Add CLI command with `@cli.command()`
3. Add logging calls
4. Write tests in `test_main.py`

### Logging Levels

- **DEBUG**: Detailed information for debugging
- **INFO**: General operational messages
- **WARNING**: Warning messages for unusual situations
- **ERROR**: Error messages for exceptions

## License

This project is open source and available under the MIT License.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request 