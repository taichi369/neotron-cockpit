import streamlit as st
import pandas as pd
import numpy as np

# タブ名（ブラウザ用）
st.set_page_config(page_title="NeoTRON", page_icon="⚡")

# タイトル：1行で収まる最短の表現
st.title("⚡ 体調と助言")

st.divider()

# サイドバー：入力
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

# 判定ロジック
if bpm > 100:
    status_msg = "負荷過多。冷静さを欠く恐れあり。"
    action = "深呼吸・休憩・水分補給"
    alert_type = "error"
elif bpm < 50:
    status_msg = "活動低下。集中力低下の恐れあり。"
    action = "散歩・ストレッチ・軽い運動"
    alert_type = "warning"
else:
    status_msg = "安定。最適な状態。"
    action = "3S（整理・整頓・清掃）と重要課題の処理"
    alert_type = "success"

# 1. 体調
st.subheader("▼ 体調")
if alert_type == "error":
    st.error(status_msg)
elif alert_type == "warning":
    st.warning(status_msg)
else:
    st.success(status_msg)

# 2. 助言
st.subheader("▼ 助言")
st.info(f"### {action}")

# グラフ
st.divider()
chart_data = pd.DataFrame(
    np.random.randn(20, 1) * 10 + bpm,
    columns=['推移'])
st.line_chart(chart_data, height=200)
