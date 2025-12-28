import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="個人金融數據分析",
    layout="centered"
)

st.title("個人金融數據分析系統")
st.write("輸入每月財務資訊，系統將進行試算與模擬分析。")

st.divider()

# 使用者輸入
monthly_income = st.number_input("每月收入（元）", min_value=0, value=30000, step=1000)
fixed_expense = st.number_input("每月固定支出（元）", min_value=0, value=15000, step=1000)
investment_amount = st.number_input("每月投資金額（元）", min_value=0, value=5000, step=500)
risk_type = st.selectbox("投資風險屬性", ["保守型", "穩健型", "積極型"])
years = st.slider("投資年數", min_value=1, max_value=30, value=10)

st.divider()

# 收支計算
remaining_money = monthly_income - fixed_expense - investment_amount
st.subheader("每月收支分析")
if remaining_money > 0:
    st.success(f"每月剩餘金額：{remaining_money:,} 元")
elif remaining_money == 0:
    st.warning("每月收支剛好平衡")
else:
    st.error(f"每月超支金額：{abs(remaining_money):,} 元")

st.divider()

# 風險對應設定
if risk_type == "保守型":
    annual_return = 0.03
    allocation = {"債券型 / 現金": 0.6, "高股息 ETF": 0.3, "市值型 ETF": 0.1}
elif risk_type == "穩健型":
    annual_return = 0.06
    allocation = {"市值型 ETF": 0.5, "高股息 ETF": 0.3, "債券型 / 現金": 0.2}
else:
    annual_return = 0.09
    allocation = {"市值型 ETF": 0.7, "高股息 ETF": 0.2, "其他成長型": 0.1}

# 投資比例圓餅圖（Streamlit 內建）
st.subheader("投資配置比例")
alloc_df = pd.DataFrame({
    "資產類型": list(allocation.keys()),
    "比例": list(allocation.values())
})
st.write(alloc_df)

st.divider()

# 資產成長模擬
st.subheader("資產成長模擬")
monthly_return = (1 + annual_return) ** (1 / 12) - 1
total_months = years * 12
balance = 0
balances = []

for _ in range(total_months):
    balance = balance * (1 + monthly_return) + investment_amount
    balances.append(balance)

growth_df = pd.DataFrame({"月份": range(1, total_months + 1), "資產總額": balances})
st.line_chart(growth_df.set_index("月份"))

st.write(f"{years} 年後預估資產：約 {int(balance):,} 元（假設年化報酬率 {annual_return*100:.0f}%）")

st.divider()

# ETF 建議表
st.subheader("ETF 參考建議")
etf_data = [
    {"ETF": "0050", "類型": "市值型", "說明": "台灣大型企業"},
    {"ETF": "0056", "類型": "高股息", "說明": "穩定配息"},
    {"ETF": "00878", "類型": "高股息", "說明": "低波動"},
    {"ETF": "VT", "類型": "全球市場", "說明": "全球分散"},
    {"ETF": "VTI", "類型": "美國市場", "說明": "長期成長"}
]
st.table(pd.DataFrame(etf_data))

st.divider()
st.write("本工具僅供試算與學習用途，不構成任何投資建議。")
