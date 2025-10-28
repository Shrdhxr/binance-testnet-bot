"""
Utility functions for input validation, formatting, and output display.
"""

from rich.console import Console
from rich.table import Table
from typing import Tuple, Optional

console = Console()


def validate_symbol(symbol: str) -> bool:
    """
    Validate trading symbol format.
    
    Args:
        symbol: Trading symbol (e.g., BTCUSDT)
    
    Returns:
        True if valid, False otherwise
    """
    if not symbol or len(symbol) < 6:
        return False
    return symbol.isupper() and symbol.isalpha() or symbol[-4:] == "USDT"


def validate_side(side: str) -> bool:
    """
    Validate order side (BUY or SELL).
    
    Args:
        side: Order side
    
    Returns:
        True if valid, False otherwise
    """
    return side.upper() in ["BUY", "SELL"]


def validate_order_type(order_type: str) -> bool:
    """
    Validate order type (MARKET, LIMIT, STOP_LIMIT).
    
    Args:
        order_type: Type of order
    
    Returns:
        True if valid, False otherwise
    """
    return order_type.upper() in ["MARKET", "LIMIT", "STOP_LIMIT"]


def validate_quantity(quantity: float) -> bool:
    """
    Validate order quantity.
    
    Args:
        quantity: Order quantity
    
    Returns:
        True if valid, False otherwise
    """
    try:
        qty = float(quantity)
        return qty > 0
    except (ValueError, TypeError):
        return False


def validate_price(price: float) -> bool:
    """
    Validate order price.
    
    Args:
        price: Order price
    
    Returns:
        True if valid, False otherwise
    """
    try:
        p = float(price)
        return p > 0
    except (ValueError, TypeError):
        return False


def parse_and_validate_inputs(
    symbol: str,
    side: str,
    order_type: str,
    quantity: str,
    price: Optional[str] = None,
    stop_price: Optional[str] = None,
) -> Tuple[bool, str, dict]:
    """
    Parse and validate all user inputs.
    
    Args:
        symbol: Trading symbol
        side: Order side (BUY/SELL)
        order_type: Order type (MARKET/LIMIT/STOP_LIMIT)
        quantity: Order quantity
        price: Order price (required for LIMIT and STOP_LIMIT)
        stop_price: Stop price (required for STOP_LIMIT)
    
    Returns:
        Tuple of (is_valid, error_message, validated_data)
    """
    errors = []
    
    # Validate symbol
    if not validate_symbol(symbol):
        errors.append("Invalid symbol format (e.g., BTCUSDT)")
    
    # Validate side
    if not validate_side(side):
        errors.append("Side must be BUY or SELL")
    
    # Validate order type
    if not validate_order_type(order_type):
        errors.append("Order type must be MARKET, LIMIT, or STOP_LIMIT")
    
    # Validate quantity
    if not validate_quantity(quantity):
        errors.append("Quantity must be a positive number")
    
    # Validate price for LIMIT and STOP_LIMIT orders
    if order_type.upper() in ["LIMIT", "STOP_LIMIT"]:
        if not price or not validate_price(price):
            errors.append("Price is required and must be positive for LIMIT orders")
    
    # Validate stop price for STOP_LIMIT orders
    if order_type.upper() == "STOP_LIMIT":
        if not stop_price or not validate_price(stop_price):
            errors.append("Stop price is required and must be positive for STOP_LIMIT orders")
    
    if errors:
        return False, " | ".join(errors), {}
    
    validated_data = {
        "symbol": symbol.upper(),
        "side": side.upper(),
        "type": order_type.upper(),
        "quantity": float(quantity),
    }
    
    if price:
        validated_data["price"] = float(price)
    
    if stop_price:
        validated_data["stopPrice"] = float(stop_price)
    
    return True, "", validated_data


def display_success_table(order_data: dict) -> None:
    """
    Display order details in a formatted table.
    
    Args:
        order_data: Order response data from API
    """
    table = Table(title="Order Placed Successfully", show_header=True, header_style="bold green")
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="magenta")
    
    # Extract relevant fields
    fields = {
        "Order ID": order_data.get("orderId", "N/A"),
        "Symbol": order_data.get("symbol", "N/A"),
        "Side": order_data.get("side", "N/A"),
        "Type": order_data.get("type", "N/A"),
        "Quantity": order_data.get("origQty", "N/A"),
        "Price": order_data.get("price", "N/A"),
        "Status": order_data.get("status", "N/A"),
        "Time": order_data.get("time", "N/A"),
    }
    
    for field, value in fields.items():
        table.add_row(field, str(value))
    
    console.print(table)


def display_error(message: str) -> None:
    """
    Display error message in red.
    
    Args:
        message: Error message to display
    """
    console.print(f"[bold red]Error:[/bold red] {message}")


def display_info(message: str) -> None:
    """
    Display info message in blue.
    
    Args:
        message: Info message to display
    """
    console.print(f"[bold blue]Info:[/bold blue] {message}")


def display_success(message: str) -> None:
    """
    Display success message in green.
    
    Args:
        message: Success message to display
    """
    console.print(f"[bold green]Success:[/bold green] {message}")
