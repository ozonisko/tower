from TowerInterface import TowerInterface
from CannonProjectile import CannonProjectile
import config as c
import utilities as u
import math
from PIL import Image, ImageTk

def RBGAImage(path):
    return Image.open(path).convert("RGBA")

class CannonTower(TowerInterface):
    def __init__(self, id, C=None):
        print("CannonTower created with ID: %i" % id)
        self.alive = True
        self.id = id
        self.x = self.__getX()
        self.y = self.__getY()
        # wspolrzedne na Canvas
        self.xx = self.x * c.kratka + c.kratka // 2
        self.yy = self.y * c.kratka + c.kratka // 2
        self.range = 6
        self.attackInterval = 1500
        self.projectileStepInterval = 50
        self.damage = 0
        self.cost = 25
        self.C = C
        self.pos = self.y * c.skala + self.x
        self.master = C
        self.tower1_image = ImageTk.PhotoImage(RBGAImage('t1.png'))
        self.image = self.master.create_image(self.xx, self.yy, image=self.tower1_image)

        self.attack()

    def rotate_image(self, angle):
        self.tower1_image = ImageTk.PhotoImage(RBGAImage('t1.png').rotate(angle))
        self.image = self.master.create_image(self.xx, self.yy, image=self.tower1_image)


    def attack(self):
        target = self.findTarget()
        if target is not None:
            angle = abs(math.atan2(target.y - self.y, target.x - self.x) * 180 /math.pi)
            print(angle)
            self.rotate_image(angle)
            CannonProjectile(self.damage, self.range, self.id, self.projectileStepInterval, target, C=self.C)

        if self.alive:
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

    def kill(self):
        self.alive = False
        del self.image
        c.towers.remove(self)
        del self

    def __getX(self):
        return c.mapa[self.id].x

    def __getY(self):
        return c.mapa[self.id].y
