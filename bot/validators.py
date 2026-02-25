def validate_order_input(symbol, side, order_type,
                         quantity, price, stop_price):
    """
    Validate order input parameters
    
    Args:
        symbol: Trading pair symbol
        side: BUY or SELL
        order_type: MARKET, LIMIT, or STOP
        quantity: Order quantity
        price: Limit price (required for LIMIT)
        stop_price: Stop price (required for STOP)
    
    Raises:
        ValueError: If validation fails
    """
    if not symbol or not isinstance(symbol, str):
        raise ValueError("Symbol must be a valid string")
    
    if side.upper() not in ["BUY", "SELL"]:
        raise ValueError("Side must be BUY or SELL")
    
    if order_type.upper() not in ["MARKET", "LIMIT", "STOP"]:
        raise ValueError("Order type must be MARKET, LIMIT, or STOP")
    
    if quantity <= 0:
        raise ValueError("Quantity must be greater than 0")
    
    if order_type.upper() == "LIMIT" and not price:
        raise ValueError("Price is required for LIMIT orders")
    
    if order_type.upper() == "LIMIT" and price <= 0:
        raise ValueError("Price must be greater than 0")
    
    if order_type.upper() == "STOP" and not stop_price:
        raise ValueError("Stop price is required for STOP orders")
    
    if order_type.upper() == "STOP" and stop_price <= 0:
        raise ValueError("Stop price must be greater than 0")
