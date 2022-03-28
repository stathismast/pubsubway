import socket

HOST = "127.0.0.1"
PORT = 5000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  s.bind((HOST, PORT))
  print(f"[SERVER] Listening on port {PORT}")
  s.listen()
  conn, addr = s.accept()
  data = b""
  with conn:
    print(f"[SERVER] Connected by {addr}")
    while True:
      data += conn.recv(1)
      if data[-1] == b'\4'[0]:
        break
      print(f"[SERVER] {addr[0]}:{addr[1]} sent: {data}")
    conn.sendall(b"OK")