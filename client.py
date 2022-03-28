import socket

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5000
CLIENT_IP = "127.0.0.1"
CLIENT_PORT = 5001
EOT_CHAR = b'\4'

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  s.bind((CLIENT_IP, CLIENT_PORT))
  s.connect((SERVER_IP, SERVER_PORT))
  message = b"Hello, world"
  s.sendall(message + EOT_CHAR)
  data = s.recv(1024)

print(f"[CLIENT] Received {data}")