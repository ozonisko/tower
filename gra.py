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



field.pack(side=LEFT)
menu.pack(side=RIGHT)
Lb1 = Listbox(menu, width=15, height=20, selectmode=SINGLE, selectbackground='black')
Lb1.insert(1, "Wieza 1")
Lb1.insert(2, "Wieza 2")
Lb1.insert(0, "Usun wieze")
Lb1.grid(row=0, column=0, sticky='w')
C.pack()
C.bind("<Button-1>", click)

#m1 = Monster(c.start.x,c.start.y, C)
#c.monsters = [m1]

wave1 = Wave(40, 1000, C)


top.mainloop()