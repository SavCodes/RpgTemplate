import pygame

class Minimap:
    def __init__(self, world_width, world_height, minimap_size, player):
        self.world_width = world_width
        self.world_height = world_height
        self.minimap_width, self.minimap_height = minimap_size
        self.player = player

        # Scaling factor to convert world coordinates to minimap coordinates
        self.scale_x = self.minimap_width / self.world_width
        self.scale_y = self.minimap_height / self.world_height

        # Create a surface for the minimap
        self.surface = pygame.Surface(minimap_size)

    def render(self, screen, enemies, items):
        # Clear the minimap surface
        self.surface.fill((30, 30, 30))  # Background color for the minimap (dark gray)

        # Draw the player
        player_x = int(self.player.position[0] * self.scale_x)
        player_y = int(self.player.position[1] * self.scale_y)
        pygame.draw.circle(self.surface, (0, 255, 0), (player_x, player_y), 4)  # Green dot for the player

        # Draw other entities (e.g., enemies, collectibles)
        for entity in enemies:
            entity_x = int(entity.position[0] * self.scale_x)
            entity_y = int(entity.position[1] * self.scale_y)
            pygame.draw.circle(self.surface, (255, 0, 0), (entity_x, entity_y), 3)  # Red dots for enemies

        for entity in items:
            entity_x = int(entity.position[0] * self.scale_x)
            entity_y = int(entity.position[1] * self.scale_y)
            pygame.draw.circle(self.surface, (155, 155, 155), (entity_x, entity_y), 3)  # Grey dots for items

        # Add a border to the minimap
        pygame.draw.rect(self.surface, (255, 255, 255), self.surface.get_rect(), 2)

        # Blit the minimap onto the main screen (bottom-right corner)
        screen_width, screen_height = screen.get_size()
        screen.blit(self.surface, (screen_width - self.minimap_width - 10, 10))
