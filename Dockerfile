FROM python:3.11-slim

# Install minimal system requirements
RUN apt-get update && apt-get install -y curl libgl1 && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -L https://ollama.com/download/ollama-linux-amd64 -o /usr/bin/ollama && chmod +x /usr/bin/ollama

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

# Use Shell form for ENTRYPOINT to ensure $PORT is expanded
ENTRYPOINT ["/bin/sh", "-c", "ollama serve & sleep 5 && ollama pull llama3.2:1b && streamlit run app.py --server.port=$PORT --server.address=0.0.0.0"]
