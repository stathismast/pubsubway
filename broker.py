import socket

HOST = "127.0.0.1"
PUB_PORT = 5000
EOT_CHAR = b"\4"
BUFFER_SIZE = 1024

def log(message):
  print("[BROKER] " +  message);

log("Broker process started")
log(f"Publisher port {PUB_PORT}")

while True:
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Setup socket and listen for connections
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PUB_PORT))
    s.listen()

    # Accept connections
    conn, addr = s.accept()
    data = b""
    with conn:
      log(f"Publisher connected from {addr[0]}:{addr[1]}")
      # Loop through connections until we get the EOT_CHAR (end-of-transmission)
      while True:
        data += conn.recv(BUFFER_SIZE)
        if data[-1] == b'\4'[0]:
          data = data[:-1]
          log(f"{addr[0]}:{addr[1]} sent: {data.decode()}")
          break
      # Send OK response
      conn.sendall(b"OK")