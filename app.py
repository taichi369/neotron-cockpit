import streamlit as st
import pandas as pd
import google.generativeai as genai
from datetime import datetime
import pytz

# ページ設定
st.set_page_config(page_title="体調と助言", page_icon="⚡")

# CSS設定
st.markdown("""
    <style>
        html, body, [class*="css"] { font-family: "Hiragino Sans", "Meiryo", sans-serif; }
        .block-container { padding-top: 3rem; }
        [data-testid="stMetricLabel"] { font-size: 16px !important; color: #666666 !important; font-weight: 600 !important; }
        [data-testid="stMetricValue"] div { font-size: 32px !important; color: #333333 !important; font-weight: 700 !important; }
        .custom-label { font-size: 16px !important; color: #666666 !important; font-weight: 600 !important; margin-bottom: 5px !important; }
        .ai-box { padding: 15px; background-color: #f0f2f6; border-radius: 10px; border-left: 5px solid #ff4b4b; }
    </style>
""", unsafe_allow_html=True)

# AI初期化 (Gemini Pro - 安定版)
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-pro')
        ai_available = True
    else:
        ai_available = False
except:
    ai_available = False

# データ初期化
if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=['時刻', '心拍数', '状態'])
if 'ai_comment' not in st.session_state:
    st.session_state.ai_comment = "システムスタンバイ... データを受信待機中。"

st.title("⚡ 体調と助言")

# 入力エリア
st.sidebar.header("データ入力")
bpm = st.sidebar.slider("現在の心拍数 (BPM)", 40, 180, 65)
mood_val = st.sidebar.select_slider("メンタルコンディション", ["絶不調", "低調", "通常", "好調", "絶好調"], value="通常")

col1, col2 = st.columns(2)
with col1: st.metric("心拍数 (BPM)", bpm, bpm - 65)
with col2: st.metric("状態", mood_val)

# AIエリア
st.markdown('<p class="custom-label">AI参謀の助言</p>', unsafe_allow_html=True)
st.info(f"🤖 **司令部より:**\n\n{st.session_state.ai_comment}")

# ボタン処理
if st.button("状況を報告する (AI分析開始)"):
    jp_time = datetime.now(pytz.timezone('Asia/Tokyo')).strftime('%H:%M:%S')
    new_row = pd.DataFrame({'時刻': [jp_time], '心拍数': [bpm], '状態': [mood_val]})
    st.session_state.history = pd.concat([st.session_state.history, new_row], ignore_index=True)

    if ai_available:
        prompt = f"あなたは戦術オペレーター。ユーザーの状態（心拍数:{bpm}, 気分:{mood_val}）に対し、軍隊調で簡潔に的確なアドバイスをせよ。"
        try:
            with st.spinner('通信中...'):
                response = model.generate_content(prompt)
                st.session_state.ai_comment = response.text
        except Exception as e:
            st.session_state.ai_comment = f"通信エラー: {e}"
    else:
        st.session_state.ai_comment = "APIキー未設定"
    
    st.rerun()

# グラフ
st.markdown('<p class="custom-label">バイタル推移 (ログ)</p>', unsafe_allow_html=True)
if not st.session_state.history.empty:
    st.line_chart(st.session_state.history[['心拍数']])
