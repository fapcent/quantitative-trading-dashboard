# --- Étape 1 : Le "Builder" ---
# On utilise une image Node 18 pour CONSTRUIRE notre application
FROM node:20-alpine AS builder

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances
COPY package*.json ./

# Installer les dépendances
RUN npm install

# Copier tout le code source
COPY . .

# Construire l'application (crée un dossier 'dist' optimisé)
RUN npm run build

# --- Étape 2 : Le "Serveur" ---
# On utilise une image Nginx (serveur web léger) pour SERVIR nos fichiers
FROM nginx:1.25-alpine

# Copier les fichiers construits depuis l'étape "builder"
# On copie le contenu du dossier 'dist' du builder...
# ...dans le dossier que Nginx utilise pour servir des sites web
COPY --from=builder /app/dist /usr/share/nginx/html

# Exposer le port 80 (port web par défaut)
EXPOSE 80

# La commande de Nginx démarre automatiquement, pas besoin de CMD