import config as c
from tkinter import *
from point import Point
from tkinter import filedialog as fd

def create_canvas(field):
    return Canvas(field,
                  bg=c.canvas_bg,
                  height=c.wysokosc,
                  width=c.szerokosc,
                  bd=0)

def create_blocks(C):
    for i in range(c.wysokosc // c.kratka):
        for j in range(c.skala):
            c.mapa.append(Point(j, i, C))
    c.start = c.mapa[c.wysokosc // c.kratka//2 * c.skala]
    c.koniec = c.mapa[c.wysokosc // c.kratka // 2 * c.skala + c.skala -1]
    c.start.typ = 2
    c.koniec.typ = 3
    c.start.master.itemconfig(c.start.image, fill="green")
    c.koniec.master.itemconfig(c.koniec.image, fill="red")

    return c.mapa

