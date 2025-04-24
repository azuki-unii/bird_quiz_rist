import streamlit as st
import os
import random
import base64

AUDIO_FOLDER = "data"

# 初回読み込み時のみシャッフル
if "shuffled_files" not in st.session_state:
    files = [f for f in os.listdir(AUDIO_FOLDER) if f.endswith(".mp3")]
    random.shuffle(files)
    st.session_state.shuffled_files = files
    st.session_state.answers = {}
    st.session_state.results = {}

files = st.session_state.shuffled_files
correct_count = 0

st.title("鳥の鳴き声クイズ（まとめて記述式）")

for file in files:
    bird_name = os.path.splitext(file)[0]
    col1, col2, col3 = st.columns([2, 3, 2])

    with open(os.path.join(AUDIO_FOLDER, file), "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    col1.markdown(
        f"""
        <audio controls>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            Your browser does not support the audio element.
        </audio>
        """,
        unsafe_allow_html=True,
    )

    answer_key = f"answer_{bird_name}"
    answer = col2.text_input("鳥の名前を入力", key=answer_key)

    result_key = f"result_{bird_name}"
    if answer:
        is_correct = answer.strip().lower() == bird_name.lower()
        st.session_state[result_key] = is_correct

        if is_correct:
            col3.success("正解！")
        else:
            col3.error(f"不正解（正解：{bird_name}）")
    else:
        col3.write("未回答")

    if st.session_state.get(result_key):
        correct_count += 1

st.markdown("---")
st.success(f"正解数：{correct_count} / {len(files)}")

# ====== もう一度やる（シャッフル）ボタン ======
if st.button("もう一度やる（ランダム順）"):
    new_files = [f for f in os.listdir(AUDIO_FOLDER) if f.endswith(".mp3")]
    random.shuffle(new_files)
    st.session_state.shuffled_files = new_files
    st.session_state.answers = {}
    st.session_state.results = {}
    st.rerun()
