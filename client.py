import socket
from .message import Message
from .formatter import Formatter, JSONFormatter
from .session import Session


class Client():
    def __init__(self):
        self.formatter = JSONFormatter()
        self.session = None
        self.is_connected = False

    def set_formatter(self, formatter):
        if not isinstance(formatter, Formatter):
            raise TypeError("Object of type Formatter is required.")

        self.formatter = formatter

    def connect(self, address, port):
        if self.is_connected:
            raise ValueError("Client is already connected.")

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(20)
        sock.connect((address, port))

        self.session = Session(sock)
        self.is_connected = True

    def close(self):
        if not self.is_connected:
            raise ValueError("Client is not connected.")

        self.session.shutdown()
        self.session.close()
        self.is_connected = False

    def send_message(self, msg):
        if not self.is_connected:
            raise ValueError("Client is not connected.")

        self.session.send_message(msg, self.formatter)

    def recv_message(self):
        if not self.is_connected:
            raise ValueError("Client is not connected.")

        return self.session.recv_message(self.formatter)

    def send(self, msg):
        self.send_message(msg)

        return self.recv_message()

    def ping(self):
        return self.send(Message.ping())

    def signature(self):
        return self.send(Message.signature())