from model import Map


class Controller:

    def __init__(self):
        self.running = True
        self.map = Map("./map/map1.txt")
        self.hero = self.map.hero
        self.guard = self.map.guard

    def run(self):
        while self.running:
            input_direction = input("""Choisissez une direction
8 (haut), 2 (bas), 4 (gauche), 6 (left) : """)
            new_position_dict =\
                self.map.scan_position(input_direction, self.hero)
            # new_position_dict est sous la forme:
            #       {"status":"safe/blocked/won/lost","direction":"UP/DOWN/LEFT/RIGHT"}
            if new_position_dict["status"] == "safe":
                self.hero.move(new_position_dict["direction"])
                self.map.check_for_interaction()
            elif new_position_dict["status"] == "won":
                print("YOU WON!")
                self.running = False
            elif new_position_dict["status"] == "lost":
                print("YOU LOST!")
                self.running = False
            self.map.display()
