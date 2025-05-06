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
if 'questions' not in st.session_state:
    st.session_state.questions = {}

# Function to generate questions per level
def generate_questions(level):
    q_list = []
    for _ in range(5):
        if level == 1:
            a, b = random.randint(1, 10), random.randint(1, 10)
            op = random.choice(['+', '-'])
            q = f"{a} {op} {b}"
            ans = eval(q)
        elif level == 2:
            a, b = random.randint(2, 10), random.randint(1, 10)
            op = random.choice(['*', '/'])
            if op == '/':
                a = a * b  # Ensure clean division
            q = f"{a} {op} {b}"
            ans = int(eval(q))
        elif level == 3:
            templates = [
                lambda: (
                    (lambda a, b: (f"Tom has {a} candies. He got {b} more. How many?", a + b))(
                        random.randint(1, 10), random.randint(1, 10)
                    )
                ),
                lambda: (
                    (lambda a, b: (f"Anna had {a} apples, gave away {b}. How many left?", a - b))(
                        random.randint(5, 15), random.randint(1, 5)
                    )
                ),
                lambda: (
                    (lambda a, b: (f"There are {a} bags, each with {b} toys. How many?", a * b))(
                        random.randint(2, 5), random.randint(2, 5)
                    )
                ),
                lambda: (
                    (lambda a, b: (f"A pizza is cut into {a} slices. You ate {b}. Left?", a - b))(
                        random.choice([6, 8, 10]), random.randint(1, 4)
                    )
                ),
                lambda: (
                    (lambda a, b: (f"You have {a} pens, gave {b} to a friend. Left?", a - b))(
                        random.randint(5, 10), random.randint(1, 4)
                    )
                )
            ]
            q, ans = random.choice(templates)()
        q_list.append((q, ans))
    return q_list

# Generate questions when starting a new level
if st.session_state.page == 'welcome' or st.session_state.page == 'congrats':
    st.session_state.questions[st.session_state.level] = generate_questions(st.session_state.level)

# Pages
if st.session_state.page == 'welcome':
    st.markdown("""
        <div style='background-color: #ffe6f0; padding: 20px; border-radius: 15px;'>
            <h1 style='text-align:center; font-size: 60px; color:#FF1493;'>🌟 Welcome to Math Fun Land! 🌟</h1>
            <p style='text-align:center; font-size: 22px; color:#7b2cbf;'>Get ready for an exciting math adventure!</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Start Test", use_container_width=True):
        st.session_state.page = 'question'
        st.session_state.start_time = time.time()

elif st.session_state.page == 'question':
    level = st.session_state.level
    q_idx = st.session_state.question_index
    questions_this_level = st.session_state.questions[level]

    if q_idx < len(questions_this_level):
        question, answer = questions_this_level[q_idx]
        st.markdown(f"<h2>Level {level} - Question {q_idx + 1}/5</h2>", unsafe_allow_html=True)
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

    if st.session_state.get('show_feedback', False):
        st.markdown(f"<h4>{st.session_state.feedback}</h4>", unsafe_allow_html=True)
        if st.button("Next Question", key=f"next_{q_idx}"):
            st.session_state.question_index += 1
            st.session_state.show_feedback = False
            st.rerun()

elif st.session_state.page == 'congrats':
    score = st.session_state.score
    level = st.session_state.level

    if score >= 3:
        st.balloons()
        st.markdown(f"""
            <h1 style='color:green;'>🎉 Congratulations!</h1>
            <p>You have completed Level {level} with a score of <b>{score}/5</b>.</p>
        """, unsafe_allow_html=True)

        if level < 3:
            if st.button("Proceed to Next Level", use_container_width=True):
                st.session_state.level += 1
                st.session_state.question_index = 0
                st.session_state.score = 0
                st.session_state.start_time = time.time()
                st.session_state.questions[st.session_state.level] = generate_questions(st.session_state.level)
                st.session_state.page = 'question'
                st.rerun()
        else:
            if st.button("Show Final Performance Summary", use_container_width=True):
                st.session_state.page = 'summary'
                st.rerun()
    else:
        st.markdown(f"""
            <h1 style='color:#cc0000;'>😢 Oops!</h1>
            <p>You scored <b>{score}/5</b> in Level {level}. You need at least 3 to proceed.</p>
            <p>Don't worry! Practice makes perfect. 💪 Try again!</p>
        """, unsafe_allow_html=True)

        if st.button("Retry Level", use_container_width=True):
            st.session_state.question_index = 0
            st.session_state.score = 0
            st.session_state.start_time = time.time()
            st.session_state.answers = [
                a for a in st.session_state.answers if a["Level"] != level
            ]
            st.session_state.questions[level] = generate_questions(level)
            st.session_state.page = 'question'
            st.rerun()

elif st.session_state.page == 'summary':
    st.title("📊 Final Performance Summary")
    df = pd.DataFrame(st.session_state.answers)

    def highlight_result(val):
        return 'background-color: lightgreen' if val == '✅ Correct' else 'background-color: lightcoral'

    st.dataframe(df.style.applymap(highlight_result, subset=['Result']))

    score = sum(1 for a in st.session_state.answers if a['Result'] == '✅ Correct')
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
