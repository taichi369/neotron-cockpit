import streamlit as st
import pandas as pd
import numpy as np

# ページ設定
st.set_page_config(page_title="NeoTRON", page_icon="⚡")

# --- 【デザインシステム：文字サイズの調整】 ---
st.markdown("""
    <style>
        /* 基本設定 */
        html, body, p, .stMarkdown {
            font-size: 1.0rem !important;
        }

        /* --- ランク1：タイトル（修正：スマホで見やすいサイズへ縮小） --- */
        /* 3.5rem -> 2.2rem に変更 */
        h1 {
            font-size: 2.2rem !important;
            font-weight: 900 !important;
            line-height: 1.2 !important;
            padding: 0 !important;
            margin-bottom: 0.5rem !important;
        }

        /* --- ランク2：数値と気分の文字 --- */
        [data-testid="stMetricValue"] {
            font-size: 2.5rem !important;
            font-weight: 700 !important;
            line-height: 1.2 !important;
        }

        /* ランク3：項目ラベル */
        [data-testid="stMetricLabel"] {
            font-size: 0.875rem !important;
            color: #555 !important;
        }

        /* レイアウト調整 */
        .block-container {
            padding-top: 2rem !important; /* 上の余白も少し詰める */
            padding-bottom: 1rem !important;
        }

        /* 余分な隙間の削除 */
        hr { margin: 1rem 0 !important; }
        .stAlert { padding: 0.5rem 1rem !important; }

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

# 状態の表示
if alert_type == "error":
    st.error(f"**状態：** {msg}")
elif alert_type == "warning":
    st.warning(f"**状態：** {msg}")
else:
    st.success(f"**状態：** {msg}")

# 助言の表示
st.info(f"**助言：** {act}")

# グラフ
st.divider()
chart_data = pd.DataFrame(
    np.random.randn(20, 1) * 10 + bpm,
    columns=['推移'])
st.line_chart(chart_data, height=150)
