import streamlit as st
import pandas as pd
import google.generativeai as genai
from datetime import datetime
import pytz

# ページ設定
st.set_page_config(page_title="体調と助言", page_icon="⚡")

# --- デザイン設定 (CSS) ---
st.markdown("""
    <style>
        html, body, [class*="css"] {
            font-family: "Hiragino Sans", "Meiryo", "Yu Gothic", sans-serif;
        }
        .block-container {
            padding-top: 3rem;
        }
        /* 項目ラベル */
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
        /* データ値 */
        [data-testid="stMetricValue"] div {
            font-size: 32px !important;
            color: #333333 !important;
            font-weight: 700 !important;
        }
        /* AIアドバイスボックス */
        .ai-box {
            padding: 15px;
            background-color: #f0f2f6;
            border-radius: 10px;
            border-left: 5px solid #ff4b4b;
            margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# --- AI (Gemini) の初期化 ---
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
        ai_available = True
    else:
        ai_available = False
except Exception as e:
    ai_available = False

# --- データ保存機能の初期化 ---
if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=['時刻', '心拍数', '状態'])
if 'ai_comment' not in st.session_state:
    st.session_state.ai_comment = "システムスタンバイ... データを受信待機中。"

# タイトル
st.title("⚡ 体調と助言")

# サイドバー
st.sidebar.header("データ入力")
bpm = st.sidebar.slider("現在の心拍数 (BPM)", min_value=40, max_value=180, value=65)
mood_val = st.sidebar.select_slider("メンタルコンディション", options=["絶不調", "低調", "通常", "好調", "絶好調"], value="通常")

# メイン画面：指標表示
col1, col2 = st.columns(2)
with col1:
    st.metric(label="心拍数 (BPM)", value=bpm, delta=bpm - 65)
with col2:
    st.metric(label="状態", value=mood_val)

# --- AI参謀のアドバイスエリア ---
st.markdown('<p class="custom-label">AI参謀の助言</p>', unsafe_allow_html=True)

# ここにAIの言葉が表示される
st.info(f"🤖 **司令部より:**\n\n{st.session_state.ai_comment}")

# --- アクションボタン ---
if st.button("状況を報告する (AI分析開始)"):
    # 1. データの記録
    jp_time = datetime.now(pytz.timezone('Asia/Tokyo')).strftime('%H:%M:%S')
    new_data = pd.DataFrame({'時刻': [jp_time], '心拍数': [bpm], '状態': [mood_val]})
    st.session_state.history = pd.concat([st.session_state.history, new_data], ignore_index=True)

    # 2. AIへの指令 (プロンプト)
    if ai_available:
        prompt = f"""
        あなたはSF映画に出てくるような優秀な戦術オペレーターです。
        パイロット（ユーザー）の現在の状態は以下の通りです。

        - 心拍数: {bpm} BPM
        - 気分: {mood_val}

        この状態に基づき、パイロットに対して「簡潔で」「軍事的で」「的確な」アドバイスを1つだけしてください。
        敬語は不要。「〜せよ」「〜だ」という口調で、司令官のように振る舞ってください。
        """

        with st.spinner('司令部と通信中...'):
            try:
                response = model.generate_content(prompt)
                st.session_state.ai_comment = response.text
            except Exception as e:
                st.session_state.ai_comment = "通信エラー。手動で対処せよ。"
    else:
        st.session_state.ai_comment = "APIキー未設定。AIシステム稼働不可。"

    st.rerun() # 画面を更新して結果を表示

# --- グラフセクション ---
st.markdown('<p class="custom-label">バイタル推移 (ログ)</p>', unsafe_allow_html=True)

if not st.session_state.history.empty:
    chart_data = st.session_state.history[['心拍数']].copy()
    st.line_chart(chart_data)
