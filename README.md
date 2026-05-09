# FINOVO - Financial Education Platform

A gamified financial education web platform with three integrated learning games.

## Quick Start (Windows)

### Option 1: Use the Installation Script (Easiest)

1. Double-click `install.bat` to install dependencies
2. Double-click `run.bat` to start the application
3. Open your browser to `http://localhost:5000`

### Option 2: Manual Installation

1. **Install dependencies:**
   ```bash
   python -m pip install -r requirements.txt
   ```
   (If that doesn't work, try: `py -m pip install -r requirements.txt`)

2. **Run the application:**
   ```bash
   python app.py
   ```
   (Or: `py app.py`)

3. **Access the application:**
   Open your browser to `http://localhost:5000`

## Detailed Setup

For detailed Windows installation instructions, troubleshooting, and more information, see:
- **[SETUP_WINDOWS.md](SETUP_WINDOWS.md)** - Complete Windows setup guide
- **[README_INTEGRATION.md](README_INTEGRATION.md)** - Technical documentation
- **[INTEGRATION_SUMMARY.md](INTEGRATION_SUMMARY.md)** - Integration summary

## Available Games

1. **Beginner Level** - Needs vs Wants Quiz (`/games/beginner`)
2. **Moderate Level** - Budget Balancer Game (`/games/moderate`)
3. **Advanced Level** - Stock Market Simulator (`/games/advanced`)

## Features

✅ Single Flask application (no multiple servers)
✅ Consistent FINOVO styling across all games
✅ Modular blueprint architecture
✅ Session-based game state management
✅ Responsive design

## Requirements

- Python 3.7 or higher
- Flask 2.3.3
- Werkzeug 2.3.7

No virtual environment required - works with standard Python installation.

## Project Structure

```
finovo/
├── app.py              # Main Flask application
├── requirements.txt    # Dependencies
├── install.bat         # Windows installation script
├── run.bat             # Windows run script
├── templates/          # HTML templates
├── static/             # CSS and JavaScript
└── games/              # Game modules (blueprints)
```

## Notes

- All games are integrated as internal modules
- Game state is stored in Flask sessions
- No database required
- Debug mode enabled by default

For more information, see the detailed documentation files.

## New Features Added

This section documents **additive** work only: existing games, routes, and behavior were left unchanged.

### Newly added games (3)

| Game | Level | Blueprint package | URL prefix |
|------|--------|-------------------|------------|
| **Savings Challenge** | Level 1 (Beginner) | `games/beginner_savings_challenge/` | `/games/beginner/savings-challenge` |
| **Credit Score Challenge** | Level 2 (Moderate) | `games/moderate_credit_score/` | `/games/moderate/credit-score` |
| **Retirement Road** | Level 3 (Advanced) | `games/advanced_retirement_road/` | `/games/advanced/retirement-road` |

### Level-based system

- **Level 1 – Beginner:** foundational games (including Needs vs Wants, Budget Balancer, and **Savings Challenge**).
- **Level 2 – Moderate:** applied scenarios (loan, insurance, budget balancer, and **Credit Score Challenge**).
- **Level 3 – Advanced:** investing and long-term planning (stock simulator, portfolio tool, and **Retirement Road**).

All titles appear on the central **Financial Games** dashboard (`/games`) under the matching level.

### Integration approach

- **Flask Blueprints:** each new game is its own blueprint module (`__init__.py` + `routes.py`), consistent with the rest of the project.
- **Centralized dashboard:** `templates/games.html` lists every game by level with working `url_for` links; no existing cards were removed.
- **Session state:** gameplay uses Flask `session` only, with dedicated keys—`savings_game`, `credit_score`, and `retirement_game`—without altering other session keys used by existing games.

### What each new game does (prototype)

- **Savings Challenge:** move amounts from “cash on hand” into savings toward a fixed goal, or spend from cash; progress bar reflects savings vs goal.
- **Credit Score Challenge:** short multiple-choice scenarios adjust a **simulated** score (educational only, not a real credit model).
- **Retirement Road:** user enters starting balance, annual contribution, years, and expected return; the app projects an ending balance with simple year-by-year compounding.

No existing blueprint code paths were modified; integration is limited to **new modules**, **additional `register_blueprint` registrations** in `app.py`, and **new rows** on the games dashboard.
"# Finovo" 
