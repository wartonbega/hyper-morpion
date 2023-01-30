import random
from terrain import *

player = "O"
other = "X"

def floor(x):
    if x < 0:
        return 0
    elif x > 2:
        return 2
    return x

def numcase(x, y):
    c = x*3 + y + 1
    return c

def autre(who):
    if who == player:
        return other
    return player

def realname(who):
    if who == player:
        return "bot"
    return "adversaire"

def voisin(x, y, t):
    v = []
    
    
    v.append(t[floor(x+1)][y])
    v.append(t[floor(x-1)][y])
    v.append(t[x][floor(y-1)])
    v.append(t[x][floor(y-1)])

    v.append(t[floor(x+1)][floor(y+1)])
    v.append(t[floor(x-1)][floor(y-1)])
    v.append(t[floor(x-1)][floor(y+1)])
    v.append(t[floor(x+1)][floor(y-1)])

    return v


def choix(poids, cases):
    m = [list(poids.keys())[0]]
    
    for i in cases:
        if poids[i] > poids[m[-1]] :
            m = [i]
        elif poids[i] == poids[m[-1]]:
            m.append(i)
        
    if len(m) == 0:
        return random.choice(cases)
    return random.choice(m)

def check_block(plateau:field, terrain:list, case:tuple, who:str):
    terrain[case[0]][case[1]] = who
    r = plateau.check_alignement(who, terrain)
    terrain[case[0]][case[1]] = "."
    return r

def saut(terrain:field):
    gagnes = []
    bloques = []
    log = []
    for t in range(1, 10):
        ter = terrain.getTerrain(t)
        if terrain.checkSmallVictory(player, t) or terrain.checkSmallVictory(autre(player), t):
            continue
        for x in range(len(ter)):
            for y in range(len(ter[x])):
                if ter[x][y] == ".":
                    if check_block(terrain, ter, (x, y), autre(player)):
                        log.append(f"bot bloque en terrain {t} case {numcase(x, y)}")
                        bloques.append((t, numcase(x, y)))

                    ter[x][y] = player
                    if terrain.check_alignement(player, ter):
                        log.append(f"bot aligne en terrain {t} case {numcase(x, y)}")
                        gagnes.append((t, numcase(x, y)))                    
                    ter[x][y] = "."

    if len(gagnes) != 0:
        r = random.choice(gagnes)
        log.append(f"choix final terrain {r[0]} case {r[1]} (alignes)")
        return (r, log)
    
    if len(bloques) != 0:
        r = random.choice(bloques)
        log.append(f"choix final terrain {r[0]} case {r[1]} (bloques)")
        return (r, log)

    r = (random.randint(1, 9), random.randint(1, 9))
    log.append(f"choix final terrain {r[0]} case {r[1]} (random)")
    return (r, log)

def poids_case(case, plateau, t, who):
    l = []
    i = case # flemme de changer les noms
    poids = 0
    v = voisin(i[0], i[1], t)    
    t[i[0]][i[1]] = who
    if plateau.check_alignement(who, t):
        # Gagne un terrain
        l.append(f"{realname(who)} aligne en {numcase(i[0], i[1])}, rule = 4")
        poids += 4
    elif who in v:
        # Pose à coté
        l.append(f"{realname(who)} voisine en {numcase(i[0], i[1])}, rule = 1")
        poids += 1

    if check_block(plateau, t, i, autre(who)):
        # Bloque
        l.append(f"{realname(who)} bloque en {numcase(i[0], i[1])}, rule = 3")
        poids += 3

    if plateau.checkSmallVictory(who, i[0]*3 + i[1] + 1) or plateau.checkSmallVictory(autre(who), i[0]*3 + i[1] + 1):
        # Le plateau est déja plein
        l.append(f"{realname(who)} envoie voler en {numcase(i[0], i[1])}, rule = -6")
        poids -= 6
    
    
    t[i[0]][i[1]] = "."
    return (poids, l)

def analyse_plusone(terrain:int, plateau:field):
    # Analyse de la case dans laquelle vas devoire jouer l'adversaire
    t = plateau.getTerrain(terrain)
    cases = []
    poids = {}
    log = {}

    for x in range(len(t)):
        for y in range(len(t[x])):
            if t[x][y] == ".":
                cases.append((x, y))
                poids[(x, y)] = 0
                log[(x, y)] = []

    for i in cases:
        p = poids_case(i, plateau, t, other)

        poids[i] -= p[0]
        for l in p[1]:
            log[i].append(l)
        
    if len(cases) != 0:
        m = cases[0]
    else:
        return (0, log)

    moyenne = 0
    for i in cases:
        if poids[i] < poids[m]:
            m = i
            moyenne += poids[i]

    #if len(cases) != 0: 
    #   moyenne /= len(cases) 
    
    
    return (poids[m], log)

def play(terrain:int, plateau:field):
    terrain += 1

    if terrain >= 10:
        r = saut(plateau)
        for l in r[1]:
            print(l)
        print("——————————————————————————————————————")
        return r[0]

    t = plateau.getTerrain(terrain)
    cases = []
    poids = {}
    log = {}

    for x in range(len(t)):
        for y in range(len(t[x])):
            if t[x][y] == ".":
                cases.append((x, y))
                poids[(x, y)] = 0
                log[(x, y)] = []

    for i in cases:
        p = poids_case(i, plateau, t, player)

        poids[i] += p[0]
        for l in p[1]:
            log[i].append(l)
        
        c = i[0]*3 + i[1] + 1
        a = analyse_plusone(c, plateau)
        poids[i] += a[0]
        for l in a[1]:
            for x in a[1][l]:
                log[i].append("\t" + x)

    
    for i in cases:
        c = i[0]*3 + i[1] + 1
        print(f"case {c} : poids {poids[i]}")
        for l in log[i]:
            print(f"\t{l}")

    

    Bchoix = choix(poids, cases)
    c = Bchoix[0]*3 + Bchoix[1] + 1
    print("choix final", c)
    print("——————————————————————————————————————-")
    return c