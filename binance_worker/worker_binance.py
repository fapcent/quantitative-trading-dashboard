import asyncio
import json
import os
import time
import websockets
import mysql.connector

# Configuration BDD
DB_HOST = os.environ.get('DB_HOST', 'db')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASS = os.environ.get('DB_PASS', 'fabrice')
DB_NAME = os.environ.get('DB_NAME', 'trading_dashboard')

# Binance écoute le Bitcoin (BTCUSDT)
BINANCE_WS_URL = "wss://stream.binance.com:9443/ws/btcusdt@trade"

def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME
    )

def insert_data(price, timestamp):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
        INSERT INTO market_data (timestamp, symbol, price, volume, source)
        VALUES (%s, %s, %s, %s, %s);
        """
        # Binance envoie le temps en millisecondes, on divise par 1000
        # On simule le symbole AAPL pour pouvoir comparer sur le même graphique que Alpaca
        # (Dans la vraie vie, on comparerait BTC sur Alpaca vs BTC sur Binance)
        values = (timestamp, 'AAPL', price, 0, 'Binance') 
        
        cursor.execute(sql, values)
        conn.commit()
        print(f"Donnée insérée (Binance) : AAPL (Simulé) - Prix: {price}")
        conn.close()
    except Exception as e:
        print(f"Erreur BDD : {e}")

async def listen_binance():
    print(f"Connexion au flux Binance : {BINANCE_WS_URL}")
    async with websockets.connect(BINANCE_WS_URL) as websocket:
        while True:
            message = await websocket.recv()
            data = json.loads(message)
            
            # Extraction des données du JSON de Binance
            price = float(data['p']) # 'p' = price
            event_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data['E']/1000))
            
            # Pour l'exercice, comme Alpaca nous envoie du Apple (~220$), 
            # et que le Bitcoin est à ~95000$, on va diviser le prix du Bitcoin 
            # pour qu'il ressemble à celui d'Apple sur le graphique !
            # Sinon le graphique sera illisible.
            simulated_price = price / 430 # Ratio approximatif BTC/AAPL
            
            insert_data(simulated_price, event_time)

if __name__ == "__main__":
    # Attente que la BDD soit prête
    time.sleep(10)
    while True:
        try:
            asyncio.run(listen_binance())
        except Exception as e:
            print(f"Erreur connexion Binance: {e}")
            time.sleep(5)