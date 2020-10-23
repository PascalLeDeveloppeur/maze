from os import path
import time
import sys

import pygame

from models.model import Map
from views.views import MapView


class Controller:

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()

        # sound init
        self.find_item_sound = pygame.mixer.Sound(
            path.join("maze", "assets", "sound", "beep07.wav"))
        self.walk_sound = pygame.mixer.Sound(
            path.join("maze", "assets", "sound", "beep28.wav"))

        self.is_game_running = True
        self.map_file = path.join("maze", "map", "map1.txt")
        self.map = Map(self.map_file)
        self.map_view = MapView(self.map, pygame)
        self.is_pygame_running = True
        self.key = ""
        self.game_message = ""
        self.hero_status = "blocked"
        self.choice = ""

    def run(self):
        while self.is_pygame_running:
            self.detect_input_event()
            while self.is_game_running:
                self.detect_input_event()
                self.hero_status, self.direction =\
                    self.map.scan_position(self.key)
                # The received tuple is in the form:
                #   "safe"/"blocked"/"won"/"lost", "UP"/"DOWN"/"LEFT"/"RIGHT"
                if self.hero_status == "safe":
                    self.map.hero.move(self.key)
                    self.map.check_for_interaction()
                    self.hero_status = "blocked"
                elif self.hero_status == "won":
                    self.game_message = "YOU WON!"
                    self.is_game_running = False
                elif self.hero_status == "lost":
                    self.game_message = "YOU LOST!"
                    self.is_game_running = False
                self.key = ""
                self.map_view.display()

            # Game over
            self.map_view.display(
                self.game_message + " Play again? (Y=> yes N=> no)")

            if self.choice == "YES":
                Controller.__init__(self)
            elif self.choice == "NO":
                pygame.quit()
                sys.exit()

            # Updating the window
            self.clock.tick(7)  # Speed of the game ( n loops per second)

    def detect_input_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN
                    and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.key = "DOWN"
                elif event.key == pygame.K_UP:
                    self.key = "UP"
                elif event.key == pygame.K_LEFT:
                    self.key = "LEFT"
                elif event.key == pygame.K_RIGHT:
                    self.key = "RIGHT"
                elif event.key == pygame.K_y:
                    self.choice = "YES"
                elif event.key == pygame.K_n:
                    self.choice = "NO"
