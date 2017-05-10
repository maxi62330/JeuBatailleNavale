from engine import Engine

class Server:
    def __init__(self):
        import socket
        # port = input("PORT Server : ")
        port = 15556

        socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.bind(('', port))
        socket.listen(5)

        self.client = None

        print("Server started")
        while True:
            if self.client is None:
                self.client, address = socket.accept()
                print("{} connected".format(address))
                #self.client.send(b"OK")
                self.sendDataOnFlux("OK")
            else:
                self #Engine.play(self, "SERVEUR", False, Server)

        client.close()

        print("Close")
        socket.close()

    def sendDataOnFlux(self, message):
        self.client.send(message.encode())

    def listenFlux(self):
        return self.mySocket.recv(255).decode()



