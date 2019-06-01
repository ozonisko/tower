class ProjectileInterface:
    def __init__(self, damage, range, towerId, C=None):
        raise NotImplementedError

    def step(self):
        raise NotImplementedError
