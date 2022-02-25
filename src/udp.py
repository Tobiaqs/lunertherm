import socket, requests
from os import environ

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 5190))

while True:
    data, addr = sock.recvfrom(1024)
    data = data.decode('utf-8')

    requests.post('http://web:5000/new_state/' + environ['COMM_TOKEN'], data=data)
