from . import resources
from .solidobj import SolidObj
from game import defaults


class Player(SolidObj):
    def __init__(self, *args, **kwargs):
        super(Player, self).__init__(resources.player_image, *args, **kwargs)
        self.jump = False
        self.jump_speed = 150
        self.acc_y = 0.0

    def update(self, dt):
        super().update(dt)

        if self.jump:
            self.velocity_y = self.jump_speed
            self.jump = False

