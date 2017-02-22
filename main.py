import pyglet
import math
import sys
import neat
import random
from pyglet.window import key
from game import *

# Define game window and main batch
window = pyglet.window.Window(800, 600)
main_batch = pyglet.graphics.Batch()

# Define score and ground
score_label = pyglet.text.Label(text="Score: 0", x=20, y=300)
generation_label = pyglet.text.Label(text="Generation: 0", x=20, y=400)
max_fitness_label = pyglet.text.Label(text="Max Fitness: 0", x=20, y=500)
ground_text = '-' * 1000
ground = pyglet.text.Label(text=ground_text, x=0, y=150, anchor_y='center')

PLAYER_SIZE = 100
score = 1
game_objects = []
gamer = None
blocks = []

def fitness(pop):
    global score
    for g in pop:
        g['fitness'] = score

nn = neat.main(fitness, gen_size=99999, pop_size=100)
fittest = None
fittest_act = None
generation = 0
max_fitness = 1


def init():
    global fittest, fittest_act, max_fitness
    # try:
    generation += 1
    fittest = next(nn)
    max_fitness = max(max_fitness, fittest['fitness'])
    # except:
    #     sys.exit()
    fittest_act = neat.generate_network(fittest)

    global score, generation, max_fitness
    # Set score to 0
    score = 0
    score_label.text = "Score: {}".format(score)
    generation_label.text = "Generation:: {}".format(generation)
    max_fitness_label.text = "Max Fitness:: {}".format(max_fitness)

    reset_game()


def reset_game():
    global game_objects, gamer, blocks

    # Delete all blocks
    for block in blocks:
        block.delete()

    # Delete gamer
    if gamer:
        gamer.delete()
        gamer = None

    # Initialize a single Player
    gamer = player.Player(x=100, y=150, batch=main_batch)
    gamer.scale = 0.25
    gamer.y += float(gamer.scale * PLAYER_SIZE / 2)

    # Initialize 3 starting blocks
    blocks = load.gen_blocks(3, batch=main_batch)

    # Store all objects
    game_objects = [gamer] + blocks


@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.UP and gamer.y == defaults.GROUND_HT:
        gamer.jump = True


@window.event
def on_key_release(symbol, modifiers):
    pass
    # if symbol == key.UP and gamer.velocity_y > 25:
    #     gamer.velocity_y -= 25


@window.event
def on_draw():
    window.clear()
    ground.draw()
    score_label.draw()
    generation_label.draw()
    max_fitness_label.draw()
    main_batch.draw()


def update(dt):
    dt = 3*dt
    # print([block.x for block in blocks])
    global blocks

    if len(blocks) < defaults.MAX_BLOCKS:
        blocks.extend(load.gen_blocks(4, blocks[-1].x, batch=main_batch))

    blocks_ahead = filter(lambda b: b.x > gamer.x, blocks)
    nn_in = [0, 0]
    nn_in[0] = min(blocks_ahead, key=lambda b: b.x).x
    nn_in[1] = 1
    if fittest_act(nn_in)[0] > 0.5:
        if gamer.y == defaults.GROUND_HT:
            gamer.jump = True

    gamer.update(dt)

    # run job to update blocks and clear dead blocks
    removal = []
    for block in blocks:
        block.update(dt)
        if gamer.collides_with(block):
            # pyglet.clock.schedule_interval(restart, 1 / 120.0)
            pyglet.clock.unschedule(update)
            print("Dead. Restarting..")
            restart()
            return

        if block.remove:
            removal.append(block)

    for block in removal:
        blocks.remove(block)
        block.delete()

    global score
    score += 10 * dt
    score_label.text = "Score: {}".format(int(score))


def restart():
    init()
    pyglet.clock.schedule_interval(update, 1 / 120.0)


if __name__ == '__main__':
    init()
    pyglet.clock.schedule_interval(update, 1 / 120.0)
    pyglet.app.run()
