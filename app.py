from flask import Flask, render_template, request, redirect, url_for, session, g, flash, jsonify
from werkzeug.urls import url_parse
import os
import random
import json
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'finovo-secret-key-2024'

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'finovo.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
from models import db, User
db.init_app(app)

# Create tables on first run
with app.app_context():
    db.create_all()

# Import authentication utilities
from auth import login_required, load_logged_in_user

# Session timeout configuration - Security feature
# Auto-logout users after 5 minutes of inactivity to prevent unauthorized access
SESSION_TIMEOUT_MINUTES = 5

# Load user before each request
@app.before_request
def load_user():
    # Temporarily disabled session timeout to fix redirect loop
    # TODO: Re-enable after fixing authentication issues
    load_logged_in_user()

# Import game modules
from games.beginner_quiz import beginner_bp
from games.beginner_budget_balancer import beginner_budget_bp
from games.moderate_budget import moderate_bp
from games.moderate_loan_game import moderate_loan_bp
from games.moderate_insurance_game import moderate_insurance_bp
from games.advanced_stock import advanced_bp
from games.advanced_portfolio_tool import advanced_portfolio_bp
from games.beginner_savings_challenge import beginner_savings_challenge_bp
from games.moderate_credit_score import moderate_credit_score_bp
from games.advanced_retirement_road import advanced_retirement_road_bp

# Register blueprints
# Beginner level games
app.register_blueprint(beginner_bp, url_prefix='/games/beginner')
app.register_blueprint(beginner_budget_bp, url_prefix='/games/beginner/budget-balancer')
app.register_blueprint(beginner_savings_challenge_bp, url_prefix='/games/beginner/savings-challenge')

# Moderate level games
app.register_blueprint(moderate_bp, url_prefix='/games/moderate')
app.register_blueprint(moderate_loan_bp, url_prefix='/games/moderate/loan')
app.register_blueprint(moderate_insurance_bp, url_prefix='/games/moderate/insurance')
app.register_blueprint(moderate_credit_score_bp, url_prefix='/games/moderate/credit-score')

# Advanced level games
app.register_blueprint(advanced_bp, url_prefix='/games/advanced')
app.register_blueprint(advanced_portfolio_bp, url_prefix='/games/advanced/portfolio')
app.register_blueprint(advanced_retirement_road_bp, url_prefix='/games/advanced/retirement-road')


@app.context_processor
def inject_nav_games():
    """
    Navbar Financial Games menu: grouped labels -> (title, url) pairs.
    URLs are generated with url_for (actual routes use /games/... prefixes).
    """
    games = {
        'Beginner': [
            ('Quiz', url_for('beginner_bp.beginner_game')),
            ('Budget Balancer', url_for('beginner_budget_bp.beginner_budget_game')),
            ('Savings Challenge', url_for('beginner_savings_challenge_bp.savings_page')),
        ],
        'Moderate': [
            ('Budget Game', url_for('moderate_bp.moderate_game')),
            ('Loan Game', url_for('moderate_loan_bp.loan_game')),
            ('Insurance Game', url_for('moderate_insurance_bp.insurance_game')),
            ('Credit Score Challenge', url_for('moderate_credit_score_bp.credit_page')),
        ],
        'Advanced': [
            ('Stock Simulator', url_for('advanced_bp.advanced_game')),
            ('Portfolio Tool', url_for('advanced_portfolio_bp.portfolio_tool')),
            ('Retirement Road', url_for('advanced_retirement_road_bp.retirement_page')),
        ],
    }
    nav_game_blueprints = {
        'beginner_bp',
        'beginner_budget_bp',
        'beginner_savings_challenge_bp',
        'moderate_bp',
        'moderate_loan_bp',
        'moderate_insurance_bp',
        'moderate_credit_score_bp',
        'advanced_bp',
        'advanced_portfolio_bp',
        'advanced_retirement_road_bp',
    }
    return dict(games=games, nav_game_blueprints=nav_game_blueprints)


