import datetime
from .message import Message


def handle_ping(msg):
    return Message.ok()


def handle_error(msg):
    print("Client reported error: {0}".format(msg.get_error()))
    return Message.ok()