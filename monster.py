
import config as c
from mapa import create_blocks
from PIL import Image, ImageTk
import copy

def RBGAImage(path):
    return Image.open(path).convert("RGBA")

class Monster():
    def __init__(self, x, y, C=None):
        self.master = C
        # potrzebne do A*
        self.x = x
        self.y = y
        self.droga = []
        self.queue = []
        self.hp = 5
        self.pos = self.y * c.skala + self.x
        self.gold = 10
        self.stepInterval = 700
        self.opened = []
        self.closed = []
        self.start = None
        self.koniec = None
        self.local_map = create_blocks()

        self.alive = True

        # wspolrzedne na Canvas
        self.xx = self.x * c.kratka + c.kratka // 2
        self.yy = self.y * c.kratka + c.kratka // 2


        # rysuj kwadrat o rogach:
        #self.image = self.master.create_rectangle(self.x * c.kratka, self.y * c.kratka, (self.x + 1) * c.kratka, (self.y + 1) * c.kratka,
        #                           fill="red",
        #                           width=c.block_outline_width)
        self.monster1r_image = ImageTk.PhotoImage(RBGAImage('m1r.png'))
        self.monster1d_image = ImageTk.PhotoImage(RBGAImage('m1d.png'))
        self.monster1l_image = ImageTk.PhotoImage(RBGAImage('m1l.png'))
        self.monster1u_image = ImageTk.PhotoImage(RBGAImage('m1u.png'))
        self.image = self.master.create_image(self.xx, self.yy, image=self.monster1r_image)
        self.find_way()
        self.step()

    def kill(self):
        self.alive = False
        c.monsters.remove(self)
        print(c.monsters)
        del self

    def step(self):
        if self.droga: direction = self.droga.pop(0)
        else:
            print("-1 lives")
            c.HP -= 1
            print("Monster reached destination. Player HP is", c.HP)
            self.kill()
            return

        if self.hp < 0:
            print("Killed by tower")
            self.kill()
            return

        if direction == [1,0]:
            self.x += 1
            self.master.itemconfig(self.image, image=self.monster1r_image)
        elif direction == [0,-1]:
            self.y -= 1
            self.master.itemconfig(self.image, image=self.monster1u_image)
        elif direction == [-1,0]:
            self.x -= 1
            self.master.itemconfig(self.image, image=self.monster1l_image)
        elif direction == [0,1]:
            self.y += 1
            self.master.itemconfig(self.image, image=self.monster1d_image)
        self.xx = self.x * c.kratka + c.kratka // 2
        self.yy = self.y * c.kratka + c.kratka // 2
        self.pos = self.y * c.skala + self.x
        self.update_image()

        if self.alive:
            self.master.after(self.stepInterval, self.step)

    def update_image(self):
        self.master.coords(self.image, self.xx, self.yy)

    def find_way(self):
        self.find(self.local_map[self.pos])
        self.prepare_way()
        self.queue = self.droga


    def prepare_way(self):
        for i in range(len(self.droga) - 1):
            self.droga[i][0] -= self.droga[i + 1][0]
            self.droga[i][1] -= self.droga[i + 1][1]
        self.droga.reverse()
        self.droga.pop(0)
        #print(self.droga)

    def find_new_way(self):
        self.clean_map()
        self.update_map()
        self.droga = []
        self.queue = []
        self.find_way()

    def dist(self, a, b):
        return min(abs(a.x - b.x), abs(a.y - b.y)) * 100 + abs(abs(a.x - b.x) - abs(a.y - b.y)) * 10

    
    def szukaj_sciezki(self, punkt):
        #print(punkt)
        self.droga.append([punkt.x, punkt.y])
        if punkt.rodzic:
            self.szukaj_sciezki(punkt.rodzic)
    
    def find(self, start):
        self.opened = []
        self.closed = []
        self.start = start
        self.koniec = c.koniec
        self.clean_map()
    
        # DODAWANIE SASIADOW I TYPU
    
        for i in self.local_map:
            if i.x < c.skala-1:  # prawa krawedz
                i.sasiady.append(self.local_map[i.pos+1])
            if i.x > 0:  # lewa
                i.sasiady.append(self.local_map[i.pos - 1])
            if i.y > 0:  # gora
                i.sasiady.append(self.local_map[i.pos - c.skala])
            if i.y < c.wysokosc/c.kratka-1:  # dol
                i.sasiady.append(self.local_map[i.pos + c.skala])
            i.h = self.dist(i, self.koniec)
    
        self.opened.append(self.start)  # Dodanie self.startu
        self.current = self.start
    
        while True:
            self.opened.sort(key=lambda x: (x.all, x.h))  # Wybierz best z sasiadow
            if len(self.opened):
                self.current = self.opened.pop(0)
                self.closed.append(self.current)
            else:
                # TODO nie mozna zrobic wiezy jak nie ma przejscia, jakis test przy stawianiu wiezy trzeba dac
                messagebox.showinfo("Koniec", "Brak drogi do celu")
                return
    
            if self.current.typ == 3:  # ostatni
                self.szukaj_sciezki(self.current)
                return
            for sasiad in self.current.sasiady:
                if sasiad in self.opened and sasiad.typ is not 1:
                    if sasiad.f > self.current.f + self.dist(self.current, sasiad):
                        sasiad.f = self.current.f + self.dist(self.current, sasiad)
                        sasiad.all = sasiad.f + sasiad.h
                        sasiad.rodzic = self.current
                if sasiad not in self.opened and sasiad not in self.closed and sasiad.typ is not 1:
                    sasiad.f = self.current.f + self.dist(self.current, sasiad)
                    sasiad.all = sasiad.f + sasiad.h
                    sasiad.rodzic = self.current
                    self.opened.append(sasiad)

    def clean_map(self):
        for i in self.local_map:
            i.sasiady = []
            i.f = 0
            i.all = i.f + i.h
            i.rodzic = None

    def update_map(self):
        for i in range(len(c.mapa)):
            if c.mapa[i].typ is 0: self.local_map[i].typ = 0
            elif c.mapa[i].typ is 1: self.local_map[i].typ = 1
