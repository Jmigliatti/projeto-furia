FROM python:3.9-slim

WORKDIR /app

# Instalar wait-for-it
RUN apt-get update && apt-get install -y wget && \
    wget -O /wait-for-it.sh https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh && \
    chmod +x /wait-for-it.sh && \
    apt-get remove -y wget && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Usar a variável de ambiente MYSQL_HOST no wait-for-it
CMD ["/wait-for-it.sh", "--timeout=30", "--strict", "$(MYSQL_HOST):3306", "--", "python", "serve_webapp.py"]

EXPOSE 8080
