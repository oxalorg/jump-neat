import pyglet


def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width / 2
    image.anchor_y = image.height / 2


pyglet.resource.path = ['resources']
pyglet.resource.reindex()

player_image = pyglet.resource.image("player.png")
center_image(player_image)

block_image = pyglet.resource.image("block.png")
center_image(block_image)
