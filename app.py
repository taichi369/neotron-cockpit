import streamlit as st
import pandas as pd
import numpy as np

# ページ設定
st.set_page_config(page_title="NeoTRON", page_icon="⚡")

# --- CSSで「文字サイズの統一」と「タイトルの表示」を強制設定 ---
st.markdown("""
    <style>
        /* 1. 画面上部の余白を確保（タイトルが見えるように調整） */
        .block-container {
            padding-top: 2rem !important; /* 余裕を持たせる */
            padding-bottom: 1rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }

        /* 2. 基本の文字サイズを12pt（16px）に統一 */
        html, body, p, .stMarkdown, .stRadio label {
            font-size: 16px !important;
        }

        /* 3. タイトルを14pt（19px）にし、余計な余白を消す */
        h1 {
            font-size: 19px !important;
            font-weight: bold !important;
            margin-bottom: 15px !important;
            padding-top: 0 !important;
        }

        /* 4. 【重要】「心拍数」と「気分」の文字サイズを強制的に揃える */
        /* 数値も文字も、両方30px（かなり大きく）で統一 */
        [data-testid="stMetricValue"] {
            font-size: 30px !important;
            font-weight: bold !important;
            line-height: 1.2 !important;
        }
        
        /* ラベル（項目名）は小さく */
        [data-testid="stMetricLabel"] {
            font-size: 14px !important;
        }

        /* 5. その他の隙間調整 */
        .stAlert { padding: 0.5rem !important; }
        hr { margin: 0.5rem 0 !important; }
        .stButton button { width: 100%; }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------

# タイトル（h1タグとして出力）
st.title("⚡ 体調と助言")

# サイドバー
st.sidebar.header("▼ 入力")
bpm = st.sidebar.slider("心拍数", 40, 180, 65)
mood = st.sidebar.select_slider("気分", ["絶不調", "低調", "普通", "好調", "絶好調"], value="普通")

# メイン表示（文字サイズはCSSで統一済み）
col1, col2 = st.columns(2)
with col1:
    st.metric("心拍数", f"{bpm}", delta=bpm-65)
with col2:
    st.metric("気分", mood)

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

# 状態と助言
if alert_type == "error":
    st.error(f"**状態：** {msg}")
elif alert_type == "warning":
    st.warning(f"**状態：** {msg}")
else:
    st.success(f"**状態：** {msg}")

st.info(f"**助言：** {act}")

# グラフ（一画面に収まるよう高さを抑制）
chart_data = pd.DataFrame(
    np.random.randn(20, 1) * 10 + bpm,
    columns=['推移'])
st.line_chart(chart_data, height=150)
