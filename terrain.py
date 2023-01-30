import copy

class field:
    def __init__(self, t=None):
        self.full = [["." for _ in range(9)] for _ in range(9)]
        if t != None:
            self.full = copy.deepcopy(t.full)
        self.p1 = "X"
        self.p2 = "O"
        self.lastPlayed = (4, self.p2)
        # 1  2  3
        # 4  5  6
        # 7  8  9

    def __str__(self):
        """
        For debugging purposes, returns the game board as a string.
        """
        s = ""
        for j in range(len(self.full)):
            i = self.full[j]
            for x in range(len(i)):
                s += (i[x] + " ") if x % 3 != 2 else (i[x] + "  ")
            s += "\n" if j % 3 != 2 else "\n\n"
        return s
        
    def move(self, player:str, terrain:int, case:int):
        """This makes an actual move

        Args:
            player (str): The symbol ("X" or "O")
            terrain (int): The big terrain used
            case (int): The smaller case used
        """
        terrain -= 1
        case -= 1
        Brow = terrain % 3
        Bcol = terrain // 3
        Srow = Brow * 3 + case//3
        Scol = Bcol * 3 + case%3

        if self.full[Srow][Scol] != ".":
            #print("already in use")
            return False
        if terrain != self.nextTerrain() and self.nextTerrain() != 10:
            #print(f"not the right one, expected {self.nextTerrain()} and got {terrain}")
            return False
        if self.checkSmallVictory(self.p1, terrain + 1) or self.checkSmallVictory(self.p2, terrain + 1):
            #print("already won")
            return False

        self.full[Srow][Scol] = player
        self.lastPlayed = (case, player)
        return True
    
        
    def getTerrain(self, terrain:int):
        terfull = [[] for _ in range(3)]
        terrain -= 1
        Brow = (terrain // 3) * 3
        Bcol = (terrain % 3) * 3

        for i in range(Bcol, Bcol + 3):
            for x in range(Brow, Brow + 3):
                terfull[i - Bcol].append(self.full[i][x])
        return terfull
    
    def getAllTerrain(self):
        ts = []
        for i in range(1, 10):
            ts.append(self.getTerrain(i))
        return ts

    def check_alignement(self, player, full_terrain):
        for i in range(3):
            for j in range(3):
                if full_terrain[i][j] != player:
                    break
                elif j == 2:
                    return True
        
        for i in range(3):
            for j in range(3):
                if full_terrain[j][i] != player: # Fait gaffe à l'index
                    break
                elif j == 2:
                    return True
        
        for i in range(3):
            if full_terrain[i][i] != player:
                break
            elif i == 2:
                return True
        
        for i in range(3):
            if full_terrain[i][2-i] != player:
                break
            elif i == 2:
                return True

        return False

    def checkSmallVictory(self, player:str, terrain:int):
        full_terrain = self.getTerrain(terrain)
        return self.check_alignement(player, full_terrain)

    def getSmallVictoryBoard(self, player:str):
        sv_board = [[] for i in range(3)]

        for i in range(9):
            v = self.checkSmallVictory(player, i + 1)
            sv_board[i//3].append(player if v else ".")
        return sv_board
        
    def checkBigVictory(self, player):
        full_terrain = self.getSmallVictoryBoard(player)
        return self.check_alignement(player, full_terrain)
    
    def nextTerrain(self):
        lp = self.lastPlayed[0]
        if self.checkSmallVictory(self.p1, lp + 1) or self.checkSmallVictory(self.p2, lp + 1):
            return 10
        return lp

    def nextPlayer(self):
        return self.p1 if self.lastPlayed[1] == self.p2 else self.p2

#t = field()
#print(t)
#t.move("O", 1, 3)
#t.move("O", 1, 5)
#t.move("O", 1, 7)
#print(t)
#print(t.getTerrain(3))
#print(t.checkSmallVictory("O", 1))
#print(t.checkBigVictory("O"))