from os import path


class ViewProperties:
    def __init__(self, pygame, screen,
                 margin_x, margin_y,
                 sprite_width_in_pxl, sprite_height_in_pxl):

        self.pygame = pygame
        self.margin_x = margin_x
        self.margin_y = margin_y
        self.sprite_width_in_pxl = sprite_width_in_pxl
        self.sprite_height_in_pxl = sprite_height_in_pxl
        self.screen = screen


class MapView:

    def __init__(self, map, pygame):
        self.sprite_width_in_pxl = 43
        self.sprite_height_in_pxl = 43
        self.pygame = pygame
        self.green_color = (0, 100, 0)
        self.black = (0, 0, 0)
        self.bg_color = pygame.Color(self.black)
        self.map = map
        self.screen_width = 1200
        self.screen_height = 800
        self.walls_views_list = []
        self.paths_views_list = []
        self.items_views_list = []

        # Margin between the screen and the maze
        self.margin_x = (
            self.screen_width
            - (self.map.width * self.sprite_width_in_pxl)
            ) // 2
        self.margin_y = (
            self.screen_height
            - (self.map.height * self.sprite_height_in_pxl)
            ) // 2

        self.pygame.display.set_caption("MacGyver escapes from the maze")
        self.screen = self.pygame.display.set_mode(
            (self.screen_width, self.screen_height))

        self.view_properties = ViewProperties(self.pygame, self.screen,
                                              self.margin_x, self.margin_y,
                                              self.sprite_width_in_pxl,
                                              self.sprite_height_in_pxl)

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
                             self.sprite_width_in_pxl * self.map.width,
                             self.sprite_width_in_pxl * self.map.height)

        self.pygame.draw.rect(self.screen, self.green_color, self.maze_bg)

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

        if game_message:
            available_fonts = self.pygame.font.get_fonts()
            font = self.pygame.font.SysFont(available_fonts[0], 30)
            text = font.render(game_message, True, (0, 128, 0))
            self.screen.blit(text,
                             (self.screen_width//2 - text.get_width() // 2,
                              self.screen_height//20 - text.get_height() // 2))

        self.pygame.display.flip()  # Updating visuals


class ObjectView:

    def __init__(self, instance, view_properties):
        self.instance = instance
        self.view_properties = view_properties
        self.image = self.view_properties.pygame.image.load(
            path.join("maze", "assets", "images", instance.name + ".png"))

    def display(self):
        self.rect = self.view_properties.pygame.Rect(
            self.view_properties.margin_x
            + self.instance.x_pos * self.view_properties.sprite_width_in_pxl,
            self.view_properties.margin_y
            + self.instance.y_pos * self.view_properties.sprite_height_in_pxl,
            self.view_properties.sprite_width_in_pxl,
            self.view_properties.sprite_height_in_pxl)

        self.view_properties.screen.blit(self.image, self.rect)
