import socket
import threading
from time import sleep
from sys import exit, argv

host = "127.0.0.1"
pub_port = None      # port that listens for messages from publishers
sub_port = None      # port that listens for messages from subscribers
port_offset = 1 # offset for port sends messages to subscribers
verbose = False

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
  sub_count = 0
  for sub in subscriptions:
    if sub['topic'] == topic:
      sub_count += 1
      if verbose: log(f"Sending message \"{message}\" to {sub['id']} @ {sub['ip']}:{sub['port']}")
      send_message(message, sub['ip'], sub['port'])
  log(f"{pub_id} published to {topic} ({sub_count} subs): {message}")

def send_message(message, ip, port):
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Setup socket and connect
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, sub_port + port_offset))
    connected = False
    while not connected:
      try:
        s.connect((ip, port + port_offset))
        connected = True
      except:
        log("Error on connection. Retrying in 30 seconds...")
        sleep(30)

    # Send message
    message = bytes(message, 'UTF-8')
    s.sendall(message + EOT_CHAR)

    # Wait for OK response
    # return s.recv(BUFFER_SIZE).decode()

def pubthread():
  log(f"Publisher thread is up at port {pub_port}")

  while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      # Setup socket and listen for connections
      s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      s.bind((host, pub_port))
      s.listen()

      # Accept connections
      conn, addr = s.accept()
      data = b""
      with conn:
        if verbose: log(f"Publisher connected from {addr[0]}:{addr[1]}")
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
  log(f"{sub_id} {logging_output} {topic}")
  if action == "sub":
    subscribe(sub_id, topic, addr[0], addr[1])
  else:
    unsubscribe(sub_id, topic)
  if verbose: log("Current subs: " + str(subscriptions))

def subthread():
  log(f"Subscriber thread is up at port {sub_port}")

  while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      # Setup socket and listen for connections
      s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      s.bind((host, sub_port))
      s.listen()

      # Accept connections
      conn, addr = s.accept()
      data = b""
      with conn:
        if verbose: log(f"Subscriber connected from {addr[0]}:{addr[1]}")
        # Loop through connections until we get the EOT_CHAR (end-of-transmission)
        while True:
          data += conn.recv(BUFFER_SIZE)
          if data[-1] == EOT_CHAR[0]:
            data = data[:-1]
            break
        # Send OK response
        conn.sendall(b"OK")
      handle_sub_message(data, addr)

def handle_option_sub_port(arguments, i):
  global sub_port
  try:
    sub_port = int(arguments[i+1])
  except: 
    print("Invalid port number")
    return -1

def handle_option_pub_port(arguments, i):
  global pub_port
  try:
    pub_port = int(arguments[i+1])
  except: 
    print("Invalid port number")
    return -1

def handle_option_port_offset(arguments, i):
  global port_offset
  try:
    port_offset = int(arguments[i+1])
  except: 
    print("Invalid port number")
    return -1

def handle_option_verbose(arguments, i):
  global verbose
  verbose = True
  return 1

def handle_command_line_args():
  options = {
    "-s": handle_option_sub_port,
    "-p": handle_option_pub_port,
    "-o": handle_option_port_offset,
    "-v": handle_option_verbose,
  }

  arguments = argv[1:]
  i = 0
  while i < len(arguments):
    if arguments[i] in options.keys():
      try:
        ret_val = options[arguments[i]](arguments, i)
      except:
        print("Invalid input")
        return -1
      if ret_val == -1:
        return -1
      elif ret_val == 1:
        i -= 1
    i += 2

  if not sub_port or not pub_port:
    print("Arguments missing")
    return -1

  return 0

ret_val = handle_command_line_args()
if ret_val != -1:
  log("Broker process started")
  try:
    threading.Thread(target=pubthread).start()
    threading.Thread(target=subthread).start()
  except KeyboardInterrupt:
    exit(0)
else:
  print("Use: python broker.py -s sub_port -p pub_port [-o port_offset -v]")