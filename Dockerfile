FROM python:3.11-slim

# Instala dependências do Chromium
RUN apt-get update && apt-get install -y \
  wget gnupg curl ca-certificates fonts-liberation \
  libgbm-dev libnss3 libatk-bridge2.0-0 libxss1 libasound2 libxcomposite1 \
  libxdamage1 libxrandr2 libx11-xcb1 libgtk-3-0 libx11-dev \
  libxext6 libglib2.0-dev libdbus-1-3 libdrm2 libxtst6 \
  && apt-get clean

# Cria pasta do app
WORKDIR /app

# Copia os arquivos
COPY . /app

# Instala dependências do Python e do projeto
RUN python -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install playwright && \
    playwright install chromium

ENV PATH="/opt/venv/bin:$PATH"

# Expõe a porta
EXPOSE 5000

# Comando de inicialização
CMD ["python", "main.py"]
