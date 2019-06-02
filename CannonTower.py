from TowerInterface import TowerInterface
from CannonProjectile import CannonProjectile
import config as c
import utilities as u
import os

file = "file.mp3"
os.system("mpg123 " + file)

class CannonTower(TowerInterface):
    def __init__(self, id, C=None):
        print("CannonTower created with ID: %i" % id)
        self.id = id
        self.x = self.__getX()
        self.y = self.__getY()
        self.range = 7
        self.attackInterval = 1500
        self.projectileStepInterval = 50
        self.damage = 2
        self.cost = 25
        self.C = C

        self.attack()

    def attack(self):
        target = self.findTarget()
        if target is not None:
            CannonProjectile(self.damage, self.range, self.id, self.projectileStepInterval, target, C=self.C)
        self.C.after(self.attackInterval, self.attack)


    def findTarget(self):
        target = None

        for monster in c.monsters:
            distance = u.calculateDistance(self.x, self.y, monster.x, monster.y)

            if target is not None:
                prevDistance = u.calculateDistance(self.x, self.y, target.x, target.y)

            if distance <= self.range and target is None or distance <= self.range and distance < prevDistance:
                target = monster

        if target is None:
            print("CannonTower%i did not find any target in its range" % self.id)
        else:
            targetDistance = u.calculateDistance(self.x, self.y, target.x, target.y)
            printArgs = (self.id, target.x, target.y, targetDistance)
            print("CannonTower%i acquired target: (x:%i, y:%i, distance: %f)" % printArgs)

        return target


    def __getX(self):
        return c.mapa[self.id].x

    def __getY(self):
        return c.mapa[self.id].y
