import streamlit as st
import pandas as pd
import numpy as np

# ページ設定
st.set_page_config(page_title="体調と助言", page_icon="⚡")

# ▼▼▼ デザイン統一設定（CSS） ▼▼▼
# ここでフォント、色、サイズを一括管理します
st.markdown("""
    <style>
        /* 1. 日本語フォントの指定 (Windows/Mac両対応) */
        html, body, [class*="css"] {
            font-family: "Hiragino Sans", "Meiryo", "Yu Gothic", sans-serif;
        }

        /* 2. 画面上部の余白設定 */
        .block-container {
            padding-top: 3rem;
        }

        /* 3. 文字サイズの3段階ルール */
        /* 大 (Title) */
        h1 {
            font-size: 2.2rem !important;
            color: #262730; /* 濃い黒 */
            font-weight: 700;
        }
        /* 中 (Header) */
        h2, h3 {
            font-size: 1.5rem !important;
            color: #444444; /* 少し柔らかい黒 */
            font-weight: 600;
        }
        /* 小 (Body) はデフォルト設定を使用 */
    </style>
""", unsafe_allow_html=True)
# ▲▲▲ 設定ここまで ▲▲▲

# タイトル（大）
st.title("⚡ 体調と助言")

# サイドバー（中）
st.sidebar.header("データ入力")
bpm = st.sidebar.slider("現在の心拍数 (BPM)", min_value=40, max_value=180, value=65)
mood = st.sidebar.select_slider("メンタルコンディション", options=["絶不調", "低調", "通常", "好調", "絶好調"], value="通常")

# メイン画面（数値表示）
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

# 助言表示
st.info(f"**助言：** {action}")

# グラフ（中）
# 名称をシンプルに「バイタル」へ変更
st.subheader("バイタル")

chart_data = pd.DataFrame(
    np.random.randn(20, 1) * 10 + bpm,
    columns=['BPM'])
st.line_chart(chart_data)
