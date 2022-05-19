import socket

class Player:
    def __init__(self):
        self.ID = 0
        self.pos = [0, 0, 0]
        self.connection = None

    def connect_to_server(self, server_addr, server_port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((server_addr, server_port))

    def connect_to_client(self, client_sock):
        self.connection = client_sock

    def fileno(self):
        return self.connection.fileno()
