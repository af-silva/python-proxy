import os
import socket
import logging
import sys

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

bind_ip = os.environ['BIND_IP']
bind_port = int(os.environ['BIND_PORT'])
dest_ip = os.environ['DEST_IP']
dest_port = int(os.environ['DEST_PORT'])

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)

logger.info(f'[*] Listening on {bind_ip}:{bind_port}')

while True:
    client_socket, addr = server.accept()

    logger.info(f'[*] Accepted connection from {addr[0]}:{addr[1]}')

    destination_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    destination_socket.connect((dest_ip, dest_port))

    while True:
        data = client_socket.recv(4096)
        if not data:
            break
        destination_socket.send(data)
        logger.info(f'[+] Sent {len(data)} bytes to {dest_ip}:{dest_port}')

    destination_socket.close()
    client_socket.close()
