"""Advanced Retirement Road — session['retirement_game'] (simplified projection)."""
from flask import render_template, request, session, jsonify
from games.advanced_retirement_road import advanced_retirement_road_bp


def _grow(start_bal, contrib, years, ret_pct):
    bal = float(start_bal)
    c = float(contrib)
    r = float(ret_pct) / 100.0
    rows = []
    for y in range(1, int(years) + 1):
        bal += c
        bal *= (1.0 + r)
        rows.append({'year': y, 'balance': round(bal, 2)})
    return round(bal, 2), rows


@advanced_retirement_road_bp.route('/')
def retirement_page():
    if 'retirement_game' not in session or not isinstance(session.get('retirement_game'), dict):
        session['retirement_game'] = {
            'starting_balance': 0,
            'annual_contribution': 6000,
            'years': 30,
            'annual_return_pct': 7.0,
            'final_balance': None,
            'sample_years': [],
            'goal': None,
        }
    rg = session['retirement_game']
    if 'goal' not in rg:
        rg['goal'] = None
    if rg.get('final_balance') is not None and not rg.get('all_years'):
        _final, all_rows = _grow(
            rg.get('starting_balance', 0),
            rg.get('annual_contribution', 0),
            rg.get('years', 30),
            rg.get('annual_return_pct', 7.0),
        )
        rg['all_years'] = all_rows
    session.modified = True
    return render_template('games/retirement_road.html', game=session['retirement_game'])


@advanced_retirement_road_bp.route('/simulate', methods=['POST'])
def simulate():
    data = request.get_json(silent=True) or {}
    goal = None
    try:
        sb = max(0.0, float(data.get('starting_balance', 0)))
        ac = max(0.0, float(data.get('annual_contribution', 0)))
        years = int(data.get('years', 30))
        rp = float(data.get('annual_return_pct', 7.0))
        g_raw = data.get('retirement_goal', data.get('goal'))
        if g_raw not in (None, ''):
            goal = max(0.0, float(g_raw))
    except (TypeError, ValueError):
        return jsonify({'error': 'Invalid numbers'}), 400
    if years < 1 or years > 80:
        return jsonify({'error': 'Years must be 1–80'}), 400
    if rp < -20 or rp > 30:
        return jsonify({'error': 'Return % must be −20 to 30'}), 400
    final, all_rows = _grow(sb, ac, years, rp)
    sample = all_rows[-12:] if len(all_rows) > 12 else all_rows
    session['retirement_game'] = {
        'starting_balance': round(sb, 2),
        'annual_contribution': round(ac, 2),
        'years': years,
        'annual_return_pct': rp,
        'final_balance': final,
        'sample_years': sample,
        'total_years_simulated': len(all_rows),
        'goal': goal,
        'all_years': all_rows,
    }
    session.modified = True
    out = dict(session['retirement_game'])
    return jsonify(out)
