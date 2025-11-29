import hvac
import os
import time

# Configuration
VAULT_URL = 'http://vault:8200' # 'vault' est le nom du service Docker
TOKEN = 'root_token_secret'     # Le token défini dans docker-compose

def test_vault_security():
    print("🔒 Connexion au coffre-fort (Vault)...")
    
    try:
        # 1. Authentification
        client = hvac.Client(url=VAULT_URL, token=TOKEN)
        
        if client.is_authenticated():
            print("✅ Authentification réussie !")
        else:
            print("❌ Échec authentification.")
            return

        # 2. Écriture d'un secret (Simulé)
        # Dans la vraie vie, un administrateur ferait ça manuellement au début
        secret_path = 'secret/data/trading_app'
        secret_data = {'api_key': 'MA_SUPER_CLE_SECRETE_CACHEE', 'db_pass': 'fabrice'}
        
        client.secrets.kv.v2.create_or_update_secret(
            path='trading_app',
            secret=secret_data,
        )
        print("✅ Secret stocké dans le coffre avec succès.")

        # 3. Lecture du secret (Ce que ferait le Worker)
        print("🕵️  Tentative de récupération du secret...")
        read_response = client.secrets.kv.v2.read_secret_version(path='trading_app')
        
        recovered_pass = read_response['data']['data']['db_pass']
        
        print(f"🔓 SUCCÈS ! Mot de passe récupéré du coffre : {recovered_pass}")
        print("   (Ce mot de passe n'était pas dans le code de ce script, il vient du réseau)")

    except Exception as e:
        print(f"❌ Erreur Vault : {e}")

if __name__ == "__main__":
    # Petite attente pour être sûr que Vault est démarré
    time.sleep(5)
    test_vault_security()