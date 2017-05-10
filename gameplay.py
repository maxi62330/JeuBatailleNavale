from client import Client
from server import Server


typeApp = input("CLIENT (C) ou SERVEUR (S) : ")


if(typeApp == "C"):
    Client()

else:
    Server()
