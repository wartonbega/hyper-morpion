import terrain
from terrain import *
import pygame
import random
import math
import bot

class Game:
    def __init__(self):
        self.terrain = terrain.field()
        self.player1 = "O"
        self.player2 = "X"
        self.p1_color = (60, 60, 255)
        self.p2_color = (255, 60, 60)
        self.bot = True
        self.case_size = 60
        self.t = 0

    def playerColor(self):
        return self.p1_color if self.terrain.nextPlayer() == self.player1 else self.p2_color

    def actualiser(self, window):
        self.t += 0.1
        next_ter = self.terrain.nextTerrain()
        if self.terrain.checkBigVictory(self.player1):
            p = pygame.Surface((600, 600))
            p.fill(self.p1_color)
            window.blit(p, (0, 0))
            return

        if self.terrain.checkBigVictory(self.player2):
            p = pygame.Surface((600, 600))
            p.fill(self.p2_color)
            window.blit(p, (0, 0))
            return
        
        if next_ter == 10:
            p = pygame.Surface((600, 600))
            p.fill("yellow")
            window.blit(p, (0, 0))
        else:
            p = pygame.Surface((self.case_size * 3 + 2, self.case_size*3 + 2))
            p.fill("yellow")
            window.blit(p, (((next_ter) % 3)*3*self.case_size - 1, ((next_ter) // 3)*3*self.case_size - 1))

        xM, yM = pygame.mouse.get_pos()
        if 0 <= xM <= 570 and 0 <= yM <= 570:
            Sx = xM - xM % 60
            Sy = yM - yM % 60
        
            shadow = pygame.Surface((self.case_size, self.case_size))
            shadow.fill(self.playerColor())
            window.blit(shadow, (Sx, Sy))

            Sx = xM - xM % 60
            Sy = yM - yM % 60
            Bx = xM - xM % 180
            By = yM - yM % 180
            
            Sx, Sy = Sx - Bx, Sy - By
            Sx //= 60
            Sy //= 60
            case = (3 * Sy + Sx)
            
            if case != next_ter:
                p = pygame.Surface((self.case_size * 3 + 2, self.case_size*3 + 2))
                p.fill((200*abs(math.sin(self.t/2)), 60, 200*abs(math.cos(self.t/2)), 255))
                window.blit(p, (((case) % 3)*3*self.case_size, ((case) // 3)*3*self.case_size))

        for i in range(1, 10):
            ter = self.terrain.getTerrain(i)
            if self.terrain.checkSmallVictory(self.player1, i):
                p = pygame.Surface((3*self.case_size, 3*self.case_size))
                p.fill(self.p1_color)
                Brow = ((i - 1) // 3) * self.case_size * 3
                Bcol = ((i - 1) % 3) * self.case_size * 3
                window.blit(p, (Bcol, Brow))
                continue

            elif self.terrain.checkSmallVictory(self.player2, i):
                p = pygame.Surface((3*self.case_size, 3*self.case_size))
                p.fill(self.p2_color)
                Brow = ((i - 1) // 3) * self.case_size * 3
                Bcol = ((i - 1) % 3) * self.case_size * 3
                window.blit(p, (Bcol, Brow))
                continue

            for x in range(len(ter)):
                for y in range(len(ter[x])):
                    p = pygame.Surface(
                        (self.case_size - 2, self.case_size - 2))
                    if ter[x][y] == self.player1:
                        p.fill(self.p1_color)
                    elif ter[x][y] == self.player2:
                        p.fill(self.p2_color)
                        

                    Brow = ((i - 1) // 3) * self.case_size * \
                        3 + self.case_size * (x % 3) + 1
                    Bcol = ((i - 1) % 3) * self.case_size * \
                        3 + self.case_size * (y % 3) + 1
                    window.blit(p, (Bcol, Brow))

        if self.bot and self.terrain.nextPlayer() == self.player1:
            nt = self.terrain.nextTerrain()
            copy = field(self.terrain)
            r = bot.play(self.terrain.nextTerrain(), copy)
            # Si le terrain est 10 alors le bot doit renvoyer un couple de coordonnées : 
            # (terrain, case)
            if type(r) == tuple and nt >= 10:
                self.terrain.move(self.player1, r[0], r[1])
            else:
                self.terrain.move(self.player1, nt + 1, r)
        
        #if self.bot and self.terrain.nextPlayer() == self.player2 and round(self.t) % 10 == 0:
        #    bot.player, bot.other = bot.autre(bot.other), bot.player
        #    nt = self.terrain.nextTerrain()
        #    copy = field(self.terrain)
        #    r = bot.play(self.terrain.nextTerrain(), copy)
        #    # Si le terrain est 10 alors le bot doit renvoyer un couple de coordonnées : 
        #    # (terrain, case)
        #    if type(r) == tuple and nt >= 10:
        #        self.terrain.move(self.player2, r[0], r[1])
        #    else:
        #        self.terrain.move(self.player2, nt + 1, r)
        #    bot.player, bot.other = bot.autre(bot.other), bot.player
            
        mouse = pygame.mouse.get_pressed(3)
        if mouse[0]:
            x, y = pygame.mouse.get_pos()
            Sx = x - x % 60
            Sy = y - y % 60
            
            Bx = x - x % 180
            By = y - y % 180
            
            Sx, Sy = Sx - Bx, Sy - By
            
            Bx //= 180
            By //= 180
            Sx //= 60
            Sy //= 60
        
            case = 3 * Sy + Sx + 1
            terrain = 3 * By + Bx + 1

            self.terrain.move(self.terrain.nextPlayer(), terrain, case)
        return
