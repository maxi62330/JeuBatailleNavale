from engine import Engine

class Client:

    def __init__(self):
        import socket


        hote = input("Server Name (localhost):") or "localhost"
        port = int(input("PORT Server (15555): ") or "15555")

        self.mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mySocket.connect((hote, port))
        print("Connection on {} with port {}".format(hote , port))

        # On attend l'initialisation du coté server -> "OK"
        listen = True
        while listen:
            print("Attente d'initialisation avec le serveur")
            response = self.mySocket.recv(255)
            print(response.decode)
            if response.decode() == "OK":
                print("Initialisation avec le serveur établi")
                listen = False

        Engine.play(self, "CLIENT", True, self)


        print("Close")
        self.mySocket.close()

    def sendDataOnFlux(self, message):
        self.mySocket.send(message.encode())

    def listenFlux(self):
        return self.mySocket.recv(255).decode()
