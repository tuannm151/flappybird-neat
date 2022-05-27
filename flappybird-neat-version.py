from unittest import skip
import pygame
import neat
import time
import os
from sprites import BG_IMG
from constants import OBJ_SPEED, WIN_WIDTH, WIN_HEIGHT
from modules.Player import Player
from modules.Obstacle import Obstacle

pygame.font.init()
STAT_FONT = pygame.font.SysFont("comicsans", 40)


def draw_window(win, players, bg_pos, obstacles, score, gen):
    win.fill((0, 0, 0,))
    win.blit(BG_IMG, (bg_pos, 0))
    win.blit(BG_IMG, (WIN_WIDTH+bg_pos, 0))

    for obstacle in obstacles:
        obstacle.draw(win)
        obstacle.move()

    text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    gen_text = STAT_FONT.render("Generation: " + str(gen), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))
    win.blit(gen_text, (10, 10))
    for player in players:
        player.move()
        player.render(win)
    pygame.display.update()


GEN = 0


def main(genomes, config):
    # keep track of each player in the genomes and it's fitness
    global GEN
    GEN += 1
    nets = []
    ge = []
    players = []

    for _, g in genomes:
        # setting up neural network for genomes
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        players.append(Player(150, 250))
        g.fitness = 0
        ge.append(g)

    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    isRun = True
    clock = pygame.time.Clock()
    bg_pos = 0
    obstacles = [Obstacle(600)]
    score = 0

    while isRun:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRun = False
                pygame.quit()
                quit()

        # check if players have passed the first obstacle
        ob_ind = 0
        if(len(players) > 0):
            if(len(obstacles) > 1 and players[0].x > obstacles[0].x + obstacles[0].OBtop.get_width()):
                ob_ind = 1
        else:

            break
        for x, player in enumerate(players):
            player.move()
            ge[x].fitness += 0.1

            output = nets[x].activate(
                (player.y, abs(player.y - (-40 + obstacles[ob_ind].OBtop.get_height())), abs(player.y - obstacles[ob_ind].bottom)))

            if(output[0] > 0.5):
                player.jump()
        draw_window(win, players, bg_pos, obstacles, score, GEN)
        bg_pos -= OBJ_SPEED
        if(bg_pos < -WIN_WIDTH):
            bg_pos = 0

        toRemove = []
        add_obstacle = False
        for obstacle in obstacles:
            for idx, player in enumerate(players):
                if(obstacle.collide(player)):
                    # set fitness to 0 to remove the object
                    ge[idx].fitness -= 1
                    players.pop(idx)
                    nets.pop(idx)
                    ge.pop(idx)
                if not obstacle.passed and obstacle.x < player.x:
                    obstacle.passed = True
                    add_obstacle = True
            if(obstacle.x + obstacle.OBtop.get_width() < 0):
                toRemove.append(obstacle)

            obstacle.move()
        if(add_obstacle):
            score += 1
            for g in ge:
                g.fitness += 5
            obstacles.append(Obstacle(650))
        for r in toRemove:
            obstacles.remove(r)

        for idx, player in enumerate(players):
            cur_pos = player.y + player.image.get_height()
            if cur_pos <= 0 or cur_pos >= WIN_HEIGHT:
                ge[idx].fitness -= 1
                players.pop(idx)
                nets.pop(idx)
                ge.pop(idx)


def run(config_path):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 50)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)
