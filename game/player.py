from . import resources
from .solidobj import SolidObj
from game import defaults


class Player(SolidObj):
    def __init__(self, *args, **kwargs):
        super(Player, self).__init__(resources.player_image, *args, **kwargs)
        self.alive = True
        self.jump = False
        self.jump_speed = defaults.JUMP_SPEED
        self.acc_y = 0.0
        self.genome = None
        self.activate = None

    def update(self, dt):
        if self.alive:
            super().update(dt)

            if self.jump:
                self.velocity_y = self.jump_speed
                self.jump = False

