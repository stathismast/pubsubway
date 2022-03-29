import socket
import threading
import sys

HOST = "127.0.0.1"
PUB_PORT = 8000
SUB_PORT = 9000
EOT_CHAR = b"\4"
BUFFER_SIZE = 1024

def log(message):
  print("[BROKER] " + message);

def pubthread():
  log(f"Publisher thread is up at port {PUB_PORT}")

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
          if data[-1] == EOT_CHAR[0]:
            data = data[:-1]
            log(f"{addr[0]}:{addr[1]} sent: {data.decode()}")
            break
        # Send OK response
        conn.sendall(b"OK")

def subthread():
  log(f"Subscriber thread is up at port {SUB_PORT}")

  while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      # Setup socket and listen for connections
      s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      s.bind((HOST, SUB_PORT))
      s.listen()

      # Accept connections
      conn, addr = s.accept()
      data = b""
      with conn:
        log(f"Publisher connected from {addr[0]}:{addr[1]}")
        # Loop through connections until we get the EOT_CHAR (end-of-transmission)
        while True:
          data += conn.recv(BUFFER_SIZE)
          if data[-1] == EOT_CHAR[0]:
            data = data[:-1]
            log(f"{addr[0]}:{addr[1]} sent: {data.decode()}")
            break
        # Send OK response
        conn.sendall(b"OK")


log("Broker process started")
try:
  threading.Thread(target=pubthread).start()
  threading.Thread(target=subthread).start()
except KeyboardInterrupt:
  sys.exit(0)