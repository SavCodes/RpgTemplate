import pygame
import physics

from config import GAME_SCALE, TILE_SIZE


class Platform(physics.KinematicObject):
    def __init__(self, tile, x_position, y_position, is_collidable=True, scale=GAME_SCALE):
        super().__init__((x_position, y_position), width=TILE_SIZE, height=TILE_SIZE, scale=GAME_SCALE)
        self.tile = tile
        self.tile_number = self.tile[self.tile.rfind("_") + 1:self.tile.rfind(".")]
        self.image = pygame.transform.scale_by(pygame.image.load(tile), scale).convert_alpha()
        self.is_collidable = is_collidable
        self.collision = None

    def __repr__(self):
        return f"'{self.tile}'"

    def display_tile(self, screen):
        screen.blit(self.image, self.rect)


