"""
FinGPT API 本地測試 - Google 開發計畫整合
驗證 FinGPT API 連線與功能
"""

import requests
import json
import sys
import os
from datetime import datetime

# FinGPT API 配置
FINGPT_API_KEY = "your_fingpt_api_key_here"
FINGPT_BASE_URL = "https://api.fingpt.com/v1"

def test_fingpt_connection():
    """測試 FinGPT API 連線"""
    print("🧠 開始測試 FinGPT API 連線...")
    
    try:
        headers = {
            "Authorization": f"Bearer {FINGPT_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # 測試基本連線
        test_data = {
            "model": "fingpt-pro",
            "messages": [
                {"role": "system", "content": "你是頂尖的台股AI分析師，請回應連線測試。"},
                {"role": "user", "content": "請回應「FinGPT API 連線成功」確認連線正常。"}
            ],
            "max_tokens": 100,
            "temperature": 0.7
        }
        
        print("📡 正在發送測試請求...")
        response = requests.post(f"{FINGPT_BASE_URL}/chat/completions", 
                              headers=headers, 
                              json=test_data, 
                              timeout=30)
        
        print(f"📊 回應狀態碼: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            reply = result["choices"][0]["message"]["content"]
            print(f"✅ FinGPT API 連線成功！")
            print(f"🤖 FinGPT 回應: {reply}")
            return True
        else:
            print(f"❌ FinGPT API 連線失敗: {response.status_code}")
            print(f"📄 錯誤內容: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ FinGPT API 連線異常: {str(e)}")
        return False

def test_stock_analysis():
    """測試股票分析功能"""
    print("\n🧠 開始測試股票分析功能...")
    
    test_symbol = "0050.TW"
    
    try:
        headers = {
            "Authorization": f"Bearer {FINGPT_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # 股票分析測試
        analysis_data = {
            "model": "fingpt-pro",
            "messages": [
                {"role": "system", "content": "你是頂尖的台股AI分析師，擅長技術分析和基本面分析。"},
                {"role": "user", "content": f"請分析 {test_symbol} 的投資機會，包括：1.技術指標分析 2.基本面評估 3.風險評估 4.投資建議"}
            ],
            "max_tokens": 500,
            "temperature": 0.7
        }
        
        print(f"📊 正在分析 {test_symbol}...")
        response = requests.post(f"{FINGPT_BASE_URL}/chat/completions", 
                              headers=headers, 
                              json=analysis_data, 
                              timeout=45)
        
        print(f"📊 分析狀態碼: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            analysis = result["choices"][0]["message"]["content"]
            print(f"✅ {test_symbol} 分析成功！")
            print(f"🤖 FinGPT 分析結果:\n{analysis}")
            return True
        else:
            print(f"❌ {test_symbol} 分析失敗: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ {test_symbol} 分析異常: {str(e)}")
        return False

def test_risk_assessment():
    """測試風險評估功能"""
    print("\n🎯 開始測試風險評估功能...")
    
    try:
        headers = {
            "Authorization": f"Bearer {FINGPT_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # 風險評估測試
        risk_data = {
            "model": "fingpt-pro",
            "messages": [
                {"role": "system", "content": "你是專業的投資風險評估師，請提供詳細的風險分析。"},
                {"role": "user", "content": "請評估當前台股市場的整體風險，包括：1.市場風險 2.政策風險 3.流動性風險 4.投資建議"}
            ],
            "max_tokens": 800,
            "temperature": 0.5
        }
        
        print("🎯 正在進行風險評估...")
        response = requests.post(f"{FINGPT_BASE_URL}/chat/completions", 
                              headers=headers, 
                              json=risk_data, 
                              timeout=60)
        
        print(f"🎯 風險評估狀態碼: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            risk_analysis = result["choices"][0]["message"]["content"]
            print(f"✅ 風險評估成功！")
            print(f"🎯 FinGPT 風險分析:\n{risk_analysis}")
            return True
        else:
            print(f"❌ 風險評估失敗: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 風險評估異常: {str(e)}")
        return False

def main():
    """主測試程式"""
    print("=" * 60)
    print("🧠 FinGPT API 本地測試 - Google 開發計畫整合")
    print("=" * 60)
    print(f"📅 測試時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔑 API 端點: {FINGPT_BASE_URL}")
    print(f"🔑 API 金鑰: {FINGPT_API_KEY[:20]}...")
    print()
    
    # 執行測試
    tests = [
        ("🔗 基本連線測試", test_fingpt_connection),
        ("📊 股票分析測試", test_stock_analysis),
        ("🎯 風險評估測試", test_risk_assessment)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20}")
        print(f"執行: {test_name}")
        print(f"{'='*20}")
        
        result = test_func()
        results.append((test_name, "✅ 成功" if result else "❌ 失敗"))
        
        print(f"{'='*20}")
        print(f"結果: {'✅ 成功' if result else '❌ 失敗'}")
        print(f"{'='*20}")
    
    # 測試結果總結
    print(f"\n{'='*60}")
    print("📊 測試結果總結")
    print(f"{'='*60}")
    
    for test_name, result in results:
        print(f"{test_name}: {result}")
    
    print(f"\n{'='*60}")
    print("💡 使用說明:")
    print("1. 請將 FINGPT_API_KEY 替換為真實的 API 金鑰")
    print("2. 在 PyCharm 中運行此檔案進行測試")
    print("3. 測試成功後，可在 dashboard_secure.py 中使用 FinGPT API")
    print("4. 確保網路連線正常")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
