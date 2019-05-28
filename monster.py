
import config as c

class Monster():
    def __init__(self, x, y, C=None):
        # potrzebne do A*
        self.x = x
        self.y = y
        self.hp = 1

        # wspolrzedne na Canvas
        self.xx = self.x * c.kratka + c.kratka // 2
        self.yy = self.y * c.kratka + c.kratka // 2

        self.master = C
        # rysuj kwadrat o rogach:
        self.image = self.master.create_rectangle(self.x * c.kratka, self.y * c.kratka, (self.x + 1) * c.kratka, (self.y + 1) * c.kratka,
                                   fill="red",
                                   width=c.block_outline_width)
        self.step()

    def step(self):
        print("Monster", self.x, self.y)
        self.x += 1
        self.update_image()
        self.master.after(300, self.step)

    def update_image(self):
        self.master.coords(self.image, self.x * c.kratka, self.y * c.kratka, (self.x + 1) * c.kratka, (self.y + 1) * c.kratka)