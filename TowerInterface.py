class TowerInterface:
    def __init__(self, id, C=None):
        raise NotImplementedError

    def attack(self):
        raise NotImplementedError

    def findTarget(self):
        raise NotImplementedError

    id = int() # numerek pola na mapie
    damage = int() # obrażenia wieżu
    cost = int() # koszt zbudowania
    range = int() # zasieg ataku
    C = None
