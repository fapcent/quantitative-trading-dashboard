import os
import time
import mysql.connector  # Importe le connecteur MySQL
import asyncio          # <-- Requis
from mysql.connector import errorcode
from alpaca_trade_api.stream import CryptoDataStream # <-- La bonne classe
from alpaca_trade_api.common import URL

# --- 1. Configuration ---
# (Cette section ne change pas)
API_KEY = os.environ.get('API_KEY')
API_SECRET = os.environ.get('API_SECRET')
BASE_URL = "https://paper-api.alpaca.markets" # Requis pour l'argument URL()
DB_NAME = os.environ.get('DB_NAME', 'trading_dashboard')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASS = os.environ.get('DB_PASS', 'votre_mot_de_passe')
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = os.environ.get('DB_PORT', '3306')
SYMBOL_TO_WATCH = 'BTC-USD'

# --- 2. Connexion à la base de données ---
# (Cette fonction est correcte et ne change pas)
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            database=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT
        )
        print("Connexion à la base de données MySQL réussie.")
        return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Erreur : Mauvais utilisateur ou mot de passe.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Erreur : La base de données n'existe pas.")
        else:
            print(f"Erreur de connexion à la base de données : {err}")
        return None

# --- 3. Logique d'insertion ---
# (Cette fonction est correcte et ne change pas)
def insert_trade_data(conn, data):
    # Notez l'ajout de la colonne 'source' et du placeholder %s à la fin
    sql = """
    INSERT INTO market_data (timestamp, symbol, price, volume, source)
    VALUES (%s, %s, %s, %s, %s);
    """
    try:
        data_tuple = (
            data.timestamp,
            data.symbol,
            data.price,
            data.size,
            'Alpaca' # <--- On écrit en dur que ça vient d'Alpaca
        )
        with conn.cursor() as cur:
            cur.execute(sql, data_tuple)
        conn.commit()
        print(f"Donnée insérée (Alpaca) : {data.symbol} - Prix: {data.price}")
    except mysql.connector.Error as err:
        print(f"Erreur lors de l'insertion : {err}")
        conn.rollback()

# --- 4. Le "Handler" de Stream (Asynchrone) ---
# (Cette fonction est correcte et ne change pas)
async def on_crypto_trade(trade):
    """Callback asynchrone pour gérer les données de trade."""
    trade_data = trade.to_dict()
    conn = get_db_connection()
    if conn:
        try:
            insert_trade_data(conn, trade_data)
        finally:
            conn.close()

# --- 5. Lancement du Worker (Point d'entrée) ---
async def main():
    if not API_KEY or not API_SECRET:
        print("Erreur : Les variables d'environnement API_KEY et API_SECRET")
        print("         doivent être définies avant de lancer le script.")
        exit(1)

    print("Démarrage du worker...")
    print(f"Connexion à la base de données sur '{DB_HOST}'...")
    
    test_conn = get_db_connection()
    if not test_conn:
        print("Échec de la connexion à la base de données. Vérifiez vos variables d'environnement.")
        exit(1)
    test_conn.close()

    # Initialisation du client (cette ligne était correcte)
    stream = CryptoDataStream(API_KEY, API_SECRET, URL(BASE_URL), 'coinbase')
    # Abonnement au flux (cette ligne était correcte)
    print(f"Abonnement au flux de trades pour : {SYMBOL_TO_WATCH}")
    stream.subscribe_trades(on_crypto_trade, SYMBOL_TO_WATCH)

    print("Le worker est en marche. En attente de données...")
    print("Appuyez sur CTRL+C pour arrêter.")
    
    # CORRECTION CLÉ :
    # Au lieu de 'await stream.run_async()', nous mettons le script
    # en "sommeil" infini pour laisser les 'callbacks' fonctionner.
    while True:
        await asyncio.sleep(1)

# Lanceur asynchrone (cette ligne était correcte)
if __name__ == "__main__":
    asyncio.run(main())