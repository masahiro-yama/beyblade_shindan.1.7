import streamlit as st
import random

# ------------------------
# 初期化
# ------------------------
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.answers = []
    st.session_state.questions = []

# ------------------------
# 質問データ
# ------------------------
base_questions = [
    ("やすみじかん、なにしてる？", [
        ("A", "🏃 はしりまわってあそぶ"),
        ("B", "👀 みんなのようすを見る"),
        ("C", "🧩 しずかにあそぶ"),
        ("D", "🎲 きぶんでかえる"),
    ]),
    ("ともだちとけんかしたら？", [
        ("A", "🔥 すぐいいかえす"),
        ("B", "🧠 いちど考える"),
        ("C", "😌 気にしない"),
        ("D", "🤝 あわせる"),
    ]),
]

extra_questions = [
    ("ヒーローになるなら？", [
        ("A", "💥 こうげき"),
        ("B", "🛡 まもり"),
        ("C", "🔄 ずっとがんばる"),
        ("D", "⚡ なんでもできる"),
    ])
]

def generate_questions():
    q = base_questions.copy()
    q.append(random.choice(extra_questions))
    random.shuffle(q)
    return q

# ------------------------
# 判定
# ------------------------
def get_result(answers):
    count = {"A":0, "B":0, "C":0, "D":0}
    for a in answers:
        count[a] += 1

    max_score = max(count.values())
    top = [k for k, v in count.items() if v == max_score]

    if len(top) > 1:
        return "バランス"

    return {
        "A": "アタック",
        "B": "ディフェンス",
        "C": "スタミナ",
        "D": "バランス"
    }[top[0]]

# ------------------------
# トップ画面（ワクワク強化）
# ------------------------
if st.session_state.step == 0:
    st.markdown("## 🌀 ベイブレードX しんだん")
    st.markdown("### ⚔ キミのタイプを見つけろ！")
    st.image("https://i.imgur.com/8QfQFqK.png")  # 雰囲気画像（差し替えOK）

    if st.button("🚀 バトルスタート！", use_container_width=True):
        st.session_state.questions = generate_questions()
        st.session_state.answers = []
        st.session_state.step = 1
        st.rerun()

# ------------------------
# 質問画面（ボタン化＋戻る）
# ------------------------
elif st.session_state.step <= len(st.session_state.questions):

    q_index = st.session_state.step - 1
    question, options = st.session_state.questions[q_index]

    st.markdown(f"### Q{st.session_state.step}")
    st.markdown(f"## {question}")

    # 選択肢をボタンにする
    for key, text in options:
        if st.button(text, use_container_width=True):
            st.session_state.answers.append(key)
            st.session_state.step += 1
            st.rerun()

    # 戻るボタン
    if st.session_state.step > 1:
        if st.button("⬅ もどる"):
            st.session_state.step -= 1
            st.session_state.answers.pop()
            st.rerun()

# ------------------------
# 結果
# ------------------------
else:
    result = get_result(st.session_state.answers)

    st.markdown("## 🎉 けっか！")

    if result == "アタック":
        st.markdown("### 💥 こうげきマスター！")
    elif result == "ディフェンス":
        st.markdown("### 🛡 まもりのたつじん！")
    elif result == "スタミナ":
        st.markdown("### 🔄 ねばりの王！")
    else:
        st.markdown("### ⚡ オールラウンダー！")

    st.divider()

    if st.button("🔁 もういちどやる", use_container_width=True):
        st.session_state.step = 0
        st.rerun()