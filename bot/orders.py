from .client import BinanceFuturesClient

class OrderService:
    """
    Service layer for order management
    Handles business logic for placing orders
    """
    
    def __init__(self):
        self.client = BinanceFuturesClient()
    
    def _format_quantity(self, symbol: str, quantity: float) -> float:
        """
        Format quantity to appropriate precision for the symbol
        
        Args:
            symbol: Trading pair
            quantity: Raw quantity
            
        Returns:
            Formatted quantity with correct precision
        """
        # Common precision rules for major pairs
        symbol_upper = symbol.upper()
        
        if symbol_upper in ['BTCUSDT', 'ETHUSDT']:
            # BTC and ETH: 3 decimal places
            return round(quantity, 3)
        elif symbol_upper in ['BNBUSDT', 'ADAUSDT', 'SOLUSDT', 'XRPUSDT']:
            # Most altcoins: 1 decimal place
            return round(quantity, 1)
        else:
            # Default: 3 decimal places
            return round(quantity, 3)
    
    def _format_price(self, price: float) -> float:
        """
        Format price to appropriate precision (2 decimal places for USDT pairs)
        
        Args:
            price: Raw price
            
        Returns:
            Formatted price
        """
        return round(price, 2)
    
    def place_order(self, symbol: str, side: str, order_type: str,
                    quantity: float, price: float = None, stop_price: float = None) -> dict:
        """
        Place an order on Binance Futures
        
        Args:
            symbol: Trading pair (e.g., BTCUSDT)
            side: BUY or SELL
            order_type: MARKET, LIMIT, or STOP
            quantity: Order quantity
            price: Limit price (required for LIMIT and STOP orders)
            stop_price: Stop trigger price (required for STOP orders)
            
        Returns:
            Order response from API
        """
        # Format quantity and price to correct precision
        formatted_quantity = self._format_quantity(symbol, quantity)
        
        params = {
            "symbol": symbol.upper(),
            "side": side.upper(),
            "quantity": formatted_quantity,
        }
        
        if order_type.upper() == "MARKET":
            params["type"] = "MARKET"
            return self.client.send_signed_request("/fapi/v1/order", params)
        
        elif order_type.upper() == "LIMIT":
            params["type"] = "LIMIT"
            params["price"] = self._format_price(price)
            params["timeInForce"] = "GTC"
            return self.client.send_signed_request("/fapi/v1/order", params)
        
        elif order_type.upper() == "STOP":
            # STOP orders use STOP_MARKET type on Binance Futures (no limit price)
            params["type"] = "STOP_MARKET"
            params["stopPrice"] = self._format_price(stop_price)
            # Remove price parameter for STOP_MARKET orders
            return self.client.send_signed_request("/fapi/v1/order", params)
        
        else:
            raise ValueError(f"Unsupported order type: {order_type}")
