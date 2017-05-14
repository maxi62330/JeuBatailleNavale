from engine import Engine

class Server:
    def __init__(self):
        import socket
        # port = input("PORT Server : ")
        port = 15556

        self.mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mySocket.bind(('', port))
        self.mySocket.listen(5)

        self.client = None

        print("Server started")
        while self.client is None:
            self.client, address = self.mySocket.accept()
            print("{} connected".format(address))
            self.sendDataOnFlux("OK")

        Engine.play(self, "SERVEUR", False, self)

        self.client.close()
        print("Close")

    def sendDataOnFlux(self, message):
        self.client.send(message.encode())

    def listenFlux(self):
        return self.client.recv(255).decode()
