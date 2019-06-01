from TowerInterface import TowerInterface
from CannonProjectile import CannonProjectile
from config import *

class CannonTower(TowerInterface):
    def __init__(self, id, C=None):
        print("CannonTower created with ID: %i" % id)
        self.id = id
        self.damage = 2
        self.cost = 25
        self.C = C

        self.attack()

    def attack(self):
        projectile = CannonProjectile(self.damage, 5, self.id, self.C)