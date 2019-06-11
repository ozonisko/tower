from monster import *
from FatMonster import *

class Wave:
    def __init__(self, size, interval, C, stats_C):
        self.size = size
        self.interval = interval
        self.C = C
        self.stats_C = stats_C

        self.createWave()

    def createWave(self):
        if self.size > 0:
            self.createMonster()
            self.size -= 1
            self.C.after(self.interval, self.createWave)

    def createMonster(self):
        c.monsters.append(FatMonster(c.start.x,c.start.y, self.C, self.stats_C))
