import streamlit as st
import pandas as pd
import numpy as np

# ページ設定
st.set_page_config(page_title="体調と助言", page_icon="⚡")

# ▼▼▼ デザイン・級数 厳格統一ルール（CSS） ▼▼▼
st.markdown("""
    <style>
        /* 0. 日本語フォント指定 */
        html, body, [class*="css"] {
            font-family: "Hiragino Sans", "Meiryo", "Yu Gothic", sans-serif;
        }

        /* 1. スマホ用上部余白 */
        .block-container {
            padding-top: 3rem;
        }

        /* === 統一ルール：項目ラベル（中） === */
        /* 「心拍数」「状態」のラベルを強制上書き */
        [data-testid="stMetricLabel"] {
            font-size: 16px !important;      /* 級数：16pxに固定 */
            color: #666666 !important;       /* 色：濃いグレーに固定 */
            font-weight: 600 !important;     /* 太さ：太字に固定 */
        }
        
        /* 「バイタル」など、手動で作るラベル用のクラス定義 */
        .custom-label {
            font-size: 16px !important;      /* MetricLabelと完全に同じ設定 */
            color: #666666 !important;
            font-weight: 600 !important;
            margin-bottom: 0px !important;
        }

        /* === 統一ルール：データ値（大） === */
        /* 「65」「通常」の文字を強制上書き */
        [data-testid="stMetricValue"] div {
            font-size: 32px !important;      /* 級数：32pxに固定 */
            color: #333333 !important;       /* 色：黒に固定 */
            font-weight: 700 !important;
        }

    </style>
""", unsafe_allow_html=True)
# ▲▲▲ 設定ここまで ▲▲▲

# タイトル（特大）
st.title("⚡ 体調と助言")

# サイドバー
st.sidebar.header("データ入力")
bpm = st.sidebar.slider("現在の心拍数 (BPM)", min_value=40, max_value=180, value=65)
mood = st.sidebar.select_slider("メンタルコンディション", options=["絶不調", "低調", "通常", "好調", "絶好調"], value="通常")

st.divider()

# メイン画面：指標表示
col1, col2 = st.columns(2)

with col1:
    # ラベル「心拍数」 -> CSSで16pxグレーになります
    # 値「65」 -> CSSで32px黒になります
    st.metric(label="心拍数 (BPM)", value=bpm, delta=bpm - 65)

with col2:
    # ラベル「状態」 -> CSSで16pxグレーになります
    # 値「通常」 -> CSSで32px黒になります
    st.metric(label="状態", value=mood)

# 状況判定
if bpm > 100:
    st.error("警告：心拍数上昇")
    action = "深呼吸・休憩・水分補給をして下さい。"
elif bpm < 50:
    st.warning("注意：覚醒レベル低下")
    action = "ストレッチや散歩をお勧めします。"
else:
    st.success("状態：安定")
    action = "安定、この状態を続けてください。"

st.info(f"**助言：** {action}")

# グラフセクション
# 【修正】st.subheaderを使わず、metricラベルと同じ見た目のHTMLを使用
st.markdown('<p class="custom-label">バイタル</p>', unsafe_allow_html=True)

chart_data = pd.DataFrame(
    np.random.randn(20, 1) * 10 + bpm,
    columns=['BPM'])
st.line_chart(chart_data)

