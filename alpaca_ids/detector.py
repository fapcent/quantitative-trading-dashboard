import os
import time
import mysql.connector
import pandas as pd
import numpy as np

# --- Configuration ---
DB_HOST = os.environ.get('DB_HOST', 'db')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASS = os.environ.get('DB_PASS', 'fabrice')
DB_NAME = os.environ.get('DB_NAME', 'trading_dashboard')

# Paramètres de détection
WINDOW_SIZE = 20  # On regarde les 20 derniers prix
Z_THRESHOLD = 2.0 # Seuil d'alerte (2 écarts-types)

def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME
    )

def analyze_market():
    conn = None
    try:
        conn = get_db_connection()
        
        # 1. Récupérer les données (Pandas est fait pour ça !)
        query = f"SELECT * FROM market_data ORDER BY timestamp DESC LIMIT {WINDOW_SIZE}"
        df = pd.read_sql(query, conn)
        
        # On a besoin d'au moins 5 points pour faire des stats
        if len(df) < 5:
            print("Pas assez de données pour l'analyse...")
            return

        # Les données arrivent de la plus récente à la plus ancienne, on inverse
        df = df.iloc[::-1] 
        
        # 2. Calculs Quantitatifs (Moyenne & Volatilité)
        # On convertit la colonne 'price' en nombres flottants
        prices = df['price'].astype(float)
        
        mean = np.mean(prices)
        std_dev = np.std(prices) # Écart-type (Volatilité)
        last_price = prices.iloc[-1]

        # Éviter la division par zéro si le prix ne bouge pas du tout
        if std_dev == 0:
            return

        # 3. Calcul du Z-Score
        # Formule : (Prix Actuel - Moyenne) / Volatilité
        z_score = (last_price - mean) / std_dev

        print(f"Analyse : Prix=${last_price:.2f} | Moyenne=${mean:.2f} | Z-Score={z_score:.2f}")

        # 4. Détection d'Intrusion / Anomalie
        if abs(z_score) > Z_THRESHOLD:
            print(f"\n🚨 ALERTE IDS : ANOMALIE DÉTECTÉE !")
            print(f"   Le prix a dévié de {z_score:.2f} sigmas.")
            print(f"   Ceci pourrait être une attaque ou un crash.\n")

    except Exception as e:
        print(f"Erreur : {e}")
    finally:
        if conn and conn.is_connected():
            conn.close()

# --- Boucle principale ---
if __name__ == "__main__":
    print("Démarrage du Market IDS (Intrusion Detection System)...")
    time.sleep(10) # Attente que la BDD soit prête au démarrage
    
    while True:
        analyze_market()
        time.sleep(5) # Analyse toutes les 5 secondes