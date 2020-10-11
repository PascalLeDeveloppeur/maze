from os import system

import ipdb

from CONSTANT import UP
from CONSTANT import DOWN
from CONSTANT import LEFT
from CONSTANT import RIGHT


# ipdb.set_trace()


class Map:
    def __init__(self, file_path):
        self.hero = None
        self.guard = None
        self.items_list = []
        self.path_list = []
        self.walls_list = []
        self.width = 0
        self.height = 0
        self.load_map(file_path)

    def load_map(self, file_path):
        with open(file_path) as f:
            self.rows_list = f.readlines()
            self.height = len(self.rows_list)
            self.width = len(self.rows_list[0]) - 1  # because of \n
            for y, row in enumerate(self.rows_list):
                for x, cell in enumerate(row):
                    if cell.upper() == "S":
                        self.hero = Hero(x, y)
                        self.path_list.append(Path(x, y))
                    if cell == ".":
                        self.path_list.append(Path(x, y))
                    if cell.upper() == "X":
                        self.walls_list.append(Path(x, y))
                    if cell.upper() == "E":
                        self.guard = Guard(x, y)

    def clear_console(self):
        system("clear")

    def display(self):
        self.clear_console()
        print(" ", "_" * 15)
        for y in range(0, self.height):
            print(u"\u23B9", end=' ')
            for x in range(0, self.width):
                is_cell_filled = False
                if self.hero.x_pos == x and self.hero.y_pos == y:
                    print("S", end='')
                    continue
                if self.guard.x_pos == x and self.guard.y_pos == y:
                    print("E", end='')
                    continue
                for wall in self.walls_list:
                    if wall.x_pos == x and wall.y_pos == y:
                        print(u"\u2588", end='')
                        is_cell_filled = True
                        continue
                if not is_cell_filled:
                    print(" ", end='')
            print(u"\u23B8")
        print(" ", u"\u203E" * 15)

    def scan_position(self, proposed_direction, hero):
        scan_x_pos = hero.x_pos
        scan_y_pos = hero.y_pos
        direction = ""
        if proposed_direction == UP and scan_y_pos > 0:
            scan_x_pos = hero.x_pos
            scan_y_pos = hero.y_pos - 1
            direction = proposed_direction
        elif proposed_direction == DOWN and scan_y_pos < self.height - 1:
            scan_x_pos = hero.x_pos
            scan_y_pos = hero.y_pos + 1
            direction = proposed_direction
        elif proposed_direction == LEFT and scan_x_pos > 0:
            scan_x_pos = hero.x_pos - 1
            scan_y_pos = hero.y_pos
            direction = proposed_direction
        elif proposed_direction == RIGHT and scan_x_pos < self.width - 1:
            scan_x_pos = hero.x_pos + 1
            scan_y_pos = hero.y_pos
            direction = proposed_direction
        elif proposed_direction == "5"\
                or proposed_direction.upper() == "S"\
                or proposed_direction.upper() == "Q":
            return {"status": "lost", "direction": ""}

        for wall in self.walls_list:
            if wall.x_pos == scan_x_pos and wall.y_pos == scan_y_pos:
                return {"status": "bloked", "direction": ""}
        return {"status": "safe", "direction": direction}

    def check_for_interaction(self):
        pass


class Position:
    def __init__(self, x, y):
        self.x_pos = x
        self.y_pos = y


class Path(Position):
    def __init__(self, x, y):
        super().__init__(x, y)


class Wall(Position):
    def __init__(self, x, y):
        super().__init__(x, y)


class Guard(Position):
    def __init__(self, x, y):
        super().__init__(x, y)


class Hero(Position):
    def __init__(self, x, y):
        super().__init__(x, y)

    def move(self, direction):
        if direction == UP:
            self.y_pos -= 1
        elif direction == DOWN:
            self.y_pos += 1
        elif direction == LEFT:
            self.x_pos -= 1
        elif direction == RIGHT:
            self.x_pos += 1
        print(self.x_pos, self.y_pos)
