import streamlit as st
import pandas as pd
import numpy as np

# ページ設定
st.set_page_config(page_title="NeoTRON", page_icon="⚡")

# --- CSS設定 ---
st.markdown("""
    <style>
        /* 1. 【修正箇所】画面上部の余白を大幅に確保（隠れるのを防ぐ） */
        .block-container {
            padding-top: 5rem !important; /* これだけ空ければ絶対に隠れません */
            padding-bottom: 1rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }

        /* 2. 基本文字サイズ */
        html, body, p, .stMarkdown, .stRadio label {
            font-size: 16px !important;
        }

        /* 3. タイトル（h1）の設定 */
        h1 {
            font-size: 22px !important; /* 少し大きくして視認性アップ */
            font-weight: bold !important;
            margin-bottom: 0px !important;
            padding: 0 !important;
        }

        /* 4. 「心拍数」と「気分」の数字・文字の大きさを完全一致させる */
        [data-testid="stMetricValue"] {
            font-size: 32px !important; /* 両方ともこのサイズに強制統一 */
            font-weight: bold !important;
            line-height: 1.2 !important;
        }
        
        /* 項目名（心拍数、気分）は小さく控えめに */
        [data-testid="stMetricLabel"] {
            font-size: 14px !important;
        }

        /* 5. 余計な隙間をカット */
        .stAlert { padding: 0.5rem !important; }
        hr { margin: 0.5rem 0 !important; }
        div[data-testid="stVerticalBlock"] > div { gap: 0.5rem; }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------

# タイトル
st.title("⚡ 体調と助言")

# 区切り線をタイトルの直下に配置
st.divider()

# サイドバー
st.sidebar.header("▼ 入力")
bpm = st.sidebar.slider("心拍数", 40, 180, 65)
mood = st.sidebar.select_slider("気分", ["絶不調", "低調", "普通", "好調", "絶好調"], value="普通")

# メイン表示（文字サイズはCSSで32pxに統一済み）
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

#
