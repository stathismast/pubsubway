import socket
from time import sleep

SERVER_IP = "127.0.0.1"
SERVER_PORT = 8000
CLIENT_IP = "127.0.0.1"
CLIENT_PORT = 8001
EOT_CHAR = b"\4"
ID = "p1"

def log(message):
  print(f"[Pub {ID}] " + message);

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

def publish(topic, message):
  log(f"Sending message \"{message}\" to topic \"{topic}\"")
  response = send_message(ID + " pub " + topic + " " + message)
  log(f"Received {response.decode()}")

def check_command(command):
  return not command[0].isdigit() or int(command[0]) < 0 or len(command) < 4 or command[1] != "pub"

def handle_command(command):
  command = [command[0], command[1], command[2], ' '.join(command[3:])]
  topic = command[2]
  message = ' '.join(command[3:])
  if(int(command[0]) > 0):
    log(f"Waiting {command[0]} second(s)...")
    sleep(int(command[0]))
  publish(topic, message)

while True:
  log("Enter command:")
  command = input().split(" ")
  while check_command(command):
    log("Invalid command")
    log("Use: <wait time> pub <topic> <message>")
    command = input().split(" ")
  handle_command(command)