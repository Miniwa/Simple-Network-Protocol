import json
from .message import Message


class Formatter:
    name = None

    def serialize_message(self, message):
        try:
            return self.format_message(message)
        except Exception as e:
            raise FormatError(e)

    def deserialize_message(self, byte_str):
        try:
            return self.unformat_message(byte_str)
        except Exception as e:
            raise FormatError(e)

    def format_message(self, message):
        raise NotImplementedError()

    def unformat_message(self, byte_str ):
        raise NotImplementedError()


class JSONFormatter(Formatter):
    name = "json"

    def format_message(self, message):
        obj = {"id": message.id, "data": message.data}
        json_str = json.dumps(obj)

        return json_str.encode("utf-8", "strict")

    def unformat_message(self, byte_str):
        json_str = byte_str.decode("utf-8", "strict")
        obj = json.loads(json_str)

        msg = Message(obj["id"])
        msg.data = obj["data"]

        return msg


class FormatError(Exception):
    pass
