"""Beginner Savings Challenge — session['savings_game']"""
from flask import render_template, request, session, jsonify
from games.beginner_savings_challenge import beginner_savings_challenge_bp

DEFAULT = {
    'goal': 500,
    'saved': 0,
    'cash': 250,
    'goal_label': 'Emergency fund',
    'invested': 0,
    'streak': 0,
    'last_action': None,
}


def _ensure():
    if 'savings_game' not in session or not isinstance(session.get('savings_game'), dict):
        session['savings_game'] = dict(DEFAULT)
    else:
        for k, v in DEFAULT.items():
            session['savings_game'].setdefault(k, v)
    session.modified = True


def _amount(data):
    try:
        n = float(data.get('amount', 0))
    except (TypeError, ValueError):
        return None
    if n <= 0:
        return None
    return round(min(n, 1_000_000), 2)


@beginner_savings_challenge_bp.route('/')
def savings_page():
    _ensure()
    return render_template('games/savings_challenge.html', game=session['savings_game'])


@beginner_savings_challenge_bp.route('/transact', methods=['POST'])
def transact():
    """JSON: action save|spend|invest|reset|set_goal (+ amount / goal fields)."""
    _ensure()
    data = request.get_json(silent=True) or {}
    action = (data.get('action') or '').lower()
    if action == 'reset':
        session['savings_game'] = dict(DEFAULT)
        session.modified = True
        return jsonify(session['savings_game'])
    if action == 'set_goal':
        st = session['savings_game']
        try:
            g = float(data.get('goal', st.get('goal', 500)))
        except (TypeError, ValueError):
            return jsonify({'error': 'Invalid goal'}), 400
        if g < 50 or g > 1_000_000:
            return jsonify({'error': 'Goal out of range'}), 400
        st['goal'] = round(g, 2)
        label = (data.get('goal_label') or st.get('goal_label') or 'Goal')[:48]
        st['goal_label'] = label
        session['savings_game'] = st
        session.modified = True
        return jsonify(st)
    amt = _amount(data)
    if amt is None and action not in ('reset', 'set_goal'):
        return jsonify({'error': 'Invalid amount'}), 400
    st = session['savings_game']
    prev = st.get('last_action')
    streak = int(st.get('streak', 0) or 0)

    def bump_streak(act):
        nonlocal streak, prev
        if prev == act:
            streak += 1
        else:
            streak = 1
        prev = act
        st['last_action'] = act
        st['streak'] = streak

    if action == 'save':
        move = min(amt, st['cash'])
        st['cash'] = round(st['cash'] - move, 2)
        bonus = 5 if streak >= 3 else 0
        st['saved'] = round(st['saved'] + move + bonus, 2)
        bump_streak('save')
    elif action == 'spend':
        spend = min(amt, st['cash'])
        st['cash'] = round(st['cash'] - spend, 2)
        st['streak'] = 0
        st['last_action'] = 'spend'
    elif action == 'invest':
        move = min(amt, st['cash'])
        st['cash'] = round(st['cash'] - move, 2)
        # Simple educational return: portion grows savings immediately
        growth = round(move * 0.06, 2)
        st['saved'] = round(st['saved'] + move + growth, 2)
        st['invested'] = round(float(st.get('invested', 0) or 0) + move, 2)
        bump_streak('invest')
    else:
        return jsonify({'error': 'Invalid action'}), 400
    session['savings_game'] = st
    session.modified = True
    return jsonify(st)
