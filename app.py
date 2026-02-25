from flask import Flask, render_template, request, jsonify
from bot.orders import OrderService
from bot.validators import validate_order_input
import traceback

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/place-order', methods=['POST'])
def place_order():
    try:
        data = request.json
        print(f"Received data: {data}")  # Debug log
        
        symbol = data.get('symbol', '').strip().upper()
        side = data.get('side')
        order_type = data.get('type')
        quantity = float(data.get('quantity')) if data.get('quantity') else 0
        price = float(data.get('price')) if data.get('price') and data.get('price') != '' else None
        stop_price = float(data.get('stop_price')) if data.get('stop_price') and data.get('stop_price') != '' else None
        
        print(f"Parsed - Symbol: {symbol}, Side: {side}, Type: {order_type}, Qty: {quantity}, Price: {price}, Stop: {stop_price}")
        
        # Basic validation
        if not symbol:
            return jsonify({
                'success': False,
                'error': 'Symbol is required'
            }), 400
        
        validate_order_input(symbol, side, order_type, quantity, price, stop_price)
        
        service = OrderService()
        response = service.place_order(symbol, side, order_type, quantity, price, stop_price)
        
        return jsonify({
            'success': True,
            'data': response
        })
    
    except ValueError as e:
        error_msg = str(e)
        print(f"Validation Error: {error_msg}")
        
        return jsonify({
            'success': False,
            'error': f"Validation Error: {error_msg}"
        }), 400
    
    except Exception as e:
        error_msg = str(e)
        print(f"Error: {error_msg}")
        print(traceback.format_exc())
        
        return jsonify({
            'success': False,
            'error': error_msg
        }), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
