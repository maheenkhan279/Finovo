from flask import render_template, request, redirect, url_for, session, jsonify
from games.advanced_portfolio_tool import advanced_portfolio_bp
import random

# Sample stocks for portfolio simulation
AVAILABLE_STOCKS = [
    {'symbol': 'TECH', 'name': 'Tech Corp', 'price': 150.00, 'volatility': 'High', 'sector': 'Technology'},
    {'symbol': 'BANK', 'name': 'Bank Financial', 'price': 75.00, 'volatility': 'Medium', 'sector': 'Finance'},
    {'symbol': 'ENERGY', 'name': 'Energy Power', 'price': 45.00, 'volatility': 'High', 'sector': 'Energy'},
    {'symbol': 'HEALTH', 'name': 'Health Care Inc', 'price': 120.00, 'volatility': 'Low', 'sector': 'Healthcare'},
    {'symbol': 'CONSUMER', 'name': 'Consumer Goods', 'price': 60.00, 'volatility': 'Medium', 'sector': 'Consumer'},
    {'symbol': 'REAL', 'name': 'Real Estate Trust', 'price': 35.00, 'volatility': 'Low', 'sector': 'Real Estate'},
]

def calculate_portfolio_value(portfolio):
    """Calculate total portfolio value"""
    total_value = 0
    for stock in portfolio:
        total_value += stock['shares'] * stock['current_price']
    return round(total_value, 2)

def calculate_diversification_score(portfolio):
    """Calculate diversification score based on sectors"""
    if not portfolio:
        return 0
    
    sectors = {}
    total_value = calculate_portfolio_value(portfolio)
    
    for stock in portfolio:
        sector = stock['sector']
        value = stock['shares'] * stock['current_price']
        sectors[sector] = sectors.get(sector, 0) + value
    
    # Score based on number of sectors and balance
    num_sectors = len(sectors)
    max_sector_pct = max(sectors.values()) / total_value if total_value > 0 else 0
    
    # Ideal: 4+ sectors with no single sector > 40%
    score = min(num_sectors * 15, 60)  # Up to 60 points for sectors
    if max_sector_pct <= 0.4:
        score += 40  # Bonus for balanced allocation
    elif max_sector_pct <= 0.6:
        score += 20
    
    return min(score, 100)

@advanced_portfolio_bp.route('/')
def portfolio_tool():
    """Portfolio Diversification Tool"""
    # Initialize game state
    if 'portfolio_game_state' not in session:
        session['portfolio_game_state'] = {
            'initial_capital': 10000,
            'remaining_capital': 10000,
            'portfolio': [],
            'initial_prices': {stock['symbol']: stock['price'] for stock in AVAILABLE_STOCKS},
            'current_prices': {stock['symbol']: stock['price'] for stock in AVAILABLE_STOCKS},
            'diversification_score': 0,
            'total_value': 10000
        }
    
    game_state = session['portfolio_game_state']
    # Update diversification score
    if game_state['portfolio']:
        game_state['diversification_score'] = calculate_diversification_score(game_state['portfolio'])
        game_state['total_value'] = calculate_portfolio_value(game_state['portfolio'])
    
    return render_template('games/advanced_portfolio_tool.html', 
                         game_state=game_state,
                         available_stocks=AVAILABLE_STOCKS)

@advanced_portfolio_bp.route('/buy_stock', methods=['POST'])
def buy_stock():
    """Buy stock for portfolio"""
    data = request.json
    symbol = data.get('symbol')
    shares = int(data.get('shares', 0))
    
    game_state = session.get('portfolio_game_state', {})
    
    # Find stock
    stock_info = next((s for s in AVAILABLE_STOCKS if s['symbol'] == symbol), None)
    if not stock_info:
        return jsonify({'error': 'Stock not found'}), 400
    
    current_price = game_state['current_prices'].get(symbol, stock_info['price'])
    total_cost = shares * current_price
    
    if total_cost > game_state['remaining_capital']:
        return jsonify({'error': 'Insufficient funds'}), 400
    
    # Add or update stock in portfolio
    portfolio = game_state['portfolio']
    existing = next((s for s in portfolio if s['symbol'] == symbol), None)
    
    if existing:
        existing['shares'] += shares
        existing['current_price'] = current_price
    else:
        portfolio.append({
            'symbol': symbol,
            'name': stock_info['name'],
            'shares': shares,
            'purchase_price': current_price,
            'current_price': current_price,
            'sector': stock_info['sector'],
            'volatility': stock_info['volatility']
        })
    
    game_state['remaining_capital'] -= total_cost
    game_state['portfolio'] = portfolio
    game_state['diversification_score'] = calculate_diversification_score(portfolio)
    game_state['total_value'] = calculate_portfolio_value(portfolio)
    
    session['portfolio_game_state'] = game_state
    return jsonify(game_state)

@advanced_portfolio_bp.route('/sell_stock', methods=['POST'])
def sell_stock():
    """Sell stock from portfolio"""
    data = request.json
    symbol = data.get('symbol')
    shares = int(data.get('shares', 0))
    
    game_state = session.get('portfolio_game_state', {})
    portfolio = game_state['portfolio']
    
    stock = next((s for s in portfolio if s['symbol'] == symbol), None)
    if not stock or stock['shares'] < shares:
        return jsonify({'error': 'Insufficient shares'}), 400
    
    current_price = game_state['current_prices'].get(symbol, stock['current_price'])
    total_value = shares * current_price
    
    stock['shares'] -= shares
    if stock['shares'] == 0:
        portfolio.remove(stock)
    
    game_state['remaining_capital'] += total_value
    game_state['portfolio'] = portfolio
    game_state['diversification_score'] = calculate_diversification_score(portfolio)
    game_state['total_value'] = calculate_portfolio_value(portfolio)
    
    session['portfolio_game_state'] = game_state
    return jsonify(game_state)

@advanced_portfolio_bp.route('/simulate_market', methods=['POST'])
def simulate_market():
    """Simulate market changes"""
    game_state = session.get('portfolio_game_state', {})
    current_prices = game_state['current_prices'].copy()
    
    # Simulate price changes (-10% to +10%)
    for symbol in current_prices:
        change_percent = random.uniform(-0.10, 0.10)
        current_prices[symbol] = round(current_prices[symbol] * (1 + change_percent), 2)
    
    game_state['current_prices'] = current_prices
    
    # Update portfolio prices
    for stock in game_state['portfolio']:
        stock['current_price'] = current_prices.get(stock['symbol'], stock['current_price'])
    
    game_state['total_value'] = calculate_portfolio_value(game_state['portfolio'])
    game_state['diversification_score'] = calculate_diversification_score(game_state['portfolio'])
    
    session['portfolio_game_state'] = game_state
    return jsonify(game_state)

@advanced_portfolio_bp.route('/reset_game', methods=['POST'])
def reset_game():
    """Reset the game"""
    session['portfolio_game_state'] = {
        'initial_capital': 10000,
        'remaining_capital': 10000,
        'portfolio': [],
        'initial_prices': {stock['symbol']: stock['price'] for stock in AVAILABLE_STOCKS},
        'current_prices': {stock['symbol']: stock['price'] for stock in AVAILABLE_STOCKS},
        'diversification_score': 0,
        'total_value': 10000
    }
    return jsonify(session['portfolio_game_state'])

