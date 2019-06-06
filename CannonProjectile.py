from ProjectileInterface import ProjectileInterface
from PIL import Image, ImageTk
import config as c
import utilities as u

class CannonProjectile(ProjectileInterface):
    def __init__(self, damage, range, towerId, stepInterval, target, C=None):
        self.damage = damage
        self.range = range
        self.towerId = towerId
        self.stepInterval = stepInterval
        self.target = target
        self.routeStep = 20
        self.C = C
        self.image_base = ImageTk.PhotoImage(u.RBGAImage("CannonTower_projectile.png"))

        self.x = self.__getX()
        self.y = self.__getY()
        self.xx = u.convertToCanvasCoord(self.x)
        self.yy = u.convertToCanvasCoord(self.y)

        self.image = self.C.create_image(self.xx, self.yy, image=self.image_base)
        self.route = self.prepareRoute()

        self.step()
        self.target.hp -= self.damage
        #self.C.after(self.stepInterval, self.step)

    def step(self):
        if len(self.route) == 0:
            c.gold += self.target.gold
            del self.target
            del self
            return

        self.C.coords(self.image, self.route[0][0], self.route[0][1])
        self.route.pop(0)

        self.C.after(self.stepInterval, self.step)

    def prepareRoute(self):
        x1 = self.xx
        y1 = self.yy
        x2 = self.target.xx
        y2 = self.target.yy

        route = []

        if x1 != x2:
            a, b = u.findLineIncludingTwoPoints(x1, y1, x2, y2)
            X = u.generateValuesInBetween(x1, x2, self.routeStep)
            for x in X:
                route.append([x, u.linearFunction(a, b, x)])

        else:
            Y = u.generateValuesInBetween(y1, y2, self.routeStep)
            for y in Y:
                route.append([x1, y])

        return route

    def __getX(self):
        return c.mapa[self.towerId].x

    def __getY(self):
        return c.mapa[self.towerId].y