@app.route('/')
def home():
    """Main homepage"""
    return render_template('home.html')

@app.route('/games')
def games():
    """Financial Games page listing all games"""
    return render_template('games.html')

@app.route('/dashboard')
def dashboard():
    """User dashboard with results and progress"""
    return render_template('dashboard.html')

@app.route('/beginner_shopping_game')
def beginner_shopping_game():
    """Beginner level shopping adventure game"""
    return render_template('beginner_shopping_game.html')

@app.route('/needs-vs-wants')
def needs_vs_wants_game():
    """Interactive Needs vs Wants classification game"""
    return render_template('needs_vs_wants_interactive.html')

@app.route('/needs_vs_wants_game')
def needs_vs_wants_game_old():
    """Interactive Needs vs Wants classification game"""
    return render_template('needs_vs_wants_interactive.html')

@app.route('/budget-balancer')
def budget_balancer_game():
    """Interactive Budget Balancer simulation game"""
    return render_template('budget_balancer_interactive.html')

@app.route('/budget_balancer_game')
def budget_balancer_game_old():
    """Interactive Budget Balancer simulation game"""
    return render_template('budget_balancer_interactive.html')

@app.route('/savings-challenge')
def savings_challenge_game():
    """Interactive Savings Challenge decision game"""
    return render_template('savings_challenge_interactive.html')

@app.route('/savings_challenge_game')
def savings_challenge_game_old():
    """Interactive Savings Challenge decision game"""
    return render_template('savings_challenge_interactive.html')

# Moderate Level Games
@app.route('/loan-repayment')
def moderate_loan_game():
    """Loan Management game"""
    return render_template('moderate_loan_game.html')

@app.route('/loan-repayment-game')
def moderate_loan_game_old():
    """Loan Management game"""
    return render_template('moderate_loan_game.html')

@app.route('/credit-score')
def moderate_credit_score_game():
    """Credit Score Challenge game"""
    return render_template('moderate_credit_score_game.html')

@app.route('/credit-score-game')
def moderate_credit_score_game_old():
    """Credit Score Challenge game"""
    return render_template('moderate_credit_score_game.html')

@app.route('/insurance')
def moderate_insurance_game():
    """Insurance Planning game"""
    return render_template('moderate_insurance_game.html')

@app.route('/insurance-game')
def moderate_insurance_game_old():
    """Insurance Planning game"""
    return render_template('moderate_insurance_game.html')

# Advanced Level Games
@app.route('/stock-simulator')
def advanced_stock_game():
    """Stock Market game"""
    return render_template('advanced_stock_game.html')

@app.route('/stock-simulator-game')
def advanced_stock_game_old():
    """Stock Market game"""
    return render_template('advanced_stock_game.html')

@app.route('/portfolio')
def advanced_portfolio_tool():
    """Portfolio Management game"""
    return render_template('advanced_portfolio_tool.html')

@app.route('/portfolio-tool')
def advanced_portfolio_tool_old():
    """Portfolio Management game"""
    return render_template('advanced_portfolio_tool.html')

@app.route('/retirement')
def retirement_road():
    """Retirement Planning game"""
    return render_template('retirement_road.html')

@app.route('/retirement-road')
def retirement_road_old():
    """Retirement Planning game"""
    return render_template('retirement_road.html')

@app.route('/loan_repayment_quest')
def loan_repayment_quest():
    """Interactive Loan Repayment Quest simulation game"""
    return render_template('loan_repayment_quest.html')

@app.route('/credit_score_challenge')
def credit_score_challenge():
    """Interactive Credit Score Challenge decision game"""
    return render_template('credit_score_challenge.html')

@app.route('/insurance_inspector')
def insurance_inspector():
    """Interactive Insurance Inspector scenario game"""
    return render_template('insurance_inspector.html')

@app.route('/stock_market_simulator')
def stock_market_simulator():
    """Interactive Stock Market Simulator game"""
    return render_template('stock_market_simulator.html')

