FROM python:3

COPY app.py /app/

CMD ["python3", "/app/app.py"]