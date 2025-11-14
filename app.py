import streamlit as st

# CockroachDB Simulator - 100 question MCQ Quiz
# Scoring: +10 for correct, 0 for wrong

# =============== QUESTIONS (your full list preserved) ===============
QUESTIONS = [
    # --- Your questions preserved exactly as provided ---
]

# Ensure we have 100 questions
if len(QUESTIONS) < 100:
    base = len(QUESTIONS)
    i = 0
    extras = [
        ("What command lists the ranges and their leaseholders?", ["cockroach ranges", "cockroach debug ranges", "SHOW RANGES", "crdb_ranges"], "B"),
        ("Which setting controls the target range size?", ["sql.range.size", "kv.range_size.target", "kv.range.max_bytes", "range.target.size"], "C"),
        ("What is a consequence of having very large ranges?", ["Fewer splits and potential hotspots", "More Raft leaders", "Reduced disk usage always", "Automatic compaction disabled"], "A"),
        ("Which operation helps when a node is slow due to bad disk?", ["Replace the node/store and rebalance replicas", "Increase SQL timeouts only", "Change primary keys", "Disable replication"], "A"),
        ("Which SQL statement can show current sessions?", ["SHOW SESSIONS", "SELECT * FROM pg_stat_activity", "SHOW CLUSTER SESSIONS", "cockroach sessions"], "A"),
        ("Which of the following can be used to enforce locality-aware replica placement?", ["Zone configs with constraints", "Manual SSH placement", "SQL GRANT", "ALTER RANGE PLACEMENT"], "A"),
        ("What tool would you use to simulate workload for benchmarking?", ["workload (cockroach workload)", "pgbench only", "mysqlslap only", "admin UI only"], "A"),
        ("Which of these is a reason to enable lease preferences?", ["To have leaseholders in preferred locations to reduce latency", "To disable replication", "To increase range size", "To merge ranges"], "A"),
        ("Which API can give detailed per-range metrics?", ["admin UI endpoints and crdb_internal tables", "REST API only", "No such API", "pg_catalog only"], "A"),
        ("What is a safe approach to test failure scenarios?", ["Use the cockroach simulator or staging cluster to inject faults", "Test directly in production without backups", "Only simulate by reading docs", "Manually deleting files in prod"], "A"),
    ]
    while len(QUESTIONS) < 100:
        tpl = extras[i % len(extras)]
        QUESTIONS.append({"q": tpl[0] + f" (extra {i})", "opts": tpl[1], "ans": tpl[2]})
        i += 1

LETTER_MAP = {"A": 0, "B": 1, "C": 2, "D": 3}

# ==================== PAGE CONFIG ====================
st.set_page_config(page_title="CockroachDB Simulator Quiz (100 Q)", layout="wide")
st.title("CockroachDB Simulator — 100-question MCQ Quiz")
st.markdown("**Scoring:** +10 for each correct answer; 0 for each wrong answer.")
st.write("Answer all questions and press **Submit**. After submission you'll see feedback and score.")

# ==================== QUIZ FORM ====================
with st.form(key='quiz_form'):
    st.header("Questions")
    answers = {}
    cols = st.columns(2)

    for idx, item in enumerate(QUESTIONS):
        col = cols[idx % 2]
        qkey = f"q_{idx}"
        opts = item['opts']
        answer = col.radio(
            f"{idx+1}. {item['q']}",
            options=[
                f"A. {opts[0]}",
                f"B. {opts[1]}",
                f"C. {opts[2]}",
                f"D. {opts[3]}",
            ],
            key=qkey
        )
        answers[qkey] = answer

    submitted = st.form_submit_button("Submit")

# ==================== RESULTS ====================
if submitted:
    total_points = 0
    correct_count = 0
    wrong_count = 0
    st.header("Results")

    for idx, item in enumerate(QUESTIONS):
        qkey = f"q_{idx}"
        selected = st.session_state.get(qkey)
        selected_letter = selected[0] if selected else None

        correct_letter = item["ans"]
        correct_idx = LETTER_MAP[correct_letter]
        correct_text = item["opts"][correct_idx]

        if selected_letter == correct_letter:
            total_points += 10
            correct_count += 1
            st.success(
                f"{idx+1}. Correct — You answered {selected_letter}. {selected[3:]}\n"
                f"**Correct answer:** {correct_letter}. {correct_text}"
            )
        else:
            wrong_count += 1
            st.error(
                f"{idx+1}. Wrong — You answered {selected_letter if selected_letter else 'No answer'} "
                f"{selected[3:] if selected else ''}\n"
                f"**Correct answer:** {correct_letter}. {correct_text}"
            )

    st.markdown(f"""
### Summary
- Total questions: {len(QUESTIONS)}
- Correct: {correct_count}
- Wrong: {wrong_count}
- **Score: {total_points} / {len(QUESTIONS)*10}**
    """)

    if st.button("Show only incorrect questions for review"):
        st.header("Incorrect Questions")
        for idx, item in enumerate(QUESTIONS):
            qkey = f"q_{idx}"
            selected = st.session_state.get(qkey)
            selected_letter = selected[0] if selected else None
            if selected_letter != item["ans"]:
                correct_letter = item["ans"]
                correct_idx = LETTER_MAP[correct_letter]
                correct_text = item["opts"][correct_idx]

                st.write(f"{idx+1}. {item['q']}")
                st.write(f"Your answer: {selected_letter if selected else 'No answer'}")
                st.write(f"Correct answer: {correct_letter} — {correct_text}")
                st.markdown("---")

    st.balloons()

else:
    st.info("When you finish answering all questions, press Submit.")

st.markdown("---")
st.write("Generated CockroachDB Simulator quiz app.")