@app.route('/portfolio_diversifier')
def portfolio_diversifier():
    """Interactive Portfolio Diversifier game"""
    return render_template('portfolio_diversifier.html')


# Authentication routes
@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validation
        errors = []
        if not username:
            errors.append('Username is required')
        if not email:
            errors.append('Email is required')
        if not password:
            errors.append('Password is required')
        if password != confirm_password:
            errors.append('Passwords do not match')
        if len(password) < 6:
            errors.append('Password must be at least 6 characters')
        
        # Check if username or email already exists
        if User.query.filter_by(username=username).first():
            errors.append('Username already exists')
        if User.query.filter_by(email=email).first():
            errors.append('Email already registered')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('register.html')
        
        # Create new user
        try:
            print(f"DEBUG: Creating user - username: '{username}', email: '{email}'")
            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            print(f"DEBUG: User created successfully - ID: {user.id}")
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('Registration failed. Please try again.', 'error')
            return render_template('register.html')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        print(f"DEBUG: Login attempt - username: '{username}', password length: {len(password)}")
        
        if not username or not password:
            flash('Please enter both username and password', 'error')
            return render_template('login.html')
        
        # Find user by username
        user = User.query.filter_by(username=username).first()
        print(f"DEBUG: User found: {user is not None}")
        
        if user:
            print(f"DEBUG: User details - ID: {user.id}, Email: {user.email}")
            password_check = user.check_password(password)
            print(f"DEBUG: Password check result: {password_check}")
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session.permanent = True
            # Set last activity time for session timeout tracking
            session['last_activity'] = datetime.now().isoformat()
            print(f"DEBUG: Session created - user_id: {session.get('user_id')}, permanent: {session.permanent}")
            flash(f'Welcome back, {user.username}!', 'success')
            
            # Redirect to next page or games
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('games')
            print(f"DEBUG: Redirecting to: {next_page}")
            return redirect(next_page)
        else:
            # More specific error message
            if not user:
                print(f"DEBUG: No user found with username '{username}'")
                flash(f'No account found with username "{username}". Please check your username or register for a new account.', 'error')
            else:
                print(f"DEBUG: Password mismatch for user '{username}'")
                flash('Incorrect password. Please try again.', 'error')
            return render_template('login.html')
    
    return render_template('login.html')

