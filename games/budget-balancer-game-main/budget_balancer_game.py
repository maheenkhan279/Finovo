import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Budget Balancer Simulation", page_icon="💸")

# --------------------------
# Constants / config
# --------------------------

if "current_month" not in st.session_state:
    st.session_state.current_month = 1
if "phase" not in st.session_state:
    st.session_state.phase = "await_income"

#This prevents the user from changing money mid-game.
disabled_settings = st.session_state.current_month > 1

with st.sidebar:
    st.header("Game Settings")

    st.number_input(
        "Starting Balance ($)",
        min_value = 0,
        value = 1000,
        step = 100,
        key = "starting_balance",
        disabled = disabled_settings,
    )
    st.number_input(
        "Monthly Income ($)",
        min_value = 0,
        value = 2500,
        step = 100,
        key = "monthly_income",
        disabled = disabled_settings,
    )
    st.markdown("---")
    st.write("Tip: You can change these before you recieve income for month 1.")


TOTAL_MONTHS = 3
INFLATION_RATE = 0.03  # 3% per month

SPENDING_OPTIONS = {
    "HOUSING": [
        {"label": "Room Share (Low)", "cost": 950},
        {"label": "Studio Apartment (Mid)", "cost": 1300},
        {"label": "One-Bedroom (High)", "cost": 1700},
    ],
    "FOOD": [
        {"label": "Basic (Ramen & Staples)", "cost": 350},
        {"label": "Average (Groceries + Occasional Takeout)", "cost": 550},
        {"label": "Gourmet (Dining Out Often)", "cost": 850},
    ],
    "UTILITIES": [
        {"label": "Fixed Bills", "cost": 175},
    ],
    "ENTERTAINMENT": [
        {"label": "Skip (Free)", "cost": 0},
        {"label": "Movie Night", "cost": 50},
        {"label": "Concert/Event", "cost": 150},
    ],
}

# --------------------------
# Helper Functions
# --------------------------
def cost_for(category_key, label):
    for item in SPENDING_OPTIONS[category_key]:
        if item["label"] == label:
            return item["cost"]
    return 0

def inflated_cost(base):
    month_index = st.session_state.current_month - 1
    return round(base * ((1 + INFLATION_RATE) ** month_index), 2)

# --------------------------
# Session state init
# --------------------------
if "player_balance" not in st.session_state:
    st.session_state.player_balance = st.session_state.starting_balance
if "current_month" not in st.session_state:
    st.session_state.current_month = 1
if "phase" not in st.session_state:
    st.session_state.phase = "await_income"
if "history" not in st.session_state:
    st.session_state.history = []
if "choices" not in st.session_state:
    st.session_state.choices = {
        "HOUSING": SPENDING_OPTIONS["HOUSING"][0]["label"],
        "FOOD": SPENDING_OPTIONS["FOOD"][1]["label"],
        "UTILITIES": SPENDING_OPTIONS["UTILITIES"][0]["label"],
        "ENTERTAINMENT": SPENDING_OPTIONS["ENTERTAINMENT"][0]["label"],
    }

# --------------------------
# Random Events (fixed amounts)
# --------------------------
NEGATIVE_EVENTS = [
    ("Car broke down — mechanic cost", 300),
    ("Medical bill — urgent visit", 200),
    ("Lost wallet — lost cash", 150),
    ("Phone screen repair", 100),
    ("Unexpected bank fee", 50),
    ("You lended money to a friend", 100),
    ("Paid wifi bill", 50),
    ("You had to buy a gift for someone", 20)
]

POSITIVE_EVENTS = [
    ("Tax refund received", 200),
    ("Gift from friend", 100),
    ("Sold old bike", 150)
]

SUPER_POSITIVE_EVENTS = [
    ("You beat all odds. You won the lottery!", 244000000),
]

