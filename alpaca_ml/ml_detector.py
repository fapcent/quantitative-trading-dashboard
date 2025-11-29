import os
import time
import mysql.connector
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# Configuration BDD
DB_HOST = os.environ.get('DB_HOST', 'db')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASS = os.environ.get('DB_PASS', 'fabrice')
DB_NAME = os.environ.get('DB_NAME', 'trading_dashboard')

def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME
    )

def train_and_detect():
    conn = None
    try:
        conn = get_db_connection()
        
        # 1. Récupérer assez de données pour l'entraînement (500 points)
        query = "SELECT price, volume FROM market_data ORDER BY timestamp DESC LIMIT 500"
        df = pd.read_sql(query, conn)
        
        # Il faut un minimum de données pour que le ML ait du sens
        if len(df) < 50:
            print(f"⏳ En attente de plus de données (Actuel: {len(df)}/50)...")
            return

        # 2. Préparation des données (Feature Engineering)
        # Le ML fonctionne mieux si on "normalise" les données (les mettre à la même échelle)
        scaler = StandardScaler()
        X = scaler.fit_transform(df[['price', 'volume']])

        # 3. Entraînement du modèle (Isolation Forest)
        # contamination=0.05 signifie qu'on s'attend à environ 5% d'anomalies
        model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
        model.fit(X)

        # 4. Prédiction sur le dernier point (le plus récent)
        # Le dernier point est le premier de la liste car on a fait DESC
        last_point = X[0].reshape(1, -1)
        prediction = model.predict(last_point)
        
        # Isolation Forest renvoie -1 pour une anomalie, 1 pour normal
        is_anomaly = prediction[0] == -1
        
        current_price = df.iloc[0]['price']
        current_vol = df.iloc[0]['volume']

        if is_anomaly:
            # Score d'anomalie (plus c'est bas, plus c'est anormal)
            score = model.decision_function(last_point)[0]
            print(f"🤖 [AI DETECTOR] 🚨 ANOMALIE COMPLEXE DÉTECTÉE !")
            print(f"   Prix: {current_price} | Vol: {current_vol} | Score IA: {score:.4f}")
            print(f"   (Ce pattern ne ressemble pas à l'historique récent)")
        else:
            print(f"🤖 [AI DETECTOR] ✅ Comportement Normal (Prix: {current_price})")

    except Exception as e:
        print(f"Erreur ML : {e}")
    finally:
        if conn and conn.is_connected():
            conn.close()

if __name__ == "__main__":
    print("🧠 Démarrage du détecteur de fraude par IA (Isolation Forest)...")
    time.sleep(15) # Attente BDD
    
    while True:
        train_and_detect()
        time.sleep(10) # Ré-entraînement et analyse toutes les 10s