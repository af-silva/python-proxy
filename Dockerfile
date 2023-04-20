FROM python:3-alpine

COPY config.env .env

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "-m", "dotenv", "-f", ".env", "app.py"]
