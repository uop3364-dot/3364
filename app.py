"""
莫連投資代理人主程式 - 整合大戶投資審核系統
Google 開發計畫整合 v2.8
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json
import sys
import os
import io
import requests
from typing import Dict, List, Optional
import sqlite3

# 🔒 密碼保護機制 (必須放在程式最開頭)
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

def login_screen():
    st.title("🔒 MO-LIEN SYSTEM LOGIN")
    password = st.text_input("請輸入密碼", type="password")
    if st.button("🚀 登入"):
        if password == "1234":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("❌ 密碼錯誤")

if not st.session_state.authenticated:
    login_screen()
    st.stop()  # 密碼沒過，後面的功能通通不准跑

# 解決 Windows 編碼問題
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# 設定頁面配置
st.set_page_config(
    page_title="莫連投資代理人",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 整合深色主題 CSS
st.markdown("""
<style>
/* 整合深色主題 */
.stApp {
    background-color: #0a0a0a;
    color: #ffffff;
}

/* 頂部導航欄 */
[data-testid="stHeader"] {
    background-color: #1a1a1a !important;
    color: #ff6b35 !important;
    border-bottom: 2px solid #ff6b35 !important;
}

/* 側邊欄 */
[data-testid="stSidebar"] {
    background-color: #1a1a1a !important;
    color: #ffffff !important;
    border-right: 2px solid #ff6b35 !important;
}

/* 主內容區 */
[data-testid="stMainBlockContainer"] {
    background-color: #0a0a0a !important;
}

/* 按鈕樣式 */
.stButton > button {
    background: linear-gradient(135deg, #ff6b35 0%, #e55100 100%) !important;
    color: #ffffff !important;
    border: 2px solid #ff6b35 !important;
    border-radius: 8px !important;
    padding: 12px 24px !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    box-shadow: 0 0 20px rgba(255, 107, 53, 0.4) !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #e55100 0%, #cc4000 100%) !important;
    box-shadow: 0 0 30px rgba(255, 107, 53, 0.6) !important;
    transform: translateY(-2px);
}

/* 輸入框樣式 */
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
    background-color: #1a1a1a !important;
    color: #ffffff !important;
    border: 2px solid #ff6b35 !important;
    border-radius: 8px !important;
    box-shadow: 0 0 10px rgba(255, 107, 53, 0.3) !important;
}

/* 功能卡片 */
.feature-card {
    background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
    border: 2px solid #ff6b35;
    color: #ff6b35;
    padding: 25px;
    border-radius: 15px;
    margin: 15px 0;
    box-shadow: 0 0 30px rgba(255, 107, 53, 0.4);
    text-align: center;
}

/* 審核卡片 */
.audit-card {
    background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
    border: 2px solid #ff6b35;
    color: #ff6b35;
    padding: 25px;
    border-radius: 15px;
    margin: 15px 0;
    box-shadow: 0 0 30px rgba(255, 107, 53, 0.4);
    text-align: center;
}

/* 風險指標 */
.risk-high {
    color: #ff4444;
    font-weight: bold;
    text-shadow: 0 0 10px rgba(255, 68, 68, 0.8);
}

.risk-medium {
    color: #ffaa00;
    font-weight: bold;
    text-shadow: 0 0 10px rgba(255, 170, 0, 0.8);
}

.risk-low {
    color: #00ff00;
    font-weight: bold;
    text-shadow: 0 0 10px rgba(0, 255, 0, 0.8);
}

