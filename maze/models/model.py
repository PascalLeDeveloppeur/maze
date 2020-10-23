from os import system
from random import sample

from constants import UP, DOWN, RIGHT, LEFT, BLOCKED, SAFE


class Map:
    def __init__(self, file_path):
        self.hero = None
        self.guard = None
        self.items_list = []
        self.paths_list = []
        self.walls_list = []
        self.width = 0
        self.height = 0
        self.items_name_list = ["aiguille", "ether", "seringue", "tube"]
        self.load_map(file_path)
        self.place_items()

    def load_map(self, file_path):
        with open(file_path) as f:
            self.rows_list = f.readlines()
            self.height = len(self.rows_list)
            self.width = len(self.rows_list[0]) - 1  # because of \n
            for y, row in enumerate(self.rows_list):
                for x, cell in enumerate(row):
                    if cell.upper() == "S":
                        self.hero = Hero(x, y)
                        self.paths_list.append(Path(x, y))
                    if cell == ".":
                        self.paths_list.append(Path(x, y))
                    if cell.upper() == "X":
                        self.walls_list.append(Wall(x, y))
                    if cell.upper() == "E":
                        self.guard = Guard(x, y)

    def place_items(self):
        items_position = sample(self.paths_list, len(self.items_name_list))
        for i, path in enumerate(items_position):
            self.items_list.append(
                Item(path.x_pos, path.y_pos, self.items_name_list[i])
                )

    def clear_console(self):
        system("clear")

    def scan_position(self, key):
        scan_x_pos = self.hero.x_pos
        scan_y_pos = self.hero.y_pos
        direction = ""
        if key:
            pass
        if key == UP and scan_y_pos > 0:
            scan_y_pos = self.hero.y_pos - 1
            direction = key
        elif key == DOWN and scan_y_pos < self.height - 1:
            scan_y_pos = self.hero.y_pos + 1
            direction = key
        elif key == LEFT and scan_x_pos > 0:
            scan_x_pos = self.hero.x_pos - 1
            direction = key
        elif key == RIGHT and scan_x_pos < self.width - 1:
            scan_x_pos = self.hero.x_pos + 1
            direction = key

        if not direction:
            return BLOCKED, ""

        # Checking interaction with the guard
        if scan_x_pos == self.guard.x_pos\
                and scan_y_pos == self.guard.y_pos:
            if len(self.hero.items_carried_list)\
                    == len(self.items_name_list):
                return "won", ""
            return "lost", ""

        # Checking interaction with the wall
        for wall in self.walls_list:
            if wall.x_pos == scan_x_pos and wall.y_pos == scan_y_pos:
                return BLOCKED, ""

        return SAFE, direction

    def check_for_interaction(self):

        # Checking interaction with items
        for item in self.items_list:
            if self.hero.same_position(item):
                self.hero.pick_up(item)
                self.items_list.remove(item)
                return True
        return False


class PositionMixin:
    def __init__(self, x, y):
        self.x_pos = x
        self.y_pos = y

    def same_position(self, obj):
        return self.x_pos == obj.x_pos and self.y_pos == obj.y_pos


class Path(PositionMixin):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.name = "greyfloor2"


class Wall(PositionMixin):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.name = "wall"


class Guard(PositionMixin):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.name = "guard"


class Hero(PositionMixin):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.items_carried_list = []
        self.name = "MacGyver"

    def pick_up(self, item):
        self.items_carried_list.append(item)

    def move(self, direction):
        if direction == UP:
            self.y_pos -= 1
        elif direction == DOWN:
            self.y_pos += 1
        elif direction == LEFT:
            self.x_pos -= 1
        elif direction == RIGHT:
            self.x_pos += 1


class Item(PositionMixin):
    def __init__(self, x, y, name):
        super().__init__(x, y)
        self.name = name
