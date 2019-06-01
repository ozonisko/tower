from ProjectileInterface import ProjectileInterface
from PIL import Image, ImageTk
import config as c

def RBGAImage(path):
    return Image.open(path).convert("RGBA")

class CannonProjectile(ProjectileInterface):
    def __init__(self, damage, range, towerId, C=None):
        self.damage = damage
        self.range = range
        self.towerId = towerId
        self.C = C
        self.image_base = ImageTk.PhotoImage(RBGAImage("CannonTower_projectile.png"))

        self.x = c.mapa[towerId].x-1
        self.y = c.mapa[towerId].y
        self.xx = self.x * c.kratka + c.kratka // 2
        self.yy = self.y * c.kratka + c.kratka // 2

        self.image = self.C.create_image(self.xx, self.yy, image=self.image_base)
        self.step()

    def step(self):
        self.x -= 1
        self.xx = self.x * c.kratka + c.kratka // 2



        self.C.coords(self.image, self.xx, self.yy)

        if self.range < 0:
            del self
            return

        self.range -= 1
        self.C.after(400, self.step)
