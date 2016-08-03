from . import resources
from .solidobj import SolidObj


class Player(SolidObj):
    def __init__(self, *args, **kwargs):
        super(Player, self).__init__(resources.player_image, *args, **kwargs)
