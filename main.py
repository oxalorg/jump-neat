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
generation_label = pyglet.text.Label(text="Generation: 0", x=20, y=320)
max_fitness_label = pyglet.text.Label(text="Max Fitness: 0", x=20, y=340)
avg_fitness = pyglet.text.Label(text="Avg Fitness: 0", x=20, y=340)
alive_label = pyglet.text.Label(text="Alive gamers: 0", x=20, y=360)
ground_text = '-' * 1000
ground = pyglet.text.Label(text=ground_text, x=0, y=150, anchor_y='center')

PLAYER_SIZE = 100
score = 1
game_objects = []
gamers = []
blocks = []

def fitness(pop):
    global score
    for genome, gamer in zip(pop, gamers):
        genome['fitness'] = gamer.genome['fitness']


nn = neat.main(fitness, gen_size=99999, pop_size=200)
pop = []
generation = 0
max_fitness = 1
avg_fitness = 1
alive_gamers = 0

def restart():
    global fittest, fittest_act, max_fitness, pop, avg_fitness
    generation += 1
    pop = next(nn)
    max_fitness = max(max_fitness, score)
    avg_fitness = sum(x['fitness'] for x in pop)/len(pop)

    global score, generation, max_fitness
    # Set score to 0
    score = 0
    score_label.text = "Score: {}".format(score)
    generation_label.text = "Generation:: {}".format(generation)
    max_fitness_label.text = "Max Fitness:: {}".format(max_fitness)

    global game_objects, gamers, blocks

    # Delete game objects
    for block in blocks:
        block.delete()

    for gamer in gamers:
        gamer.delete()

    # Initialize gamers of the new generation
    gamers = []
    for genome in pop:
        gamer = player.Player(x=100, y=150, batch=main_batch)
        gamer.scale = 0.25
        gamer.y += float(gamer.scale * PLAYER_SIZE / 2)
        gamer.genome = genome
        gamer.activate = neat.generate_network(genome)
        gamers.append(gamer)

    # Initialize 3 starting blocks
    blocks = load.gen_blocks(3, batch=main_batch)

    # Store all objects
    game_objects = gamers + blocks


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
    alive_label.draw()
    main_batch.draw()


def update(dt):
    alive_label.text = "Alive gamers: {}".format(len([x for x in gamers if x.alive]))
    dt = 3*dt
    # print([block.x for block in blocks])
    global blocks

    if len(blocks) < defaults.MAX_BLOCKS:
        blocks.extend(load.gen_blocks(4, blocks[-1].x, batch=main_batch))

    blocks_ahead = filter(lambda b: b.x > 100, blocks)
    closest_block = min(blocks_ahead, key=lambda b: b.x).x
    nn_in = [0, 0]
    nn_in[0] = closest_block
    nn_in[1] = 1
    for gamer in gamers:
        if gamer.alive:
            if gamer.activate(nn_in)[0] > 0.5:
                if gamer.y == defaults.GROUND_HT:
                    gamer.jump = True
        gamer.update(dt)

    # run job to update blocks and clear dead blocks
    removal = []
    for block in blocks:
        block.update(dt)
        for gamer in gamers:
            if gamer.alive:
                if gamer.collides_with(block):
                    gamer.genome['fitness'] = score
                    gamer.alive = False
                    gamer.y = -99999

        if block.remove:
            removal.append(block)

    if len([g for g in gamers if g.alive]) == 0:
        # if no gamers are alive, start next generation
        pyglet.clock.unschedule(update)
        print("Dead. Restarting..")
        init()
        return

    for block in removal:
        blocks.remove(block)
        block.delete()

    global score
    score += 10 * dt
    score_label.text = "Score: {}".format(int(score))


def init():
    restart()
    pyglet.clock.schedule_interval(update, 1 / 120.0)


if __name__ == '__main__':
    init()
    pyglet.app.run()
