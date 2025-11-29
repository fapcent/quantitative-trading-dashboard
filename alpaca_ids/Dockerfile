FROM python:3.9-slim

# CORRECTION : Force Python à afficher les logs tout de suite
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "detector.py"]