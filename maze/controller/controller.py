from os import path

from models.model import Map
from views.views import MapView


class Controller:

    def __init__(self):
        self.running = True
        self.map_file = path.join("maze", "map", "map1.txt")
        self.map = Map(self.map_file)
        self.map_view = MapView(self.map)
        self.game_message = ""

    def run_console(self):
        self.map.display()
        while self.running:
            input_direction = input("""Choisissez une direction
8 (haut), 2 (bas), 4 (gauche), 6 (left) : """)
            new_position_dict =\
                self.map.scan_position(input_direction, self.map.hero)
            # new_position_dict est sous la forme:
            #       {"status":"safe/blocked/won/lost","direction":"UP/DOWN/LEFT/RIGHT"}
            if new_position_dict["status"] == "safe":
                self.map.hero.move(new_position_dict["direction"])
                self.map.check_for_interaction()
            elif new_position_dict["status"] == "won":
                self.game_message = "YOU WON!"
                self.running = False
            elif new_position_dict["status"] == "lost":
                self.game_message = "YOU LOST!"
                self.running = False
            self.map.display()

        print(self.game_message)

    def run(self):
        self.map_view.display()
        while self.running:
            # ecouter le clavier avec pygame
            status, direction = self.map.scan_position(
                input_direction, self.map.hero
            )
            if status == "safe":
                self.map.hero.move(direction)
                self.map.check_for_interaction()
            elif status == "won":
                self.game_message = "YOU WON!"
                self.running = False
            elif status == "lost":
                self.game_message = "YOU LOST!"
                self.running = False
            self.map_view.display()

        print(self.game_message)
