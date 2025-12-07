import streamlit as st
import pandas as pd
import numpy as np

# ブラウザのタブ名にはシステム名を残す（画面には出ない）
st.set_page_config(page_title="NeoTRON システム", page_icon="⚡")

# タイトル：マークと、要点のみ
st.title("⚡ 今の体調と、あなたへの助言")

st.divider()

# サイドバー：極限までシンプルに
st.sidebar.header("▼ 入力")
bpm = st.sidebar.slider("心拍数", min_value=40, max_value=180, value=65)
mood = st.sidebar.select_slider("気分", options=["絶不調", "低調", "普通", "好調", "絶好調"], value="普通")

# 数値表示
col1, col2 = st.columns(2)
with col1:
    st.metric(label="心拍数", value=f"{bpm}", delta=bpm - 65)
with col2:
    st.metric(label="気分", value=mood)

st.divider()

# 判定ロジック（裏側の仕組みはそのまま）
if bpm > 100:
    status_msg = "負荷過多。冷静さを欠いている可能性あり。"
    action = "深呼吸し、一度休憩せよ（水分補給）"
    alert_type = "error"
elif bpm < 50:
    status_msg = "活動低下。集中力が落ちている可能性あり。"
    action = "軽く体を動かし、覚醒させよ（散歩・ストレッチ）"
    alert_type = "warning"
else:
    status_msg = "安定。心身ともに最適な状態。"
    action = "「3S（整理・整頓・清掃）」を行い、重要課題に着手せよ"
    alert_type = "success"

# --- ここが要点 ---

# 1. 体調の表示
st.subheader("▼ 今の体調")
if alert_type == "error":
    st.error(status_msg)
elif alert_type == "warning":
    st.warning(status_msg)
else:
    st.success(status_msg)

# 2. 助言の表示
st.subheader("▼ あなたへの助言")
st.info(f"### {action}")

# グラフ（補足情報として下に置く）
st.divider()
chart_data = pd.DataFrame(
    np.random.randn(20, 1) * 10 + bpm,
    columns=['推移'])
st.line_chart(chart_data, height=200)
