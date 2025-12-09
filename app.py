import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

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
        [data-testid="stMetricLabel"] {
            font-size: 16px !important;
            color: #666666 !important;
            font-weight: 600 !important;
        }
        
        .custom-label {
            font-size: 16px !important;
            color: #666666 !important;
            font-weight: 600 !important;
            margin-bottom: 5px !important;
        }

        /* === 統一ルール：データ値（大） === */
        [data-testid="stMetricValue"] div {
            font-size: 32px !important;
            color: #333333 !important;
            font-weight: 700 !important;
        }
        
        /* ボタンのデザイン強化 */
        div.stButton > button {
            width: 100%;
            font-weight: bold;
            border: 2px solid #444;
        }

    </style>
""", unsafe_allow_html=True)
# ▲▲▲ 設定ここまで ▲▲▲

# --- データ保存機能の初期化 ---
if 'history' not in st.session_state:
    # まだデータがない場合、空の箱を用意する
    st.session_state.history = pd.DataFrame(columns=['時刻', '心拍数', '状態'])

# タイトル
st.title("⚡ 体調と助言")

# サイドバー
st.sidebar.header("データ入力")
bpm = st.sidebar.slider("現在の心拍数 (BPM)", min_value=40, max_value=180, value=65)
mood_val = st.sidebar.select_slider("メンタルコンディション", options=["絶不調", "低調", "通常", "好調", "絶好調"], value="通常")

# 状況判定ロジック
if bpm > 100:
    status_color = "error"
    action = "深呼吸・休憩・水分補給をして下さい。"
elif bpm < 50:
    status_color = "warning"
    action = "ストレッチや散歩をお勧めします。"
else:
    status_color = "success"
    action = "安定、この状態を続けてください。"

# メイン画面：指標表示
col1, col2 = st.columns(2)

with col1:
    st.metric(label="心拍数 (BPM)", value=bpm, delta=None)

with col2:
    st.metric(label="状態", value=mood_val)

# 助言表示
if status_color == "error":
    st.error(f"**助言：** {action}")
elif status_color == "warning":
    st.warning(f"**助言：** {action}")
else:
    st.success(f"**助言：** {action}")

# --- 記録ボタンセクション ---
if st.button("状況を記録する"):
    # 現在時刻を取得 (日本時間)
    jp_time = datetime.now(pytz.timezone('Asia/Tokyo')).strftime('%H:%M:%S')
    
    # 新しいデータをデータフレームに追加
    new_data = pd.DataFrame({
        '時刻': [jp_time],
        '心拍数': [bpm],
        '状態': [mood_val]
    })
    
    # 履歴に追加結合
    st.session_state.history = pd.concat([st.session_state.history, new_data], ignore_index=True)
    st.toast('記録完了！', icon='✅') # スマホ画面下に通知を出す

st.divider()

# --- グラフセクション（実データ） ---
st.markdown('<p class="custom-label">バイタル推移 (ログ)</p>', unsafe_allow_html=True)

if not st.session_state.history.empty:
    # データがある場合のみグラフを表示
    chart_data = st.session_state.history[['心拍数']].copy()
    st.line_chart(chart_data)
    
    # 最新の履歴を表で表示
    st.markdown('<p class="custom-label">記録履歴</p>', unsafe_allow_html=True)
    st.dataframe(st.session_state.history.tail(5), use_container_width=True)
else:
    # データがない時のメッセージ
    st.info("「状況を記録する」ボタンを押すと、ここにグラフが生成されます。")
