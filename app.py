import streamlit as st

# 1. 基礎設定
st.set_page_config(page_title="莫連投資代理人", layout="centered")

# 2. 密碼驗證邏輯
if 'auth' not in st.session_state:
    st.session_state.auth = False

# 3. 介面邏輯
if not st.session_state.auth:
    st.header("🔒 莫連投資系統")
    # 簡單的登入表單
    pwd = st.text_input("請輸入密碼", type="password")
    if st.button("點擊登入"):
        if pwd == "1234":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("密碼錯誤")
else:
    # 登入成功後的畫面
    st.success("✅ 雲端連線成功！歡迎莫連老師")
    
    # 永豐大戶投監控區
    st.subheader("🏦 永豐大戶投 - 活存狀態")
    st.metric(label="活存利率", value="1.5%", delta="優於一般活存")
    st.write("目前資金已就緒，隨時可進行選股配置。")
    
    st.divider()
    
    # 功能測試區
    st.subheader("🤖 AI 選股助理")
    stock_id = st.text_input("輸入台股代號 (例如: 2330)")
    if stock_id:
        st.info(f"正在為莫連老師分析 {stock_id} ...")
        st.write("📊 目前趨勢：強勢整理中")
    
    # 側邊欄登出
    if st.sidebar.button("安全登出"):
        st.session_state.auth = False
        st.rerun()
