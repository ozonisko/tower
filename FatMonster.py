
import config as c
import utilities as u
from mapa import create_blocks
from PIL import Image, ImageTk
from tkinter import messagebox
import copy
from monster import Monster

def RBGAImage(path):
    return Image.open(path).convert("RGBA")

class FatMonster(Monster):
    def __init__(self, x, y, C=None, stats_C=None):
        self.master = C
        self.stats_C = stats_C
        # potrzebne do A*
        self.x = x
        self.y = y
        self.droga = []
        self.queue = []
        self.MAX_HP = 20
        self.hp = self.MAX_HP
        self.pos = self.y * c.skala + self.x
        self.gold = 30
        self.stepInterval = 1600
        self.speedModifier = 1.0
        self.slowDuration = 0
        self.explosionRange = 1
        self.opened = []
        self.closed = []
        self.start = None
        self.koniec = None
        self.local_map = create_blocks()

        self.exploded = False
        self.alive = True

        # wspolrzedne na Canvas
        self.xx = self.x * c.kratka + c.kratka // 2
        self.yy = self.y * c.kratka + c.kratka // 2


        # rysuj kwadrat o rogach:
        #self.image = self.master.create_rectangle(self.x * c.kratka, self.y * c.kratka, (self.x + 1) * c.kratka, (self.y + 1) * c.kratka,
        #                           fill="red",
        #                           width=c.block_outline_width)
        self.monster1r_image_base = u.RGBAImage('m2r.png')
        self.monster1d_image_base = u.RGBAImage('m2d.png')
        self.monster1l_image_base = u.RGBAImage('m2l.png')
        self.monster1u_image_base = u.RGBAImage('m2u.png')

        self.monster1r_image_slowed = u.createCircle(u.RGBAImage('m2r.png'))
        self.monster1d_image_slowed = u.createCircle(u.RGBAImage('m2d.png'))
        self.monster1l_image_slowed = u.createCircle(u.RGBAImage('m2l.png'))
        self.monster1u_image_slowed = u.createCircle(u.RGBAImage('m2u.png'))

        self.monster1r_image = self.monster1r_image_base
        self.monster1d_image = self.monster1d_image_base
        self.monster1l_image = self.monster1l_image_base
        self.monster1u_image = self.monster1u_image_base

        self.image_current = self.monster1r_image
        self.image_current_tk = u.RGBAImageTk(self.image_current)

        self.image = self.master.create_image(self.xx, self.yy, image=self.image_current_tk)
        self.find_way()
        self.step()

    def findNeighborTowers(self):
        neighbors = []
        for tower in c.towers:
            distance = u.calculateDistance(self.x, self.y, tower.x, tower.y)
            if distance <= self.explosionRange:
                neighbors.append(tower)

        return neighbors
    
    def kamikaze(self, towers):
        for tower in towers:
            fieldId = u.findFieldByCoordinates(tower.x, tower.y)
            c.mapa[fieldId].update(0)
            tower.kill()

        self.exploded = True
        self.hp = 0
        c.monsters.append(Monster(self.x, self.y, self.master, self.stats_C))

    def step(self):
        if self.droga: direction = self.droga.pop(0)
        else:
            print("-1 lives")
            c.HP -= 1
            self.update_stats()
            print("Monster reached destination. Player HP is", c.HP)
            self.kill()
            return

        towersToBeDestroyed = self.findNeighborTowers()
        if len(towersToBeDestroyed) > 0:
            self.kamikaze(towersToBeDestroyed)

        if self.hp <= 0:
            if not self.exploded:
                c.GOLD += self.gold
                self.image_current = u.RGBAImage("blood.png")
            else:
                self.image_current = u.RGBAImage("explosion.png")

            self.image_current_tk = u.RGBAImageTk(self.image_current)
            self.master.itemconfig(self.image, image=self.image_current_tk)
            self.master.after(100, self.kill)
            self.update_stats()
            print("Killed by tower")
            return

        if direction == [1,0]:
            self.image_current = self.monster1r_image
            self.image_current_tk = u.RGBAImageTk(u.drawProgressBarOver(self.image_current, self.hp, self.MAX_HP))
            self.master.itemconfig(self.image, image=self.image_current_tk)
        elif direction == [0,-1]:
            self.image_current = self.monster1u_image
            self.image_current_tk = u.RGBAImageTk(u.drawProgressBarOver(self.image_current, self.hp, self.MAX_HP))
            self.master.itemconfig(self.image, image=self.image_current_tk)
        elif direction == [-1,0]:
            self.image_current = self.monster1l_image
            self.image_current_tk = u.RGBAImageTk(u.drawProgressBarOver(self.image_current, self.hp, self.MAX_HP))
            self.master.itemconfig(self.image, image=self.image_current_tk)
        elif direction == [0,1]:
            self.image_current = self.monster1d_image
            self.image_current_tk = u.RGBAImageTk(u.drawProgressBarOver(self.image_current, self.hp, self.MAX_HP))
            self.master.itemconfig(self.image, image=self.image_current_tk)

        self.x += direction[0]
        self.y += direction[1]
        self.pos = self.y * c.skala + self.x
        self.animate_step(3, direction)

        if self.slowDuration > 0:
            self.slowDuration -= 1
        else:
            self.speedModifier = 1.0
            self.setImagesBase()

        if self.alive:
            self.master.after(int(self.stepInterval * self.speedModifier), self.step)
            
        