import datetime
from .message import Message


def handle_ping(msg):
    sent = datetime.datetime.strptime(msg.data["sent"], "%Y-%m-%d %H:%M:%S.%f")
    latency = datetime.datetime.utcnow() - sent
    resp = Message("PING_RESP")
    resp.data["latency"] = latency.total_seconds() * 1000

    return resp


def handle_error(msg):
    print("Client reported error: {0}".format(msg.get_error()))
    return Message.ok()