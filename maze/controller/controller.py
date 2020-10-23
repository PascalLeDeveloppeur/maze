from os import path
import sys

import pygame

from constants import MAZE, ASSETS, SOUND, BLOCKED, SAFE,\
    DOWN, UP, LEFT, RIGHT, YES, NO
from models.model import Map
from views.views import MapView


class Controller:

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()

        # sound init
        self.find_item_sound = pygame.mixer.Sound(
            path.join(MAZE, ASSETS, SOUND, "beep07.wav"))
        self.walk_sound = pygame.mixer.Sound(
            path.join(MAZE, ASSETS, SOUND, "beep28.wav"))

        self.is_game_running = True
        self.map_file = path.join(MAZE, "map", "map1.txt")
        self.map = Map(self.map_file)
        self.map_view = MapView(self.map, pygame)
        self.is_pygame_running = True
        self.key = ""
        self.game_message = ""
        self.hero_status = BLOCKED
        self.choice = ""

    def run(self):
        while self.is_pygame_running:
            self.map_view.display()
            event = self.detect_input_event()
            self.choice = event.get('choice')
            while self.is_game_running:
                event = self.detect_input_event()
                if event.get("key") or event.get("choice"):
                    self.walk_sound.play()
                    self.key = event.get('key')
                    self.choice = event.get('choice')
                    if event.get("quit_game"):
                        self.key, self.choice = "", ""
                        self.game_message = "GAME OVER!"
                        self.is_game_running = False
                    self.hero_status, self.direction =\
                        self.map.scan_position(self.key)
                    # The received tuple is in the form:
                    #   SAFE/BLOCKED/"won"/"lost", "UP"/"DOWN"/"LEFT"/"RIGHT"
                    if self.hero_status == SAFE:
                        self.map.hero.move(self.key)
                        is_interaction = self.map.check_for_interaction()
                        if is_interaction:
                            self.find_item_sound.play()
                            pass
                        self.hero_status = BLOCKED
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
        key, choice = "", ""
        quit_game = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN
                    and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    key = DOWN
                elif event.key == pygame.K_UP:
                    key = UP
                elif event.key == pygame.K_LEFT:
                    key = LEFT
                elif event.key == pygame.K_RIGHT:
                    key = RIGHT
                elif event.key == pygame.K_y:
                    choice = YES
                elif event.key == pygame.K_n:
                    choice = NO
                elif event.key == pygame.K_q:
                    quit_game = True
        return {"quit_game": quit_game,
                "key": key,
                "choice": choice}
