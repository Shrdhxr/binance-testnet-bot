"""
Unit tests for utility functions.
"""

import pytest
from utils import (
    validate_symbol,
    validate_side,
    validate_order_type,
    validate_quantity,
    validate_price,
    parse_and_validate_inputs,
)


class TestValidateSymbol:
    """Tests for symbol validation."""
    
    def test_valid_symbol(self):
        assert validate_symbol("BTCUSDT") is True
        assert validate_symbol("ETHUSDT") is True
    
    def test_invalid_symbol_short(self):
        assert validate_symbol("BTC") is False
    
    def test_invalid_symbol_empty(self):
        assert validate_symbol("") is False


class TestValidateSide:
    """Tests for order side validation."""
    
    def test_valid_buy(self):
        assert validate_side("BUY") is True
        assert validate_side("buy") is True
    
    def test_valid_sell(self):
        assert validate_side("SELL") is True
        assert validate_side("sell") is True
    
    def test_invalid_side(self):
        assert validate_side("HOLD") is False
        assert validate_side("") is False


class TestValidateOrderType:
    """Tests for order type validation."""
    
    def test_valid_market(self):
        assert validate_order_type("MARKET") is True
        assert validate_order_type("market") is True
    
    def test_valid_limit(self):
        assert validate_order_type("LIMIT") is True
    
    def test_valid_stop_limit(self):
        assert validate_order_type("STOP_LIMIT") is True
    
    def test_invalid_order_type(self):
        assert validate_order_type("INVALID") is False


class TestValidateQuantity:
    """Tests for quantity validation."""
    
    def test_valid_quantity(self):
        assert validate_quantity(0.001) is True
        assert validate_quantity("1.5") is True
        assert validate_quantity("100") is True
    
    def test_invalid_quantity_zero(self):
        assert validate_quantity(0) is False
        assert validate_quantity("0") is False
    
    def test_invalid_quantity_negative(self):
        assert validate_quantity(-1) is False
        assert validate_quantity("-0.5") is False
    
    def test_invalid_quantity_non_numeric(self):
        assert validate_quantity("abc") is False


class TestValidatePrice:
    """Tests for price validation."""
    
    def test_valid_price(self):
        assert validate_price(100.5) is True
        assert validate_price("50000") is True
    
    def test_invalid_price_zero(self):
        assert validate_price(0) is False
    
    def test_invalid_price_negative(self):
        assert validate_price(-100) is False
    
    def test_invalid_price_non_numeric(self):
        assert validate_price("xyz") is False


class TestParseAndValidateInputs:
    """Tests for complete input validation."""
    
    def test_valid_market_order(self):
        is_valid, error_msg, data = parse_and_validate_inputs(
            symbol="BTCUSDT",
            side="BUY",
            order_type="MARKET",
            quantity="0.001",
        )
        assert is_valid is True
        assert error_msg == ""
        assert data["symbol"] == "BTCUSDT"
        assert data["side"] == "BUY"
        assert data["type"] == "MARKET"
    
    def test_valid_limit_order(self):
        is_valid, error_msg, data = parse_and_validate_inputs(
            symbol="ETHUSDT",
            side="SELL",
            order_type="LIMIT",
            quantity="1.0",
            price="2000",
        )
        assert is_valid is True
        assert data["price"] == 2000.0
    
    def test_invalid_symbol(self):
        is_valid, error_msg, data = parse_and_validate_inputs(
            symbol="BTC",
            side="BUY",
            order_type="MARKET",
            quantity="0.001",
        )
        assert is_valid is False
        assert "Invalid symbol" in error_msg
    
    def test_limit_order_missing_price(self):
        is_valid, error_msg, data = parse_and_validate_inputs(
            symbol="BTCUSDT",
            side="BUY",
            order_type="LIMIT",
            quantity="0.001",
            price=None,
        )
        assert is_valid is False
        assert "Price is required" in error_msg
