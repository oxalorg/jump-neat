import pyglet, math, random
from . import solidobj, resources, block


def distance(point_1=(0, 0), point_2=(0, 0)):
    """Returns the distance between two points"""
    return math.sqrt((point_1[0] - point_2[0])**2 + (point_1[1] - point_2[1])**2)


def gen_blocks(num_icons, start_x=100, batch=None):
    blocks = []
    for i in range(num_icons):
        x = start_x + random.randint(40, 150) * (i + 1) + 100 * (i + 1)
        new_sprite = block.Block(x=x, y=150, batch=batch)
        new_sprite.scale = 0.2
        blocks.append(new_sprite)
    return blocks

# def blocks(num_blocks, player_position, batch=None):
#     """Generate block objects with random positions and velocities, not close to the player"""
#     blocks = []
#     for i in range(num_blocks):
#         block_x, block_y = player_position
#         while distance((block_x, block_y), player_position) < 100:
#             block_x = random.randint(0, 800)
#             block_y = random.randint(0, 600)
#         new_block = myobj.MyObj(img=resources.block_image,
#                                                      x=block_x, y=block_y,
#                                                      batch=batch)
#         new_block.rotation = random.randint(0, 360)
#         new_block.velocity_x, new_block.velocity_y = random.random()*40, random.random()*40
#         blocks.append(new_block)
#     return blocks
