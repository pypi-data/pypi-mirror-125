import socket


HOST = '34.94.55.153'
PORT = 61135


def request(op, value=None):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(bytes(str((op, value)), encoding='utf8'))
        data = s.recv(1024).decode('utf8')

    print(data)

