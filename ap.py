import streamlit as st
import random
import time
import pandas as pd
import re

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

# Question generator
def generate_questions(level):
    q_list = []
    for _ in range(5):
        if level == 1:
            a, b = random.randint(1, 10), random.randint(1, 10)
            op = random.choice(['+', '-'])
            q, ans = f"{a} {op} {b}", eval(f"{a}{op}{b}")
        elif level == 2:
            a, b = random.randint(2, 10), random.randint(1, 10)
            op = random.choice(['*', '/'])
            if op == '/':
                a = a * b
            q, ans = f"{a} {op} {b}", int(eval(f"{a}{op}{b}"))
        else:
            def t1():
                a, b = random.randint(1, 10), random.randint(1, 10)
                return f"Tom has {a} candies. He got {b} more. How many?", a + b
            def t2():
                a, b = random.randint(5, 15), random.randint(1, 5)
                return f"Anna had {a} apples, gave away {b}. How many left?", a - b
            def t3():
                a, b = random.randint(2, 5), random.randint(2, 5)
                return f"There are {a} bags, each with {b} toys. How many?", a * b
            def t4():
                a = random.choice([6, 8, 10])
                b = random.randint(1, a // 2)
                return f"A pizza is cut into {a} slices. You ate {b}. Left?", a - b
            def t5():
                a, b = random.randint(5, 10), random.randint(1, 4)
                return f"You have {a} pens, gave {b} to a friend. Left?", a - b
            q, ans = random.choice([t1, t2, t3, t4, t5])()
        q_list.append((q, ans))
    return q_list

# Regenerate on entering welcome or congrats
if st.session_state.page in ('welcome', 'congrats'):
    st.session_state.questions[st.session_state.level] = generate_questions(st.session_state.level)

# --- Welcome Page ---
if st.session_state.page == 'welcome':
    st.markdown("""
        <div style='background-color:#ffe6f0;padding:20px;border-radius:15px;'>
            <h1 style='text-align:center;font-size:60px;color:#FF1493;'>🌟 Welcome to Math Fun Land! 🌟</h1>
            <p style='text-align:center;font-size:22px;color:#7b2cbf;'>Get ready for an exciting math adventure!</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Start Test", use_container_width=True):
        st.session_state.page = 'question'
        st.session_state.start_time = time.time()

# --- Question Page ---
elif st.session_state.page == 'question':
    level = st.session_state.level
    q_idx = st.session_state.question_index
    questions = st.session_state.questions[level]

    # Progress indicator (blank when q_idx=0)
    label = "" if q_idx == 0 else str(q_idx)
    st.markdown(f"<h3 style='text-align:center;color:#800080;'>📚 Level {level} Progress: {label}/5</h3>", unsafe_allow_html=True)
    st.progress(q_idx / 5)

    if q_idx < len(questions):
        question, answer = questions[q_idx]
        st.markdown(f"""
            <div style='background-color:#fff3cd;color:black;padding:20px;
                        border-radius:15px;box-shadow:2px 2px 8px rgba(0,0,0,0.1);
                        font-size:24px;text-align:center;margin-bottom:20px;'>
                <b>Level {level} - Question {q_idx+1}/5</b><br><br>
                <span>Solve: {question}</span>
            </div>
        """, unsafe_allow_html=True)

        # Text input for integer-only answer (allow + or -)
        user_input = st.text_input("Your Answer", key=f"answer_{q_idx}", placeholder="e.g., -3, 0, 7")
        pattern = r'^[+-]?\d+$'
        is_valid_int = bool(re.match(pattern, user_input.strip()))

        if user_input and not is_valid_int:
            st.warning("Please enter only whole numbers (e.g., -2, 0, 5).")

        if st.button("Submit Answer", key=f"submit_{q_idx}", disabled=not is_valid_int):
            user_answer = int(user_input)
            correct = (user_answer == answer)
            elapsed = round(time.time() - st.session_state.start_time, 2)
            st.session_state.answers.append({
                "Level": level,
                "Question": question,
                "Correct Answer": answer,
                "Your Answer": user_answer,
                "Result": "✅ Correct" if correct else "❌ Incorrect",
                "Time (s)": elapsed
            })
            if correct:
                st.session_state.score += 1
            st.session_state.feedback = "✅ Correct!" if correct else f"❌ Incorrect! The correct answer is {answer}."
            st.session_state.show_feedback = True
            st.session_state.start_time = time.time()
            st.rerun()
    else:
        st.session_state.page = 'congrats'
        st.rerun()

    # Feedback + Next
    if st.session_state.get('show_feedback', False):
        st.markdown(f"<h4>{st.session_state.feedback}</h4>", unsafe_allow_html=True)
        if st.button("Next Question", key=f"next_{q_idx}"):
            st.session_state.question_index += 1
            st.session_state.show_feedback = False
            st.rerun()

# --- Congrats Page ---
elif st.session_state.page == 'congrats':
    score = st.session_state.score
    passed = (score >= 3)

    if passed:
        st.balloons()
        st.markdown(f"""
            <div style='background-color:#d4edda;padding:20px;border-radius:15px;'>
                <h1 style='color:green;'>🎉 Congratulations!</h1>
                <p>You completed Level {st.session_state.level} with a score of <b>{score}/5</b>.</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div style='background-color:#ffe6e6;padding:20px;border-radius:15px;'>
                <h1 style='color:red;'>😞 Oops!</h1>
                <p style='color:black;'>You scored <b>{score}/5</b>. You need at least 3 correct answers to move to the next level.</p>
            </div>
        """, unsafe_allow_html=True)

    if passed:
        if st.session_state.level < 3:
            if st.button("Proceed to Next Level", use_container_width=True):
                st.session_state.level += 1
                st.session_state.questions[st.session_state.level] = generate_questions(st.session_state.level)
                st.session_state.question_index = 0
                st.session_state.score = 0
                st.session_state.page = 'question'
                st.session_state.start_time = time.time()
                st.rerun()
        else:
            if st.button("Show Final Performance Summary", use_container_width=True):
                st.session_state.page = 'summary'
                st.rerun()
    else:
        if st.button("Retry Level", use_container_width=True):
            st.session_state.questions[st.session_state.level] = generate_questions(st.session_state.level)
            st.session_state.question_index = 0
            st.session_state.score = 0
            st.session_state.show_feedback = False
            st.session_state.page = 'question'
            st.session_state.start_time = time.time()
            st.rerun()

# --- Summary Page ---
elif st.session_state.page == 'summary':
    st.title("📊 Final Performance Summary")
    df = pd.DataFrame(st.session_state.answers)

    def highlight_result(val):
        return 'background-color: lightgreen' if val == '✅ Correct' else 'background-color: lightcoral'

    st.dataframe(df.style.applymap(highlight_result, subset=['Result']))

    total_correct = sum(a['Result']=='✅ Correct' for a in st.session_state.answers)
    total_q = len(st.session_state.answers)
    st.markdown(f"<h2 style='color:#0055ff;'>You got {total_correct} out of {total_q} questions right!</h2>", unsafe_allow_html=True)

    chart_df = pd.DataFrame({
        'Time Taken (s)': [e['Time (s)'] for e in st.session_state.answers],
        'Question': list(range(1, total_q+1))
    })
    st.line_chart(chart_df.set_index('Question'))
    st.success("Great job completing all levels! 🎉")
    if st.button("Restart Test"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()
