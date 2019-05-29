
import config as c
from PIL import Image, ImageTk

def RBGAImage(path):
    return Image.open(path).convert("RGBA")
# KLASA POINT
class Point():
    def __init__(self, x, y, C=None):
        # potrzebne do A*
        self.x = x
        self.y = y
        self.h = 0
        self.f = 0
        self.all = self.f + self.h
        self.pos = self.y*c.skala + self.x

        # wspolrzedne na Canvas
        self.xx = self.x * c.kratka + c.kratka // 2
        self.yy = self.y * c.kratka + c.kratka // 2

        self.typ = 0  # 0-mozna, 1-niemozna, 2-start, 3-koniec
        self.tower_type = None
        self.tower1_image = ImageTk.PhotoImage(RBGAImage('tower1.png'))
        self.sasiady = []
        self.rodzic = None
        self.master = C
        # rysuj kwadrat o rogach:
        self.image = self.master.create_rectangle(self.x * c.kratka, self.y * c.kratka, (self.x + 1) * c.kratka, (self.y + 1) * c.kratka,
                                   fill=c.block_fill,
                                   width=c.block_outline_width)


    def update(self, tower_type):
        if tower_type == 0:
            # delete tower, clean all vars
            self.tower_type = None
            self.typ = 0
            self.master.delete(self.image)
            self.image = self.master.create_rectangle(self.x * c.kratka, self.y * c.kratka, (self.x + 1) * c.kratka,
                                                      (self.y + 1) * c.kratka,
                                                      fill=c.block_fill,
                                                      width=c.block_outline_width)
        else:
            self.tower_type = tower_type
            # pole po ktorym nie mozna chodzic
            self.typ = tower_type
            # self.image = self.master.create_oval(self.x * c.kratka, self.y * c.kratka, (self.x + 1) * c.kratka, (self.y + 1) * c.kratka,
            #                        fill="green",
            #                        outline=c.block_outline,
            #                        activewidth=c.active_block_outline_width,
            #                        width=c.block_outline_width)
            self.image = self.master.create_image(self.xx, self.yy, image=self.tower1_image)

        for monster in c.monsters:
            monster.find_new_way()