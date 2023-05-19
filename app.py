import os
import socket
import logging
import sys
import time

# Configure logging
__version = "1.3"
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Load environment variables
bind_ip = os.environ['BIND_IP']
bind_port = int(os.environ['BIND_PORT'])
dest_ip = os.environ['DEST_IP']
dest_port = int(os.environ['DEST_PORT'])

# Create a socket object for the source endpoint
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
server.bind((bind_ip, bind_port))
server.listen(5)

logger.info(f'[*] Version: {__version}')
logger.info(f'[*] Listening on {bind_ip}:{bind_port}')

while True:
    try:
        client_socket, addr = server.accept()

        logger.info(f'[*] Accepted connection from {addr[0]}:{addr[1]}')

        # Create a socket object for the destination endpoint
        destination_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        destination_socket.settimeout(5)  # set a timeout of 5 seconds for the connect() call

        try:
            destination_socket.connect((dest_ip, dest_port))
        except socket.timeout:
            logger.debug(f'[!] Connection to {dest_ip}:{dest_port} timed out')
            client_socket.close()
            destination_socket.close()
            continue
        except socket.error as err:
            logger.error(f'[!] Error connecting to {dest_ip}:{dest_port}: {err}')
            client_socket.close()
            destination_socket.close()
            time.sleep(1)  # wait for 1 second before trying to accept another connection
            continue

        logger.info(f'[*] Connected to {dest_ip}:{dest_port}')

        while True:
            try:
                data = client_socket.recv(4096)
                if not data:
                    break
                try:
                    destination_socket.sendall(data)
                except socket.error as err:
                    logger.error(f'[!] Error sending data to {dest_ip}:{dest_port}: {err}')
                    break
            except socket.error as err:
                logger.error(f'[!] Error receiving data from {addr[0]}:{addr[1]}: {err}')
                break

            try:
                data = destination_socket.recv(4096)
                if not data:
                    break
                try:
                    client_socket.sendall(data)
                except socket.error as err:
                    logger.error(f'[!] Error sending data to {addr[0]}:{addr[1]}: {err}')
                    break
            except socket.error as err:
                logger.error(f'[!] Error receiving data from {dest_ip}:{dest_port}: {err}')
                break

        destination_socket.close()
        client_socket.close()

    except ConnectionResetError:
        # Clean buffers if connection reset by the peer
        logger.info(f'[*] Connection reset by peer. Cleaning buffers...')
        client_socket.close()
        destination_socket.close()

    except socket.timeout:
        # Handle timeout when client takes too long to exchange data
        logger.info(f'[*] Client took too long to exchange data. Restarting...')
        client_socket.close()
        destination_socket.close()

    except Exception as ex:
        logger.error(f'[!] Unexpected error: {ex}')

    finally:
        server.close()
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((bind_ip, bind_port))
        server.listen(5)
