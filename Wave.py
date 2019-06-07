from monster import *

class Wave:
    def __init__(self, size, interval, C):
        self.size = size
        self.interval = interval
        self.C = C

        self.createWave()

    def createWave(self):
        if self.size > 0:
            self.createMonster()
            self.size -= 1
            self.C.after(self.interval, self.createWave)

    def createMonster(self):
        c.monsters.append(Monster(c.start.x,c.start.y, self.C))