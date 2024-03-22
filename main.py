# This file was created by: Ethan Suriaga

# import necessary modules
from asyncio import BufferedProtocol
import filecmp
from math import floor
from typing import Any
import pygame as pg
import sys
from settings import *
from sprites import *
from random import randint
from os import path
from time import sleep
from pygame import mixer

# classes
class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map_data = []
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line)

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.power_ups = pg.sprite.Group()
        self.foods = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'U':
                    PowerUp(self, col, row)
                if tile == 'F':
                    Food(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)

        # Initialize the timer
        self.timer = 45  # 45 seconds
        self.timer_font = pg.font.SysFont(None, 36)
        self.paused = False

    def run(self):
        self.show_start_screen()  # Show the start screen initially
        while True:
            self.new()
            self.run_game()
            self.show_victory_screen()  # Show the victory screen when all food is collected

    def run_game(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if not self.paused:
                self.update()
                self.draw()
            else:
                self.draw_pause_screen()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        self.all_sprites.update()
        # Decrease the timer only if the game is still playing
        if self.playing:
            self.timer -= self.dt
            if self.timer <= 0 or len(self.foods) == 0:  # Check if all food has been collected
                self.playing = False  # End the game when timer reaches 0 or all food is collected
                if len(self.foods) == 0:  # If all food is collected, set victory flag for player
                    self.player.victory = True

    def draw_grid(self):
        # Draw grid lines
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)

        # Display timer on the screen
        timer_text = f"Time: {max(0, int(self.timer))}"  # Ensure timer doesn't go below 0
        timer_surface = self.timer_font.render(timer_text, True, BLACK)
        self.screen.blit(timer_surface, (10, 10))

        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYUP:
                if event.key == pg.K_p:
                    self.paused = not self.paused  # Toggle pause state when 'P' key is pressed

    def show_start_screen(self):
        self.screen.fill(BLACK)  # Fill the screen with black
        self.draw_text("Don't Leave.", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Collect enough resources in order to survive what's coming.", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press Any Key To Play", 15, WHITE, WIDTH / 2, HEIGHT / 1.5)
        pg.display.flip()
        self.wait_for_key()

    def show_victory_screen(self):
        self.screen.fill(BLACK)
        self.draw_text("We don't know if you survived. Let's hope you did.", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Press any key to play again", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        pg.display.flip()
        self.wait_for_key()

    def draw_pause_screen(self):
        self.draw_text("Paused", 48, YELLOW, WIDTH / 2, HEIGHT / 2)

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(pg.font.match_font('arial'), size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False

g = Game()
g.run()

