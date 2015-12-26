import socket, struct

class Session:
    def __init__(self, sock):
        self.socket = sock
        self.state_data = {}

        self.socket.settimeout(20)

    def send_raw_message(self, raw_data):
        size = len(raw_data)
        prefixed_msg = struct.pack("!I", size) + raw_data

        #Send the size prefixed message.
        self.socket.sendall(prefixed_msg)

    def recv_raw_message(self):
        size = self.recv_bytes(4)
        if size is None:
            #Connection was closed.
            return None

        size = struct.unpack("!I", size)[0]
        raw_data = self.recv_bytes(size)

        return raw_data

    def recv_bytes(self, nr_bytes):
        received = 0
        data = bytes()

        while received != nr_bytes:
            chunk = self.socket.recv(nr_bytes)
            if not chunk:
                return None
            received += len(chunk)
            data += chunk

        return data

    def send_message(self, msg, formatter):
        self.send_raw_message(formatter.serialize_message(msg))

    def recv_message(self, formatter):
        raw_msg = self.recv_raw_message()
        if raw_msg is None:
            return None

        return formatter.deserialize_message(raw_msg)

    def shutdown(self):
        self.socket.shutdown(2)

    def close(self):
        self.socket.close()
