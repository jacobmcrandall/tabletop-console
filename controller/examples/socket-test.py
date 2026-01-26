import socket
import time

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 1031  # Port to listen on (non-privileged ports are > 1023)

# Server code
# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.bind((HOST, PORT))
#     s.listen()
#     conn, addr = s.accept()
#     with conn:
#         print(f"Connected by {addr}")
#         while True:
#             data = conn.recv(1031)
#             if not data:
#                 break
#             conn.sendall(data)

# Client code
# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientsocket:
#     clientsocket.connect((HOST, PORT))
#     i = 0
#     while True:
#         time.sleep(2) # waits 2 seconds
#         i = i+1
#         clientsocket.send(str(i))

tcp1 = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
tcp_ip = "127.0.0.1"
port = 1031
buffer_size = 1024
msg = ("Client test.")

tcp1.connect((tcp_ip , port))
print ("Sending message: " + msg)
tcp1.send(msg.encode('utf8'))

data = tcp1.recv(buffer_size).decode('utf-8')

print ("Data reveived: " +  data)