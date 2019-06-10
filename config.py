wysokosc, szerokosc = 450, 600
kratka = 50
skala = szerokosc // kratka
label = []
skos = False
algorytm = 1
krok = 0
mapa = []
start = None
koniec = None
opened = []
closed = []
debug = True
monsters = []
towers = []
waves = []
slowDurations = []

HP = 5
GOLD = 400
wave = 1

cannon_tower_cost = 50
icy_tower_cost = 70

# common stats
stats_label_life = None
stats_label_cash = None
stats_label_wave = None
top = None

# Colors
canvas_bg = "white"
# empty fill=transparent
block_fill = ""
block_outline = "black"
block_outline_width = "1"
active_block_outline_width = "2"
open_color = "burlywood2"
current_color = "khaki"
closed_color = "burlywood3"
startend_color = "navy"
path_color = "red"

#pieniazki do kupowania wiezy
gold = 50