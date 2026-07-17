# Usa l'immagine ufficiale Python slim per un container leggero
FROM python:3.10-slim

# Installa git per permettere la clonazione del repository
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Imposta la directory di lavoro
WORKDIR /app

# Copia i requisiti e installa le dipendenze
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia il resto dei file (strumenti, app, dati aziendali)
COPY . .

# Esponi la porta 8000 per FastAPI
EXPOSE 8000

# Avvia l'applicazione FastAPI con Uvicorn
CMD ["uvicorn", "progetto_agentic_ai:app", "--host", "0.0.0.0", "--port", "8000"]
