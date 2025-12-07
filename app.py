import streamlit as st
import pandas as pd
import numpy as np

# ページ設定
st.set_page_config(page_title="NeoTRON", page_icon="⚡")

# --- 【重要】CSSでデザインを強制変更（余白削除・文字サイズ固定） ---
st.markdown("""
    <style>
        /* 1. 全体のフォントサイズを12ptに固定 */
        html, body, [class*="css"] {
            font-size: 16px !important; /* Web上の16px ≒ 約12pt */
        }
        /* 2. タイトルのフォントサイズを14pt強（18px）に固定・余白削除 */
        h1, h2, h3 {
            font-size: 19px !important; /* 約14pt */
            font-weight: bold !important;
            padding: 0 !important;
            margin-bottom: 10px !important;
        }
        /* 3. 画面上部の巨大な余白を削除 */
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 1rem !important;
        }
        /* 4. 各要素の隙間を詰める */
        .stAlert { padding: 0.5rem !important; }
        .stMetric { margin-bottom: 0px !important; }
        hr { margin: 0.5rem 0 !important; }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------

# タイトル（コンパクトに）
st.markdown("### ⚡ 体調と助言")

# サイドバー（入力）
st.sidebar.header("▼ 入力")
bpm = st.sidebar.slider("心拍数", 40, 180, 65)
mood = st.sidebar.select_slider("気分", ["絶不調", "低調", "普通", "好調", "絶好調"], value="普通")

# 数値表示（2列でコンパクトに）
col1, col2 = st.columns(2)
with col1:
    st.metric("心拍数", f"{bpm}", delta=bpm-65)
with col2:
    st.metric("気分", mood)

# 区切り線
st.divider()

# 判定ロジック
if bpm > 100:
    msg = "負荷過多。冷静を欠く恐れがあります。"
    act = "深呼吸・休憩・水分補給をお勧めします。"
    alert_type = "error"
elif bpm < 50:
    msg = "活動低下。集中力低下の恐れがあります。"
    act = "散歩・ストレッチ・軽い運動をお勧めします。"
    alert_type = "warning"
else:
    msg = "安定しています。"
    act = "問題はありません。"
    alert_type = "success"

# 状態と助言（縦並びでスペース節約）
if alert_type == "error":
    st.error(f"**状態：** {msg}")
elif alert_type == "warning":
    st.warning(f"**状態：** {msg}")
else:
    st.success(f"**状態：** {msg}")

st.info(f"**助言：** {act}")

# グラフ（高さを半分以下の150pxにして一画面に収める）
chart_data = pd.DataFrame(
    np.random.randn(20, 1) * 10 + bpm,
    columns=['推移'])
st.line_chart(chart_data, height=150)
