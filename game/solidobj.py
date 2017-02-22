import pyglet
import math
from game import defaults


def distance(point_1=(0, 0), point_2=(0, 0)):
    """Returns the distance between two points"""
    return math.sqrt((point_1[0] - point_2[0])**2 + (point_1[1] - point_2[1])**2)


class SolidObj(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super(SolidObj, self).__init__(*args, **kwargs)

        self.velocity_x, self.velocity_y = 0.0, 0.0
        self.acc_x, self.acc_y = 0.0, 0.0
        self.remove = False

    def update(self, dt):
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        self.velocity_y += self.acc_y * dt

        if self.y > defaults.GROUND_HT:
            self.acc_y = defaults.GRAVITY
        else:
            self.acc_y = 0
            self.velocity_y = 0
            self.y = defaults.GROUND_HT

        self.check_bounds()

    def check_bounds(self):
        min_x = -self.image.width / 2
        min_y = -self.image.height / 2
        max_x = 800 + self.image.width / 2
        max_y = 600 + self.image.height / 2
        if self.x < min_x:
            self.x = max_x
        elif self.x > max_x:
            self.x = min_x
        if self.y < min_y:
            self.y = max_y
        elif self.y > max_y:
            self.y = min_y

    def collides_with(self, other_object):
        collision_distance = self.image.width * 0.5 * self.scale + other_object.image.width * 0.5 * other_object.scale
        actual_distance = distance(self.position, other_object.position)
        return (actual_distance <= collision_distance)

    def handle_collision_with(self, other_object):
        if other_object.__class__ is not self.__class__:
            self.dead = True
