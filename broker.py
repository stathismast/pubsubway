import socket
import threading
from time import sleep
import sys

HOST = "127.0.0.1"
PUB_PORT = 8000
SUB_PORT = 9000
EOT_CHAR = b"\4"
BUFFER_SIZE = 1024

subscriptions = []

def log(message):
  print("[BROKER] " + message);

def handle_pub_message(data):
  data = data.decode().split()
  data = [data[0], data[1], data[2], ' '.join(data[3:])]
  pub_id = data[0]
  topic = data[2]
  message = data[3]
  log(f"Publisher {pub_id} sent message \"{message}\" to topic \"{topic}\"")

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
            break
        # Send OK response
        conn.sendall(b"OK")
      handle_pub_message(data)

def subscribe(id, topic, ip, port):
  sub_obj = { "id": id, "topic": topic, "ip": ip, "port": port }
  if sub_obj not in subscriptions:
    subscriptions.append(sub_obj)

def unsubscribe(id, topic):
  global subscriptions
  subscriptions = [s for s in subscriptions if s["id"] != id or s["topic"] != topic]

def handle_sub_message(data, addr):
  data = data.decode().split()
  sub_id = data[0]
  action = data[1]
  topic = data[2]
  logging_output = "subscribed to" if action == "sub" else "unsubscribed from"
  log(f"Subscriber {sub_id} {logging_output} topic \"{topic}\"")
  if action == "sub":
    subscribe(sub_id, topic, addr[0], addr[1])
  else:
    unsubscribe(sub_id, topic)
  log(str(subscriptions))

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
            break
        # Send OK response
        conn.sendall(b"OK")
      handle_sub_message(data, addr)


log("Broker process started")
try:
  threading.Thread(target=pubthread).start()
  threading.Thread(target=subthread).start()
except KeyboardInterrupt:
  sys.exit(0)