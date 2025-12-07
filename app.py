import streamlit as st
import pandas as pd
import numpy as np

# ページ設定
st.set_page_config(page_title="体調と助言", page_icon="⚡")

# ▼▼▼ スマホ用レイアウト調整（タイトル隠れ防止） ▼▼▼
st.markdown("""
    <style>
        .block-container {
            padding-top: 3rem;
        }
    </style>
""", unsafe_allow_html=True)
# ▲▲▲ 調整ここまで ▲▲▲

# タイトル（ご指定の名前）
st.title("⚡ 体調と助言")

# サイドバー（入力エリア）
st.sidebar.header("データ入力")
bpm = st.sidebar.slider("現在の心拍数 (BPM)", min_value=40, max_value=180, value=65)
mood = st.sidebar.select_slider("メンタルコンディション", options=["絶不調", "低調", "通常", "好調", "絶好調"], value="通常")

# メイン画面（表示エリア）
col1, col2 = st.columns(2)

with col1:
    st.metric(label="心拍数 (BPM)", value=bpm, delta=bpm - 65)

with col2:
    st.metric(label="状態", value=mood)

st.divider()

# 状況判定ロジック
if bpm > 100:
    st.error("🚨 警告：心拍数上昇。深呼吸を実行せよ。")
    action = "深呼吸・休憩・水分補給"
elif bpm < 50:
    st.warning("⚠️ 注意：覚醒レベル低下。軽く運動せよ。")
    action = "ストレッチ・散歩・カフェイン摂取"
else:
    st.success("✅ 状態：安定。論理的思考が可能。")
    action = "3S（整理・整頓・清掃）・重要課題の処理"

st.info(f"**助言：** {action}")

# グラフ（シミュレーション）
st.subheader("バイタル推移")
chart_data = pd.DataFrame(
    np.random.randn(20, 1) * 10 + bpm,
    columns=['BPM'])
st.line_chart(chart_data)
