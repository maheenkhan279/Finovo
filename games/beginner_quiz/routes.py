from flask import render_template, request, redirect, url_for, session, jsonify
from games.beginner_quiz import beginner_bp

# Needs vs Wants Questions
QUESTIONS = [
    {
        'id': 1,
        'question': 'Which of the following is a NEED?',
        'options': ['A) New smartphone', 'B) Groceries for the week', 'C) Designer clothes', 'D) Video game console'],
        'correct': 'B) Groceries for the week',
        'explanation': 'Groceries are essential for survival and are a need. The other options are wants.'
    },
    {
        'id': 2,
        'question': 'Which of the following is a WANT?',
        'options': ['A) Rent payment', 'B) Utility bills', 'C) Monthly gym membership', 'D) Health insurance'],
        'correct': 'C) Monthly gym membership',
        'explanation': 'While exercise is important, a gym membership is a want. You can exercise for free at home or outdoors.'
    },
    {
        'id': 3,
        'question': 'Is "Internet service" a need or want?',
        'options': ['A) Need - Essential for work', 'B) Want - Luxury item', 'C) Need - Everyone has it', 'D) Want - Entertainment only'],
        'correct': 'A) Need - Essential for work',
        'explanation': 'In modern times, internet can be a need if required for work/education, but it depends on circumstances.'
    },
    {
        'id': 4,
        'question': 'Which expense should be prioritized?',
        'options': ['A) New shoes', 'B) Emergency fund contribution', 'C) Concert tickets', 'D) Latest fashion trends'],
        'correct': 'B) Emergency fund contribution',
        'explanation': 'Building an emergency fund is a financial need that provides security and should be prioritized.'
    },
    {
        'id': 5,
        'question': 'What is the best approach to buying wants?',
        'options': ['A) Buy immediately when you want it', 'B) Save for it after covering needs', 'C) Use credit cards', 'D) Borrow money'],
        'correct': 'B) Save for it after covering needs',
        'explanation': 'Always cover your needs first, then save for wants. This prevents financial stress.'
    },
    {
        'id': 6,
        'question': 'Which is a need in most situations?',
        'options': ['A) Brand new car', 'B) Basic transportation', 'C) Luxury vacation', 'D) Premium streaming services'],
        'correct': 'B) Basic transportation',
        'explanation': 'Basic transportation is a need for most people, but it doesn\'t have to be a brand new car.'
    },
    {
        'id': 7,
        'question': 'Should you prioritize wants over needs?',
        'options': ['A) Yes, always', 'B) No, needs come first', 'C) Sometimes', 'D) Depends on the situation'],
        'correct': 'B) No, needs come first',
        'explanation': 'Needs should always be prioritized over wants to maintain financial stability.'
    },
    {
        'id': 8,
        'question': 'Which is typically a want?',
        'options': ['A) Basic healthcare', 'B) Food and water', 'C) Shelter', 'D) Dining at expensive restaurants'],
        'correct': 'D) Dining at expensive restaurants',
        'explanation': 'While food is a need, dining at expensive restaurants is a want. Basic food is sufficient.'
    },
    {
        'id': 9,
        'question': 'What should you do if you can\'t afford both needs and wants?',
        'options': ['A) Buy wants anyway', 'B) Focus only on needs', 'C) Skip both', 'D) Take a loan'],
        'correct': 'B) Focus only on needs',
        'explanation': 'When money is tight, focus on needs first. Wants can wait until you have financial stability.'
    },
    {
        'id': 10,
        'question': 'Which mindset helps with needs vs wants?',
        'options': ['A) "I deserve everything"', 'B) "Needs first, wants later"', 'C) "Buy now, worry later"', 'D) "More is always better"'],
        'correct': 'B) "Needs first, wants later"',
        'explanation': 'Prioritizing needs and saving for wants helps build financial discipline and security.'
    }
]

