import socket
from time import sleep

SERVER_IP = "127.0.0.1"
SERVER_PORT = 9000
CLIENT_IP = "127.0.0.1"
CLIENT_PORT = 9001
EOT_CHAR = b"\4"
ID = "s1"

def log(message):
  print(f"[{ID}]\t " + message);

def send_message(message):
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Setup socket and connect
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((CLIENT_IP, CLIENT_PORT))
    s.connect((SERVER_IP, SERVER_PORT))

    # Send message
    message = bytes(message, 'UTF-8')
    s.sendall(message + EOT_CHAR)

    # Wait for OK response
    return s.recv(1024)

def subscribe(topic):
  log(f"Subscribing to topic \"{topic}\"")
  response = send_message(ID + " sub " + topic)
  log(f"Received {response.decode()}")

def unsubscribe(topic):
  log(f"Unsubscribing from topic \"{topic}\"")
  response = send_message(ID + " unsub " + topic)
  log(f"Received {response.decode()}")

def checkCommand(command):
  return not command[0].isdigit() or int(command[0]) < 0 or len(command) != 3 or (command[1] != "sub" and command[1] != "unsub")

def handleCommand(command):
  topic = command[2]
  if(int(command[0]) > 0):
    log(f"Waiting {command[0]} second(s)...")
    sleep(int(command[0]))
  subscribe(topic) if command[1] == "sub" else unsubscribe(topic)

while True:
  log("Enter command:")
  command = input().split(" ")
  while checkCommand(command):
    log("Invalid command")
    log("Use: <wait time> <sub/unsub> <topic>")
    command = input().split(" ")
  handleCommand(command)