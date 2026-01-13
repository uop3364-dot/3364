import streamlit as st
import pandas as pd
from streamlit_google_auth import Authenticate

# --- 1. 頁面基本設定 ---
st.set_page_config(page_title="莫連投資代理人 v2.9", layout="wide")

# --- 2. 安全保險箱 (加密讀取) ---
# 注意：在本地 PyCharm 執行時，需要在 .streamlit/secrets.toml 設定這些值
# 在雲端時，則直接讀取 Streamlit Cloud 的 Secrets
try:
    client_id = st.secrets["GOOGLE_CLIENT_ID"]
    client_secret = st.secrets["GOOGLE_CLIENT_SECRET"]
except:
    st.warning("⚠️ 偵測到安全憑證尚未設定。請在 Secrets 中配置 Google OAuth 資訊。")
    client_id = "temp_id"
    client_secret = "temp_secret"

# 初始化 Google 驗證器
auth = Authenticate(
    secret_id=client_id,
    secret_key=client_secret,
    cookie_name="mo_lien_auth",
    key="mo_lien_crypto_key",
    cookie_duration_days=30
)

# --- 3. Google OAuth 登入邏輯 ---
auth.check_authenticity()

if not st.session_state.get('connected'):
    st.title("🔒 莫連投資中心")
    st.subheader("全職交易員安全驗證")
    st.info("請使用您的 Gmail 帳號登入系統，系統將自動跳轉至 Google 驗證頁面。")
    auth.login() # 這裡會自動產生 Google 登入按鈕並處理跳轉
    st.stop()

# --- 4. 登入成功後的內容 ---
# 只有登入成功才會執行到這裡
user_info = st.session_state.get('user_info', {})
st.sidebar.success(f"✅ 已登入：{user_info.get('email')}")

if st.sidebar.button("🚪 安全登出"):
    auth.logout()

# --- 5. 修復後的對話框功能 (LINE 風格) ---
st.title("🤖 莫連投資代理人 v2.9")
st.caption("Google 安全認證連線中 | 永豐大戶投審核中")

# 初始化對話紀錄 (確保重新整理不會消失)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 建立滾動對話區域
chat_container = st.container()

with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# --- 6. 永豐大戶投 - 存錢筒區 ---
with st.sidebar.expander("🏦 永豐大戶投：活存監控", expanded=True):
    st.write("目前活存利率：**1.5%**")
    balance = st.number_input("輸入目前的活存餘額", value=100000)
    daily_earn = (balance * 0.015) / 365
    st.metric("每日預計利息 (TWD)", f"{daily_earn:.2f}")

# --- 7. 對話輸入框 (修復點：必須放在最後以確保不被中斷) ---
if prompt := st.chat_input("莫連，想聊聊哪支股票？或是分析活存配置？"):
    # 立即顯示使用者訊息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with chat_container:
        with st.chat_message("user"):
            st.markdown(prompt)

    # 模擬 FinGPT 回應 (莫連，這裡之後會串接你的 fin_gpt_test.py 邏輯)
    with chat_container:
        with st.chat_message("assistant"):
            response = f"【FinGPT 診斷】莫連，針對您的提問「{prompt}」，我正在調閱 Google 開發計畫中的大數據進行分析..."
            st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})