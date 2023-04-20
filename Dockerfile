FROM python:3-alpine

WORKDIR /app

COPY requirements.txt .
COPY app.py .

COPY config.env ./.env

# Set environment variables
ENV BIND_IP=0.0.0.0 \
    BIND_PORT=8080 \
    DEST_IP=10.0.0.2 \
    DEST_PORT=80
    
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]