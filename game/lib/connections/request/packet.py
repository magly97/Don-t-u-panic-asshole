

class Packet:

    data = []

    def __init__(self, type, data, key):
        self.type = type
        self.data = data
        self.authKey = key

