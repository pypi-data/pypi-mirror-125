import socket
import time
from struct import pack

HOST = '35.235.69.154'
PORT = 61135


def request(op: str, value: str = None) -> None:
    """Sends a TCP request to the server with a packet containing the desired operation and value to be added

    Args:
        op (str): The operation that should be sent to the server to perform
        value (str): The value (if any) that should be sent to the server to use
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        data = bytes(str((op, value)), encoding='utf8')
        size = pack('>Q', len(data))
        s.sendall(size)
        s.sendall(data)
        data = s.recv(1024).decode('utf8')

    print(data)
    time.sleep(0.5)
    print('\n\n')