def random_event():
    chance = random.random()
    if chance < 0.75:  # 75% chance of negative event
        desc, amount = random.choice(NEGATIVE_EVENTS)
        st.session_state.player_balance -= amount
        st.warning(f"{desc}: -${amount}")
        return f"{desc} (-${amount})"
    elif chance < 0.98:  # 23% chance of positive event
        desc, amount = random.choice(POSITIVE_EVENTS)
        st.session_state.player_balance += amount
        st.info(f"{desc}: +${amount}")
        return f"{desc} (+${amount})"
##Add a new event, one that makes it so you win the lottery some how.
    elif chance < 0.99: # 1% chance of this event happening.
        desc, amount = random.choice(SUPER_POSITIVE_EVENTS)
        st.session_state.player_balance += amount
        st.success(f"{desc}: +${amount}")
        return f"{desc} (+${amount})"

##
    else:
        return "No random event"

# --------------------------
# Game functions
# --------------------------
def receive_income():
    if st.session_state.phase == "await_income":
        st.session_state.player_balance += st.session_state.monthly_income
        st.session_state.phase = "await_choices"

def simulate_month():
    if st.session_state.phase != "await_choices":
        return

    # Deduct spending
    monthly_spending = sum(
        inflated_cost(cost_for(cat, st.session_state.choices[cat]))
        for cat in SPENDING_OPTIONS.keys()
    )
    st.session_state.player_balance -= monthly_spending

    # Random event
    event_desc = random_event()

    # Month summary
    summary = {
        "month": st.session_state.current_month,
        "housing": st.session_state.choices["HOUSING"],
        "food": st.session_state.choices["FOOD"],
        "utilities": st.session_state.choices["UTILITIES"],
        "entertainment": st.session_state.choices["ENTERTAINMENT"],
        "spending_total": monthly_spending,
        "event": event_desc,
        "end_balance": st.session_state.player_balance,
    }

    # Update or add history
    for i, rec in enumerate(st.session_state.history):
        if rec["month"] == st.session_state.current_month:
            st.session_state.history[i] = summary
            break
    else:
        st.session_state.history.append(summary)

    # Determine next phase
    if st.session_state.player_balance <= 0:
        st.session_state.phase = "lost"
    elif st.session_state.current_month >= TOTAL_MONTHS:
        st.session_state.phase = "won"
    else:
        st.session_state.phase = "simulated"

def next_month():
    if st.session_state.phase == "simulated":
        st.session_state.current_month += 1
        st.session_state.phase = "await_income"

def reset_game():
    st.session_state.player_balance = st.session_state.starting_balance
    st.session_state.current_month = 1
    st.session_state.phase = "await_income"
    st.session_state.history = []
    st.session_state.choices = {
        "HOUSING": SPENDING_OPTIONS["HOUSING"][0]["label"],
        "FOOD": SPENDING_OPTIONS["FOOD"][1]["label"],
        "UTILITIES": SPENDING_OPTIONS["UTILITIES"][0]["label"],
        "ENTERTAINMENT": SPENDING_OPTIONS["ENTERTAINMENT"][0]["label"],
    }

# --------------------------
# Phase logic / messages
# --------------------------
if st.session_state.phase == "await_income":
    st.info("Start of month: Click **Receive Income** to add your monthly income, then make your choices.")
    st.button("Receive Income", on_click=receive_income)
    disabled_inputs = True
elif st.session_state.phase == "await_choices":
    st.success("Income received. Choose your expenses, then click **Lock Choices & Simulate Month**.")
    disabled_inputs = False
elif st.session_state.phase == "simulated":
    st.info("Month simulated. Review the summary below, then click **Next Month ▶**.")
    disabled_inputs = True
elif st.session_state.phase == "won":
    st.success(f"🎉 You balanced your budget for {TOTAL_MONTHS} months! Final Balance: ${st.session_state.player_balance:.2f}")
    disabled_inputs = True
elif st.session_state.phase == "lost":
    st.error(f"💀 GAME OVER! You ran out of money in Month {st.session_state.current_month}. Final Balance: ${st.session_state.player_balance:.2f}")
    disabled_inputs = True
else:
    disabled_inputs = True

