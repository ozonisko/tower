from ProjectileInterface import ProjectileInterface
from PIL import Image, ImageTk
import config as c
import utilities as u

class IcyProjectile(ProjectileInterface):
    def __init__(self, damage, range, towerId, stepInterval, target, slow, slowTime, aoeSize, C=None):
        self.damage = damage
        self.range = range
        self.towerId = towerId
        self.stepInterval = stepInterval
        self.target = target
        self.slow = slow
        self.aoeSize = aoeSize
        self.slowTime = slowTime
        self.routeStep = 20
        self.C = C
        self.image_base = ImageTk.PhotoImage(u.RGBAImage("IcyTower_projectile.PNG"))

        self.x = self.__getX()
        self.y = self.__getY()
        self.xx = u.convertToCanvasCoord(self.x)
        self.yy = u.convertToCanvasCoord(self.y)

        self.image = self.C.create_image(self.xx, self.yy, image=self.image_base)
        self.route = self.prepareRoute()
        print("ROUTE", self.route)

        self.step()
        
    def __slowEffect(self, target):
        target.speedModifier = 1.0 + self.slow
        target.slowDuration = self.slowTime
    
    def __dealDamage(self):
        for monster in c.monsters:
            distance = u.calculateDistance(monster.x, monster.y, self.endPointX, self.endPointY)
            if distance <= self.aoeSize:
                monster.hp -= self.damage
                monster.setImagesSlowed()
                self.__slowEffect(monster)
                
    def step(self):
        if len(self.route) == 0:
            self.__dealDamage()
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
        
        self.endPointX = self.target.x
        self.endPointY = self.target.y

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
