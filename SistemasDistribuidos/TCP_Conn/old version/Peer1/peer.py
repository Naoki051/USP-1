class Peer:
    def __init__(self, ip, port, clock=0):
        self.ip = ip
        self.port = port
        self.clock = clock
        self.lista_vizinhos = []
