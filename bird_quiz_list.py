import streamlit as st
import os
import base64

# ====== 設定 ======
AUDIO_FOLDER = "data"
PASSWORD = "toridaisuki"

# ====== パスワード認証 ======
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("鳥クイズ（一覧モード）ログイン")
    pwd = st.text_input("パスワードを入力してください", type="password")
    if pwd == PASSWORD:
        st.session_state.authenticated = True
        st.rerun()
    elif pwd:
        st.error("パスワードが違います")
    st.stop()

# ====== クイズ表示 ======
st.title("鳥の鳴き声クイズ（一覧モード）")

files = [f for f in os.listdir(AUDIO_FOLDER) if f.endswith(".mp3")]
files.sort()  # 並び順は名前順。シャッフルしたければ random.shuffle(files)

# セッションに回答・結果の保持用辞書を用意
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "results" not in st.session_state:
    st.session_state.results = {}

# 結果集計用
correct_count = 0

# 表示
for file in files:
    bird_name = os.path.splitext(file)[0]
    col1, col2, col3 = st.columns([2, 3, 2])

    # 音声（base64埋め込みで互換性向上）
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

    # 回答入力
    answer_key = f"answer_{bird_name}"
    answer = col2.text_input("鳥の名前を入力", key=answer_key)

    # 判定
    if answer:
        if answer.strip().lower() == bird_name.lower():
            st.session_state.results[bird_name] = True
            col3.success("正解！")
            correct_count += 1
        else:
            st.session_state.results[bird_name] = False
            col3.error(f"不正解（正解：{bird_name}）")
    else:
        col3.write("未回答")

# 最後に正解数表示
st.markdown("---")
st.success(f"正解数：{correct_count} / {len(files)}")

