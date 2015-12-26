import socket
from concurrent.futures import ThreadPoolExecutor
from .session import Session
from .formatter import Formatter, JSONFormatter
from .message import Message
from .handlers import handle_ping, handle_error

class Server:
    def __init__(self):
        self.formatter = JSONFormatter()
        self.th_executor = ThreadPoolExecutor(max_workers=50)
        self.handlers = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #Register default handlers.
        self.register_handler("PING", handle_ping)
        self.register_handler("ERROR", handle_error)

    def register_handler(self, message_id, handler_function):
        found = [pair for pair in self.handlers if pair[0] == message_id]
        if found:
            raise KeyError("Duplicate handler already exists.")

        self.handlers.append((message_id, handler_function))

    def unregister_handler(self, message_id):
        found = [pair for pair in self.handlers if pair[0] == message_id]
        if not found:
            raise KeyError("No such handler exists.")

        self.handlers.remove(found[0])


    def set_formatter(self, formatter):
        if not isinstance(formatter, Formatter):
            raise TypeError("An object of type Formatter is required.")

        self.formatter = formatter

    def start(self, port):
        addr = (socket.gethostbyname(socket.gethostname()), port)
        self.server_socket.bind(addr)
        self.server_socket.listen(5)
        print("Server started at: {0}".format(addr))

    def get_handler(self, message_id):
        found = [pair for pair in self.handlers if pair[0] == message_id]
        if found:
            return found[0][1]

        return None

    def get_signature(self):
        resp = Message("GET_SIGNATURE_RESP")

        resp.data["authentication_required"] = False
        resp.data["secure"] = False
        resp.data["format"] = self.formatter.name
        resp.data["methods"] = []

        for pair in self.handlers:
            resp.data["methods"].append(pair[0])

        return resp

    def run(self):
        should_exit = False

        while not should_exit:
            (client_socket, address) = self.server_socket.accept()
            print("New connection from {0}".format(address))

            ses = Session(client_socket)

            #Schedule handling of the session.
            self.th_executor.submit(self.serve_session, ses)

    def serve_session(self, session):
        try:
            while True:
                msg = session.recv_message(self.formatter)
                if msg is None:
                    break

                #Check for special messages.
                if msg.id == "GET_SIGNATURE":
                    resp = self.get_signature()
                else:
                    #Try to find a matching handler.
                    handler = self.get_handler(msg.id)
                    if handler is not None:
                        resp = handler(msg)
                    else:
                        resp = Message.error("Method {0} is not supported by the remote host.".format(msg.id))

                #Send response.
                session.send_message(resp, self.formatter)

            print("Connection closed gracefully.")
        except socket.timeout:
            print("Connection timed out.")
        except OSError:
            print("Connection was forcibly closed.")