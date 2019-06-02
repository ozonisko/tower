class ProjectileInterface:
    def __init__(self, damage, range, towerId, stepInterval, target, C=None):
        raise NotImplementedError

    def step(self):
        raise NotImplementedError

    def prepareRoute(self):
        raise NotImplementedError