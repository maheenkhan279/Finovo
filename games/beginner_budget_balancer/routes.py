from flask import render_template, request, redirect, url_for, session, jsonify
from games.beginner_budget_balancer import beginner_budget_bp
import random

# Game constants
TOTAL_MONTHS = 12
INFLATION_RATE = 0.03  # 3% per month

SPENDING_OPTIONS = {
    "HOUSING": [
        {"label": "Room Share (Low)", "cost": 950},
        {"label": "Studio Apartment (Mid)", "cost": 1300},
        {"label": "One-Bedroom (High)", "cost": 1700},
    ],
    "FOOD": [
        {"label": "Basic (Ramen & Staples)", "cost": 350},
        {"label": "Average (Groceries + Occasional Takeout)", "cost": 550},
        {"label": "Gourmet (Dining Out Often)", "cost": 850},
    ],
    "UTILITIES": [
        {"label": "Fixed Bills", "cost": 175},
    ],
    "ENTERTAINMENT": [
        {"label": "Skip (Free)", "cost": 0},
        {"label": "Movie Night", "cost": 50},
        {"label": "Concert/Event", "cost": 150},
    ],
}

NEGATIVE_EVENTS = [
    ("Car broke down — mechanic cost", 300),
    ("Medical bill — urgent visit", 200),
    ("Lost wallet — lost cash", 150),
    ("Phone screen repair", 100),
    ("Unexpected bank fee", 50),
]

POSITIVE_EVENTS = [
    ("Tax refund received", 200),
    ("Gift from friend", 100),
    ("Sold old bike", 150)
]

def cost_for(category_key, label):
    for item in SPENDING_OPTIONS[category_key]:
        if item["label"] == label:
            return item["cost"]
    return 0

def inflated_cost(base, month_index):
    return round(base * ((1 + INFLATION_RATE) ** month_index), 2)

def random_event():
    chance = random.random()
    if chance < 0.75:  # 75% chance of negative event
        desc, amount = random.choice(NEGATIVE_EVENTS)
        return {"type": "negative", "desc": desc, "amount": amount}
    elif chance < 0.98:  # 23% chance of positive event
        desc, amount = random.choice(POSITIVE_EVENTS)
        return {"type": "positive", "desc": desc, "amount": amount}
    else:
        return {"type": "none", "desc": "No random event", "amount": 0}

@beginner_budget_bp.route('/')
def beginner_budget_game():
    """Start the beginner budget balancer game"""
    # Initialize game state
    if 'budget_game_state' not in session:
        session['budget_game_state'] = {
            'player_balance': 1000,
            'current_month': 1,
            'phase': 'await_income',
            'history': [],
            'choices': {
                'HOUSING': SPENDING_OPTIONS['HOUSING'][0]['label'],
                'FOOD': SPENDING_OPTIONS['FOOD'][1]['label'],
                'UTILITIES': SPENDING_OPTIONS['UTILITIES'][0]['label'],
                'ENTERTAINMENT': SPENDING_OPTIONS['ENTERTAINMENT'][0]['label'],
            },
            'starting_balance': 1000,
            'monthly_income': 2500
        }
    
    game_state = session['budget_game_state']
    return render_template('games/beginner_budget_balancer.html', 
                         game_state=game_state,
                         spending_options=SPENDING_OPTIONS,
                         total_months=TOTAL_MONTHS)

@beginner_budget_bp.route('/receive_income', methods=['POST'])
def receive_income():
    """Receive monthly income"""
    game_state = session.get('budget_game_state', {})
    if game_state.get('phase') == 'await_income':
        game_state['player_balance'] += game_state.get('monthly_income', 2500)
        game_state['phase'] = 'await_choices'
        session['budget_game_state'] = game_state
    return jsonify(game_state)

@beginner_budget_bp.route('/simulate_month', methods=['POST'])
def simulate_month():
    """Simulate the current month"""
    game_state = session.get('budget_game_state', {})
    
    if game_state.get('phase') != 'await_choices':
        return jsonify({'error': 'Invalid phase'}), 400
    
    current_month = game_state['current_month']
    month_index = current_month - 1
    
    # Calculate monthly spending
    monthly_spending = sum(
        inflated_cost(cost_for(cat, game_state['choices'][cat]), month_index)
        for cat in SPENDING_OPTIONS.keys()
    )
    
    game_state['player_balance'] -= monthly_spending
    
    # Random event
    event = random_event()
    if event['type'] == 'negative':
        game_state['player_balance'] -= event['amount']
    elif event['type'] == 'positive':
        game_state['player_balance'] += event['amount']
    
    # Create summary
    summary = {
        'month': current_month,
        'housing': game_state['choices']['HOUSING'],
        'food': game_state['choices']['FOOD'],
        'utilities': game_state['choices']['UTILITIES'],
        'entertainment': game_state['choices']['ENTERTAINMENT'],
        'spending_total': monthly_spending,
        'event': event['desc'],
        'event_type': event['type'],
        'event_amount': event['amount'],
        'end_balance': game_state['player_balance']
    }
    
    # Update history
    game_state['history'].append(summary)
    
    # Determine next phase
    if game_state['player_balance'] <= 0:
        game_state['phase'] = 'lost'
    elif current_month >= TOTAL_MONTHS:
        game_state['phase'] = 'won'
    else:
        game_state['phase'] = 'simulated'
    
    session['budget_game_state'] = game_state
    return jsonify(game_state)

@beginner_budget_bp.route('/next_month', methods=['POST'])
def next_month():
    """Move to next month"""
    game_state = session.get('budget_game_state', {})
    
    if game_state.get('phase') == 'simulated':
        game_state['current_month'] += 1
        game_state['phase'] = 'await_income'
        session['budget_game_state'] = game_state
    
    return jsonify(game_state)

@beginner_budget_bp.route('/update_choice', methods=['POST'])
def update_choice():
    """Update spending choice"""
    data = request.json
    game_state = session.get('budget_game_state', {})
    
    category = data.get('category')
    choice = data.get('choice')
    
    if category in game_state.get('choices', {}):
        game_state['choices'][category] = choice
        session['budget_game_state'] = game_state
    
    return jsonify(game_state)

@beginner_budget_bp.route('/reset_game', methods=['POST'])
def reset_game():
    """Reset the game"""
    session['budget_game_state'] = {
        'player_balance': 1000,
        'current_month': 1,
        'phase': 'await_income',
        'history': [],
        'choices': {
            'HOUSING': SPENDING_OPTIONS['HOUSING'][0]['label'],
            'FOOD': SPENDING_OPTIONS['FOOD'][1]['label'],
            'UTILITIES': SPENDING_OPTIONS['UTILITIES'][0]['label'],
            'ENTERTAINMENT': SPENDING_OPTIONS['ENTERTAINMENT'][0]['label'],
        },
        'starting_balance': 1000,
        'monthly_income': 2500
    }
    return jsonify(session['budget_game_state'])

