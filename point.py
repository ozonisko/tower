
import config as c

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

        self.sasiady = []
        self.rodzic = None
        self.master = C
        # rysuj kwadrat o rogach:
        if (self.master): self.image = self.master.create_rectangle(self.x * c.kratka, self.y * c.kratka, (self.x + 1) * c.kratka, (self.y + 1) * c.kratka,
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
            self.typ = 1


        for monster in c.monsters:
            monster.find_new_way()