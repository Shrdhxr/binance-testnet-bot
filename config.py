"""
Configuration module for the Binance Futures Trading Bot.
Handles environment variables, constants, and base configuration.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Project root directory
PROJECT_ROOT = Path(__file__).parent

# Binance API Configuration
BINANCE_TESTNET_BASE_URL = "https://testnet.binancefuture.com"
BINANCE_API_KEY = os.getenv("API_KEY", "")
BINANCE_API_SECRET = os.getenv("API_SECRET", "")

# Logging Configuration
LOG_DIR = PROJECT_ROOT / "logs"
LOG_FILE = LOG_DIR / "bot.log"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LEVEL = "INFO"
LOG_MAX_BYTES = 5 * 1024 * 1024  # 5 MB
LOG_BACKUP_COUNT = 5

# Order Configuration
VALID_ORDER_TYPES = ["MARKET", "LIMIT", "STOP_LIMIT"]
VALID_ORDER_SIDES = ["BUY", "SELL"]
MIN_QUANTITY = 0.001
MIN_PRICE = 0.01

# Create logs directory if it doesn't exist
LOG_DIR.mkdir(exist_ok=True)
