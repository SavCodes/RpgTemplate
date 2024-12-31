import pygame
import physics
import spritesheet as sheet

from config import TILE_SIZE


class Item(physics.KinematicObject):
    def __init__(self, name, slot, category, stats=None, icon=None, position=[0,0], spritesheet=None):
        physics.KinematicObject.__init__(self, position, width=64, height=64)
        self.name = name
        self.slot = slot
        self.category = category
        self.stats = stats
        self.position = [position[0], position[1]]
        self.icon = icon
        self.image = pygame.image.load(icon).convert_alpha() if icon else None
        self.color = "gold"
        self.spritesheet = sheet.SpriteSheet(spritesheet, frame_width=self.width, frame_height=self.height) if spritesheet else None


    def is_picked_up(self, player):
        player_rect = pygame.Rect(player.position[0], player.position[1], player.width, player.height)
        if player_rect.collidepoint(self.position):
            player.inventory.content[self.category].append(self)
            return True

        return False

    def display(self, screen):
        if not self.icon:
            pygame.draw.circle(screen, self.color, self.position, self.size)
        else:
            screen.blit(self.image, (self.position[0] - self.image.get_width() // 2, self.position[1] - self.image.get_height() // 2))

