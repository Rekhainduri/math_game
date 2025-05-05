import streamlit as st
import random
import time
import pandas as pd

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'
if 'question_index' not in st.session_state:
    st.session_state.question_index = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'answers' not in st.session_state:
    st.session_state.answers = []
if 'start_time' not in st.session_state:
    st.session_state.start_time = 0
if 'level' not in st.session_state:
    st.session_state.level = 1

# Define questions by level
questions = {
    1: [("5 + 3", 8), ("10 - 4", 6), ("6 + 2", 8), ("9 - 3", 6), ("4 + 5", 9)],
    2: [("3 * 2", 6), ("12 / 4", 3), ("5 * 3", 15), ("16 / 4", 4), ("6 * 2", 12)],
    3: [("Tom has 4 candies. He got 3 more. How many?", 7),
        ("Anna had 10 apples, gave away 4. How many left?", 6),
        ("There are 3 bags, each with 2 toys. How many?", 6),
        ("A pizza is cut into 8 slices. You ate 4. Left?", 4),
        ("You have 9 pens, gave 3 to a friend. Left?", 6)]
}

# Navigate pages
if st.session_state.page == 'welcome':
    st.markdown("""
    <h1 style='text-align:center; font-size: 50px; color:#FF5733;'>🎮 Welcome to Math Fun Land!</h1>
    <p style='text-align:center; font-size: 20px;'>Get ready for an exciting math adventure!</p>
    """, unsafe_allow_html=True)
    if st.button("Start Test", use_container_width=True):
        st.session_state.page = 'question'
        st.session_state.start_time = time.time()

elif st.session_state.page == 'question':
    level = st.session_state.level
    q_idx = st.session_state.question_index
    questions_this_level = questions[level]

    if q_idx < len(questions_this_level):
        question, answer = questions_this_level[q_idx]
        st.markdown(f"<h2>Level {level} - Question {q_idx + 1}/{len(questions_this_level)}</h2>", unsafe_allow_html=True)
        st.markdown(f"<h3>Solve: {question}</h3>", unsafe_allow_html=True)
        user_answer = st.number_input("Your Answer", step=1, format="%d", key=f"answer_{q_idx}")

        if st.button("Submit Answer", key=f"submit_{q_idx}"):
            correct = user_answer == answer
            time_taken = round(time.time() - st.session_state.start_time, 2)
            st.session_state.answers.append({
                "Level": level,
                "Question": question,
                "Correct Answer": answer,
                "Your Answer": user_answer,
                "Result": "✅ Correct" if correct else "❌ Incorrect",
                "Time (s)": time_taken
            })
            if correct:
                st.session_state.score += 1
            st.session_state.show_feedback = True
            st.session_state.feedback = f"{'✅ Correct!' if correct else f'❌ Incorrect! The correct answer is: {question} = {answer}'}"
            st.session_state.start_time = time.time()
            st.rerun()

    elif q_idx >= len(questions_this_level):
        st.session_state.page = 'congrats'
        st.rerun()

    # Feedback after submission
    if st.session_state.get('show_feedback', False):
        st.markdown(f"<h4>{st.session_state.feedback}</h4>", unsafe_allow_html=True)
        if st.button("Next Question", key=f"next_{q_idx}"):
            st.session_state.question_index += 1
            st.session_state.show_feedback = False
            st.rerun()

elif st.session_state.page == 'congrats':
    st.balloons()
    st.markdown(f"""
    <h1 style='color:green;'>🎉 Congratulations!</h1>
    <p>You have completed Level {st.session_state.level}.</p>
    """, unsafe_allow_html=True)
    if st.session_state.level < 3:
        if st.button("Proceed to Next Level", use_container_width=True):
            st.session_state.level += 1
            st.session_state.question_index = 0
            st.session_state.start_time = time.time()
            st.session_state.page = 'question'
            st.rerun()
    else:
        if st.button("Show Final Performance Summary", use_container_width=True):
            st.session_state.page = 'summary'
            st.rerun()

elif st.session_state.page == 'summary':
    st.title("📊 Final Performance Summary")
    df = pd.DataFrame(st.session_state.answers)

    # Highlight table
    def highlight_result(val):
        return 'background-color: lightgreen' if val == '✅ Correct' else 'background-color: lightcoral'

    st.dataframe(df.style.applymap(highlight_result, subset=['Result']))

    score = st.session_state.score
    total = len(st.session_state.answers)
    st.markdown(f"<h2 style='color:#0055ff;'>You got {score} out of {total} questions right!</h2>", unsafe_allow_html=True)

    time_chart_data = pd.DataFrame({
        'Time Taken (s)': [entry['Time (s)'] for entry in st.session_state.answers],
        'Question': list(range(1, len(st.session_state.answers)+1))
    })
    st.line_chart(time_chart_data.set_index('Question'))

    st.success("Great job completing all levels! 🎉")
    if st.button("Restart Test"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
