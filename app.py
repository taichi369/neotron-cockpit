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
""", unsafe_allow_html
