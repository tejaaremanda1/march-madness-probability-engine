import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="March Madness Probability Engine", layout="centered")

st.title("NCAA Tournament Advancement Probability Engine")
st.markdown("""
This model estimates tournament advancement probabilities using:

• Historical seed baselines  
• Engineered efficiency metrics  
• Conservative actuarial adjustment  
• Conditional round modeling  
""")

# 1. User Inputs

st.header("Team Inputs")

col1, col2 = st.columns(2)

with col1:
    seed = st.selectbox("Seed", list(range(1,17)), index=2)
    wins = st.number_input("Wins", min_value=0, max_value=40, value=24)
    losses = st.number_input("Losses", min_value=0, max_value=40, value=2)
    ppg = st.number_input("Points Per Game", value=83.0)
    opp_ppg = st.number_input("Opponent Points Per Game", value=63.2)

with col2:
    fg_pct = st.number_input("FG%", value=0.501)
    three_pct = st.number_input("3PT%", value=0.349)
    ft_pct = st.number_input("FT%", value=0.714)
    rebounds_per_game = st.number_input("Rebounds Per Game", value=39.6)
    rebound_margin = st.number_input("Rebound Margin", value=9.8)

assists = st.number_input("Assists Per Game", value=17.0)
turnovers = st.number_input("Turnovers Per Game", value=10.8)
steals = st.number_input("Steals Per Game", value=8.2)
blocks = st.number_input("Blocks Per Game", value=3.5)

#2. Calculating Power Score

win_pct = wins / (wins + losses) if (wins + losses) > 0 else 0
scoring_margin = ppg - opp_ppg

# True Shooting Proxy
true_shooting_proxy = (fg_pct + three_pct + ft_pct) / 3

# Offensive Index
offensive_index = (
    0.4 * (ppg / 90) +
    0.3 * true_shooting_proxy +
    0.3 * (assists / 20)
)

# Defensive Index
defensive_index = (
    0.4 * (scoring_margin / 25) +
    0.3 * (steals / 10) +
    0.3 * (blocks / 6)
)

# Ball Security
ball_security = assists / turnovers if turnovers > 0 else 0

# Rebounding Strength
rebounding_index = rebound_margin / 15

# Composite Power Rating
raw_power = (
    0.30 * offensive_index +
    0.30 * defensive_index +
    0.15 * ball_security / 2 +
    0.15 * rebounding_index +
    0.10 * win_pct
)

power_score = np.clip(raw_power, 0, 1)

# 3. Historical Seed Baselines

seed_baselines = {
    1: {"R32": 0.99, "S16": 0.85, "E8": 0.60, "F4": 0.38, "Champ": 0.14},
    2: {"R32": 0.94, "S16": 0.65, "E8": 0.42, "F4": 0.22, "Champ": 0.07},
    3: {"R32": 0.88, "S16": 0.55, "E8": 0.30, "F4": 0.14, "Champ": 0.04},
    4: {"R32": 0.80, "S16": 0.45, "E8": 0.25, "F4": 0.10, "Champ": 0.025},
    5: {"R32": 0.65, "S16": 0.30, "E8": 0.15, "F4": 0.06, "Champ": 0.015},
    6: {"R32": 0.60, "S16": 0.25, "E8": 0.12, "F4": 0.04, "Champ": 0.01},
    7: {"R32": 0.55, "S16": 0.22, "E8": 0.10, "F4": 0.03, "Champ": 0.008},
    8: {"R32": 0.50, "S16": 0.18, "E8": 0.08, "F4": 0.02, "Champ": 0.006},
}

if seed > 8:
    seed = 8

base = seed_baselines[seed]

# 4. Actuarial Adjustment Logic

# Conservative credibility factor
credibility = 0.12

# Seed-relative scaling
seed_strength_factor = (17 - seed) / 16

adjustment = credibility * (power_score - 0.5) * seed_strength_factor

def adjust_probability(base_prob):
    adjusted = base_prob * (1 + adjustment)
    return np.clip(adjusted, 0, 1)

R32 = adjust_probability(base["R32"])
S16 = adjust_probability(base["S16"])
E8 = adjust_probability(base["E8"])
F4 = adjust_probability(base["F4"])
Champ = adjust_probability(base["Champ"])

S16 = min(S16, R32)
E8 = min(E8, S16)
F4 = min(F4, E8)
Champ = min(Champ, F4)

# 5. OUTPUT

st.header("Results")

st.metric("Power Score", round(power_score,3))

st.write(f"Round of 32: {round(R32*100,2)}%")
st.write(f"Sweet 16: {round(S16*100,2)}%")
st.write(f"Elite 8: {round(E8*100,2)}%")
st.write(f"Final Four: {round(F4*100,2)}%")
st.write(f"National Champion: {round(Champ*100,2)}%")

# Chance Statement Logic

if Champ < 0.01:
    statement = "is cooked."
elif Champ < 0.03:
    statement = "should start praying."
elif Champ < 0.06:
    statement = "has a chance."
elif Champ < 0.10:
    statement = "is dangerous."
else:
    statement = "is a favorite."

st.write("")
st.write("Your team:")
st.markdown(f"<h1 style='text-align: left;'>{statement}</h1>", unsafe_allow_html=True)