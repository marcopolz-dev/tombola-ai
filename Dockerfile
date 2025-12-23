# Ambiente
FROM python:3.11-slim

RUN apt update && apt install -y \
    build-essential \
    curl \
    jq \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Buffering dei log
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Dipendenze
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Applicazione
COPY app/ .

# Mantiene il container in esecuzione
CMD ["tail", "-f", "/dev/null"]
