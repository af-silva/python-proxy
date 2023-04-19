import json
import socket

with open('/app/config.json') as f:
    config = json.load(f)

bind_ip = config['bind_ip']
bind_port = config['bind_port']
dest_ip = config['dest_ip']
dest_port = config['dest_port']

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)

print(f'[*] Listening on {bind_ip}:{bind_port}')

while True:
    client_socket, addr = server.accept()

    print(f'[*] Accepted connection from {addr[0]}:{addr[1]}')

    destination_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    destination_socket.connect((dest_ip, dest_port))

    while True:
        data = client_socket.recv(4096)
        if not data:
            break
        destination_socket.send(data)
        print(f'[+] Sent {len(data)} bytes to {dest_ip}:{dest_port}')

    destination_socket.close()
    client_socket.close()
