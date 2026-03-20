# Use a lightweight Python image
FROM python:3.11-slim

# Install system dependencies for OCR and PDF parsing
RUN apt-get update && apt-get install -y \
    curl \
    libgl1 \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama (AI Engine)
RUN curl -L https://ollama.com/download/ollama-linux-amd64 -o /usr/bin/ollama \
    && chmod +x /usr/bin/ollama

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

# Start Ollama in background, pull model, then start Streamlit
ENTRYPOINT ["/bin/sh", "-c", "ollama serve & sleep 5 && ollama pull llama3.2:1b && streamlit run app.py --server.port=$PORT"]