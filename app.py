import streamlit as st
import json
import time
import os

# --- 設定 ---
st.set_page_config(
    page_title="NeoTRON_01 Cockpit",
    page_icon="⚡",
    layout="wide"
)

STATUS_FILE = "system_status.json"

# --- 関数: 記憶を読み取る ---
def load_status():
    if not os.path.exists(STATUS_FILE):
        return None, 0, 0
    try:
        with open(STATUS_FILE, "r", encoding='utf-8') as f:
            data = json.load(f)
            return data.get("mode", "NORMAL"), data.get("heart_rate", 0), data.get("updated", 0)
    except:
        return None, 0, 0

# --- メイン画面構築 ---
st.title("⚡ NeoTRON_01: Tactical Cockpit")

# プレースホルダー（中身が入れ替わる箱）を作る
status_container = st.empty()

# --- リアルタイム表示ループ ---
# Streamlitは通常、上から下へ一度だけ実行されるが、
# ここでは簡易的に「再実行ボタン」または自動リロードのような挙動を擬似的に作る
# ※本来は while True は非推奨だが、ローカル動作確認のためシンプルに実装します

# 最新データを取得
mode, hr, updated = load_status()

with status_container.container():
    # 1. ヘッダー情報
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Heart Rate (BPM)", value=hr, delta=None)
    with col2:
        st.caption(f"Last Update: {time.ctime(updated)}")

    st.divider()

    # 2. モード別表示
    if mode == "COMBAT":
        # 緊急モード（赤）
        st.error("🔥 COMBAT MODE (戦闘態勢)")
        st.markdown("""
        ### ⚠️ 警告：心拍数上昇
        * **判断:** 直感優先。論理は後回し。
        * **行動:** 即断即決。結論から話せ。
        """)
    elif mode == "NORMAL":
        # 通常モード（緑）
        st.success("🍀 NORMAL MODE (平時)")
        st.markdown("""
        ### ✅ 状態：安定
        * **判断:** 論理的思考が可能。
        * **行動:** 3S（整理・整頓・清掃）を実行せよ。
        """)
    else:
        # データなし（グレー）
        st.warning("📡 WAITING FOR SIGNAL... (信号待機中)")

    st.divider()
    
    # 自動更新のためのボタン（押すと最新になる）
    if st.button('🔄 画面更新 (Refresh)'):
        st.rerun()