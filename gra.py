from tkinter import *
import config as c
from mapa import *
from monster import *
from PIL import Image, ImageTk
from Wave import *

from CannonTower import CannonTower
from IcyTower import IcyTower

top = Tk()
field = Frame(top)

menu = Frame(top)
stats_frame = Frame(menu)
user_frame = Frame(menu)
   

def findTower(id):
    for tower in c.towers:
        if tower.id == id:
            return tower

def removeTower(id):
    tower = findTower(id)
    tower.kill()
    print("Removed tower%i" % id)

def click(event):
    i = (event.x // c.kratka) + (event.y // c.kratka) * c.skala
    if i < c.szerokosc/c.kratka * c.wysokosc/c.kratka:
        tower_type = Lb1.curselection()[0]
        c.mapa[i].update(tower_type)
        print("clicked at field:", c.mapa[i].x, c.mapa[i].y)

        if tower_type == 0:
            removeTower(i)
        else:
            c.towers.append(IcyTower(i, C=C))


# TWORZENIE TLA
C = create_canvas(field)
pil_bg = Image.open('bg.png')
bg_image = ImageTk.PhotoImage(pil_bg)
cbg = C.create_image(c.szerokosc//2,c.wysokosc//2, image=bg_image)
c.mapa = create_blocks(C)



stats_bg = Image.open('stats.png')
stats_image = ImageTk.PhotoImage(stats_bg)
wave_bg = Image.open('wave.png')
wave_image = ImageTk.PhotoImage(wave_bg)

field.pack(side=LEFT)
menu.pack(side=BOTTOM)
stats_frame.grid(column=0, row=0)

stats_C = Canvas(stats_frame, bg=c.canvas_bg,height=130,width=187,bd=0)
stats_C.pack()

stats_label = stats_C.create_image(94,40, image=stats_image)
stats_label = stats_C.create_image(94,90, image=wave_image)

c.stats_label_life = stats_C.create_text(60,38, text="10", fill="khaki")
c.stats_label_cash = stats_C.create_text(140,38, text="4000", fill="khaki")
c.stats_label_wave = stats_C.create_text(140,88, text="1", fill="khaki")

user_frame.grid(column=0, row=10)

Lb1 = Listbox(user_frame, width=30, height=20, selectmode=SINGLE, selectbackground='black')
Lb1.insert(1, "Cannon Tower 3dmg 1speed")
Lb1.insert(2, "Icy Tower chill 2speed")
Lb1.insert(0, "Sell tower - 50% net worth")
Lb1.grid(row=4, column=0, sticky='w')
C.pack()
C.bind("<Button-1>", click)

#m1 = Monster(c.start.x,c.start.y, C)
#c.monsters = [m1]

wave1 = Wave(40, 2000, C, stats_C)


top.mainloop()