import pyglet, math, random
from . import solidobj, resources, block


def distance(point_1=(0, 0), point_2=(0, 0)):
    """Returns the distance between two points"""
    return math.sqrt((point_1[0] - point_2[0])**2 + (point_1[1] - point_2[1])**2)


def gen_blocks(num_icons, start_x=100, batch=None):
    """Generate sprites for player life icons"""
    blocks = []
    for i in range(num_icons):
        x = start_x + random.randint(40, 70) * (i + 1) + 100 * (i + 1)
        new_sprite = block.Block(x=x, y=150, batch=batch)
        new_sprite.scale = 0.2
        blocks.append(new_sprite)
    return blocks

# def asteroids(num_asteroids, player_position, batch=None):
#     """Generate asteroid objects with random positions and velocities, not close to the player"""
#     asteroids = []
#     for i in range(num_asteroids):
#         asteroid_x, asteroid_y = player_position
#         while distance((asteroid_x, asteroid_y), player_position) < 100:
#             asteroid_x = random.randint(0, 800)
#             asteroid_y = random.randint(0, 600)
#         new_asteroid = myobj.MyObj(img=resources.asteroid_image,
#                                                      x=asteroid_x, y=asteroid_y,
#                                                      batch=batch)
#         new_asteroid.rotation = random.randint(0, 360)
#         new_asteroid.velocity_x, new_asteroid.velocity_y = random.random()*40, random.random()*40
#         asteroids.append(new_asteroid)
#     return asteroids
