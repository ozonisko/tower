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
    return c.mapa

