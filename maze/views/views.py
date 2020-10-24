from constants import BLACK_COLOR, GREEN_COLOR,\
    MAZE, ASSETS, IMAGES, SCREEN_WIDTH, SCREEN_HEIGHT,\
    BOTTOM_TEXT, SPRITE_WIDTH_IN_PX, SPRITE_HEIGHT_IN_PX
from os import path


class ViewProperties:
    def __init__(self, pygame, screen, margin_x, margin_y):

        self.pygame = pygame
        self.margin_x = margin_x
        self.margin_y = margin_y
        self.screen = screen


class MapView:

    def __init__(self, map, pygame):
        self.pygame = pygame
        self.bg_color = pygame.Color(BLACK_COLOR)
        self.map = map
        self.walls_views_list = []
        self.paths_views_list = []
        self.items_views_list = []

        # Margin between the screen and the maze
        self.margin_x = (
            SCREEN_WIDTH
            - (self.map.width * SPRITE_WIDTH_IN_PX)
            ) // 2
        self.margin_y = (
            SCREEN_HEIGHT
            - (self.map.height * SPRITE_HEIGHT_IN_PX)
            ) // 2

        self.pygame.display.set_caption("MacGyver escapes from the maze")
        self.screen = self.pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.view_properties = ViewProperties(self.pygame, self.screen,
                                              self.margin_x, self.margin_y)

        # Initialization of the visual of each object
        for one_wall in self.map.walls_list:
            self.walls_views_list.append(
                ObjectView(one_wall, self.view_properties))

        for one_path in self.map.paths_list:
            self.paths_views_list.append(
                ObjectView(one_path, self.view_properties))

        self.hero_view = ObjectView(self.map.hero, self.view_properties)
        self.guard_view = ObjectView(self.map.guard, self.view_properties)

    def display(self, game_message=""):
        self.screen.fill(self.bg_color)  # Screen background

        # Maze background
        self.maze_bg =\
            self.pygame.Rect(self.margin_x, self.margin_y,
                             SPRITE_WIDTH_IN_PX * self.map.width,
                             SPRITE_WIDTH_IN_PX * self.map.height)

        self.pygame.draw.rect(self.screen, GREEN_COLOR, self.maze_bg)

        # paths
        for one_path_view in self.paths_views_list:
            one_path_view.display()
        # walls
        for one_wall_view in self.walls_views_list:
            one_wall_view.display()

        # items
        for one_item in self.map.items_list:
            one_item_view = ObjectView(one_item, self.view_properties)
            one_item_view.display()

        # characters
        self.hero_view.display()
        self.guard_view.display()

        # text
        font = self.pygame.font.SysFont("Arial", 30)
        top_text = font.render(game_message, True, (0, 128, 0))
        bottom_text = font.render(BOTTOM_TEXT, True, (0, 128, 0))

        self.screen.blit(bottom_text, (
            SCREEN_WIDTH//2 - bottom_text.get_width() // 2,
            SCREEN_HEIGHT//20 * 19 - bottom_text.get_height() // 2))

        if game_message:
            self.screen.blit(top_text,
                             (SCREEN_WIDTH//2 - top_text.get_width() // 2,
                              SCREEN_HEIGHT//20 - top_text.get_height() // 2))

        self.pygame.display.flip()  # Updating visuals


class ObjectView:

    def __init__(self, instance, view_properties):
        self.instance = instance
        self.view_properties = view_properties
        self.image = self.view_properties.pygame.image.load(
            path.join(MAZE, ASSETS, IMAGES, instance.name + ".png"))

    def display(self):
        self.rect = self.view_properties.pygame.Rect(
            self.view_properties.margin_x
            + self.instance.x_pos * SPRITE_WIDTH_IN_PX,
            self.view_properties.margin_y
            + self.instance.y_pos * SPRITE_HEIGHT_IN_PX,
            SPRITE_WIDTH_IN_PX,
            SPRITE_HEIGHT_IN_PX)

        self.view_properties.screen.blit(self.image, self.rect)
