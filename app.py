import streamlit as st
import pandas as pd
import numpy as np

# ページ基本設定
st.set_page_config(page_title="NeoTRON", page_icon="⚡")

# --- 【デザインシステム定義】 ---
# ここで「規定値」を一括管理します。
# 1rem = ブラウザの標準文字サイズ（通常16px）
st.markdown("""
    <style>
        /* --- 1. 基準となる規定値のセット --- */
        
        /* 全体のベースライン */
        html, body, p, .stMarkdown {
            font-size: 1.0rem !important; /* 規定値：1倍 */
        }

        /* レベル1：タイトル・重要数値（2倍サイズで統一） */
        h1, [data-testid="stMetricValue"] {
            font-size: 2.5rem !important; /* 規定値：2.5倍 */
            font-weight: 700 !important;  /* 太さ：Bold */
            line-height: 1.2 !important;
            padding: 0 !important;
        }

        /* レベル2：項目ラベル（標準より少し小さく、色は薄く） */
        [data-testid="stMetricLabel"] {
            font-size: 0.875rem !important; /* 規定値：0.875倍 */
            font-weight: 400 !important;
            color: #555 !important;
        }

        /* --- 2. レイアウトの規定 --- */
        
        /* 上部余白のルール化（タイトル用スペース） */
        .block-container {
            padding-top: 3rem !important;
            padding-bottom: 1rem !important;
        }

        /* 余分な隙間の削除 */
        hr { margin: 1rem 0 !important; }
        .stAlert { padding: 0.5rem 1rem !important; }
        
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------

# タイトル（レベル1が適用される）
st.title("⚡ 体調と助言")

# 区切り線
st.divider()

# サイドバー：入力エリア
st.sidebar.header("▼ 入力")
bpm = st.sidebar.slider("心拍数", 40, 180, 65)
mood = st.sidebar.select_slider("気分", ["絶不調", "低調", "普通", "好調", "絶好調"], value="普通")

# メイン表示：重要数値（CSSにより、レベル1の大きさに自動統一）
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

# グラフ（下部に配置）
st.divider()
chart_data = pd.DataFrame(
    np.random.randn(20, 1) * 10 + bpm,
    columns=['推移'])
st.line_chart(chart_data, height=150)
