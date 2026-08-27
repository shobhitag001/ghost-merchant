# 👻 Ghost Merchant

### Agentic OSINT Risk Investigator for Payment Merchants

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red?logo=streamlit)](https://streamlit.io/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Agentic_Workflow-purple)](https://www.langchain.com/langgraph)
[![Neo4j](https://img.shields.io/badge/Neo4j-Graph_Database-blue?logo=neo4j)](https://neo4j.com/)
[![Ollama](https://img.shields.io/badge/Ollama-Local_AI-black)](https://ollama.com/)

> **An autonomous multi-agent merchant risk investigation platform that detects suspicious merchant behavior using transaction intelligence, website OSINT, identity analysis, and merchant-network intelligence.**

---

## 🚨 Problem

Payment platforms can onboard a large number of merchants every day.

Traditional merchant risk monitoring often relies heavily on:

- Initial KYC checks
- Rule-based transaction monitoring
- Manual investigations
- Periodic reviews

The problem is that a merchant may appear legitimate during onboarding but later change its behavior.

For example:

A merchant may register as an **Apparel** business, pass initial checks, and later operate a completely different business through the same payment infrastructure.

By the time manual investigation identifies the problem, suspicious activity may already have occurred.

### The key question

> **How can a payment platform continuously investigate merchants and identify hidden risk signals before they become larger problems?**

---

# 💡 Solution

**Ghost Merchant** is an agentic merchant-risk investigation platform.

Instead of depending on a single risk rule, Ghost Merchant coordinates multiple specialized investigation agents.

Each agent analyzes a different risk dimension:

```text
                    ┌──────────────────────┐
                    │    Merchant Input    │
                    │  Merchant ID / Data  │
                    └──────────┬───────────┘
                               │
                               ▼
                 ┌──────────────────────────┐
                 │   Investigation Engine   │
                 └────────────┬─────────────┘
                              │
       ┌──────────────────────┼──────────────────────┐
       ▼                      ▼                      ▼
┌───────────────┐      ┌────────────────┐     ┌─────────────────┐
│ Merchant Risk │      │ Transaction    │     │ Website OSINT   │
│    Agent      │      │     Agent      │     │     Agent       │
└───────┬───────┘      └───────┬────────┘     └────────┬────────┘
        │                      │                       │
        └──────────────────────┼───────────────────────┘
                               │
                  ┌────────────┴────────────┐
                  ▼                         ▼
          ┌────────────────┐       ┌────────────────┐
          │ Identity Agent │       │  Graph Agent   │
          └───────┬────────┘       └───────┬────────┘
                  │                        │
                  └────────────┬───────────┘
                               ▼
                    ┌──────────────────────┐
                    │ Final Risk Analyzer  │
                    └──────────┬───────────┘
                               │
                               ▼
                       ┌─────────────────┐
                       │   Risk Score    │
                       │     0 – 100     │
                       └────────┬────────┘
                                │
                                ▼
                    ┌──────────────────────┐
                    │ AI Investigation     │
                    │ Report Agent         │
                    └──────────┬───────────┘
                               │
                               ▼
                       ┌─────────────────┐
                       │ Risk Dashboard  │
                       └─────────────────┘

---

## 🤖 Multi-Agent Investigation

Ghost Merchant uses specialized agents to investigate merchants from multiple perspectives.

### 🧾 Merchant Risk Agent

Analyzes merchant-level information such as:

- Declared business category
- Website/category mismatch
- Suspicious links
- Shared payout accounts
- Merchant-level risk indicators

### 💳 Transaction Agent

Analyzes transaction behavior including:

- Transaction timing
- Late-night activity
- Repeated transaction amounts
- Transaction patterns
- Suspicious behavioral signals

### 🌐 Website OSINT Agent

Investigates merchant websites for:

- Business-category mismatch
- Suspicious keywords
- Potential gambling-related content
- External links
- Website risk indicators

### 🪪 Identity Agent

Analyzes available identity information for:

- Business identity inconsistencies
- Category mismatches
- Identity verification issues
- Merchant information inconsistencies

### 🕸️ Graph Agent

Uses merchant relationships and shared infrastructure to identify connections through:

- Devices
- IP addresses
- Payout accounts
- Other shared infrastructure

### 🧠 Final Risk Analyzer

Combines the individual risk scores into:

- Risk Score: `0–100`
- Risk Level
- Recommended Action

### 🤖 AI Investigation Report Agent

Uses a local AI model to generate a structured investigation report based on the evidence collected by the investigation agents.

---

## 📊 Risk Scoring

Ghost Merchant evaluates multiple risk dimensions and produces an overall merchant risk score.

| Risk Dimension | Description |
|---|---|
| Merchant Risk | Merchant-level behavioral and business signals |
| Transaction Risk | Transaction-pattern anomalies |
| Website Risk | Website OSINT and category mismatch |
| Identity Risk | Identity and business inconsistencies |
| Graph Risk | Shared infrastructure and merchant connections |
| Final Risk | Combined overall merchant risk |

### Risk Levels

| Score | Risk Level |
|---:|---|
| 0–39 | 🟢 LOW |
| 40–59 | 🟡 MEDIUM |
| 60–79 | 🟠 HIGH |
| 80–100 | 🔴 CRITICAL |

The final recommendation is generated from the collected risk signals and is intended to support human risk review.

---

## 🕸️ Merchant Network Intelligence

Ghost Merchant uses graph-based analysis to identify relationships between merchants that may not be visible from individual merchant records.

The network analysis looks for shared infrastructure such as:

- 💻 Devices
- 🌐 IP addresses
- 💳 Payout accounts
- 🔗 Other merchant relationships

For example, a merchant may appear low-risk when analyzed individually but become more relevant when it shares infrastructure with multiple other merchants.

The graph layer helps investigators:

1. Identify connected merchants.
2. Detect shared infrastructure.
3. Understand merchant-to-merchant relationships.
4. Surface potentially coordinated activity.
5. Provide additional context for risk review.

### Example

```text
                 M008
                  │
            Shared IP / Account
                  │
                  ▼
              M004 👻
                  │
             Shared Device
                  │
                  ▼
                 M009

---

## 🖥️ Risk Investigation Dashboard

Ghost Merchant includes a Streamlit-based dashboard for monitoring and investigating the merchant portfolio.

### Dashboard Features

- 📊 **Portfolio Overview** — View total merchants and risk distribution.
- 🚨 **Risk Ranking** — Rank merchants based on their final risk score.
- 🔍 **Merchant Search** — Search merchants by ID or business name.
- 🎯 **Risk Filters** — Filter merchants by LOW, MEDIUM, HIGH, or CRITICAL risk.
- 📈 **Risk Comparison** — Visualize risk scores across the portfolio.
- 🏪 **Merchant Deep Investigation** — Inspect an individual merchant in detail.
- 🕸️ **Network Visualization** — Visualize connected merchants and shared infrastructure.
- 🤖 **AI Investigation Report** — Generate and display a structured investigation report.
- 🧠 **Investigation Signals** — Review the evidence behind each risk category.
- 📥 **CSV Export** — Download the merchant risk ranking for further analysis.

The dashboard is designed to give a risk analyst a single interface for moving from **portfolio-level monitoring → merchant-level investigation → evidence-based review**.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application and risk analysis |
| Streamlit | Interactive risk investigation dashboard |
| LangGraph | Agentic investigation workflow |
| Ollama + Gemma 3 | Local AI investigation report generation |
| Neo4j | Merchant relationship and graph analysis |
| NetworkX | Network analysis and visualization |
| Playwright | Website OSINT investigation |
| Pandas | Transaction and portfolio data processing |
| JSON | Merchant, transaction, identity and graph data |
| Git & GitHub | Version control and project collaboration |

---

## 🏗️ Project Architecture

```text
Ghost-Merchant/
│
├── agents/
│   └── ghost_graph.py
│
├── services/
│   ├── ai_report_agent.py
│   ├── graph_agent.py
│   ├── identity_agent.py
│   ├── investigation_engine.py
│   ├── neo4j_service.py
│   ├── network_visualizer.py
│   ├── risk_engine.py
│   ├── transaction_agent.py
│   └── website_agent.py
│
├── data/
│   ├── identity_data.json
│   ├── merchant_graph.json
│   ├── merchants.json
│   ├── suspicious_merchant.html
│   └── transactions.json
│
├── dashboard.py
├── app.py
├── config.py
├── portfolio_scanner.py
├── requirements.txt
└── .gitignore

Merchant Data
     │
     ▼
Investigation Engine
     │
     ├── Merchant Risk Agent
     ├── Transaction Agent
     ├── Website OSINT Agent
     ├── Identity Agent
     └── Graph Agent
             │
             ▼
     Final Risk Analyzer
             │
             ▼
       Risk Score 0–100
             │
             ▼
      Risk Classification
             │
             ▼
    AI Investigation Report
             │
             ▼
      Streamlit Dashboard

---

## 🎯 Risk Scoring Methodology

Ghost Merchant evaluates merchants across multiple independent risk dimensions.

Each investigation agent produces a risk score and supporting evidence. These signals are then combined by the Final Risk Analyzer to produce an overall risk score.

```text
Merchant Risk        ──┐
Transaction Risk     ──┤
Website Risk         ──┤
Identity Risk        ──┼──► Final Risk Analyzer ──► Final Score
Graph Risk           ──┘                              │
                                                      ▼
                                             Risk Classification

---

## 🔎 Example Investigation

The following is an example investigation generated using the project's sample merchant dataset.

### Merchant: Urban Deals (M004)

| Field | Result |
|---|---|
| Merchant ID | M004 |
| Business | Urban Deals |
| Declared Category | Apparel |
| Final Risk Score | **74/100** |
| Risk Level | 🟠 **HIGH** |
| Recommendation | **FLAG FOR RISK REVIEW** |

### Key Findings

- 🌐 Website content was inconsistent with the declared Apparel category.
- 🔗 Potentially suspicious external links were detected.
- 💳 Unusual transaction timing patterns were identified.
- 💰 Repeated identical transaction amounts were detected.
- 🪪 Identity and business information showed inconsistencies.
- 🕸️ The merchant was connected to other merchants through shared infrastructure.
- 🤖 An AI-generated investigation report summarized the collected evidence.

### Network Connections

The sample investigation identified connections between M004 and:

- `M008`
- `M009`

The graph analysis identified shared infrastructure involving devices, payout accounts, and IP addresses.

### Final Assessment

**Risk Score:** `74/100`

**Risk Level:** `HIGH`

**Recommended Action:** `FLAG FOR RISK REVIEW`

> This example demonstrates how multiple independent signals can be combined to prioritize a merchant for human risk review. The system is designed as a decision-support tool and does not independently determine wrongdoing.

---

## 🚀 Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/shobhitag001/ghost-merchant.git
cd ghost-merchant

---

## 🔮 Future Scope

- Real-time transaction and merchant data integration
- ML-based anomaly detection
- Continuous merchant monitoring
- Advanced graph-based risk propagation
- Automated investigator alerts and case management
- Integration with production KYC and payment-risk systems

---

## 👨‍💻 Author

**Shobhit Agrawal**

Ghost Merchant — Agentic OSINT Risk Investigator