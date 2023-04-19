FROM python:3

ENV BIND_IP=0.0.0.0
ENV BIND_PORT=8080
ENV DEST_IP=10.0.0.2
ENV DEST_PORT=80

COPY app.py /app/

CMD ["python3", "/app/app.py"]
