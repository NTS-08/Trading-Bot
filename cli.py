import argparse
from bot.orders import OrderService
from bot.validators import validate_order_input

def print_order_summary(symbol, side, order_type, quantity, price=None):
    """Print order request summary"""
    print("\n" + "="*50)
    print("ORDER REQUEST SUMMARY")
    print("="*50)
    print(f"Symbol:       {symbol}")
    print(f"Side:         {side}")
    print(f"Order Type:   {order_type}")
    print(f"Quantity:     {quantity}")
    if price:
        print(f"Price:        {price}")
    print("="*50)

def print_order_response(response):
    """Print order response details"""
    print("\n" + "="*50)
    print("ORDER RESPONSE DETAILS")
    print("="*50)
    print(f"Order ID:     {response.get('orderId', 'N/A')}")
    print(f"Status:       {response.get('status', 'N/A')}")
    print(f"Symbol:       {response.get('symbol', 'N/A')}")
    print(f"Side:         {response.get('side', 'N/A')}")
    print(f"Type:         {response.get('type', 'N/A')}")
    print(f"Quantity:     {response.get('origQty', 'N/A')}")
    print(f"Executed Qty: {response.get('executedQty', 'N/A')}")
    
    avg_price = response.get('avgPrice', '0')
    if avg_price and float(avg_price) > 0:
        print(f"Avg Price:    {avg_price}")
    
    if response.get('price'):
        print(f"Price:        {response.get('price')}")
    
    print("="*50)

def main():
    parser = argparse.ArgumentParser(
        description="Binance Futures Testnet Trading Bot - Place MARKET and LIMIT orders"
    )
    
    parser.add_argument("--symbol", required=True, help="Trading pair (e.g., BTCUSDT)")
    parser.add_argument("--side", required=True, choices=["BUY", "SELL"], help="Order side: BUY or SELL")
    parser.add_argument("--type", required=True, choices=["MARKET", "LIMIT"], help="Order type: MARKET or LIMIT")
    parser.add_argument("--quantity", required=True, type=float, help="Order quantity")
    parser.add_argument("--price", type=float, help="Limit price (required for LIMIT orders)")
    
    args = parser.parse_args()
    
    try:
        # Validate input
        validate_order_input(
            args.symbol,
            args.side,
            args.type,
            args.quantity,
            args.price,
            None  # stop_price not needed for assignment
        )
        
        # Print order request summary
        print_order_summary(args.symbol, args.side, args.type, args.quantity, args.price)
        
        # Place order
        service = OrderService()
        response = service.place_order(
            args.symbol,
            args.side,
            args.type,
            args.quantity,
            args.price,
            None  # stop_price not needed for assignment
        )
        
        # Print order response details
        print_order_response(response)
        
        # Success message
        print("\nSUCCESS: Order placed successfully!")
        print()
    
    except ValueError as e:
        print(f"\nERROR: Invalid input - {e}")
        exit(1)
    except Exception as e:
        print(f"\nERROR: {e}")
        exit(1)

if __name__ == "__main__":
    main()
