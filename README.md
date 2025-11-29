# 📈 Quantitative Trading Dashboard

A Fullstack Real-Time Trading Platform designed to monitor market data and detect anomalies.

## 🚀 Key Features
* **Real-Time Ingestion:** Python workers connecting to WebSockets (Crypto & Equities).
* **Arbitrage Monitor:** Live tracking of price spreads between Exchanges (Binance vs Alpaca).
* **AI Fraud Detection:** Integrated Isolation Forest model (Scikit-learn) to detect market anomalies.
* **Architecture:** Micro-services architecture orchestrated with Docker Compose.
* **Security:** Secret management via Environment variables and Vault.

## 🛠 Stack
* **Backend:** Python, Node.js (Express)
* **Frontend:** Vue.js, Chart.js
* **Database:** MySQL
* **Ops:** Docker
