"""Moderate Credit Score Challenge — session['credit_score'] (educational simulation)."""
from flask import render_template, request, session, jsonify
from games.moderate_credit_score import moderate_credit_score_bp

MIN_S, MAX_S = 300, 850

SCENARIOS = [
    {
        'prompt': 'Your credit card bill is due. What do you do?',
        'options': [
            {'key': 'pay_full', 'label': 'Pay the full balance on time', 'delta': 22},
            {'key': 'pay_min', 'label': 'Pay only the minimum', 'delta': -12},
            {'key': 'miss', 'label': 'Skip payment this month', 'delta': -45},
        ],
    },
    {
        'prompt': 'You need a car loan. Which approach is generally better for your credit profile?',
        'options': [
            {'key': 'shop', 'label': 'Compare similar loans within a short window', 'delta': 5},
            {'key': 'cards', 'label': 'Open several new credit cards right before applying', 'delta': -28},
        ],
    },
    {
        'prompt': 'How should you treat your oldest credit card?',
        'options': [
            {'key': 'keep', 'label': 'Keep it open with occasional small use you pay off', 'delta': 15},
            {'key': 'close', 'label': 'Close it because you rarely use it', 'delta': -18},
        ],
    },
]


def _ensure():
    if 'credit_score' not in session or not isinstance(session.get('credit_score'), dict):
        session['credit_score'] = {'score': 680, 'i': 0, 'done': False}
    else:
        session['credit_score'].setdefault('score', 680)
        session['credit_score'].setdefault('i', 0)
        session['credit_score'].setdefault('done', False)
    session.modified = True


def _credit_payload(st):
    out = dict(st)
    out['total'] = len(SCENARIOS)
    if st.get('done') or st.get('i', 0) >= len(SCENARIOS):
        out['scenario'] = None
    else:
        out['scenario'] = SCENARIOS[st['i']]
    return out


@moderate_credit_score_bp.route('/')
def credit_page():
    _ensure()
    st = session['credit_score']
    scen = None if st['done'] or st['i'] >= len(SCENARIOS) else SCENARIOS[st['i']]
    return render_template(
        'games/credit_score.html',
        state=st,
        scenario=scen,
        total=len(SCENARIOS),
    )


@moderate_credit_score_bp.route('/decision', methods=['POST'])
def decision():
    _ensure()
    data = request.get_json(silent=True) or {}
    if data.get('reset'):
        session['credit_score'] = {'score': 680, 'i': 0, 'done': False}
        session.modified = True
        return jsonify(_credit_payload(session['credit_score']))
    st = session['credit_score']
    if st['done']:
        return jsonify(_credit_payload(st))
    if st['i'] >= len(SCENARIOS):
        st['done'] = True
        session.modified = True
        return jsonify(_credit_payload(st))
    key = data.get('option_key')
    scen = SCENARIOS[st['i']]
    opt = next((o for o in scen['options'] if o['key'] == key), None)
    if not opt:
        return jsonify({'error': 'Invalid choice'}), 400
    st['score'] = int(max(MIN_S, min(MAX_S, st['score'] + opt['delta'])))
    st['i'] += 1
    if st['i'] >= len(SCENARIOS):
        st['done'] = True
    session.modified = True
    return jsonify(_credit_payload(st))
