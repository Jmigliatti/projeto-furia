FROM python:3.9-slim

# Apenas instale dependências
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD ["sh", "-c", "python -u serve_webapp.py"]