import streamlit as st
from datetime import datetime, timezone, timedelta
import time

# Symptom advice dictionary (expand as needed)
SYMPTOM_ADVICE = {
    "fever": "Keep hydrated and rest. If fever persists for more than 3 days, see a doctor.",
    "cough": "Try warm liquids and throat lozenges. Avoid irritants like smoke.",
    "sore throat": "Gargle with warm salt water and stay hydrated.",
    "difficulty breathing": "Try this breathing exercise below 👇",
    "asthma": "Try this breathing exercise below 👇",
    "tiredness": "Rest well and maintain a balanced diet.",
    "body aches": "Try gentle stretching and stay hydrated.",
    "muscle cramps": "Stretch the muscle gently and apply heat.",
    "cramps": "Stretch and stay hydrated."
}

# Risk questions and scoring weights (example)
RISK_QUESTIONS = [
    ("Do you have a fever?", "fever"),
    ("Do you have a cough or sore throat?", "cough_sorethroat"),
    ("Are you experiencing difficulty breathing?", "difficulty_breathing"),
    ("Are you feeling tired or having body aches?", "tired_bodyaches"),
    ("Have you been in contact with someone who's sick recently?", "contact_sick"),
]

def greet():
    # Singapore is UTC +8
    sg_timezone = timezone(timedelta(hours=8))
    current_hour = datetime.now(sg_timezone).hour
    
    if current_hour < 12:
        time_greeting = "🌅 Good morning"
    elif current_hour < 18:
        time_greeting = "🌤️ Good afternoon"
    else:
        time_greeting = "🌙 Good evening"

    st.title(f"{time_greeting}! I'm HealthBot 🤖")
    st.write("Tell me how you're feeling, and I’ll give some basic tips.")
    st.write("**Note:** This is not professional medical advice.")

def breathing_exercise():
    st.write("### Breathing Exercise")
    st.write("Follow the steps below with the timer:")
    st.write("- Inhale for 4 seconds")
    st.write("- Hold breath for 7 seconds")
    st.write("- Exhale for 8 seconds")
    st.write("Repeat 3 cycles.")
    
    # Simple timer animation for demonstration
    for cycle in range(1, 4):
        st.write(f"**Cycle {cycle}**")
        for phase, sec in [("Inhale",4), ("Hold",7), ("Exhale",8)]:
            st.write(f"{phase} for {sec} seconds")
            for i in range(sec, 0, -1):
                st.write(f"{i}...")
                time.sleep(1)
                st.empty()  # clear last countdown to update

def main():
    if "page" not in st.session_state:
        st.session_state.page = 1
        st.session_state.choice = None
        st.session_state.symptom = None
        st.session_state.risk_answers = {}
    
    if st.session_state.page == 1:
        greet()
        st.write("What would you like to do?")
        choice = st.radio(
            "",
            ("Get advice based on symptoms", "Take a health risk check")
        )
        if st.button("Next"):
            st.session_state.choice = choice
            if choice == "Get advice based on symptoms":
                st.session_state.page = 2.1
            else:
                st.session_state.page = 2.2
        st.stop()

    elif st.session_state.page == 2.1:
        st.header("Symptom Advice")
        symptom = st.text_input("Enter your symptom (e.g. cough, fever, asthma):").lower().strip()
        if st.button("Submit"):
            if symptom in SYMPTOM_ADVICE:
                st.session_state.symptom = symptom
                st.session_state.page = 3.1
            else:
                st.warning("Symptom not recognized. Please try another symptom.")
        if st.button("Back"):
            st.session_state.page = 1
        st.stop()

    elif st.session_state.page == 2.2:
        st.header("Health Risk Check")
        answers = {}
        for q, key in RISK_QUESTIONS:
            answers[key] = st.radio(q, ("Yes", "No"), key=key)
        if st.button("Submit"):
            st.session_state.risk_answers = answers
            st.session_state.page = 3.2
        if st.button("Back"):
            st.session_state.page = 1
        st.stop()

    elif st.session_state.page == 3.1:
        st.header("Symptom Advice")
        symptom = st.session_state.symptom
        advice = SYMPTOM_ADVICE.get(symptom)
        st.write(f"**Symptom:** {symptom.capitalize()}")
        st.write(f"**Advice:** {advice}")

        # Show breathing exercise if relevant
        if symptom in ["difficulty breathing", "asthma"]:
            breathing_exercise()

        st.write("What would you like to do next?")
        next_action = st.radio("", ("Check another symptom or calculate risk", "Exit"))
        if st.button("Continue"):
            if next_action == "Check another symptom or calculate risk":
                st.session_state.page = 1
            else:
                st.session_state.page = 4
        st.stop()

    elif st.session_state.page == 3.2:
        st.header("Risk Assessment Result")

        # Simple risk calculation based on yes answers count
        risk_score = sum(1 for v in st.session_state.risk_answers.values() if v == "Yes")
        if risk_score >= 4:
            risk_level = "High Risk"
        elif risk_score >= 2:
            risk_level = "Moderate Risk"
        else:
            risk_level = "Low Risk"

        st.write(f"Your risk level is: **{risk_level}**")

        st.write("What would you like to do next?")
        next_action = st.radio("", ("Check symptom or calculate risk again", "Exit"))
        if st.button("Continue"):
            if next_action == "Check symptom or calculate risk again":
                st.session_state.page = 1
            else:
                st.session_state.page = 4
        st.stop()

    elif st.session_state.page == 4:
        st.header("Thank you for using HealthBot!")
        st.write("Remember, this is just advice and not a substitute for professional medical consultation.")
        if st.button("Restart"):
            st.session_state.page = 1
        st.stop()

if __name__ == "__main__":
    main()

