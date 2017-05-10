from cell import Cell

class Board:
    def __init__(self):
        self.grid = []
        for x in range(10) :
            line = []
            for y in range(10):
                line.append(Cell())
            self.grid.append(line)
