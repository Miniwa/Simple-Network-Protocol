import datetime


class Message:
    def __init__(self, message_id):
        self.id = message_id
        self.data = {}

    @staticmethod
    def ok():
        return Message("OK")

    @staticmethod
    def error(desc):
        msg = Message("ERROR")
        msg.data["error_desc"] = desc

        return msg

    @staticmethod
    def ping():
        return Message("PING")

    @staticmethod
    def signature():
        return Message("GET_SIGNATURE")

    def is_ok(self):
        return self.id == "OK"

    def is_error(self):
        return self.id == "ERROR"

    def get_error(self):
        if not self.is_error():
            raise ValueError("Message is not an error.")

        return self.data["error_desc"]