# --------------------------
# Choice boxes (with prices displayed)
# --------------------------
def label_with_price(category, item):
    return f"{item['label']} - ${item['cost']}"

col1, col2 = st.columns(2)
with col1:
    st.selectbox("HOUSING",
        [label_with_price("HOUSING", x) for x in SPENDING_OPTIONS["HOUSING"]],
        index=[i for i, x in enumerate(SPENDING_OPTIONS["HOUSING"]) if x["label"] == st.session_state.choices["HOUSING"]][0],
        key="HOUSING_select", disabled=disabled_inputs)
    st.session_state.choices["HOUSING"] = st.session_state.HOUSING_select.split(" - $")[0]

with col2:
    st.selectbox("FOOD",
        [label_with_price("FOOD", x) for x in SPENDING_OPTIONS["FOOD"]],
        index=[i for i, x in enumerate(SPENDING_OPTIONS["FOOD"]) if x["label"] == st.session_state.choices["FOOD"]][0],
        key="FOOD_select", disabled=disabled_inputs)
    st.session_state.choices["FOOD"] = st.session_state.FOOD_select.split(" - $")[0]

col3, col4 = st.columns(2)
with col3:
    st.selectbox("UTILITIES",
        [label_with_price("UTILITIES", x) for x in SPENDING_OPTIONS["UTILITIES"]],
        index=0, key="UTILITIES_select", disabled=True)
    st.session_state.choices["UTILITIES"] = st.session_state.UTILITIES_select.split(" - $")[0]

with col4:
    st.selectbox("ENTERTAINMENT (optional)",
        [label_with_price("ENTERTAINMENT", x) for x in SPENDING_OPTIONS["ENTERTAINMENT"]],
        index=[i for i, x in enumerate(SPENDING_OPTIONS["ENTERTAINMENT"]) if x["label"] == st.session_state.choices["ENTERTAINMENT"]][0],
        key="ENTERTAINMENT_select", disabled=disabled_inputs)
    st.session_state.choices["ENTERTAINMENT"] = st.session_state.ENTERTAINMENT_select.split(" - $")[0]

# --------------------------
# Buttons
# --------------------------
st.markdown("---")
month_spending = sum(inflated_cost(cost_for(cat, st.session_state.choices[cat])) for cat in SPENDING_OPTIONS.keys())
st.write(f"**Inflation-adjusted Monthly Spending:** ${month_spending:.2f}")

colA, colB, colC = st.columns(3)
with colA:
    st.button("Lock Choices & Simulate Month", disabled=(st.session_state.phase != "await_choices"), on_click=simulate_month)
with colB:
    st.button("Next Month ▶", disabled=(st.session_state.phase != "simulated"), on_click=next_month)
with colC:
    st.button("Reset Game", on_click=reset_game)

st.markdown("---")

# --------------------------
# Summary and End Messages
# --------------------------
if st.session_state.history:
    df = pd.DataFrame(st.session_state.history).rename(columns={
        "month": "Month",
        "housing": "Housing",
        "food": "Food",
        "utilities": "Utilities",
        "entertainment": "Entertainment",
        "spending_total": "Total Spending",
        "event": "Random Event",
        "end_balance": "End Balance",
    }).sort_values("Month")
    st.subheader("Monthly Summary")
    st.dataframe(df, use_container_width=True)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download Summary CSV", csv, "budget_balancer_summary.csv", "text/csv")

    # End-of-game reflections
    if st.session_state.phase in ["won", "lost"]:
        final_balance = st.session_state.player_balance
        if final_balance >= 2000:
            st.success("🏆 Excellent work! You’ve demonstrated great saving habits — apply those skills in real life and you’ll be financially secure.")
        elif final_balance > 0:
            st.info("✅ You made it! However, living paycheck to paycheck isn’t sustainable — aim to save a little more each month.")
        else:
            st.error("⚠️ You did not make it. Sometimes unexpected expenses arise — this highlights the importance of having savings for emergencies.")
