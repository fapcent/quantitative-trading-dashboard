# 1. Image de base
# On part d'une image Python 3.11 légère
FROM python:3.11-slim

# 2. Définir le répertoire de travail
# C'est là que notre code vivra à l'intérieur du conteneur
WORKDIR /app

# 3. Copier le fichier des dépendances
# On copie SEULEMENT ce fichier d'abord, pour profiter du cache Docker
COPY requirements.txt .

# 4. Installer les dépendances
# Installe tout ce qui est listé dans requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copier le reste du code
# Copie worker.py (ou worker1.py) dans /app
COPY . .

# 6. Commande de lancement
# C'est ce qui s'exécute quand le conteneur démarre
# (remplacez worker.py par worker1.py si c'est le nom que vous utilisez)
CMD ["python", "worker.py"]