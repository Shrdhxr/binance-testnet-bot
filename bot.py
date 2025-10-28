"""
Main CLI entry point for the Binance Futures Trading Bot.
Handles argument parsing and order execution.
"""

import argparse
import logging
import sys
from logging.handlers import RotatingFileHandler

from basic_bot import BasicBot
from config import LOG_FILE, LOG_FORMAT, LOG_LEVEL, LOG_MAX_BYTES, LOG_BACKUP_COUNT
from utils import (
    parse_and_validate_inputs,
    display_success_table,
    display_error,
    display_info,
    display_success,
)


def setup_logging():
    """Configure logging with rotating file handler."""
    logger = logging.getLogger()
    logger.setLevel(LOG_LEVEL)
    
    # Create rotating file handler
    handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=LOG_MAX_BYTES,
        backupCount=LOG_BACKUP_COUNT,
    )
    handler.setLevel(LOG_LEVEL)
    
    # Create formatter
    formatter = logging.Formatter(LOG_FORMAT)
    handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(handler)
    
    # Also add console handler for INFO and above
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


def main():
    """Main entry point for the trading bot CLI."""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    parser = argparse.ArgumentParser(
        description="Binance Futures Testnet Trading Bot",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python bot.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
  python bot.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.1 --price 2000
  python bot.py --symbol BNBUSDT --side BUY --type STOP_LIMIT --quantity 1 --price 300 --stop-price 295
        """,
    )
    
    parser.add_argument(
        "--symbol",
        type=str,
        required=True,
        help="Trading symbol (e.g., BTCUSDT)",
    )
    parser.add_argument(
        "--side",
        type=str,
        required=True,
        help="Order side: BUY or SELL",
    )
    parser.add_argument(
        "--type",
        type=str,
        required=True,
        help="Order type: MARKET, LIMIT, or STOP_LIMIT",
    )
    parser.add_argument(
        "--quantity",
        type=str,
        required=True,
        help="Order quantity",
    )
    parser.add_argument(
        "--price",
        type=str,
        default=None,
        help="Order price (required for LIMIT and STOP_LIMIT)",
    )
    parser.add_argument(
        "--stop-price",
        type=str,
        default=None,
        help="Stop price (required for STOP_LIMIT)",
    )
    
    args = parser.parse_args()
    
    # Validate inputs
    is_valid, error_msg, validated_data = parse_and_validate_inputs(
        symbol=args.symbol,
        side=args.side,
        order_type=args.type,
        quantity=args.quantity,
        price=args.price,
        stop_price=args.stop_price,
    )
    
    if not is_valid:
        display_error(error_msg)
        logger.error(f"Input validation failed: {error_msg}")
        sys.exit(1)
    
    try:
        # Initialize bot
        display_info("Initializing Binance Futures client...")
        bot = BasicBot()
        
        # Place order based on type
        order_type = validated_data["type"]
        
        if order_type == "MARKET":
            order = bot.place_market_order(
                symbol=validated_data["symbol"],
                side=validated_data["side"],
                quantity=validated_data["quantity"],
            )
        
        elif order_type == "LIMIT":
            order = bot.place_limit_order(
                symbol=validated_data["symbol"],
                side=validated_data["side"],
                quantity=validated_data["quantity"],
                price=validated_data["price"],
            )
        
        elif order_type == "STOP_LIMIT":
            order = bot.place_stop_limit_order(
                symbol=validated_data["symbol"],
                side=validated_data["side"],
                quantity=validated_data["quantity"],
                price=validated_data["price"],
                stop_price=validated_data["stopPrice"],
            )
        
        # Display success
        display_success_table(order)
        display_success("Order placed successfully!")
        logger.info(f"Order execution completed: {order}")
    
    except Exception as e:
        error_message = str(e)
        display_error(error_message)
        logger.error(f"Order execution failed: {error_message}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
