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
        print("clicked at field:", c.mapa[i].x, c.mapa[i].y)
        field = c.mapa[i]
        # jezeli stoi wieza
        if field.typ == 1:
            if tower_type == 0:
                c.GOLD += findTower(i).cost / 2
                field.update(tower_type)
                update_stats()
                removeTower(i)
        # jezeli normalne pole
        elif field.typ == 0:
            if tower_type == 1:
                if c.GOLD >= c.cannon_tower_cost:
                    c.GOLD -= c.cannon_tower_cost
                    field.update(tower_type)
                    update_stats()
                    c.towers.append(CannonTower(i, C=C))
            elif tower_type == 2:
                if c.GOLD >= c.icy_tower_cost:
                    c.GOLD -= c.icy_tower_cost
                    field.update(tower_type)
                    update_stats()
                    c.towers.append(IcyTower(i, C=C))

def update_stats():
    stats_C.itemconfig(c.stats_label_cash, text=c.GOLD)

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
menu.pack()
stats_frame.pack(side=TOP)

stats_C = Canvas(stats_frame, bg=c.canvas_bg,height=100,width=187,bd=0)
stats_C.pack(side=TOP)

stats_label = stats_C.create_image(94,30, image=stats_image)
stats_label = stats_C.create_image(94,80, image=wave_image)

c.stats_label_life = stats_C.create_text(60,28, text=c.HP, fill="khaki")
c.stats_label_cash = stats_C.create_text(140,28, text=c.GOLD, fill="khaki")
c.stats_label_wave = stats_C.create_text(140,78, text="1", fill="khaki")

user_frame.pack(side=TOP)

Lb1 = Listbox(user_frame, width=30, height=22, selectmode=SINGLE, selectbackground='orange',fg="khaki", background="black")
Lb1.insert(1, "Cannon Tower 3dmg 1speed")
Lb1.insert(2, "Icy Tower chill 2speed")
Lb1.insert(0, "Sell tower - 50% net worth")
Lb1.pack()
C.pack()
C.bind("<Button-1>", click)

wave1 = Wave(40, 2000, C, stats_C)


top.mainloop()