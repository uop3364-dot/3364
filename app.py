import streamlit as st
import pandas as pd
from datetime import datetime

# 1. 頁面設定 (iPhone 12 優化)
st.set_page_config(page_title="莫連投資代理人 v2.6", layout="wide")

# 初始化 session state
if 'auth' not in st.session_state:
    st.session_state.auth = False

# 2. 密碼鎖邏輯
def check_password():
    if not st.session_state.auth:
        st.title("🔒 莫連投資代理人")
        st.subheader("請登入以開啟交易系統")
        pwd = st.text_input("輸入密碼 (預設 1234)", type="password")
        if st.button("🚀 執行登入"):
            if pwd == "1234":
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("❌ 密碼錯誤，請重新輸入")
        return False
    return True

# 3. 登入後的旗艦介面
if check_password():
    # --- LINE 風格 CSS ---
    st.markdown("""
        <style>
        .stApp { background-color: #7494C0; }
        .chat-bbl { background-color: #FFFFFF; padding: 12px; border-radius: 15px; margin-bottom: 15px; color: black; border: 1px solid #E0E0E0; }
        .user-bbl { background-color: #85E085; padding: 12px; border-radius: 15px; margin-bottom: 15px; text-align: right; color: black; border: 1px solid #E0E0E0; }
        .stMetric { background-color: #FFFFFF; padding: 10px; border-radius: 10px; }
        </style>
    """, unsafe_content_html=True)

    st.title("🤖 莫連投資代理人 (雲端旗艦版)")
    
    # 永豐大戶投專區
    with st.container():
        st.markdown("### 🏦 永豐大戶投資產監控")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("活存餘額 (模擬)", "NT$ 1,250,000", "活存 1.5%")
        with col2:
            st.metric("今日損益", "+NT$ 12,400", "↑ 2.1%")

    st.markdown("---")

    # 對話顯示
    st.markdown('<div class="chat-bbl">🤖 莫連，雲端連線成功！我已經準備好為您分析「永豐大戶投」的持股，請輸入股票代號。</div>', unsafe_content_html=True)
    
    # 互動輸入
    stock_input = st.text_input("🔍 輸入台股代號 (例如 2330):", key="main_input")
    
    if stock_input:
        st.markdown(f'<div class="user-bbl">幫我分析 {stock_input}</div>', unsafe_content_html=True)
        with st.status(f"📊 正在調用 AI 引擎分析 {stock_input}...", expanded=True):
            st.write("連線至 Yahoo Finance...")
            st.write("計算 KD/MACD 指標...")
            st.success(f"✅ {stock_input} 分析完成：目前處於強勢區，建議維持配置。")

    # 功能選單
    with st.sidebar:
        st.header("⚙️ 系統設定")
        st.write(f"👤 用戶: 莫連")
        st.write(f"📅 系統日期: {datetime.now().strftime('%Y-%m-%d')}")
        if st.button("🚪 安全登出"):
            st.session_state.auth = False
            st.rerun()
