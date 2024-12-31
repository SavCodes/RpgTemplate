import pygame
import level_files
import physics
from config import GAME_SCALE
from main import load_tile_set

class Door:
    def __init__(self, player, x_position, y_position, game, game_scale=GAME_SCALE, door_to_level=0, player_spawn=(100, 100)):
        self.player = player
        self.game_scale = game_scale
        self.x_position = x_position
        self.y_position = y_position
        self.door_to_level = door_to_level
        self.game = game
        self.player_spawn = player_spawn
        self.color = (255,0,0)
        self.width = 32 * self.game_scale
        self.height = 32 *  GAME_SCALE * 2

    def display_objective(self, screen):
        self.objective_rect = (self.x_position, self.y_position, self.width, self.height)
        pygame.draw.rect(screen, self.color, self.objective_rect, 3)

    def check_objective_collision(self):
        if physics.colliderect(self.objective_rect, self.player.rect):
            self.game.current_level = self.door_to_level
            self.player.position = [self.player_spawn[0], self.player_spawn[1]]
            self.game.tile_set = load_tile_set(level_files.level_order[self.game.current_level])
            self.player.tile_set = self.game.tile_set
            self.game.load_room()
            self.color = (255,255,255)

