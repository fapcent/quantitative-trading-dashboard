import os
import time
import mysql.connector  # Importe le connecteur MySQL
from mysql.connector import errorcode
from alpaca_trade_api.stream import Stream
from alpaca_trade_api.common import URL

# --- 1. Configuration ---
API_KEY = os.environ.get('API_KEY')
API_SECRET = os.environ.get('API_SECRET')
BASE_URL = "https://paper-api.alpaca.markets"
DB_NAME = os.environ.get('DB_NAME', 'trading_dashboard')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASS = os.environ.get('DB_PASS', 'votre_mot_de_passe')
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = os.environ.get('DB_PORT', '3306')

SYMBOL_TO_WATCH = 'AAPL' # Apple

# --- 2. Connexion à la base de données (Version MySQL) ---
# (Cette fonction est correcte)
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

# --- 3. Logique d'insertion (Version MySQL) ---
# (CORRIGÉE POUR UTILISER LES BONS NOMS D'ATTRIBUTS IEX)
def insert_trade_data(conn, data):
    sql = """
    INSERT INTO market_data (timestamp, symbol, price, volume)
    VALUES (%s, %s, %s, %s);
    """
    try:
        # CORRECTION : On utilise les noms complets
        data_tuple = (
            data.timestamp, # <-- CHANGÉ de data.t
            data.symbol,    # <-- CHANGÉ de data.S
            data.price,     # <-- CHANGÉ de data.p
            data.size       # <-- CHANGÉ de data.s
        )
        with conn.cursor() as cur:
            cur.execute(sql, data_tuple)
        conn.commit()
        # CORRECTION : Mise à jour du print
        print(f"Donnée insérée : {data.symbol} - Prix: {data.price}")
    except mysql.connector.Error as err:
        print(f"Erreur lors de l'insertion : {err}")
        conn.rollback()

# --- 4. Le "Handler" de Stream (Asynchrone) ---
# (Cette fonction est correcte)
async def on_stock_trade(trade):
    """Callback asynchrone pour gérer les données de trade."""
    conn = get_db_connection()
    if conn:
        try:
            insert_trade_data(conn, trade) # On passe 'trade'
        finally:
            conn.close()

# --- 5. Lancement du Worker (Point d'entrée) ---
# (Cette fonction est correcte)
if __name__ == "__main__":
    if not API_KEY or not API_SECRET:
        print("Erreur : Les variables d'environnement API_KEY et API_SECRET...")
        exit(1)

    print("Démarrage du worker...")
    print(f"Connexion à la base de données sur '{DB_HOST}'...")
    
    test_conn = get_db_connection()
    if not test_conn:
        print("Échec de la connexion à la base de données.")
        exit(1)
    test_conn.close()

    stream = Stream(API_KEY, 
                    API_SECRET, 
                    base_url=URL(BASE_URL), 
                    data_feed='iex') # <-- Flux de données gratuit (IEX)

    print(f"Abonnement au flux de trades pour : {SYMBOL_TO_WATCH}")
    stream.subscribe_trades(on_stock_trade, SYMBOL_TO_WATCH)

    print("Le worker est en marche. En attente de données...")
    print("Appuyez sur CTRL+C pour arrêter.")
    
    stream.run()