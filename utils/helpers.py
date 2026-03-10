"""Helper utility functions for the grocery store system"""

from datetime import datetime, timedelta
from typing import Optional, Any
import config


def format_currency(amount: float) -> str:
    """
    Format amount as currency string
    
    Args:
        amount: Amount to format
        
    Returns:
        Formatted currency string
    """
    currency = config.BUSINESS_CONFIG['currency_symbol']
    return f"{currency}{amount:,.2f}"


def format_date(date: datetime, format_str: str = "%Y-%m-%d") -> str:
    """
    Format datetime object as string
    
    Args:
        date: Datetime object
        format_str: Format string
        
    Returns:
        Formatted date string
    """
    if not date:
        return ""
    return date.strftime(format_str)


def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Format datetime object with time
    
    Args:
        dt: Datetime object
        format_str: Format string
        
    Returns:
        Formatted datetime string
    """
    if not dt:
        return ""
    return dt.strftime(format_str)


def parse_date(date_str: str, format_str: str = "%Y-%m-%d") -> Optional[datetime]:
    """
    Parse date string to datetime object
    
    Args:
        date_str: Date string
        format_str: Format string
        
    Returns:
        Datetime object or None
    """
    try:
        return datetime.strptime(date_str, format_str)
    except (ValueError, TypeError):
        return None


def get_date_range(days: int) -> tuple:
    """
    Get date range from today backwards
    
    Args:
        days: Number of days to go back
        
    Returns:
        Tuple of (start_date, end_date) as strings
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    return (
        start_date.strftime("%Y-%m-%d"),
        end_date.strftime("%Y-%m-%d")
    )


def truncate_text(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """
    Truncate text to maximum length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated text
    """
    if not text:
        return ""
    
    text = str(text)
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def safe_float(value: Any, default: float = 0.0) -> float:
    """
    Safely convert value to float
    
    Args:
        value: Value to convert
        default: Default value if conversion fails
        
    Returns:
        Float value
    """
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def safe_int(value: Any, default: int = 0) -> int:
    """
    Safely convert value to int
    
    Args:
        value: Value to convert
        default: Default value if conversion fails
        
    Returns:
        Integer value
    """
    try:
        return int(float(value))
    except (ValueError, TypeError):
        return default


def generate_barcode(prefix: str = "GS", length: int = 10) -> str:
    """
    Generate a simple barcode
    
    Args:
        prefix: Barcode prefix
        length: Total length including prefix
        
    Returns:
        Generated barcode string
    """
    import random
    import string
    
    remaining_length = length - len(prefix)
    if remaining_length <= 0:
        remaining_length = 6
    
    digits = ''.join(random.choices(string.digits, k=remaining_length))
    return f"{prefix}{digits}"


def calculate_percentage(part: float, total: float, decimals: int = 2) -> float:
    """
    Calculate percentage
    
    Args:
        part: Part value
        total: Total value
        decimals: Number of decimal places
        
    Returns:
        Percentage value
    """
    if total == 0:
        return 0.0
    
    percentage = (part / total) * 100
    return round(percentage, decimals)


def calculate_profit_margin(cost: float, price: float, decimals: int = 2) -> float:
    """
    Calculate profit margin percentage
    
    Args:
        cost: Cost price
        price: Selling price
        decimals: Number of decimal places
        
    Returns:
        Profit margin percentage
    """
    if price == 0:
        return 0.0
    
    profit = price - cost
    margin = (profit / price) * 100
    return round(margin, decimals)


def format_phone(phone: str) -> str:
    """
    Format phone number for display
    
    Args:
        phone: Phone number string
        
    Returns:
        Formatted phone number
    """
    if not phone:
        return ""
    
    # Remove all non-digits
    digits = ''.join(filter(str.isdigit, phone))
    
    # Format based on length
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11:
        return f"+{digits[0]} ({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
    else:
        return phone


def is_valid_number(value: str) -> bool:
    """
    Check if string is a valid number
    
    Args:
        value: String to check
        
    Returns:
        Boolean indicating if valid number
    """
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False


def clean_decimal(value: float, places: int = 2) -> float:
    """
    Clean decimal to specific places
    
    Args:
        value: Float value
        places: Decimal places
        
    Returns:
        Cleaned float value
    """
    return round(float(value), places)
