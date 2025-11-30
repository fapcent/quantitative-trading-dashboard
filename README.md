# 📈 Quantitative Trading Dashboard

![License](https://img.shields.io/badge/license-MIT-blue.svg) ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white) ![Vue.js](https://img.shields.io/badge/vuejs-%2335495e.svg?style=flat&logo=vuedotjs&logoColor=%234FC08D) ![Nodejs](https://img.shields.io/badge/node.js-6DA55F?style=flat&logo=node.js&logoColor=white) ![Python](https://img.shields.io/badge/python-3670A0?style=flat&logo=python&logoColor=ffdd54)

Une plateforme de trading algorithmique fullstack capable d'ingérer, de stocker et de visualiser des données de marché haute fréquence en temps réel.

## 🏗 Architecture Micro-services

Le système est orchestré via **Docker Compose** et composé de 4 services isolés :

* 🐍 **Ingestion Workers (Python)** : Connexion aux WebSockets (Alpaca & Binance) pour la capture de données tick-by-tick.
* 🗄️ **Timeseries Storage (MySQL)** : Persistance des données avec optimisation des schémas pour la lecture rapide.
* 🚀 **API Gateway (Node.js/Express)** : API RESTful exposant les données normalisées au frontend.
* 📊 **Dashboard (Vue.js 3)** : Visualisation temps réel (Chart.js) avec rafraîchissement dynamique.

## ✨ Fonctionnalités Clés

* **Arbitrage Monitor :** Détection visuelle des écarts de prix (Spread) entre les marchés Actions (AAPL) et Crypto (BTC simulé).
* **Security First :** Gestion des secrets via variables d'environnement (Compatible Vault).
* **AI Fraud Detection :** Intégration d'un module scikit-learn (Isolation Forest) pour détecter les anomalies de marché.

## 🚀 Démarrage Rapide

\\\ash
# Lancer l'environnement complet
docker-compose up --build
\\\

Accédez ensuite au dashboard sur : \http://localhost:8080\

## 🧠 Choix Techniques

> **Pourquoi une architecture découplée ?**
> Pour garantir que l'ingestion des données (critique) ne soit jamais ralentie par le rendu graphique ou les requêtes API. Les Workers écrivent de manière asynchrone, assurant une latence minimale.
