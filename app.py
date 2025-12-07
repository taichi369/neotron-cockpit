import streamlit as st
import pandas as pd
import numpy as np

# ページ設定
st.set_page_config(page_title="体調と助言", page_icon="⚡")

# スマホ用レイアウト調整
st.markdown("""
    <style>
        .block-container {
            padding-top: 3rem;
        }
    </style>
""", unsafe_allow_html=True)

# タイトル
st.title("⚡ 体調と助言")

# サイドバー（入力エリア）
st.sidebar.header("データ入力")
bpm = st.sidebar.slider("現在の心拍数 (BPM)", min_value=40, max_value=180, value=65)
mood = st.sidebar.select_slider("メンタルコンディション", options=["絶不調", "低調", "通常", "好調", "絶好調"], value="通常")

# メイン画面
col1, col2 = st.columns(2)

with col1:
    st.metric(label="心拍数 (BPM)", value=bpm, delta=bpm - 65)

with col2:
    st.metric(label="状態", value=mood)

st.divider()

# 状況判定ロジック
if bpm > 100:
    st.error("警告：心拍数上昇")
    action = "深呼吸・休憩・水分補給をして下さい。"
elif bpm < 50:
    st.warning("注意：覚醒レベル低下")
    action = "ストレッチや散歩をお勧めします。"
else:
    st.success("状態：安定")
    action = "安定、この状態を続けてください。"

st.info(f"**助言：** {action}")

# グラフ
st.subheader("バイタル推移")
chart_data = pd.DataFrame(
    np.random.randn(20, 1) * 10 + bpm,
    columns=['BPM'])
st.line_chart(chart_data)