# Interactive drag-drop simulation items (not MCQ)
SIM_ITEMS = [
    {"id": 1, "label": "Rent / mortgage payment", "correct": "need", "tip": "Shelter is a core need."},
    {"id": 2, "label": "Concert tickets", "correct": "want", "tip": "Entertainment is usually a want."},
    {"id": 3, "label": "Basic groceries", "correct": "need", "tip": "Food is essential."},
    {"id": 4, "label": "Latest smartphone upgrade", "correct": "want", "tip": "Upgrades are often wants if the old phone still works."},
    {"id": 5, "label": "Electricity bill", "correct": "need", "tip": "Utilities keep your home livable."},
    {"id": 6, "label": "Designer sneakers", "correct": "want", "tip": "Fashion extras are typically wants."},
    {"id": 7, "label": "Bus pass for work commute", "correct": "need", "tip": "Reliable transport to earn income is a need."},
    {"id": 8, "label": "Daily fancy coffee", "correct": "want", "tip": "You can brew at home for much less."},
    {"id": 9, "label": "Health insurance premium", "correct": "need", "tip": "Protection against large medical costs is essential."},
    {"id": 10, "label": "Streaming subscriptions (all)", "correct": "want", "tip": "Nice to have, but not required to survive."},
    {"id": 11, "label": "Emergency fund deposit", "correct": "need", "tip": "Financial safety is a high priority need."},
    {"id": 12, "label": "Luxury vacation", "correct": "want", "tip": "Travel is wonderful but usually a want."},
]


@beginner_bp.route('/')
def beginner_game():
    """Start the beginner game (interactive simulation)."""
    session['quiz_score'] = 0
    session['current_question'] = 1
    session['quiz_completed'] = False
    return redirect(url_for('beginner_bp.simulation'))


@beginner_bp.route('/simulation')
def simulation():
    """Needs vs Wants interactive simulation UI."""
    session['quiz_score'] = 0
    session['quiz_completed'] = False
    session.modified = True
    return render_template('games/beginner_quiz_simulation.html', items=SIM_ITEMS)


@beginner_bp.route('/simulation/finish', methods=['POST'])
def simulation_finish():
    """Persist correct/wrong counts from the interactive simulation."""
    data = request.get_json(silent=True) or {}
    total_items = len(SIM_ITEMS)
    try:
        correct = int(data.get('correct', 0))
        wrong = int(data.get('wrong', 0))
        total = int(data.get('total', total_items))
    except (TypeError, ValueError):
        correct, wrong, total = 0, 0, total_items

    if total <= 0:
        total = total_items
    correct = max(0, min(correct, total))
    wrong = max(0, min(wrong, total))
    if correct + wrong > total:
        wrong = max(0, total - correct)

    session['sim_correct'] = correct
    session['sim_wrong'] = wrong
    session['sim_total'] = total
    session['quiz_completed'] = True
    session.modified = True
    return jsonify({'redirect': url_for('beginner_bp.quiz_score')})


@beginner_bp.route('/question/<int:question_id>')
def quiz_question(question_id):
    """Legacy quiz URLs redirect to interactive simulation."""
    return redirect(url_for('beginner_bp.simulation'))


@beginner_bp.route('/answer/<int:question_id>', methods=['POST'])
def submit_answer(question_id):
    """Process answer submission"""
    if 'quiz_score' not in session:
        session['quiz_score'] = 0
    
    selected_answer = request.form.get('answer')
    question = QUESTIONS[question_id - 1]
    is_correct = selected_answer == question['correct']
    
    if is_correct:
        session['quiz_score'] = session.get('quiz_score', 0) + 10
    
    # Store result for display
    session['last_result'] = {
        'correct': is_correct,
        'selected': selected_answer,
        'correct_answer': question['correct'],
        'explanation': question['explanation']
    }
    
    if question_id >= len(QUESTIONS):
        session['quiz_completed'] = True
        return redirect(url_for('beginner_bp.quiz_score'))
    else:
        return redirect(url_for('beginner_bp.quiz_result', question_id=question_id))

@beginner_bp.route('/result/<int:question_id>')
def quiz_result(question_id):
    """Show result of current question"""
    result = session.get('last_result')
    if not result:
        return redirect(url_for('beginner_bp.quiz_question', question_id=question_id))
    
    next_question_id = question_id + 1
    return render_template('games/beginner_result.html', 
                         result=result,
                         question_id=question_id,
                         next_question_id=next_question_id,
                         total_questions=len(QUESTIONS))

@beginner_bp.route('/score')
def quiz_score():
    """Display final score, computed accurately from correct/total counts.

    The percentage is the canonical 'score' shown to the user and persisted
    by the client-side window.saveScore call in beginner_score.html.
    """
    total = int(session.get('sim_total', len(SIM_ITEMS))) or len(SIM_ITEMS)
    correct = int(session.get('sim_correct', 0))
    wrong = int(session.get('sim_wrong', max(0, total - correct)))

    correct = max(0, min(correct, total))
    wrong = max(0, min(wrong, total))

    percentage = round((correct / total) * 100, 1) if total > 0 else 0.0
    score = int(round(percentage))

    return render_template(
        'games/beginner_score.html',
        score=score,
        correct=correct,
        wrong=wrong,
        total=total,
        percentage=percentage,
    )

