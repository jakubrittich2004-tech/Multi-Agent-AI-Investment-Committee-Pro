import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime

# Try importing LangChain for OpenAI LLM execution
try:
    from langchain_openai import ChatOpenAI
    from langchain.schema import SystemMessage, HumanMessage
    HAS_LANGCHAIN = True
except ImportError:
    HAS_LANGCHAIN = False

# 1. Page Configuration
st.set_page_config(
    page_title="Institutional AI Investment Committee",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom CSS (Bloomberg Terminal Theme)
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #e6edf3; }
    h1, h2, h3 { color: #ffffff !important; font-weight: 700 !important; }
    
    .agent-card {
        padding: 18px;
        border-radius: 8px;
        margin-bottom: 20px;
        background-color: #161b22;
        border: 1px solid #30363d;
    }
    .fund-card { border-left: 5px solid #38bdf8; }
    .bull-card { border-left: 5px solid #22c55e; }
    .bear-card { border-left: 5px solid #ef4444; }
    .risk-card { border-left: 5px solid #f59e0b; }
    
    .stButton>button { width: 100%; background: #238636; color: white; font-weight: 600; border: none; padding: 10px; border-radius: 6px; }
    .stButton>button:hover { background: #2ea043; }
</style>
""", unsafe_allow_html=True)

st.title("🏛️ Multi-Agent AI Investment Committee")
st.caption("Institutional Long/Short Equity Research & Risk Management Engine")
st.markdown("---")

# Sidebar Configuration
st.sidebar.header("⚙️ Trade Parameters")
ticker_symbol = st.sidebar.text_input("Equity Ticker:", value="NVDA").upper()
trade_type = st.sidebar.radio("Strategy Mandate:", ["LONG (Buy/Growth)", "SHORT (Bearish Speculation)"])
horizon = st.sidebar.selectbox("Investment Horizon:", ["Short-Term (1-3 mos)", "Medium-Term (6-12 mos)", "Long-Term (3-5 yrs)"])
risk_profile = st.sidebar.select_slider("Portfolio Risk Tolerance:", options=["Conservative", "Moderate", "Aggressive"])

st.sidebar.markdown("---")
api_key = st.sidebar.text_input("OpenAI API Key (optional):", type="password")

# MARKET DATA FETCHING
@st.cache_data(ttl=3600)
def fetch_financial_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        pe_val = info.get("trailingPE", None)
        fpe_val = info.get("forwardPE", None)
        margin_val = info.get("profitMargins", None)
        growth_val = info.get("revenueGrowth", None)
        
        return {
            "name": info.get("longName", ticker),
            "price": info.get("currentPrice", info.get("regularMarketPrice", 0)),
            "pe": pe_val,
            "pe_str": f"{pe_val:.1f}x" if isinstance(pe_val, (int, float)) else "N/A",
            "fpe_str": f"{fpe_val:.1f}x" if isinstance(fpe_val, (int, float)) else "N/A",
            "market_cap": info.get("marketCap", 0),
            "margin": margin_val if isinstance(margin_val, (int, float)) else 0,
            "margin_str": f"{margin_val * 100:.1f}%" if isinstance(margin_val, (int, float)) else "N/A",
            "growth": growth_val if isinstance(growth_val, (int, float)) else 0,
            "growth_str": f"{growth_val * 100:.1f}%" if isinstance(growth_val, (int, float)) else "N/A",
            "beta": info.get("beta", 1.0),
            "currency": info.get("currency", "USD")
        }
    except Exception:
        return None

# LLM AGENT ENGINE
def run_llm_agent(system_prompt, user_prompt, api_key=None):
    if api_key and HAS_LANGCHAIN:
        try:
            llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=api_key, temperature=0.2)
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            res = llm.invoke(messages)
            return res.content
        except Exception:
            return None
    return None

if st.button("🚀 Execute Committee Deliberation"):
    with st.spinner("Fetching market telemetry & synchronizing AI Agents..."):
        data = fetch_financial_data(ticker_symbol)
        
    if data:
        st.subheader(f"📈 Analysis: {data['name']} ({ticker_symbol}) | Mandate: {trade_type}")
        
        # Financial Metrics Bar
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Stock Price", f"{data['price']} {data['currency']}")
        m2.metric("P/E Ratio", data['pe_str'])
        m3.metric("Forward P/E", data['fpe_str'])
        m4.metric("YoY Rev Growth", data['growth_str'])
        m5.metric("Profit Margin", data['margin_str'])
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("💬 AI Agent Research Briefings")
        
        is_long = "LONG" in trade_type
        
        # LLM Prompts in English
        prompt_fund = f"Analyze equity fundamentals for {ticker_symbol} (P/E: {data['pe_str']}, Margin: {data['margin_str']}, Growth: {data['growth_str']}). Provide 3 concise bullet points in English."
        prompt_bull = f"Defend a {trade_type} thesis for {ticker_symbol}. Provide 3 institutional growth catalysts in English."
        prompt_bear = f"Conduct a forensic breakdown of risks for {ticker_symbol}. Provide 3 critical bullet points in English."

        llm_fund = run_llm_agent("You are a Senior Fundamental Equity Analyst.", prompt_fund, api_key)
        llm_bull = run_llm_agent("You are a Growth-focused Bullish Analyst.", prompt_bull, api_key)
        llm_bear = run_llm_agent("You are a Conservative Risk & Forensic Analyst.", prompt_bear, api_key)

        # 1. Fundamental Analyst
        fund_bullets = llm_fund if llm_fund else f"""
<ul>
    <li><b>Valuation Multiple:</b> Trailing P/E stands at <b>{data['pe_str']}</b> (Forward P/E: {data['fpe_str']}).</li>
    <li><b>Profitability & Growth:</b> Net profit margin is <b>{data['margin_str']}</b> with YoY revenue growth of <b>{data['growth_str']}</b>.</li>
    <li><b>Market Position:</b> Total market capitalization currently at <b>${data['market_cap']/1e9:.2f}B USD</b>.</li>
</ul>
"""
        st.markdown(f"""
<div class="agent-card fund-card">
    <h3 style="margin-top:0;">📊 1. Fundamental Analyst Agent</h3>
    {fund_bullets}
</div>
""", unsafe_allow_html=True)

        # 2. Bull vs 3. Bear Agent
        col_bull, col_bear = st.columns(2)
        
        with col_bull:
            bull_bullets = llm_bull if llm_bull else f"""
<ul>
    <li><b>Catalysts:</b> Revenue expansion at <b>{data['growth_str']}</b> confirms strong economic moat.</li>
    <li><b>Operating Leverage:</b> High net margin (<b>{data['margin_str']}</b>) allows aggressive reinvestment.</li>
    <li><b>Upside Potential:</b> Highly favorable risk/reward for horizon <b>{horizon}</b>.</li>
</ul>
"""
            st.markdown(f"""
<div class="agent-card bull-card">
    <h3 style="margin-top:0;">🟢 2. Bull Agent (Long Thesis)</h3>
    {bull_bullets}
</div>
""", unsafe_allow_html=True)
            
        with col_bear:
            bear_bullets = llm_bear if llm_bear else f"""
<ul>
    <li><b>Valuation Risk:</b> Elevated P/E of <b>{data['pe_str']}</b> leaves zero margin for earnings misses.</li>
    <li><b>Macro & Competition:</b> Vulnerable to macro cyclicality and emerging competitive pressure.</li>
    <li><b>Downside Exposure:</b> Risk of margin compression over upcoming fiscal quarters.</li>
</ul>
"""
            st.markdown(f"""
<div class="agent-card bear-card">
    <h3 style="margin-top:0;">🔴 3. Bear Agent (Short Thesis)</h3>
    {bear_bullets}
</div>
""", unsafe_allow_html=True)

        # Committee Decision Engine
        approve_trade = False
        if is_long:
            if data['growth'] > 0 and data['margin'] > 0:
                approve_trade = True
                verdict_action = "OPEN LONG POSITION"
                summary_text = f"Committee APPROVES LONG position in {ticker_symbol}. Core fundamentals remain robust with margins at {data['margin_str']} and YoY revenue growth of {data['growth_str']}."
            else:
                approve_trade = False
                verdict_action = "REJECT LONG (Vetoed)"
                summary_text = f"Committee REJECTS LONG position in {ticker_symbol} due to negative revenue growth ({data['growth_str']}) or unprofitable margin profiles."
        else:
            if data['growth'] < 0 or (isinstance(data['pe'], (int, float)) and data['pe'] > 50):
                approve_trade = True
                verdict_action = "OPEN SHORT POSITION"
                summary_text = f"Committee APPROVES SHORT mandate for {ticker_symbol}. Identified fundamental vulnerability (Growth: {data['growth_str']} / P/E: {data['pe_str']})."
            else:
                approve_trade = False
                verdict_action = "REJECT SHORT (Vetoed)"
                summary_text = f"Committee REJECTS SHORT mandate for {ticker_symbol}. Growth profile ({data['growth_str']}) is too strong to justify short exposure."

        rec_alloc = "3.5%" if approve_trade else "0.0% (VETO)"
        stop_loss = "-5.0%" if not is_long else "-8.5%"

        # 4. Risk Manager Card
        risk_status = "✅ APPROVED: Parameters within risk mandate" if approve_trade else "❌ VETO: Violates portfolio risk limits"
        st.markdown(f"""
<div class="agent-card risk-card">
    <h3 style="margin-top:0;">⚖️ 4. Chief Risk Officer (CRO) Agent</h3>
    <ul>
        <li><b>Asset Volatility (Beta):</b> <b>{data['beta']}</b></li>
        <li><b>Risk Committee Verdict:</b> {risk_status}</li>
        <li><b>Max Position Allocation:</b> <b>{rec_alloc}</b> portfolio cap | <b>Strict Stop-Loss:</b> <b>{stop_loss}</b></li>
    </ul>
</div>
""", unsafe_allow_html=True)
        
        # 5. CIO Memorandum
        st.markdown("---")
        st.subheader("📝 Final Investment Committee Memorandum (CIO Verdict)")
        
        memo = f"""# INVESTMENT COMMITTEE MEMORANDUM
--------------------------------------------------
Date: {datetime.now().strftime('%Y-%m-%d')}
Asset: {data['name']} ({ticker_symbol})
Strategy: {trade_type} | Horizon: {horizon}
Risk Profile: {risk_profile} | Engine: {'OpenAI GPT-4o' if (api_key and HAS_LANGCHAIN) else 'Institutional Rule Engine'}

1. EXECUTIVE SUMMARY:
{summary_text}

2. TRADE PARAMETERS:
- Final Verdict: {verdict_action}
- Entry Price: {data['price']} {data['currency']}
- Approved Allocation: {rec_alloc}
- Risk Boundary (Stop-Loss): {stop_loss}

3. COMMITTEE SIGN-OFF:
[{'X' if approve_trade else ' '}] Chief Investment Officer (CIO)
[X] Fundamental Analyst Agent
[{'X' if approve_trade else ' '}] Chief Risk Officer (CRO)
--------------------------------------------------"""
        
        st.code(memo, language="markdown")
        
        st.download_button(
            label="📄 Download Investment Memorandum (.txt)",
            data=memo,
            file_name=f"IC_Memorandum_{ticker_symbol}.txt",
            mime="text/plain"
        )
        
    else:
        st.error("Error: Please enter a valid stock ticker (e.g., NVDA, AAPL, MSFT).")
