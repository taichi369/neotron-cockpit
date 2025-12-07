import streamlit as st
import pandas as pd
import numpy as np

# ページ設定
st.set_page_config(page_title="NeoTRON", page_icon="⚡")

# --- CSS設定（デザインの強制修正） ---
st.markdown("""
    <style>
        /* 1. 画面上部の余白設定（タイトルが隠れないギリギリの高さ 4rem に調整） */
        .block-container {
            padding-top: 4rem !important;
            padding-bottom: 1rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }

        /* 2. タイトル（h1）を「一番大きく」設定（42px） */
        h1 {
            font-size: 42px !important;
            font-weight: 900 !important; /* 極太 */
            margin-bottom: 0px !important;
            padding: 0 !important;
            line-height: 1.2 !important;
        }

        /* 3. 数字・文字のサイズ（30px）→ タイトルより少し小さくする */
        [data-testid="stMetricValue"] {
            font-size: 30px !important;
            font-weight: bold !important;
        }
        
        /* 項目名（心拍数など） */
        [data-testid="stMetricLabel"] {
            font-size: 14px !important;
        }

        /* 4. アラートの余白を詰める */
        .stAlert { padding: 0.5rem !important; }
        
        /* 5. 区切り線の余白を最小化 */
        hr { margin: 0.5rem 0 !important; }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------

# タイトル（42pxで最大表示）
st.title("⚡ 体調と助言")

# 区切り線
st.divider()

# サイドバー
st.sidebar.header("▼ 入力")
bpm = st.sidebar.slider("心拍数", 40, 180, 65)
mood = st.sidebar.select_slider("気分", ["絶不調", "低調", "普通", "好調", "絶好調"], value="普通")

# メイン表示（数字は30px）
col1, col2 = st.columns(2)
with col1:
    st.metric("心拍数", f"{bpm}", delta=bpm-65)
with col2:
    st.metric("気分", mood)

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

# 状態と助言
if alert_type == "error":
    st.error(f"**状態：** {msg}")
elif alert_type == "warning":
    st.warning(f"**状態：** {msg}")
else:
    st.success(f"**状態：** {msg}")

st.info(f"**助言：** {act}")

# グラフ（確実に表示させるため divider を入れて区切る）
st.divider()
chart_data = pd.DataFrame(
    np.random.randn(20, 1) * 10 + bpm,
    columns=['推移'])
st.line_chart(chart_data, height=150)