@app.route('/store_session', methods=['POST'])
def store_session():
    """Store user session data for game saving"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        email = data.get('email')
        
        print(f"DEBUG: Storing session - user_id: {user_id}, email: {email}")
        
        # Store in Flask session
        session['user_id'] = user_id
        session['user_email'] = email
        session['last_activity'] = datetime.now().isoformat()
        
        return jsonify({
            'success': True,
            'message': 'Session stored successfully'
        })
        
    except Exception as e:
        print(f"DEBUG: Session storage error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/debug/users')
def debug_users():
    """Debug route to check existing users"""
    users = User.query.all()
    user_list = []
    for user in users:
        user_list.append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'has_password_hash': bool(user.password_hash)
        })
    return {'users': user_list, 'total_count': len(user_list)}

@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out successfully', 'success')
    return redirect(url_for('home'))

# Informational pages
@app.route('/about')
def about():
    """About FINOVO page"""
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page with form"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        message = request.form.get('message', '').strip()
        
        # Validation
        errors = []
        if not name:
            errors.append('Name is required')
        if not email:
            errors.append('Email is required')
        elif '@' not in email:
            errors.append('Please enter a valid email address')
        if not message:
            errors.append('Message is required')
        elif len(message) < 10:
            errors.append('Message must be at least 10 characters')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('contact.html', name=name, email=email, message=message)
        
        # Success - in a real app, you would send an email here
        flash('Thank you for your message! We will get back to you soon.', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html')

@app.route('/financial-tips')
def financial_tips():
    """Financial Tips & Resources page"""
    return render_template('financial_tips.html')

@app.route('/expense-tracking')
def expense_tracking():
    """Expense Tracking Overview page"""
    return render_template('expense_tracking.html')

@app.route('/demo')
def demo():
    """Demo/Help page explaining how to use FINOVO games"""
    return render_template('demo.html')


def _sf(val, default=None):
    try:
        return float(val)
    except (TypeError, ValueError):
        return default


def _si(val, default=None):
    try:
        return int(val)
    except (TypeError, ValueError):
        return default


def loan_monthly_payment(principal, annual_rate_pct, years):
    """Fixed-rate amortizing loan: monthly payment."""
    if principal is None or years is None or principal <= 0 or years <= 0:
        return None
    n = max(1, int(years * 12))
    r = (float(annual_rate_pct) / 100.0) / 12.0 if annual_rate_pct is not None else 0
    if r <= 0:
        return round(principal / n, 2)
    factor = (1 + r) ** n
    pay = principal * (r * factor) / (factor - 1)
    return round(pay, 2)


def investment_lump_sum_fv(initial, years, annual_rate_pct=7.0):
    if initial is None or years is None or initial < 0 or years < 0:
        return None
    r = float(annual_rate_pct) / 100.0
    return round(initial * ((1 + r) ** years), 2)


def retirement_basic_projection(starting, annual_contrib, years, annual_rate_pct=7.0):
    """Year-end: add contribution then apply return (matches retirement game style)."""
    if starting is None or annual_contrib is None or years is None:
        return None
    years = int(years)
    if years < 1:
        return None
    bal = float(starting)
    c = float(annual_contrib)
    r = float(annual_rate_pct) / 100.0
    for _ in range(years):
        bal += c
        bal *= (1.0 + r)
    return round(bal, 2)


def build_ai_insight_context(sess):
    """Rule-based advisor context from Flask session game keys (prototype)."""
    strengths = []
    weaknesses = []
    recommendations = []
    tips = []
    score_parts = []
    completed_games = 0
    seen_urls = set()

    def add_rec(label, endpoint):
        u = url_for(endpoint) if isinstance(endpoint, str) and '.' in endpoint else endpoint
        if u not in seen_urls:
            seen_urls.add(u)
            recommendations.append({'label': label, 'url': u})

    # Needs vs Wants Quiz
    if sess.get('quiz_completed'):
        completed_games += 1
        qs = int(sess.get('quiz_score', 0))
        score_parts.append(min(100, qs))
        if qs >= 80:
            strengths.append('Strong basics on needs vs wants (high quiz score).')
        elif qs >= 60:
            strengths.append('Quiz completed with a workable grasp of needs vs wants.')
        else:
            weaknesses.append('Quiz score is low—replay scenarios to sharpen basics.')
            add_rec('Needs vs Wants Quiz', 'beginner_bp.beginner_game')
    else:
        weaknesses.append('Complete the Needs vs Wants quiz to benchmark your foundations.')
        add_rec('Start the Quiz', 'beginner_bp.beginner_game')

    # Savings Challenge (only score if user has actually moved money into savings)
    sg = sess.get('savings_game')
    if isinstance(sg, dict) and float(sg.get('saved') or 0) > 0:
        completed_games += 1
        goal = float(sg.get('goal') or 500)
        saved = float(sg.get('saved') or 0)
        ratio = (saved / goal) if goal else 0.0
        score_parts.append(min(100, ratio * 100))
        if ratio >= 0.75:
            strengths.append('Savings Challenge: strong progress toward the practice savings goal.')
        elif ratio < 0.35:
            weaknesses.append('Savings Challenge: savings are still far from the goal—practice paying yourself first.')
            add_rec('Savings Challenge', 'beginner_savings_challenge_bp.savings_page')
            tips.append('Try saving at least 20% of your income when your budget allows.')

    # Beginner budget
    bg = sess.get('budget_game_state')
    if isinstance(bg, dict) and (bg.get('history') or bg.get('phase') not in (None, 'await_income')):
        completed_games += 1
        ph = bg.get('phase')
        if ph == 'won':
            strengths.append('Beginner Budget Balancer: finished with a positive balance.')
            score_parts.append(85)
        elif ph == 'lost':
            weaknesses.append('Beginner Budget Balancer: you ran out of funds—tighten variable spending.')
            add_rec('Budget Balancer (Beginner)', 'beginner_budget_bp.beginner_budget_game')
            score_parts.append(38)
            tips.append('Reduce unnecessary expenses and cover needs before wants.')
        else:
            score_parts.append(55)

    # Moderate budget
    mg = sess.get('game_state')
    if isinstance(mg, dict) and mg.get('player_balance') is not None and (
        mg.get('history') or mg.get('phase') not in (None, 'await_income')
    ):
        completed_games += 1
        ph = mg.get('phase')
        if ph == 'won':
            strengths.append('Moderate budget game: completed the cycle successfully.')
            score_parts.append(88)
        elif ph == 'lost':
            weaknesses.append('Moderate budget: negative balance—revisit trade-offs and shocks.')
            add_rec('Moderate Budget Game', 'moderate_bp.moderate_game')
            score_parts.append(40)
            tips.append('Reduce unnecessary expenses and keep a buffer for surprises.')
        else:
            score_parts.append(58)

    # Credit challenge
    cr = sess.get('credit_score')
    if isinstance(cr, dict) and (cr.get('done') or int(cr.get('i') or 0) > 0):
        completed_games += 1
        sc = int(cr.get('score', 680))
        score_parts.append(min(100, max(0, (sc - 500) / 3.5)))
        if cr.get('done') and sc >= 720:
            strengths.append('Credit scenarios: healthy simulated score from your choices.')
        elif cr.get('done') and sc < 660:
            weaknesses.append('Simulated credit score is weak—focus on on-time payments and lower utilization.')
            add_rec('Credit Score Challenge', 'moderate_credit_score_bp.credit_page')

    # Insurance
    ins = sess.get('insurance_game_state')
    if isinstance(ins, dict) and int(ins.get('score', 0)) > 0:
        completed_games += 1
        isc = int(ins.get('score', 0))
        score_parts.append(min(100, isc * 2.5))
        if isc >= 30:
            strengths.append('Insurance game: solid choices on scenario coverage.')
        elif isc < 20:
            weaknesses.append('Insurance scenarios: several mismatches—review when coverage matters.')
            add_rec('Insurance Game', 'moderate_insurance_bp.insurance_game')

    # Stock simulator
    st = sess.get('stock_game_state')
    if isinstance(st, dict):
        hist = st.get('history') or []
        port = st.get('portfolio') or {}
        traded = len(hist) >= 1 or any(
            isinstance(v, dict) and int(v.get('quantity') or 0) > 0
            for v in port.values()
        )
        if traded:
            completed_games += 1
        naive_score = 72 if traded else 52
        if traded:
            strengths.append('Stock simulator: you have explored trades and positions.')
        else:
            weaknesses.append('Stock simulator: little or no activity yet—practice buys/sells to learn risk.')
            add_rec('Stock Simulator', 'advanced_bp.advanced_game')
            tips.append('Start investing early for long-term growth—with small amounts in learning mode here.')
        score_parts.append(naive_score)

    # Portfolio tool
    pt = sess.get('portfolio_game_state')
    if isinstance(pt, dict) and pt.get('diversification_score') is not None:
        completed_games += 1
        div = float(pt.get('diversification_score', 0))
        score_parts.append(div)
        if div >= 65:
            strengths.append('Portfolio tool: diversification score looks healthy.')
        elif div < 40:
            weaknesses.append('Portfolio tool: concentration risk—spread across more sectors.')
            add_rec('Portfolio Diversifier', 'advanced_portfolio_bp.portfolio_tool')
            tips.append('Start investing early for long-term growth and keep investments diversified.')

    # Retirement
    rg = sess.get('retirement_game')
    if isinstance(rg, dict) and rg.get('final_balance') is not None:
        completed_games += 1
        strengths.append('Retirement Road: you ran a long-term projection—great planning habit.')
        score_parts.append(75)

    lg = sess.get('loan_game_state')
    if isinstance(lg, dict) and lg.get('calculated'):
        completed_games += 1

    if not strengths:
        strengths.append('Play a few games—we will highlight strengths as you go.')

    total_score = int(round(sum(score_parts) / max(len(score_parts), 1))) if score_parts else 25
    total_score = max(0, min(100, total_score))

    progress_pct = min(100, int(round((completed_games / 9.0) * 100)))

    if total_score >= 72 and completed_games >= 4:
        user_level = 'Advanced'
    elif total_score >= 45 and completed_games >= 2:
        user_level = 'Moderate'
    else:
        user_level = 'Beginner'

    # De-dup tips
    tips_unique = []
    for t in tips:
        if t not in tips_unique:
            tips_unique.append(t)
    if not any('20%' in x for x in tips_unique) and any('Savings' in w for w in weaknesses):
        tips_unique.append('Try saving at least 20% of your income when you can.')

    return {
        'ai_strengths': strengths,
        'ai_weaknesses': weaknesses,
        'ai_recommendations': recommendations[:8],
        'ai_tips': tips_unique[:6],
        'ai_total_score': total_score,
        'ai_completed_games': completed_games,
        'ai_user_level': user_level,
        'ai_progress_pct': progress_pct,
    }


@app.route('/ai-insights')
def ai_insights():
    """AI Insights page with rule-based analytics from session gameplay."""
    ctx = build_ai_insight_context(session)
    return render_template('ai_insights.html', **ctx)


@app.route('/simulations', methods=['GET', 'POST'])
def simulations():
    """Financial Simulations page + simple calculators (POST, session-backed)."""
    results = dict(session.get('sim_tool_results') or {})
    if request.method == 'POST':
        tool = request.form.get('sim_tool', '')
        if tool == 'loan':
            p = _sf(request.form.get('loan_amount'))
            rate = _sf(request.form.get('loan_rate'))
            years = _sf(request.form.get('loan_years'))
            pay = loan_monthly_payment(p, rate, years) if p and years else None
            results['loan'] = {
                'ok': pay is not None,
                'payment': pay,
                'principal': p,
                'rate': rate,
                'years': years,
            }
        elif tool == 'invest':
            init = _sf(request.form.get('invest_initial'))
            yrs = _sf(request.form.get('invest_years'))
            r = _sf(request.form.get('invest_rate'), 7.0)
            fv = investment_lump_sum_fv(init, yrs, r) if init is not None and yrs is not None else None
            results['invest'] = {
                'ok': fv is not None,
                'fv': fv,
                'initial': init,
                'years': yrs,
                'rate': r,
            }
        elif tool == 'budget':
            inc = _sf(request.form.get('budget_income'))
            exp = _sf(request.form.get('budget_expenses'))
            status = None
            if inc is not None and exp is not None and inc > 0:
                ratio = exp / inc
                if ratio <= 0.80:
                    status = 'Good'
                elif ratio <= 1.0:
                    status = 'Moderate'
                else:
                    status = 'Risky'
            results['budget'] = {
                'ok': status is not None,
                'status': status,
                'income': inc,
                'expenses': exp,
            }
        elif tool == 'retire':
            sb = _sf(request.form.get('retire_start'), 0.0)
            ac = _sf(request.form.get('retire_annual'))
            yrs = _si(request.form.get('retire_years'))
            rp = _sf(request.form.get('retire_rate'), 7.0)
            bal = retirement_basic_projection(sb, ac or 0, yrs, rp or 7.0)
            results['retire'] = {
                'ok': bal is not None,
                'balance': bal,
                'starting': sb,
                'annual': ac,
                'years': yrs,
                'rate': rp,
            }
        session['sim_tool_results'] = results
        session.modified = True

    return render_template('simulations.html', sim_results=session.get('sim_tool_results') or {})

if __name__ == '__main__':
    app.run(debug=True, port=5000)

