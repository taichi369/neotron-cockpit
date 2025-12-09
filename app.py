import streamlit as st
import os
import sys
import subprocess

# ▼▼▼ 強制アップデート（禁じ手） ▼▼▼
# サーバーが古い部品を使おうとするのを、力技でねじ伏せて最新版にします
try:
    import google.generativeai as genai
    # バージョンが古ければ強制インストール
    if genai.__version__ < "0.8.3":
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-U", "google-generativeai"])
        st.toast("システム更新完了。リロードしてください。", icon="🔄")
except:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-U", "google-generativeai"])
    import google.generativeai as genai
# ▲▲▲ ここまで ▲▲▲

import pandas as pd
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

# AI初期化
connect_log = "初期化中..."
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # 最新版が入ったので、堂々と最新モデルを使います
        model = genai.GenerativeModel('gemini-1.5-flash')
        ai_available = True
        connect_log = "接続成功: gemini-1.5-flash"
    else:
        ai_available = False
        connect_log = "APIキーなし"
except Exception as e:
    ai_available = False
    connect_log = f"エラー: {e}"

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
st.caption(f"System: {connect_log} (v{genai.__version__})")
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
        st.session_state.ai_comment = f"システム停止中: {connect_log}"
    
    st.rerun()

# グラフ
st.markdown('<p class="custom-label">バイタル推移 (ログ)</p>', unsafe_allow_html=True)
if not st.session_state.history.empty:
    st.line_chart(st.session_state.history[['心拍数']])
