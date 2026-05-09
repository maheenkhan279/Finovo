# FINOVO Setup Guide for Windows

## Quick Start

This guide provides Windows-friendly installation instructions for the FINOVO financial games platform.

## Prerequisites

- Python 3.7 or higher installed on your system
- Internet connection (for downloading Flask)

## Installation Steps

### Step 1: Verify Python Installation

Open PowerShell or Command Prompt and check if Python is installed:

```bash
python --version
```

If that doesn't work, try:
```bash
py --version
```

You should see something like `Python 3.x.x`. If not, install Python from [python.org](https://www.python.org/downloads/).

### Step 2: Install Dependencies

Navigate to the project directory:
```bash
cd C:\Users\Ishtiaq\Desktop\finovo
```

Install Flask and dependencies using one of these methods:

**Method 1 (Recommended):**
```bash
python -m pip install -r requirements.txt
```

**Method 2 (If Method 1 fails):**
```bash
py -m pip install -r requirements.txt
```

**Method 3 (If pip is not available):**
```bash
python -m ensurepip --upgrade
python -m pip install -r requirements.txt
```

### Step 3: Run the Application

Start the Flask server:
```bash
python app.py
```

Or if needed:
```bash
py app.py
```

You should see output like:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### Step 4: Access the Application

Open your web browser and go to:
```
http://localhost:5000
```

Or:
```
http://127.0.0.1:5000
```

## Troubleshooting

### Issue: "python is not recognized"
**Solution**: Use `py` instead of `python`, or add Python to your system PATH.

### Issue: "pip is not recognized"
**Solution**: Use `python -m pip` or `py -m pip` instead of just `pip`.

### Issue: "No module named 'flask'"
**Solution**: Make sure you ran the installation command from Step 2. Try:
```bash
python -m pip install Flask==2.3.3 Werkzeug==2.3.7
```

### Issue: Port 5000 already in use
**Solution**: The port might be in use. You can change the port in `app.py`:
```python
app.run(debug=True, port=5001)  # Change to 5001 or another port
```

## Available Routes

Once the application is running, you can access:

- **Homepage**: http://localhost:5000/
- **Games Page**: http://localhost:5000/games
- **Beginner Game**: http://localhost:5000/games/beginner
- **Moderate Game**: http://localhost:5000/games/moderate
- **Advanced Game**: http://localhost:5000/games/advanced

## Stopping the Server

To stop the Flask server, press `Ctrl+C` in the terminal where it's running.

## Notes

- No virtual environment is required
- All dependencies are minimal (only Flask and Werkzeug)
- Game data is stored in Flask sessions (resets when server restarts)
- The application runs in debug mode by default for development

## Need Help?

If you encounter any issues:
1. Make sure Python is properly installed
2. Verify you're in the correct directory
3. Try using `py` instead of `python` if available
4. Check that all files are present in the project directory

