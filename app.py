import streamlit as st
import pandas as pd
import numpy as np

# ページ設定
st.set_page_config(page_title="体調と助言", page_icon="⚡")

# ▼▼▼ デザイン・級数統一ルール（CSS） ▼▼▼
st.markdown("""
    <style>
        /* 1. フォントの統一（日本語・数字を同じ書体で表示） */
        html, body, [class*="css"] {
            font-family: "Hiragino Sans", "Meiryo", "Yu Gothic", sans-serif;
        }

        /* 2. 上部余白（スマホ対策） */
        .block-container {
            padding-top: 3rem;
        }

        /* 3. 【見出し】の級数統一 */
        /* 「心拍数」「状態」のラベル(st.metric) と 「バイタル」の見出し(h3) を同じにする */
        [data-testid="stMetricLabel"], [data-testid="stMarkdownContainer"] h3 {
            font-size: 18px !important;     /* 見出しは18pxに統一 */
            color: #555555 !important;      /* 色もグレーに統一 */
            font-weight: 600 !important;    /* 太さも統一 */
            margin-bottom: 0px !important;  /* 下の余白を詰める */
        }

        /* 4. 【値】の級数統一 */
        /* 数字(65) も 日本語(通常) も同じ大きさに強制固定 */
        [data-testid="stMetricValue"] div {
            font-size: 36px !important;     /* 値は36pxに統一 */
            font-weight: 700 !important;
            line-height: 1.2 !important;    /* 行間を整える */
        }
        
        /* 助言ボックスの文字サイズ調整 */
        .stAlert {
            font-size: 16px !important;
        }
        
    </style>
""", unsafe_allow_html=True)
# ▲▲▲ 設定ここまで ▲▲▲

# タイトル（ここはアプリ名なので最大のまま）
st.title("⚡ 体調と助言")

# サイドバー
st.sidebar.header("データ入力")
bpm = st.sidebar.slider("現在の心拍数 (BPM)", min_value=40, max_value=180, value=65)
mood = st.sidebar.select_slider("メンタルコンディション", options=["絶不調", "低調", "通常", "好調", "絶好調"], value="通常")

st.divider()

# メイン画面：指標表示
col1, col2 = st.columns(2)

with col1:
    # ラベル「心拍数」 → CSSで18pxになります
    # 値「65」 → CSSで36pxになります
    st.metric(label="心拍数 (BPM)", value=bpm, delta=bpm - 65)

with col2:
    # ラベル「状態」 → CSSで18pxになります
    # 値「通常」 → CSSで36pxになります
    st.metric(label="状態", value=mood)

# 状況判定と助言
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

st.divider()

# グラフセクション
# ここでsubheaderを使いますが、CSSでmetricラベルと同じ見た目(18px)に変えています
st.subheader("バイタル")

chart_data = pd.DataFrame(
    np.random.randn(20, 1) * 10 + bpm,
    columns=['BPM'])
st.line_chart(chart_data)
