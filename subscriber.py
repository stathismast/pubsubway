import socket
from time import sleep
from sys import argv

SERVER_IP = "127.0.0.1"
SERVER_PORT = 9000
CLIENT_IP = "127.0.0.1"
CLIENT_PORT = 9001
EOT_CHAR = b"\4"
ID = "s1"

def log(message):
  print(f"[Sub {ID}] " + message);

def send_message(message):
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Setup socket and connect
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((CLIENT_IP, CLIENT_PORT))
    connected = False
    while not connected:
      try:
        s.connect((SERVER_IP, SERVER_PORT))
        connected = True
      except:
        log("Error on connection. Retrying in 30 seconds...")
        sleep(30)

    # Send message
    message = bytes(message, 'UTF-8')
    s.sendall(message + EOT_CHAR)

    # Wait for OK response
    return s.recv(1024).decode()

def subscribe(topic):
  log(f"Subscribing to topic \"{topic}\"")
  response = send_message(ID + " sub " + topic)
  log(f"Received {response}")

def unsubscribe(topic):
  log(f"Unsubscribing from topic \"{topic}\"")
  response = send_message(ID + " unsub " + topic)
  log(f"Received {response}")

def check_command(command):
  return not command[0].isdigit() or int(command[0]) < 0 or len(command) != 3 or (command[1] != "sub" and command[1] != "unsub")

def handle_command(command):
  topic = command[2]
  if(int(command[0]) > 0):
    log(f"Waiting {command[0]} second(s)...")
    sleep(int(command[0]))
  subscribe(topic) if command[1] == "sub" else unsubscribe(topic)

# Handle single command file
filename = None
if len(argv) > 1:
  filename = argv[1]

if filename:
  command_file = open(filename, "r").readlines()
  for command in command_file:
    command = command.replace("\n", "")
    log(f"Running command from file: \"{command}\"")
    command = command.split(" ")
    handle_command(command)

while True:
  log("Enter command:")
  command = input().split(" ")
  while check_command(command):
    log("Invalid command")
    log("Use: <wait time> <sub/unsub> <topic>")
    command = input().split(" ")
  handle_command(command)