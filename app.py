"""
Streamlit Cloud 部署版 v2.5 - 莫連投資代理人
最終部署版本，支援 iPhone 12 完美體驗
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json
import sys
import os
import io
from typing import Dict, List, Optional

# 解決 Windows 編碼問題
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# 設定頁面配置 - iPhone 12 優化
st.set_page_config(
    page_title="莫連投資代理人 v2.5",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 🔒 嚴格登入驗證
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Streamlit Cloud 版標籤
st.title("Streamlit Cloud v2.5 - 莫連投資代理人")

# 登入驗證函數
def authenticate_user(password: str) -> bool:
    """驗證用戶密碼"""
    if password == "1234":
        st.session_state.authenticated = True
        st.session_state.login_time = datetime.now()
        return True
    else:
        return False

def show_login_interface():
    """顯示登入介面"""
    st.title("🔒 MO-LIEN SYSTEM LOGIN")
    
    password = st.text_input("請輸入密碼", type="password", key="login_input")
    
    if st.button("🚀 點擊登入"):
        if authenticate_user(password):
            st.success("✅ 登入成功！歡迎使用 Streamlit Cloud 版")
            st.rerun()
        else:
            st.error("❌ 密碼錯誤")

def show_chat_interface():
    """顯示對話介面"""
    
    # 僅在登入後導入模組
    try:
        from config import CONFIG
        from market_data import market_fetcher
        from analysis_engine import ta_engine
        from trade_logger import trade_logger
        from notify_manager import notify_manager
        from main import FullTimeTrader
    except ImportError as e:
        st.error(f"模組導入失敗: {e}")
        st.session_state.authenticated = False
        st.rerun()
    
    st.title("🤖 莫連投資代理人 v2.5 - Streamlit Cloud 版")
    
    # 初始化 session state
    if 'trader' not in st.session_state:
        st.session_state.trader = FullTimeTrader()
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'selected_stock' not in st.session_state:
        st.session_state.selected_stock = "0050.TW"
    
    # 歡迎訊息
    if not st.session_state.chat_history:
        st.info("🤖 您好！我是莫連投資代理人 v2.5 Streamlit Cloud 版，您的專屬投資助手。請輸入股票代號開始分析！")
    
    # 顯示對話歷史
    for message in st.session_state.chat_history:
        if message['role'] == 'user':
            st.markdown(f"👤 **您**: {message['content']}")
        else:
            st.markdown(f"🤖 **助手**: {message['content']}")
    
    # 輸入區域
    st.markdown("---")
    user_input = st.text_input("請輸入股票代號或問題...", key="chat_input")
    
    if st.button("📤 發送", use_container_width=True) or (user_input and st.session_state.get('last_input') != user_input):
        st.session_state.last_input = user_input
        
        # 添加用戶訊息
        st.session_state.chat_history.append({
            'role': 'user',
            'content': user_input,
            'timestamp': datetime.now()
        })
        
        # 處理回應
        if user_input.replace('.TW', '').replace('.tw', '').isdigit() and len(user_input) >= 4:
            # 股票分析
            symbol = user_input.upper()
            if not symbol.endswith('.TW'):
                symbol += '.TW'
            
            with st.spinner(f"📊 分析 {symbol} 中..."):
                try:
                    price = market_fetcher.get_real_time_price(symbol)
                    if price:
                        hist_data = market_fetcher.get_historical_data(symbol, "3m")
                        if not hist_data.empty:
                            data_with_indicators = ta_engine.calculate_all_indicators(hist_data)
                            signals = ta_engine.get_latest_signals(data_with_indicators)
                            
                            response = f"📊 **{symbol} 技術分析**\n💰 當前價格: NT${price:.2f}\n\n📈 **技術指標:**\n"
                            
                            if 'kd' in signals:
                                kd = signals['kd']
                                response += f"• KD: K={kd.get('k', 0):.1f}, D={kd.get('d', 0):.1f} ({kd.get('signal', 'N/A')})\n"
                            
                            if 'macd' in signals:
                                macd = signals['macd']
                                response += f"• MACD: {macd.get('trend', 'N/A')}\n"
                            
                            if 'rsi' in signals:
                                rsi = signals['rsi']
                                response += f"• RSI: {rsi.get('value', 0):.1f} ({rsi.get('signal', 'N/A')})\n"
                            
                            # 投資建議
                            score = 0
                            if 'kd' in signals and signals['kd'].get('golden_cross'):
                                score += 3
                            if 'macd' in signals and signals['macd'].get('bullish_cross'):
                                score += 3
                            if 'rsi' in signals and signals['rsi'].get('oversold'):
                                score += 2
                            
                            if score >= 4:
                                response += f"\n🎯 **建議: 買入** (信心度: {min(score/10, 0.9):.1%})"
                            elif score <= -2:
                                response += f"\n⚠️ **建議: 賣出**"
                            else:
                                response += f"\n📋 **建議: 觀望**"
                        else:
                            response = f"❌ 無法獲取 {symbol} 的歷史數據"
                    else:
                        response = f"❌ 無法獲取 {symbol} 的當前價格"
                except Exception as e:
                    response = f"❌ 分析 {symbol} 時發生錯誤: {e}"
        else:
            # 一般回應
            response = f"🤖 **莫連投資代理人 v2.5 Streamlit Cloud 版**\n\n我可以為您：\n• 分析股票技術指標\n• 提供投資建議\n• 執行交易操作\n\n請輸入股票代號開始分析！\n\n🌐 **Streamlit Cloud 部署優勢：**\n• 100% 穩定 HTTPS\n• iPhone 12 完美適配\n• 無需隧道配置\n• 全球可訪問"
        
        # 添加機器人回應
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': response,
            'timestamp': datetime.now()
        })
        
        st.rerun()
    
    # 登出按鈕
    if st.button("🚪 安全登出", key="logout_button"):
        st.session_state.authenticated = False
        st.rerun()

# 主程式邏輯
def main():
    """主程式入口"""
    if not st.session_state.authenticated:
        show_login_interface()
    else:
        show_chat_interface()

if __name__ == "__main__":
    main()
