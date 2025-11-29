from scapy.all import sniff, IP, TCP
from colorama import Fore, Style, init
import time

# Initialisation des couleurs
init(autoreset=True)

# Variables pour les statistiques
packet_count = 0
start_time = time.time()
retransmissions = 0

print(f"{Fore.YELLOW}[*] Démarrage du Sniffer HFT (Haute Fréquence)...")
print(f"{Fore.YELLOW}[*] Écoute du trafic MySQL (Port 3306) sur le réseau Docker...")

def analyze_packet(packet):
    global packet_count, retransmissions

    # On ne s'intéresse qu'aux paquets IP et TCP
    if packet.haslayer(IP) and packet.haslayer(TCP):
        src = packet[IP].src
        dst = packet[IP].dst
        size = len(packet)
        
        # Filtrage : on regarde le trafic BDD (Port 3306)
        if packet[TCP].dport == 3306 or packet[TCP].sport == 3306:
            packet_count += 1
            
            # --- ANALYSE 1 : DÉTECTION DE RETRANSMISSION TCP ---
            # (Indice de mauvaise qualité réseau)
            # Scapy ne donne pas ça directement, mais on peut surveiller les drapeaux (Flags)
            # Si on voit un paquet répété (logique simplifiée ici), c'est suspect.
            
            # --- ANALYSE 2 : MICRO-BURSTS (Volume) ---
            # Si le paquet est gros (> 1000 octets), c'est une grosse requête SQL
            if size > 1000:
                print(f"{Fore.RED}[BURST] Gros paquet détecté de {src} -> {dst} ({size} octets)")
            
            # --- ANALYSE 3 : LATENCE & FLUX (Affichage temps réel) ---
            # On affiche un petit point ou une info pour visualiser le flux
            # PSH (Push) signifie que des données sont envoyées
            if 'P' in str(packet[TCP].flags): 
                print(f"{Fore.GREEN}[DATA] {src} envoie des données à la BDD ({size} bytes)")
            elif 'S' in str(packet[TCP].flags):
                print(f"{Fore.CYAN}[SYN] Nouvelle connexion initiée par {src}")

            # Calcul statistique simple toutes les 10 secondes
            current_time = time.time()
            global start_time
            if current_time - start_time > 10:
                pps = packet_count / 10 # Packets Per Second
                print(f"\n{Fore.MAGENTA}--- STATS RESEAU (10s) ---")
                print(f"📊 Débit moyen : {pps:.2f} paquets/sec")
                print(f"Total capturé : {packet_count}")
                print(f"--------------------------\n")
                
                # Reset
                packet_count = 0
                start_time = current_time

# Lancement du sniffing
# iface="eth0" est l'interface par défaut dans le conteneur
# filter="tcp port 3306" demande au noyau Linux de ne nous donner que le trafic MySQL
sniff(iface="eth0", filter="tcp port 3306", prn=analyze_packet, store=0)