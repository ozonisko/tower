class TowerInterface:
    def __init__(self, id, C=None):
        raise NotImplementedError

    def attack(self):
        raise NotImplementedError

    def findTarget(self):
        raise NotImplementedError

    def kill(self):
        raise NotImplementedError

