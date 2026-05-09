from flask import render_template, request, redirect, url_for, session, jsonify
from games.moderate_loan_game import moderate_loan_bp
import math

@moderate_loan_bp.route('/')
def loan_game():
    """Loan Repayment Calculator Game"""
    # Initialize game state
    if 'loan_game_state' not in session:
        session['loan_game_state'] = {
            'loan_amount': 10000,
            'interest_rate': 5.0,
            'loan_term_months': 36,
            'monthly_payment': 0,
            'total_interest': 0,
            'total_payment': 0,
            'calculated': False
        }
    
    game_state = session['loan_game_state']
    return render_template('games/moderate_loan_game.html', game_state=game_state)

@moderate_loan_bp.route('/calculate', methods=['POST'])
def calculate_loan():
    """Calculate loan payment"""
    data = request.json
    loan_amount = float(data.get('loan_amount', 10000))
    yearly_interest = float(data.get('interest_rate', 5.0))
    term_months = int(data.get('loan_term_months', 36))
    
    # Calculate monthly payment using amortization formula
    monthly_rate = (yearly_interest / 100) / 12
    if monthly_rate > 0:
        monthly_payment = loan_amount * (monthly_rate / (1 - (1 + monthly_rate) ** (-term_months)))
    else:
        monthly_payment = loan_amount / term_months
    
    total_payment = monthly_payment * term_months
    total_interest = total_payment - loan_amount
    
    game_state = {
        'loan_amount': loan_amount,
        'interest_rate': yearly_interest,
        'loan_term_months': term_months,
        'monthly_payment': round(monthly_payment, 2),
        'total_interest': round(total_interest, 2),
        'total_payment': round(total_payment, 2),
        'calculated': True
    }
    
    session['loan_game_state'] = game_state
    return jsonify(game_state)

@moderate_loan_bp.route('/reset_game', methods=['POST'])
def reset_game():
    """Reset the game"""
    session['loan_game_state'] = {
        'loan_amount': 10000,
        'interest_rate': 5.0,
        'loan_term_months': 36,
        'monthly_payment': 0,
        'total_interest': 0,
        'total_payment': 0,
        'calculated': False
    }
    return jsonify(session['loan_game_state'])

