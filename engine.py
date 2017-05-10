from board import Board

class Engine:
    def createBoard(self):
        return Board()

    def fillBoard(self, path, board):
        with open(path, "r") as file:
            y = 0
            for line in file:
                line = line.rstrip('\n')
                lineContent = line.split(':')
                for x in range(10):
                    print(x, y, lineContent[x])
                    if lineContent[x] != "00":
                        board.grille[y][x].name = lineContent[x]
                y += 1

    def modifyStateCell(self, board, x, y, newState):
        board.grid[x][y].state = newState

    def modifyStateSameNameCell(self, board, name , state):
        for x in range(10):
            for y in range(10):
                if board.grid[x][y].name == name:
                    board.grid[x][y].state = state

    def format_y(y):
        return int(y) - 1

    def format_x(x):
        return int(ord(x)) - 65

    def enterCoordinates(self):
        goodFormat = False
        positionBombardement = ""
        while not goodFormat:
            positionBombardement = input("Quel case bombarder ? : ")
            if (0 <= self.format_x(positionBombardement[0]) < 11) and (0 < int(positionBombardement[1:]) < 11):
                goodFormat = True
            else:
                print("Mauvaise coordonnée fournie, format voulu [A-K][1-10], exemple 'A1' 'K3'")

        return positionBombardement

    def printBoard(self, myBoard, foeBoard):
        alpha = ["A", "B", "C", "D", "F", "G", "H", "I", "J", "K"]
        print("  Grille Joueur                                     Grille Adversaire")
        print("  1  2  3  4  5  6  7  8  9 10                      1 2 3 4 5 6 7 8 9 10")

        for x in range(10):
            line = alpha[x]
            for y in range(10):
                if myBoard.grid[x][y].name != "":
                    line = line + " " + myBoard.grid[x][y].name
                else:
                    line = line + " " + myBoard.grid[x][y].state + " "

            line = line + "                   " + alpha[x]
            for y in range(10):
                line = line + " " + foeBoard.grid[x][y].state
            print(line)

    def play(self, name, iAmClient, parent):
        print("I am {}, and {}", name, iAmClient)
        myGrid = Board()
        foeGrid = Board()

        myTurn = iAmClient
        while True:

            if(myTurn):
                # Si c'est à mon tour de jouer
                coordinates = Engine.enterCoordinates()


            else:
                # c'est au tour de l'adversaire
                self

            self.printBoard()