/* 合規狀態 */
.compliance-status {
    background: linear-gradient(135deg, #ff6b35 0%, #e55100 100%);
    color: #ffffff;
    padding: 15px 25px;
    border-radius: 10px;
    margin: 10px 0;
    font-weight: 600;
    text-align: center;
}

/* 審核報告 */
.audit-report {
    background: #1a1a1a;
    border: 2px solid #ff6b35;
    padding: 30px;
    border-radius: 15px;
    margin: 20px 0;
    font-family: 'Courier New', monospace;
    color: #ffffff;
}
</style>
""", unsafe_allow_html=True)

# ==================== 審核系統核心函數 ====================

def init_audit_database():
    """初始化審核數據庫"""
    try:
        conn = sqlite3.connect('investment_audit.db')
        cursor = conn.cursor()
        
        # 創建審核記錄表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS audit_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                investor_id TEXT,
                audit_type TEXT,
                risk_level TEXT,
                portfolio_value REAL,
                compliance_score INTEGER,
                findings TEXT,
                recommendations TEXT,
                auditor TEXT
            )
        ''')
        
        # 創建投資者表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS investors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                investor_id TEXT UNIQUE,
                name TEXT,
                registration_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                risk_profile TEXT,
                max_investment REAL,
                status TEXT DEFAULT 'active'
            )
        ''')
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"數據庫初始化失敗: {e}")
        return False

def create_audit_record(investor_id: str, audit_type: str, risk_level: str, 
                     portfolio_value: float, compliance_score: int, 
                     findings: str, recommendations: str, auditor: str):
    """創建審核記錄"""
    try:
        conn = sqlite3.connect('investment_audit.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO audit_records 
            (investor_id, audit_type, risk_level, portfolio_value, compliance_score, findings, recommendations, auditor)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (investor_id, audit_type, risk_level, portfolio_value, compliance_score, findings, recommendations, auditor))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"創建審核記錄失敗: {e}")
        return False

def calculate_risk_metrics(portfolio_data: pd.DataFrame) -> Dict:
    """計算風險指標"""
    try:
        if portfolio_data.empty:
            return {"risk_score": 0, "risk_level": "低", "volatility": 0}
        
        # 計算基本指標
        total_value = portfolio_data['current_value'].sum()
        weights = portfolio_data['current_value'] / total_value
        
        # 模擬波動率計算（簡化版）
        returns = portfolio_data['current_value'].pct_change().dropna()
        volatility = returns.std() * (252 ** 0.5) if len(returns) > 0 else 0
        
        # 計算夏普比率（假設無風險利率 2%）
        risk_free_rate = 0.02
        excess_returns = returns.mean() - risk_free_rate / 252
        sharpe_ratio = excess_returns / volatility if volatility > 0 else 0
        
        # 最大回撤
        cumulative_returns = (1 + returns).cumprod()
        rolling_max = cumulative_returns.expanding().max()
        drawdown = (cumulative_returns - rolling_max) / rolling_max
        max_drawdown = drawdown.min()
        
        # 風險評分
        risk_score = min(100, max(0, 
            (volatility * 50) + 
            (abs(max_drawdown) * 100) + 
            (100 - sharpe_ratio * 10)
        ))
        
        # 風險等級
        if risk_score >= 70:
            risk_level = "高"
        elif risk_score >= 40:
            risk_level = "中"
        else:
            risk_level = "低"
        
        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "volatility": volatility,
            "sharpe_ratio": sharpe_ratio,
            "max_drawdown": max_drawdown,
            "total_value": total_value
        }
    except Exception as e:
        return {"error": str(e)}

def generate_compliance_check(portfolio_value: float) -> Dict:
    """生成合規檢查"""
    try:
        # 大戶投資合規檢查項目
        compliance_items = {
            "投資者適當性": portfolio_value <= 10000000,  # 1000萬上限
            "分散投資": True,  # 假設已符合
            "風險揭露": True,  # 假設已符合
            "交易記錄": True,  # 假設已符合
            "定期審核": True   # 假設已符合
        }
        
        compliance_score = sum(compliance_items.values()) / len(compliance_items) * 100
        
        findings = []
        recommendations = []
        
        if not compliance_items["投資者適當性"]:
            findings.append("投資金額超過大戶定義上限")
            recommendations.append("建議降低投資金額或取得大戶投資者資格")
        
        return {
            "compliance_score": compliance_score,
            "findings": findings,
            "recommendations": recommendations,
            "details": compliance_items
        }
    except Exception as e:
        return {"error": str(e)}

# ==================== 審核介面函數 ====================

def show_audit_interface():
    """顯示審核介面"""
    st.markdown('<div class="audit-card">', unsafe_allow_html=True)
    st.markdown('<h2 style="color: #ff6b35;">🔍 新增審核記錄</h2>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 審核表單
    with st.form("audit_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            investor_id = st.text_input("投資者 ID", key="investor_id")
            audit_type = st.selectbox("審核類型", ["例行審核", "特別審核", "風險評估", "合規檢查"], key="audit_type")
        
        with col2:
            portfolio_value = st.number_input("投資組合價值", min_value=0.0, step=10000.0, format="%.0f", key="portfolio_value")
            risk_level = st.selectbox("風險等級", ["低", "中", "高"], key="risk_level")
        
        # 審核發現和建議
        findings = st.text_area("審核發現", height=100, key="findings")
        recommendations = st.text_area("改善建議", height=100, key="recommendations")
        
        # 提交按鈕
        submitted = st.form_submit_button("🔍 創建審核記錄", use_container_width=True)
        
        if submitted:
            if investor_id and portfolio_value:
                compliance_result = generate_compliance_check(portfolio_value)
                compliance_score = compliance_result.get("compliance_score", 0)
                
                success = create_audit_record(
                    investor_id, audit_type, risk_level,
                    portfolio_value, compliance_score,
                    findings, recommendations, "系統審核員"
                )
                
                if success:
                    st.success("✅ 審核記錄創建成功！")
                    st.balloons()
                else:
                    st.error("❌ 審核記錄創建失敗！")
            else:
                st.error("❌ 請填寫必要資訊！")

def show_audit_reports():
    """顯示審核報告"""
    st.markdown('<div class="audit-card">', unsafe_allow_html=True)
    st.markdown('<h2 style="color: #ff6b35;">📊 審核報告查詢</h2>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 查詢選項
    col1, col2 = st.columns(2)
    
    with col1:
        search_investor = st.text_input("投資者 ID", key="search_investor")
        search_date = st.date_input("審核日期", key="search_date")
    
    with col2:
        audit_type_filter = st.selectbox("審核類型篩選", ["全部", "例行審核", "特別審核", "風險評估", "合規檢查"], key="audit_type_filter")
    
    # 查詢按鈕
    if st.button("🔍 查詢審核記錄", use_container_width=True):
        if search_investor:
            st.info(f"🔍 正在查詢投資者 {search_investor} 的審核記錄...")
            # 這裡應該連接數據庫並查詢
            st.markdown('<div class="audit-report">', unsafe_allow_html=True)
            st.markdown("<p>📋 查詢結果將顯示在這裡...</p>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

def show_compliance_dashboard():
    """顯示合規儀表板"""
    st.markdown('<div class="audit-card">', unsafe_allow_html=True)
    st.markdown('<h2 style="color: #ff6b35;">⚖️ 合規儀表板</h2>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 合規狀態指標
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="compliance-status">', unsafe_allow_html=True)
        st.markdown("<h3>總投資者數</h3>", unsafe_allow_html=True)
        st.markdown("<h1>156</h1>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="compliance-status">', unsafe_allow_html=True)
        st.markdown("<h3>活躍審核</h3>", unsafe_allow_html=True)
        st.markdown("<h1>23</h1>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="compliance-status">', unsafe_allow_html=True)
        st.markdown("<h3>合規率</h3>", unsafe_allow_html=True)
        st.markdown("<h1>94.2%</h1>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="compliance-status">', unsafe_allow_html=True)
        st.markdown("<h3>風險警示</h3>", unsafe_allow_html=True)
        st.markdown("<h1 class='risk-medium'>3</h1>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 風險分布
    st.markdown("---")
    st.markdown('<div class="audit-card">', unsafe_allow_html=True)
    st.markdown("<h3>風險等級分布</h3>", unsafe_allow_html=True)
    
    risk_data = pd.DataFrame({
        '風險等級': ['低', '中', '高'],
        '投資者數量': [89, 54, 13],
        '佔比': ['57.1%', '34.6%', '8.3%']
    })
    
    st.dataframe(risk_data, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== 其他功能模組 ====================

def show_investment_dashboard():
    """顯示投資儀表板"""
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown('<h2 style="color: #ff6b35;">💰 投資儀表板</h2>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("總資產", "NT$ 15,234,567", "+2.3%")
    with col2:
        st.metric("今日收益", "NT$ 45,678", "+1.2%")
    with col3:
        st.metric("年化報酬率", "12.5%", "+0.8%")
    
    st.markdown("---")
    st.info("📊 投資組合詳細分析將顯示在這裡...")

def show_market_analysis():
    """顯示市場分析"""
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown('<h2 style="color: #ff6b35;">📈 市場分析</h2>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.info("🔍 市場趨勢分析將顯示在這裡...")

def show_portfolio_management():
    """顯示投資組合管理"""
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown('<h2 style="color: #ff6b35;">📊 投資組合管理</h2>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.info("📋 投資組合管理功能將顯示在這裡...")

# ==================== 主程式 ====================

def main():
    """主程式"""
    # 初始化審核數據庫
    if not init_audit_database():
        st.error("❌ 系統初始化失敗，無法啟動審核系統")
        return
    
    # 頂部標題
    st.title("🤖 莫連投資代理人 v2.8")
    
    # 側邊欄選單
    with st.sidebar:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #ff6b35;">🎯 功能選單</h3>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 主要功能選項
        page = st.radio("選擇功能", [
            "💰 投資儀表板",
            "📈 市場分析", 
            "📊 投資組合管理",
            "🏛 大戶投資審核",
            "⚙️ 系統設定"
        ])
        
        # 大戶投資審核子選單
        if page == "🏛 大戶投資審核":
            st.markdown("---")
            st.markdown('<div class="audit-card">', unsafe_allow_html=True)
            st.markdown('<h4 style="color: #ff6b35;">🏛 審核功能</h4>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            audit_page = st.radio("選擇審核功能", [
                "🔍 新增審核",
                "📊 審核報告", 
                "⚖️ 合規儀表板"
            ])
        else:
            audit_page = None
    
    # 主要內容區
    if page == "💰 投資儀表板":
        show_investment_dashboard()
    elif page == "📈 市場分析":
        show_market_analysis()
    elif page == "📊 投資組合管理":
        show_portfolio_management()
    elif page == "🏛 大戶投資審核":
        if audit_page == "🔍 新增審核":
            show_audit_interface()
        elif audit_page == "📊 審核報告":
            show_audit_reports()
        elif audit_page == "⚖️ 合規儀表板":
            show_compliance_dashboard()
    elif page == "⚙️ 系統設定":
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown('<h2 style="color: #ff6b35;">⚙️ 系統設定</h2>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.info("🔧 系統設定功能將顯示在這裡...")
    
    # 保持頁面狀態
    if 'selected_page' not in st.session_state:
        st.session_state.selected_page = "💰 投資儀表板"
    
    st.session_state.selected_page = page

if __name__ == "__main__":
    main()
