FROM python:3

COPY app.py /app/
COPY config.json /app/

CMD ["python3", "/app/app.py"]