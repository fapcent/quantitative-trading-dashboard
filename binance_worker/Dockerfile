FROM python:3.9-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app
# Installation des librairies nécessaires
RUN pip install mysql-connector-python websockets asyncio
COPY . .
CMD ["python", "worker_binance.py"]