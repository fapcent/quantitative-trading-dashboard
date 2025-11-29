# 1. Image de base
# On part d'une image Node.js 18 (LTS) légère
FROM node:18-alpine

# 2. Définir le répertoire de travail
WORKDIR /app

# 3. Copier les fichiers de dépendances
# On copie package.json ET package-lock.json (s'il existe)
COPY package*.json ./

# 4. Installer les dépendances
# 'npm ci' est plus rapide et plus fiable pour les déploiements que 'npm install'
RUN npm install

# 5. Copier le reste du code
# Copie server.js dans /app
COPY . .

# 6. Exposer le port
# Informe Docker que le conteneur écoute sur le port 3000
EXPOSE 3000

# 7. Commande de lancement
# C'est ce qui s'exécute quand le conteneur démarre
CMD ["node", "server.js"]