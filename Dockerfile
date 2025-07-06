FROM python:3.11-slim

# Instala dependências do Chromium
RUN apt-get update && apt-get install -y \
    wget gnupg curl ca-certificates fonts-liberation \
    libappindicator3-1 libasound2 libatk-bridge2.0-0 libatk1.0-0 libcups2 \
    libdbus-1-3 libgdk-pixbuf2.0-0 libnspr4 libnss3 libxcomposite1 \
    libxdamage1 libxrandr2 xdg-utils libu2f-udev libvulkan1 libxss1 \
    libxtst6 libgbm-dev && apt-get clean

# Instala dependências do projeto
WORKDIR /app
COPY . /app
RUN python -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

ENV PATH="/opt/venv/bin:$PATH"

# Expõe a porta usada pelo Flask
EXPOSE 5000

# Comando de inicialização
CMD ["python", "main.py"]
RUN playwright install chromium
