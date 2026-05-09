from flask import render_template, request, redirect, url_for, session, jsonify
from games.moderate_insurance_game import moderate_insurance_bp
import random

# Insurance scenarios for the game
INSURANCE_SCENARIOS = [
    {
        'id': 1,
        'scenario': 'You are 25 years old, single, with no dependents. You have a stable job and $5,000 in savings.',
        'options': [
            {'type': 'Basic Health Insurance', 'monthly_cost': 150, 'coverage': 'Low', 'deductible': 5000},
            {'type': 'Comprehensive Health Insurance', 'monthly_cost': 300, 'coverage': 'High', 'deductible': 1000},
            {'type': 'No Insurance', 'monthly_cost': 0, 'coverage': 'None', 'deductible': 0}
        ],
        'correct': 'Basic Health Insurance',
        'explanation': 'At 25 with stable income, basic health insurance provides essential coverage without over-insuring.'
    },
    {
        'id': 2,
        'scenario': 'You are 35, married with 2 children. You own a home worth $300,000 and have a mortgage.',
        'options': [
            {'type': 'Basic Health Insurance', 'monthly_cost': 400, 'coverage': 'Low', 'deductible': 5000},
            {'type': 'Comprehensive Health Insurance', 'monthly_cost': 800, 'coverage': 'High', 'deductible': 1000},
            {'type': 'Life Insurance + Health', 'monthly_cost': 600, 'coverage': 'Medium', 'deductible': 2500}
        ],
        'correct': 'Life Insurance + Health',
        'explanation': 'With dependents and a mortgage, life insurance is crucial to protect your family financially.'
    },
    {
        'id': 3,
        'scenario': 'You are 22, just graduated, starting your first job. You have student loans and minimal savings.',
        'options': [
            {'type': 'Basic Health Insurance', 'monthly_cost': 120, 'coverage': 'Low', 'deductible': 3000},
            {'type': 'Comprehensive Health Insurance', 'monthly_cost': 250, 'coverage': 'High', 'deductible': 500},
            {'type': 'No Insurance', 'monthly_cost': 0, 'coverage': 'None', 'deductible': 0}
        ],
        'correct': 'Basic Health Insurance',
        'explanation': 'Basic insurance provides essential protection while keeping costs manageable for someone starting out.'
    }
]

@moderate_insurance_bp.route('/')
def insurance_game():
    """Insurance Decision Game"""
    # Initialize game state
    if 'insurance_game_state' not in session:
        session['insurance_game_state'] = {
            'current_scenario': 0,
            'score': 0,
            'completed': False,
            'answers': []
        }
    
    game_state = session['insurance_game_state']
    current_scenario_id = game_state['current_scenario']
    
    if current_scenario_id >= len(INSURANCE_SCENARIOS):
        game_state['completed'] = True
        session['insurance_game_state'] = game_state
        return render_template('games/moderate_insurance_game.html', 
                             game_state=game_state,
                             scenario=None,
                             total_scenarios=len(INSURANCE_SCENARIOS))
    
    scenario = INSURANCE_SCENARIOS[current_scenario_id]
    return render_template('games/moderate_insurance_game.html', 
                         game_state=game_state,
                         scenario=scenario,
                         total_scenarios=len(INSURANCE_SCENARIOS))

@moderate_insurance_bp.route('/submit_answer', methods=['POST'])
def submit_answer():
    """Submit insurance decision answer"""
    data = request.json
    selected_option = data.get('selected_option')
    scenario_id = int(data.get('scenario_id', 1)) - 1
    
    if scenario_id < 0 or scenario_id >= len(INSURANCE_SCENARIOS):
        return jsonify({'error': 'Invalid scenario'}), 400
    
    scenario = INSURANCE_SCENARIOS[scenario_id]
    is_correct = selected_option == scenario['correct']
    
    game_state = session.get('insurance_game_state', {})
    if is_correct:
        game_state['score'] = game_state.get('score', 0) + 10
    
    game_state['answers'].append({
        'scenario_id': scenario_id + 1,
        'selected': selected_option,
        'correct': scenario['correct'],
        'is_correct': is_correct,
        'explanation': scenario['explanation']
    })
    
    game_state['current_scenario'] = scenario_id + 1
    
    if game_state['current_scenario'] >= len(INSURANCE_SCENARIOS):
        game_state['completed'] = True
    
    session['insurance_game_state'] = game_state
    return jsonify(game_state)

@moderate_insurance_bp.route('/reset_game', methods=['POST'])
def reset_game():
    """Reset the game"""
    session['insurance_game_state'] = {
        'current_scenario': 0,
        'score': 0,
        'completed': False,
        'answers': []
    }
    return jsonify(session['insurance_game_state'])

