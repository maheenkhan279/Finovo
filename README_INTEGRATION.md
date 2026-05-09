# FINOVO - Financial Games Integration

This document describes the integration of three financial learning games into the FINOVO platform.

## Project Structure

```
finovo/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── templates/
│   ├── base.html                   # Base template with FINOVO styling
│   ├── home.html                   # Homepage
│   ├── games.html                  # Games listing page
│   └── games/
│       ├── beginner_quiz.html      # Beginner game template
│       ├── beginner_result.html    # Quiz result template
│       ├── beginner_score.html     # Final score template
│       ├── moderate_budget.html    # Budget game template
│       └── advanced_stock.html     # Stock simulator template
├── static/
│   ├── css/
│   │   └── styles.css              # FINOVO styling
│   └── js/
│       └── script.js               # FINOVO JavaScript
└── games/
    ├── beginner_quiz/              # Beginner game module
    │   ├── __init__.py
    │   └── routes.py
    ├── moderate_budget/            # Moderate game module
    │   ├── __init__.py
    │   └── routes.py
    └── advanced_stock/             # Advanced game module
        ├── __init__.py
        └── routes.py
```

## Installation (Windows)

1. Install Python dependencies:
   
   **Option 1 (Recommended):**
   ```bash
   python -m pip install -r requirements.txt
   ```
   
   **Option 2 (If Option 1 doesn't work):**
   ```bash
   py -m pip install -r requirements.txt
   ```
   
   **Note**: If you get an error that pip is not installed, you may need to install it first:
   ```bash
   python -m ensurepip --upgrade
   ```

2. Run the application:
   ```bash
   python app.py
   ```
   
   Or if that doesn't work:
   ```bash
   py app.py
   ```

3. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

**Note**: No virtual environment is required. The application runs with a standard Python installation.

## Game Routes

- **Homepage**: `/`
- **Games Page**: `/games`
- **Beginner Game (Needs vs Wants)**: `/games/beginner`
- **Moderate Game (Budget Balancer)**: `/games/moderate`
- **Advanced Game (Stock Simulator)**: `/games/advanced`

## Game Descriptions

### 1. Beginner Level - Needs vs Wants Quiz
- **Route**: `/games/beginner`
- **Purpose**: Teach basic financial literacy by helping users distinguish between needs and wants
- **Features**:
  - 10 multiple-choice questions
  - Immediate feedback with explanations
  - Score tracking
  - Progress indicators

### 2. Moderate Level - Budget Balancer Game
- **Route**: `/games/moderate`
- **Purpose**: Teach budgeting concepts including income, expenses, prioritization, and savings
- **Features**:
  - 3-month budget simulation
  - Configurable starting balance and income
  - Multiple spending categories (Housing, Food, Utilities, Entertainment)
  - Random events (positive and negative)
  - Inflation simulation
  - Monthly summary tracking

### 3. Advanced Level - Stock Market Mini Simulator
- **Route**: `/games/advanced`
- **Purpose**: Teach investing concepts: buying/selling stocks, portfolio tracking, profit/loss
- **Features**:
  - Real-time stock price simulation
  - Multiple stock categories (Currency, Company Stocks, Economy Indices)
  - Buy/sell functionality
  - Portfolio tracking
  - Profit/loss calculations
  - Price change indicators

## Integration Features

✅ **Single Flask Application**: All games run under one Flask app instance
✅ **Consistent Styling**: All games use FINOVO's professional finance theme
✅ **Unified Navigation**: Games accessible through main navigation
✅ **Modular Architecture**: Each game is a separate blueprint module
✅ **Session Management**: Game state preserved using Flask sessions
✅ **Responsive Design**: Works on desktop and mobile devices

## Technical Details

- **Framework**: Flask 2.3.3
- **Templating**: Jinja2
- **State Management**: Flask sessions
- **Styling**: Custom CSS matching FINOVO theme
- **JavaScript**: Vanilla JS for game interactions

## Notes

- All games are self-contained modules that don't require external databases
- Game state is stored in Flask sessions (resets on server restart)
- No authentication required - games are accessible to all users
- All styling matches the existing FINOVO website design

## Future Enhancements

- User authentication and progress tracking
- Database integration for saving game results
- Leaderboards and achievements
- More game levels and variations
- Analytics and learning insights

