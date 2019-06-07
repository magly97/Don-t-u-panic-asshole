

class Packet:

    data = []

    def __init__(self, request_type, data, key):
        self.type = request_type
        self.data = data
        self.auth_key = key

