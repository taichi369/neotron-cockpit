import streamlit as st
import pandas as pd
import numpy as np

# ページ設定
st.set_page_config(page_title="NeoTRON", page_icon="⚡")

# --- CSS設定 ---
st.markdown("""
    <style>
        /* 1. 上部余白設定 */
        .block-container {
            padding-top: 4rem !important;
            padding-bottom: 1rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }

        /* 2. タイトル（最大サイズ 42px） */
        h1 {
            font-size: 42px !important;
            font-weight: 900 !important;
            margin-bottom: 0px !important;
            padding: 0 !important;
            line-height: 1.2 !important;
        }

        /* 3. 【重要】左右で文字サイズを変える設定 */
        
        /* 左側の列（心拍数）の数字だけを「50px（特大）」にする */
        div[data-testid="column"]:nth-of-type(1) [data-testid="stMetricValue"] {
            font-size: 50px !important;
            font-weight: 900 !important;
        }

        /* 右側の列（気分）の文字を「24px（控えめ）」にする */
        div[data-testid="column"]:nth-of-type(2) [data-testid="stMetricValue"] {
            font-size: 24px !important;
            font-weight: bold !important;
            line-height: 2.0 !important; /* 高さ位置を合わせるための調整 */
        }
        
        /* 項目名（ラベル）のサイズ */
        [data-testid="stMetricLabel"] {
            font-size: 14px !important;
            color: #666 !important;
        }

        /* 4. その他調整 */
        .stAlert { padding: 0.5rem !important; }
        hr { margin: 0.5rem 0 !important; }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------

# タイトル
st.title("⚡ 体調と助言")

# 区切り線
st.divider()

# サイドバー
st.sidebar.header("▼ 入力")
bpm = st.sidebar.slider("心拍数", 40, 180, 65)
mood = st.sidebar.select_slider("気分", ["絶不調", "低調", "普通", "好調", "絶好調"], value="普通")

# メイン表示
col1, col2 = st.columns(2)
with col1:
    # 左側：数字がデカくなる
    st.metric("心拍数", f"{bpm}", delta=bpm-65)
with col2:
    # 右側：文字が小さくなる
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

# グラフ
st.divider()
chart_data = pd.DataFrame(
    np.random.randn(20, 1) * 10 + bpm,
    columns=['推移'])
st.line_chart(chart_data, height=150)
