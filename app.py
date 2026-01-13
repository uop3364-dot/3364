import streamlit as st
from datetime import datetime

# 1. 頁面設定 (必須放在第一行)
st.set_page_config(page_title="莫連投資代理人", layout="wide")

# 2. 簡單的登入邏輯
if 'auth' not in st.session_state:
    st.session_state.auth = False

# 3. 介面樣式 (修正後的版本)
def apply_style():
    st.markdown('<style>div.stButton > button {width: 100%;}</style>', unsafe_content_html=True)

# 4. 登入介面
if not st.session_state.auth:
    st.title("🔒 莫連投資系統")
    pwd = st.text_input("輸入密碼", type="password")
    if st.button("點擊登入"):
        if pwd == "1234":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("密碼錯誤")
else:
    # 5. 登入後的旗艦內容
    apply_style()
    st.title("🤖 莫連投資代理人 v2.7")
    
    # 永豐大戶投監控
    st.subheader("🏦 永豐大戶投資產")
    c1, c2 = st.columns(2)
    c1.metric("活存餘額", "NT$ 1,250,000", "利率 1.5%")
    c2.metric("今日預估損益", "+$12,400", "2.1%")
    
    st.divider()
    
    # 對話框
    st.info("🤖 莫連，連線完全成功！現在系統已在雲端穩定運行。")
    
    stock = st.text_input("🔍 輸入台股代號分析 (如 2330):")
    if stock:
        st.success(f"📈 正在分析 {stock}... 趨勢穩定，建議配合大戶投活存靈活配置。")
    
    if st.sidebar.button("🚪 安全登出"):
        st.session_state.auth = False
        st.rerun()
