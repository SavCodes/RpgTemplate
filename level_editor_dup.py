from config import *
import pygame
import copy
import game_tile

class TileLoader:
    def __init__(self, tile_directories, default_tileset=1):
        self.tile_directories = tile_directories
        self.current_tileset = default_tileset
        self.starting_rows = 7
        self.starting_cols = 7
        self.tile_set_image = None
        self.tile_set_image_width = 0
        self.tile_set_image_height = 0
        self.working_directory = self.tile_directories[self.current_tileset]
        self.tile_set_name = 'Tileset.png'
        self.full_file_path = f'{self.working_directory}{self.tile_set_name}'
        self.load_tileset()

    def load_tileset(self):
        self.tile_set_image = pygame.image.load(self.full_file_path)
        self.tile_set_image = pygame.transform.scale(
            self.tile_set_image, (32 * self.starting_cols, 32 * self.starting_rows)
        )
        self.tile_set_image_width = self.tile_set_image.get_width()
        self.tile_set_image_height = self.tile_set_image.get_height()

    def switch_tileset(self, tileset_index):
        self.current_tileset = tileset_index
        self.working_directory = self.tile_directories[self.current_tileset]
        self.full_file_path = f'{self.working_directory}{self.tile_set_name}'
        if tileset_index == 0:
            self.starting_cols, self.starting_rows = 12, 8
        elif tileset_index == 1:
            self.starting_cols, self.starting_rows = 7, 7
        elif tileset_index == 2:
            self.starting_cols, self.starting_rows = 4, 1
        self.load_tileset()

class LevelHandler:
    def __init__(self, blank_level_template):
        self.blank_level = blank_level_template
        self.current_level_data = copy.deepcopy(blank_level_template)

    def load_level(self, level_data):
        return [
            [game_tile.Platform(tile, col_index * TILE_SIZE, row_index * TILE_SIZE)
             for col_index, tile in enumerate(row)]
            for row_index, row in enumerate(level_data)
        ]

    def save_level(self):
        # Logic for saving the level
        pass

    def update_tile(self, x, y, new_tile):
        self.current_level_data[y][x] = new_tile

class Camera:
    def __init__(self, width, height):
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height

    def pan(self, direction, speed=16):
        if direction == 'right' and self.x + PANNING_SCREEN_WIDTH < self.width:
            self.x += speed
        elif direction == 'left' and self.x > 0:
            self.x -= speed
        elif direction == 'down' and self.y + PANNING_SCREEN_HEIGHT < self.height:
            self.y += speed
        elif (direction == 'up' and
              self.y > 0):
            self.y -= speed


class EventManager:
    def __init__(self, editor):
        self.editor = editor

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                self.handle_keydown(event)
        return True

    def handle_keydown(self, event):
        if event.key == pygame.K_f:
            self.editor.showing_foreground = not self.editor.showing_foreground
        elif event.key == pygame.K_b:
            self.editor.showing_background = not self.editor.showing_background
        elif event.key in [pygame.K_0, pygame.K_1, pygame.K_2]:
            tile_set_index = int(event.unicode)
            self.editor.tile_loader.switch_tileset(tile_set_index)

class LevelEditor:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Level Editor')

        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.tile_loader = TileLoader(
            [f"{DEFAULT_TILE_PATHS}tile_files/", f"{DEFAULT_TILE_PATHS}mossy_test/", f"{DEFAULT_TILE_PATHS}hazard_tiles/"]
        )
        self.level_handler = LevelHandler(new_blank)
        self.event_manager = EventManager(self)

        self.showing_foreground = False
        self.showing_background = False
        self.selected_tile = None
