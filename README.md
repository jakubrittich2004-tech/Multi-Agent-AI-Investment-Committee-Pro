# 🏛️ Autonomous Multi-Agent AI Investment Committee

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)
![LangChain](https://img.shields.io/badge/Orchestration-LangChain-green?style=flat-square)
![OpenAI](https://img.shields.io/badge/LLM-GPT--4o-orange?style=flat-square&logo=openai)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-red?style=flat-square&logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-brightgreen?style=flat-square)

An institutional-grade, multi-agent AI system designed to automate equity research, financial analysis, and portfolio risk enforcement for **Equity Long/Short mandates**. 

By orchestrating specialized LLM agents (Fundamental, Bull, Bear, Risk Manager), this system mitigates cognitive bias (confirmation bias) and processes unstructured financial text data (SEC 10-K filings, earnings news) alongside real-time market metrics.

---

## ⚡ Key Architecture & Autonomous Agents

The system leverages a multi-agent workflow where specialized agents debate trade hypotheses based on objective telemetry and data context:

1. **📊 Fundamental Analyst Agent:** Extracts valuation multiples ($P/E$, $Forward\ P/E$), profitability metrics (Net Profit Margin), and $YoY$ revenue growth alongside SEC 10-K filings.
2. **🟢 Bull Agent (Long Thesis):** Formulates bullish investment theses, identifying secular growth catalysts, economic moats, and operating leverage.
3. **🔴 Bear Agent (Short Thesis):** Performs forensic breakdown, targeting accounting vulnerabilities, overvaluation, margin compression, and macroeconomic risks.
4. **⚖️ Chief Risk Officer (CRO):** Evaluates asset volatility ($\beta$), enforces dynamic portfolio allocation caps, sets strict Stop-Loss boundaries, and triggers an immediate **VETO** if a trade violates target risk parameters.
5. **📝 CIO Verdict Engine:** Synthesizes committee deliberations into an executive, downloadable **Investment Committee Memorandum**.

---

## 🛠️ Tech Stack & Technologies

* **Language & Runtime:** Python 3.10+
* **Orchestration & LLM Interface:** LangChain, LangChain-OpenAI (GPT-4o / GPT-4o-mini)
* **Financial Data Engine:** Yahoo Finance Telemetry API (`yfinance`), Pandas
* **UI Framework:** Streamlit (Custom Dark Institutional Terminal CSS)
* **RAG Pipeline:** Financial text parsing (SEC Filings / News Extraction Context)

---

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have Python installed on your system:
```bash
python --version
