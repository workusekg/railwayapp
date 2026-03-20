# 1. Use a much smaller base image
FROM python:3.11-slim-bookworm

# 2. Install only essential system tools (removed heavy extras)
RUN apt-get update && apt-get install -y \
    curl \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# 3. Install Ollama (this is only ~150MB)
RUN curl -L https://ollama.com/download/ollama-linux-amd64 -o /usr/bin/ollama \
    && chmod +x /usr/bin/ollama

WORKDIR /app

# 4. Install Python dependencies first (leverages caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy your app code last
COPY . .

# 6. THE FIX: Pull the model at RUNTIME, not BUILD time.
# This keeps the image size at ~800MB instead of 8GB.
ENTRYPOINT ["/bin/sh", "-c", "ollama serve & sleep 5 && ollama pull llama3.2:1b && streamlit run app.py --server.port=$PORT --server.address=0.0.0.0"]
