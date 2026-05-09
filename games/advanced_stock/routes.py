from flask import render_template, request, jsonify, session
from games.advanced_stock import advanced_bp
import random
import json
from datetime import datetime

# Stock data structure
STOCKS = {
    'CURRENCY': [
        {'symbol': 'EUR-USD', 'name': 'Euro/US Dollar', 'base_price': 1.10},
        {'symbol': 'GBP-USD', 'name': 'British Pound/US Dollar', 'base_price': 1.25},
        {'symbol': 'EUR-GBP', 'name': 'Euro/British Pound', 'base_price': 0.88},
        {'symbol': 'GBP-JPY', 'name': 'British Pound/Japanese Yen', 'base_price': 150.00},
    ],
    'COMPANY': [
        {'symbol': 'AAPL', 'name': 'Apple Inc.', 'base_price': 150.00},
        {'symbol': 'MSFT', 'name': 'Microsoft Corp.', 'base_price': 300.00},
        {'symbol': 'META', 'name': 'Meta Platforms', 'base_price': 250.00},
        {'symbol': 'BMW', 'name': 'BMW Group', 'base_price': 80.00},
    ],
    'ECONOMY': [
        {'symbol': 'FTSE', 'name': 'FTSE 100', 'base_price': 7500.00},
        {'symbol': 'DOW', 'name': 'Dow Jones', 'base_price': 35000.00},
        {'symbol': 'NIKKEI', 'name': 'Nikkei 225', 'base_price': 30000.00},
        {'symbol': 'AUSSIE', 'name': 'Aussie 200', 'base_price': 7000.00},
    ]
}

def generate_stock_prices():
    """Generate current stock prices with random fluctuations"""
    prices = {}
    for category, stocks in STOCKS.items():
        prices[category] = []
        for stock in stocks:
            # Random fluctuation between -5% and +5%
            fluctuation = random.uniform(-0.05, 0.05)
            current_price = stock['base_price'] * (1 + fluctuation)
            change = current_price - stock['base_price']
            change_percent = (change / stock['base_price']) * 100
            
            prices[category].append({
                'symbol': stock['symbol'],
                'name': stock['name'],
                'price': round(current_price, 2),
                'change': round(change, 2),
                'change_percent': round(change_percent, 2),
                'base_price': stock['base_price']
            })
    return prices

@advanced_bp.route('/')
def advanced_game():
    """Start the stock market simulator"""
    # Initialize game state
    if 'stock_game_state' not in session:
        session['stock_game_state'] = {
            'balance': 10000.00,
            'portfolio': {},  # {symbol: {'quantity': int, 'avg_price': float}}
            'history': [],
            'initial_balance': 10000.00
        }
    
    # Generate current stock prices
    current_prices = generate_stock_prices()
    session['current_prices'] = current_prices
    
    game_state = session['stock_game_state']
    
    # Calculate portfolio value
    portfolio_value = calculate_portfolio_value(game_state['portfolio'], current_prices)
    total_value = game_state['balance'] + portfolio_value
    
    return render_template('games/advanced_stock.html',
                         game_state=game_state,
                         current_prices=current_prices,
                         portfolio_value=round(portfolio_value, 2),
                         total_value=round(total_value, 2),
                         stocks=STOCKS)

def calculate_portfolio_value(portfolio, current_prices):
    """Calculate total portfolio value"""
    total = 0.0
    for category, stocks in current_prices.items():
        for stock in stocks:
            symbol = stock['symbol']
            if symbol in portfolio:
                total += portfolio[symbol]['quantity'] * stock['price']
    return total

@advanced_bp.route('/get_prices', methods=['GET'])
def get_prices():
    """Get updated stock prices"""
    current_prices = generate_stock_prices()
    session['current_prices'] = current_prices
    
    game_state = session.get('stock_game_state', {})
    portfolio_value = calculate_portfolio_value(game_state.get('portfolio', {}), current_prices)
    total_value = game_state.get('balance', 10000) + portfolio_value
    
    return jsonify({
        'prices': current_prices,
        'balance': game_state.get('balance', 10000),
        'portfolio_value': round(portfolio_value, 2),
        'total_value': round(total_value, 2)
    })

