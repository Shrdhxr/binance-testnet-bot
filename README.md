# Binance Futures Testnet Trading Bot

A production-ready Python trading bot for Binance Futures Testnet that supports MARKET, LIMIT, and STOP_LIMIT orders with comprehensive logging and validation.

## Features

- **Multiple Order Types**: MARKET, LIMIT, and STOP_LIMIT orders
- **CLI Interface**: Easy-to-use command-line interface with argparse
- **Input Validation**: Comprehensive validation for all user inputs
- **Logging**: Rotating file handler with detailed request/response/error logging
- **Error Handling**: Graceful error handling with informative messages
- **Rich Output**: Beautiful terminal output using the Rich library
- **Environment Management**: Secure API key management with python-dotenv
- **Testing**: Unit tests for validation logic using pytest
- **Code Quality**: Formatted with black, linted with flake8, sorted with isort

## Project Structure

```
trading_bot/
├── bot.py                 # Main CLI entry point
├── basic_bot.py          # BasicBot class for API interaction
├── config.py             # Configuration and constants
├── utils.py              # Utility functions and validation
├── tests/
│   └── test_utils.py     # Unit tests
├── logs/
│   └── bot.log           # Application logs
├── requirements.txt      # Python dependencies
├── .env.example          # Example environment variables
└── README.md             # This file
```

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd trading_bot
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Credentials

1. Get your Binance Futures Testnet API key and secret from: https://testnet.binancefuture.com/
2. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
3. Edit `.env` and add your credentials:
   ```
   API_KEY=your_testnet_api_key
   API_SECRET=your_testnet_api_secret
   ```

## Usage

### MARKET Order

Place a market buy order for 0.001 BTC:

```bash
python bot.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

### LIMIT Order

Place a limit sell order for 1 ETH at 2000 USDT:

```bash
python bot.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 1.0 --price 2000
```

### STOP_LIMIT Order

Place a stop-limit buy order for 1 BNB at 300 USDT with stop at 295:

```bash
python bot.py --symbol BNBUSDT --side BUY --type STOP_LIMIT --quantity 1 --price 300 --stop-price 295
```

### Get Help

```bash
python bot.py --help
```

## Logging

All API requests, responses, and errors are logged to `logs/bot.log`. The log file uses a rotating handler that:

- Rotates when the file reaches 5 MB
- Keeps up to 5 backup files
- Includes timestamp, log level, and detailed messages

Example log output:

```
2024-01-15 10:30:45,123 - basic_bot - INFO - Binance Futures client initialized successfully
2024-01-15 10:30:46,456 - basic_bot - INFO - Placing MARKET order: BUY 0.001 BTCUSDT
2024-01-15 10:30:47,789 - basic_bot - INFO - MARKET order placed successfully: {'orderId': 123456, ...}
```

## Testing

Run the test suite:

```bash
pytest tests/
```

Run tests with verbose output:

```bash
pytest tests/ -v
```

Run tests with coverage:

```bash
pytest tests/ --cov=.
```

## Code Quality

### Format Code with Black

```bash
black .
```

### Lint Code with Flake8

```bash
flake8 .
```

### Sort Imports with isort

```bash
isort .
```

### Run All Quality Checks

```bash
black . && flake8 . && isort .
```

## Environment Variables

The bot uses the following environment variables (defined in `.env`):

| Variable | Description | Example |
|----------|-------------|---------|
| `API_KEY` | Binance Futures Testnet API Key | `your_api_key` |
| `API_SECRET` | Binance Futures Testnet API Secret | `your_api_secret` |

## API Reference

### BasicBot Methods

#### `place_market_order(symbol, side, quantity)`

Place a market order.

**Parameters:**
- `symbol` (str): Trading symbol (e.g., BTCUSDT)
- `side` (str): BUY or SELL
- `quantity` (float): Order quantity

**Returns:** Order response dict

#### `place_limit_order(symbol, side, quantity, price)`

Place a limit order.

**Parameters:**
- `symbol` (str): Trading symbol
- `side` (str): BUY or SELL
- `quantity` (float): Order quantity
- `price` (float): Limit price

**Returns:** Order response dict

#### `place_stop_limit_order(symbol, side, quantity, price, stop_price)`

Place a stop-limit order.

**Parameters:**
- `symbol` (str): Trading symbol
- `side` (str): BUY or SELL
- `quantity` (float): Order quantity
- `price` (float): Limit price
- `stop_price` (float): Stop price

**Returns:** Order response dict

## Error Handling

The bot handles various error scenarios:

- **Validation Errors**: Invalid input parameters are caught and reported
- **API Errors**: Binance API errors are logged with status codes and messages
- **Network Errors**: Connection issues are caught and logged
- **Unexpected Errors**: All exceptions are logged with full tracebacks

## Example Log File

```
2024-01-15 10:30:45,123 - __main__ - INFO - Initializing Binance Futures client...
2024-01-15 10:30:45,456 - basic_bot - INFO - Binance Futures client initialized successfully
2024-01-15 10:30:46,789 - basic_bot - INFO - Placing MARKET order: BUY 0.001 BTCUSDT
2024-01-15 10:30:47,012 - basic_bot - INFO - MARKET order placed successfully: {'orderId': 12345678, 'symbol': 'BTCUSDT', 'side': 'BUY', 'type': 'MARKET', 'origQty': '0.001', 'price': '0', 'status': 'FILLED', 'time': 1705318247012}
2024-01-15 10:30:47,345 - __main__ - INFO - Order execution completed: {'orderId': 12345678, ...}
```

## Troubleshooting

### "API key or secret is invalid"

- Verify your API credentials in `.env`
- Ensure you're using testnet credentials from https://testnet.binancefuture.com/
- Check that there are no extra spaces in your `.env` file

### "Connection refused"

- Verify your internet connection
- Check that Binance Futures Testnet is accessible
- Review the logs in `logs/bot.log` for detailed error messages

### "Invalid symbol"

- Ensure the symbol is in the correct format (e.g., BTCUSDT)
- Verify the symbol is available on Binance Futures Testnet

## Notes

- This bot is designed for the **Binance Futures Testnet** only
- Always test thoroughly before using with real funds
- The bot uses GTC (Good Till Cancel) for limit orders
- All prices and quantities should be positive numbers
- Logging is configured to rotate at 5 MB to prevent excessive disk usage

## Support

For issues or questions:
1. Check the logs in `logs/bot.log`
2. Review the error messages in the terminal
3. Verify your API credentials and network connection
4. Consult the Binance API documentation: https://binance-docs.github.io/apidocs/futures/en/
