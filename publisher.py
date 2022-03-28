import socket

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5000
CLIENT_IP = "127.0.0.1"
CLIENT_PORT = 5001
EOT_CHAR = b"\4"
ID = "p1"

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

def publish(topic, message):
  log(f"Sending message \"{message}\" to topic \"{topic}\"")
  response = send_message(ID + " pub " + topic + " " + message)
  log(f"Received {response.decode()}")

publish("#hello", "This is the first message")
while True:
  log("Enter command:")
  command = input().split(" ")
  while len(command) < 4:
    log("Invalid command, too few arguments.")
    log("Use: <wait time> pub <topic> <message>")
    command = input().split(" ")
  command = [command[0], command[1], command[2], ' '.join(command[3:])]
  topic = command[2]
  message = ' '.join(command[3:])
  publish(topic, message)