@advanced_bp.route('/buy', methods=['POST'])
def buy_stock():
    """Buy stock"""
    data = request.json
    symbol = data.get('symbol')
    quantity = int(data.get('quantity', 0))
    
    if quantity <= 0:
        return jsonify({'error': 'Invalid quantity'}), 400
    
    game_state = session.get('stock_game_state', {})
    current_prices = session.get('current_prices', {})
    
    # Find stock price
    stock_price = None
    for category, stocks in current_prices.items():
        for stock in stocks:
            if stock['symbol'] == symbol:
                stock_price = stock['price']
                break
        if stock_price:
            break
    
    if not stock_price:
        return jsonify({'error': 'Stock not found'}), 404
    
    total_cost = stock_price * quantity
    
    if game_state.get('balance', 0) < total_cost:
        return jsonify({'error': 'Insufficient funds'}), 400
    
    # Update balance
    game_state['balance'] -= total_cost
    
    # Update portfolio
    if symbol not in game_state.get('portfolio', {}):
        game_state['portfolio'][symbol] = {'quantity': 0, 'avg_price': 0}
    
    portfolio = game_state['portfolio'][symbol]
    old_quantity = portfolio['quantity']
    old_avg_price = portfolio['avg_price']
    
    # Calculate new average price
    total_invested = (old_quantity * old_avg_price) + total_cost
    new_quantity = old_quantity + quantity
    new_avg_price = total_invested / new_quantity
    
    portfolio['quantity'] = new_quantity
    portfolio['avg_price'] = round(new_avg_price, 2)
    
    # Add to history
    game_state.setdefault('history', []).append({
        'type': 'buy',
        'symbol': symbol,
        'quantity': quantity,
        'price': stock_price,
        'total': total_cost,
        'timestamp': datetime.now().isoformat()
    })
    
    session['stock_game_state'] = game_state
    
    portfolio_value = calculate_portfolio_value(game_state['portfolio'], current_prices)
    total_value = game_state['balance'] + portfolio_value
    
    return jsonify({
        'success': True,
        'balance': round(game_state['balance'], 2),
        'portfolio': game_state['portfolio'],
        'portfolio_value': round(portfolio_value, 2),
        'total_value': round(total_value, 2)
    })

@advanced_bp.route('/sell', methods=['POST'])
def sell_stock():
    """Sell stock"""
    data = request.json
    symbol = data.get('symbol')
    quantity = int(data.get('quantity', 0))
    
    if quantity <= 0:
        return jsonify({'error': 'Invalid quantity'}), 400
    
    game_state = session.get('stock_game_state', {})
    current_prices = session.get('current_prices', {})
    
    if symbol not in game_state.get('portfolio', {}):
        return jsonify({'error': 'Stock not in portfolio'}), 404
    
    portfolio = game_state['portfolio'][symbol]
    
    if portfolio['quantity'] < quantity:
        return jsonify({'error': 'Insufficient shares'}), 400
    
    # Find current stock price
    stock_price = None
    for category, stocks in current_prices.items():
        for stock in stocks:
            if stock['symbol'] == symbol:
                stock_price = stock['price']
                break
        if stock_price:
            break
    
    if not stock_price:
        return jsonify({'error': 'Stock price not found'}), 404
    
    total_revenue = stock_price * quantity
    
    # Update balance
    game_state['balance'] += total_revenue
    
    # Update portfolio
    portfolio['quantity'] -= quantity
    if portfolio['quantity'] == 0:
        del game_state['portfolio'][symbol]
    
    # Calculate profit/loss
    profit_loss = (stock_price - portfolio['avg_price']) * quantity
    
    # Add to history
    game_state.setdefault('history', []).append({
        'type': 'sell',
        'symbol': symbol,
        'quantity': quantity,
        'price': stock_price,
        'total': total_revenue,
        'profit_loss': round(profit_loss, 2),
        'timestamp': datetime.now().isoformat()
    })
    
    session['stock_game_state'] = game_state
    
    portfolio_value = calculate_portfolio_value(game_state.get('portfolio', {}), current_prices)
    total_value = game_state['balance'] + portfolio_value
    
    return jsonify({
        'success': True,
        'balance': round(game_state['balance'], 2),
        'portfolio': game_state.get('portfolio', {}),
        'portfolio_value': round(portfolio_value, 2),
        'total_value': round(total_value, 2),
        'profit_loss': round(profit_loss, 2)
    })

@advanced_bp.route('/reset', methods=['POST'])
def reset_game():
    """Reset the game"""
    session['stock_game_state'] = {
        'balance': 10000.00,
        'portfolio': {},
        'history': [],
        'initial_balance': 10000.00
    }
    return jsonify(session['stock_game_state'])

