FROM python:3.9-slim

# Installation des dépendances système pour Scapy
RUN apt-get update && apt-get install -y \
    libpcap-dev \
    tcpdump \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# On force la sortie console immédiate
ENV PYTHONUNBUFFERED=1

CMD ["python", "sniffer.py"]