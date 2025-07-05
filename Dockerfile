FROM python:3.11-slim

# Instala libs necessárias para o Chromium rodar no Railway
RUN apt-get update && apt-get install -y wget gnupg curl ca-certificates fonts-liberation \
    libappindicator3-1 libasound2 libatk-bridge2.0-0 libatk1.0-0 libcups2 libdbus-1-3 \
    libgdk-pixbuf2.0-0 libnspr4 libnss3 libxcomposite1 libxdamage1 libxrandr2 xdg-utils \
    libu2f-udev libvulkan1 libxss1 libxtst6 libgbm-dev && \
    apt-get clean

# Copia os arquivos da aplicação
WORKDIR /app
COPY . .

# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Instala Chromium para o Playwright
RUN playwright install chromium

# Expõe a porta
EXPOSE 5001

# Comando para iniciar a API
CMD ["python", "main.py"]
