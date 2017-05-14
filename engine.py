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
                    if lineContent[x] != "00":
                        board.grid[y][x].name = lineContent[x]
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

    def printBoard(myBoard, foeBoard):
        alpha = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J",]
        print("  Grille Joueur                                     Grille Adversaire")
        print("  1  2  3  4  5  6  7  8  9 10                      1 2 3 4 5 6 7 8 9 10")

        for x in range(10):
            line = alpha[x]
            for y in range(10):
                if myBoard.grid[x][y].name != "-" :
                    if myBoard.grid[x][y].state != "-":
                        line = line + " XX"
                    else:
                        line = line + " " + myBoard.grid[x][y].name
                else:
                    line = line + " " + myBoard.grid[x][y].state + " "



            line = line + "                   " + alpha[x]
            for y in range(10):
                line = line + " " + foeBoard.grid[x][y].state
            print(line)

    def play(self, name, iAmClient, parent):
        print("I am {}, and {}", name, iAmClient)
        listBoardDestroy = []
        myGrid = Board()
        foeGrid = Board()

        Engine.fillBoard(self,"bateauPosition.txt" , myGrid)

        myTurn = iAmClient
        currentGame = True
        while currentGame:

            if(myTurn):
                # Si c'est à mon tour de jouer
                coordinates = Engine.enterCoordinates(Engine)
                parent.sendDataOnFlux(coordinates)

                print("Je bombarde l'adversaire : " + coordinates)

                myTurn = False

                responseBombardement = parent.listenFlux()
                print(" Réponse de l'adversaire sur mon bombardement en '" + coordinates + "' :" + responseBombardement)

                if len(responseBombardement) == 1: # Contrôle de surface
                    # Si l'instruction est 1 caractère alors c'est une réponse à un jeu
                    if(responseBombardement == "T" or responseBombardement == "C"):
                        # Si j'ai toucher ou couler l'adversaire alors je rejoue
                        myTurn = True
                    else:
                        myTurn = False

                    # On modifie la grille de l'adversaire
                    foeGrid.grid[Engine.format_x(coordinates[0])][Engine.format_y(coordinates[1:])].state = responseBombardement

                    if responseBombardement == "G":
                        print("Félicitation, Vous avez gagné")
                        currentGame = False;
                        break

            else:
                # c'est au tour de l'adversaire
                coordinatesBombardement = parent.listenFlux()
                print("Bombardement reçu de l'adversaire : " + coordinatesBombardement)

                if (0 <= Engine.format_x(coordinatesBombardement[0]) < 11) and (0 < int(coordinatesBombardement[1:]) < 11):

                    resultBombard = Engine.traitmentBombard(Engine, myGrid, coordinatesBombardement, listBoardDestroy)

                    parent.sendDataOnFlux(resultBombard)
                    print("L'adversaire m'a " + resultBombard)
                    myGrid.grid[Engine.format_x(coordinatesBombardement[0])][Engine.format_y(coordinatesBombardement[1:])].state = resultBombard
                    if resultBombard == "R": # Si l'adversaire m'a raté alors c'est à mon tour
                        myTurn = True
                    elif resultBombard == "G":
                        print("L'adversaire a gagné")
                        currentGame = False;
                        break

                else:
                    parent.sendDataOnFlux("E")
                    print("L'adversaire nous à envoyé de mauvaise coordonnée: {}", Engine.format_x(coordinatesBombardement))



            Engine.printBoard(myGrid, foeGrid)
            print("Attente de réponse")

    def traitmentBombard(self, myGrid, coordinates, listBoardDestroy):
        # On récupère la cellule qui à été bombarder
        cell = myGrid.grid[Engine.format_x(coordinates[0])][Engine.format_y(coordinates[1:])]

        resultBombard = "R" # Par défaut le bombardement à ratée

        # On regarde si on à été touché
        if(cell.name != "-"):
            cell.state = "T"
        else:
            cell.state = "R"

        if(Engine.verifyBoardIsNotDied(Engine,myGrid,cell.name)):
            cell.state = "C"
            if listBoardDestroy.count(cell.name) != 1:
                listBoardDestroy.append(cell.name)

            if len(listBoardDestroy) == 6:
                cell.state = "G"

        return cell.state


    def countBoardTouchWithSameName(self, myGrid, name):
        countNbBoard = 0

        for x in range(10):
            for y in range(10):
                if myGrid.grid[x][y].name == name:
                    if myGrid.grid[x][y].state == "T":
                        countNbBoard += 1

        return countNbBoard

    def verifyBoardIsNotDied(self, myGrid, nameBoard):

        # Récuperer le nombre de case toucher que possède le bateau
        NbTouchOnMyBoard = Engine.countBoardTouchWithSameName(self, myGrid, nameBoard)


        if (NbTouchOnMyBoard == 4 and nameBoard[0] == "P") or (NbTouchOnMyBoard == 3 and nameBoard[0] == "C") or (
                        NbTouchOnMyBoard == 2 and nameBoard[0] == "S"):

            # Mon bateau est coulé
            return True
        else:
            return False
