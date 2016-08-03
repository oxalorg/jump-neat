from . import resources
from .solidobj import SolidObj


class Block(SolidObj):
    def __init__(self, *args, **kwargs):
        super(Block, self).__init__(resources.block_image, *args, **kwargs)
        self.velocity_x = -50

    def check_bounds(self):
        if self.x < -20:
            self.remove = True
