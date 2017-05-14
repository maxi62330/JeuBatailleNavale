from engine import Engine

class Client:

    def __init__(self):
        import socket

        # configuration dev
        hote = "localhost"
        port = 15556

        self.mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mySocket.connect((hote, port))
        print("Connection on {}".format(port))

        # On attend l'initialisation du coté server -> "OK"
        listen = True
        while listen:
            print("Attente d'initialisation avec le serveur")
            response = self.mySocket.recv(255)
            print(response.decode)
            if response.decode() == "OK":
                print("Initialisation avec le serveur établi")
                listen = False

        #while True:
            # TODO : While != G
        Engine.play(self, "CLIENT", True, self)


        print("Close")
        #self.mySocket.close()

    def sendDataOnFlux(self, message):
        self.mySocket.send(message.encode())

    def listenFlux(self):
        return self.mySocket.recv(255).decode()
