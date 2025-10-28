"""
BasicBot class for Binance Futures Testnet trading.
Handles API connection and order placement.
"""

import logging
from binance.um_futures import UMFutures
from binance.exceptions import BinanceAPIException, BinanceRequestException
from config import (
    BINANCE_TESTNET_BASE_URL,
    BINANCE_API_KEY,
    BINANCE_API_SECRET,
)

logger = logging.getLogger(__name__)


class BasicBot:
    """
    A simple trading bot for Binance Futures Testnet.
    Supports MARKET, LIMIT, and STOP_LIMIT orders.
    """
    
    def __init__(self):
        """Initialize the bot with Binance Futures client."""
        try:
            self.client = UMFutures(
                key=BINANCE_API_KEY,
                secret=BINANCE_API_SECRET,
                base_url=BINANCE_TESTNET_BASE_URL,
            )
            logger.info("Binance Futures client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Binance client: {str(e)}")
            raise
    
    def place_market_order(self, symbol: str, side: str, quantity: float) -> dict:
        """
        Place a MARKET order.
        
        Args:
            symbol: Trading symbol (e.g., BTCUSDT)
            side: Order side (BUY or SELL)
            quantity: Order quantity
        
        Returns:
            Order response from API
        
        Raises:
            BinanceAPIException: If API returns an error
            BinanceRequestException: If request fails
        """
        try:
            logger.info(f"Placing MARKET order: {side} {quantity} {symbol}")
            
            order = self.client.new_order(
                symbol=symbol,
                side=side,
                type="MARKET",
                quantity=quantity,
            )
            
            logger.info(f"MARKET order placed successfully: {order}")
            return order
        
        except BinanceAPIException as e:
            logger.error(f"Binance API error: {e.status_code} - {e.message}")
            raise
        except BinanceRequestException as e:
            logger.error(f"Binance request error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error placing MARKET order: {str(e)}")
            raise
    
    def place_limit_order(
        self, symbol: str, side: str, quantity: float, price: float
    ) -> dict:
        """
        Place a LIMIT order.
        
        Args:
            symbol: Trading symbol (e.g., BTCUSDT)
            side: Order side (BUY or SELL)
            quantity: Order quantity
            price: Limit price
        
        Returns:
            Order response from API
        
        Raises:
            BinanceAPIException: If API returns an error
            BinanceRequestException: If request fails
        """
        try:
            logger.info(f"Placing LIMIT order: {side} {quantity} {symbol} @ {price}")
            
            order = self.client.new_order(
                symbol=symbol,
                side=side,
                type="LIMIT",
                timeInForce="GTC",  # Good Till Cancel
                quantity=quantity,
                price=price,
            )
            
            logger.info(f"LIMIT order placed successfully: {order}")
            return order
        
        except BinanceAPIException as e:
            logger.error(f"Binance API error: {e.status_code} - {e.message}")
            raise
        except BinanceRequestException as e:
            logger.error(f"Binance request error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error placing LIMIT order: {str(e)}")
            raise
    
    def place_stop_limit_order(
        self,
        symbol: str,
        side: str,
        quantity: float,
        price: float,
        stop_price: float,
    ) -> dict:
        """
        Place a STOP_LIMIT order.
        
        Args:
            symbol: Trading symbol (e.g., BTCUSDT)
            side: Order side (BUY or SELL)
            quantity: Order quantity
            price: Limit price
            stop_price: Stop price
        
        Returns:
            Order response from API
        
        Raises:
            BinanceAPIException: If API returns an error
            BinanceRequestException: If request fails
        """
        try:
            logger.info(
                f"Placing STOP_LIMIT order: {side} {quantity} {symbol} "
                f"@ {price} (stop: {stop_price})"
            )
            
            order = self.client.new_order(
                symbol=symbol,
                side=side,
                type="STOP",
                timeInForce="GTC",
                quantity=quantity,
                price=price,
                stopPrice=stop_price,
            )
            
            logger.info(f"STOP_LIMIT order placed successfully: {order}")
            return order
        
        except BinanceAPIException as e:
            logger.error(f"Binance API error: {e.status_code} - {e.message}")
            raise
        except BinanceRequestException as e:
            logger.error(f"Binance request error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error placing STOP_LIMIT order: {str(e)}")
            raise
    
    def get_account_info(self) -> dict:
        """
        Get account information.
        
        Returns:
            Account information from API
        """
        try:
            logger.info("Fetching account information")
            account = self.client.account()
            logger.info(f"Account info retrieved: {account}")
            return account
        except Exception as e:
            logger.error(f"Error fetching account info: {str(e)}")
            raise
