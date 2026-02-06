import socket
import json

class SocketHelper():
    def __init__(self, host = "127.0.0.1", port = 1031, buffer_size = 1024):
        self.host = host
        self.port = port
        self.buffer_size = buffer_size

        self.socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
        self.socket.connect((self.host , self.port))
        
    def sendMessage(self, msg):
        print ("Sending message: " + msg)
        self.socket.send(msg.encode('utf8'))

    def getMessage(self):
        try:
            msg = self.socket.recv(self.buffer_size).decode('utf-8')
            jsonMsg = json.loads(msg)
            return jsonMsg
        except e:
            print(e)
            pass