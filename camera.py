import random
import pygame
import time
from config import *

# class Camera:
#     def __init__(self, width, height, player, world_width, world_height):
#         self.camera = pygame.Rect(0, 0, width, height)
#         self.viewport = pygame.Rect(0, 0, width, height)
#         self.player = player
#         self.world_width = world_width
#         self.world_height = world_height
#         self.screen_width = width
#         self.screen_height = height
#         self.original_position = self.camera.topleft  # Store the original position for restoring later
#         self.shake_intensity = 0
#         self.shake_duration = 0
#         self.shake_start_time = 0
#
#     def apply(self, entity):
#         """Apply the camera's offset to a given entity."""
#         return entity.rect.move(self.camera.topleft)
#
#     def apply_to_all(self, entities):
#         """Apply the camera's offset to all entities."""
#         for entity in entities:
#             self.apply(entity)
#
#     def update(self):
#         """Update the camera position based on the player's position."""
#         x = self.player.rect[0] + self.player.rect[2] // 2 - self.viewport.width // 2
#         y = self.player.rect[1] + self.player.rect[3] // 3 - self.viewport.height // 2
#
#         # Keep the camera within the world bounds
#         x = min(max(x, 0), self.world_width - self.viewport.width)
#         y = min(max(y, 0), self.world_height - self.viewport.height)
#
#         self.x = x
#         self.y = y
#
#         # Apply shake effect if it is active
#         if self.shake_intensity > 0:
#             x += random.randint(-self.shake_intensity, self.shake_intensity)
#             y += random.randint(-self.shake_intensity, self.shake_intensity)
#             if time.time() - self.shake_start_time > self.shake_duration:
#                 self.stop_shake()  # Stop shaking after duration has passed
#
#         self.camera = pygame.Rect(x, y, self.viewport.width, self.viewport.height)
#
#         # Adjust viewport for vertical scrolling if needed
#         self.viewport = pygame.Rect(x, y, self.screen_width, self.screen_height)
#
#     def apply_offset(self, screen, background):
#         """Apply the camera offset to the background rendering."""
#         background_rect = pygame.Rect(self.camera.x, self.camera.y, self.screen_width, self.screen_height)
#         screen.blit(background, (0, 0), background_rect)  # Draw the portion of the background inside the camera view
#
#     def shake(self, intensity=10, duration=0.5):
#         """Shake the camera by applying a random offset for a short period."""
#         self.shake_intensity = intensity
#         self.shake_duration = duration
#         self.shake_start_time = time.time()
#
#     def stop_shake(self):
#         """Stop the camera shake effect and return to original position."""
#         self.shake_intensity = 0
#         self.camera.topleft = self.original_position

class Camera:
    def __init__(self, width, height, player, world_width, world_height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.viewport = pygame.Rect(0, 0, width, height)
        self.player = player
        self.world_width = world_width
        self.world_height = world_height
        self.screen_width = width
        self.screen_height = height
        self.original_position = self.camera.topleft  # Store the original position for restoring later
        self.shake_intensity = 0
        self.shake_duration = 0
        self.shake_start_time = 0

    def apply(self, entity):
        """Apply the camera's offset to a given entity."""
        return entity.rect.move(self.camera.topleft)

    def update(self):
        """Update the camera position based on the player's position."""
        x = self.player.rect[0] + self.player.rect[2] // 2 - self.viewport.width // 2
        y = self.player.rect[1] + self.player.rect[3] // 3 - self.viewport.height // 2

        # Keep the camera within the world bounds
        x = min(max(x, 0), self.world_width - self.viewport.width)
        y = min(max(y, 0), self.world_height - self.viewport.height)

        # Apply shake effect if it is active
        if self.shake_intensity > 0:
            x += random.randint(-self.shake_intensity, self.shake_intensity)
            y += random.randint(-self.shake_intensity, self.shake_intensity)
            if time.time() - self.shake_start_time > self.shake_duration:
                self.stop_shake()

        self.camera.topleft = (x, y)

    def render_parallax(self, screen, layers):
        """
        Render parallax background layers with improved performance by avoiding nested loops.

        :param screen: The pygame screen to render on.
        :param layers: List of tuples (image, parallax_factor).
                       The parallax_factor determines how much slower the layer moves compared to the camera.
        """
        for image, factor in layers:
            # Calculate the camera offset for the layer
            offset_x = -self.camera.x * factor
            offset_y = -self.camera.y * 0.1

            display_rect = pygame.Rect(self.camera.x, self.camera.y, self.screen_width + 100, self.screen_height)
            screen.blit(image, (offset_x, offset_y), display_rect)

    def apply_offset(self, screen, background):
        """Apply the camera offset to the background rendering."""
        background_rect = pygame.Rect(self.camera.x, self.camera.y, self.screen_width, self.screen_height)
        screen.blit(background, (0, 0), background_rect)  # Draw the portion of the background inside the camera view

    def shake(self, intensity=10, duration=0.5):
        """Shake the camera by applying a random offset for a short period."""
        self.shake_intensity = intensity
        self.shake_duration = duration
        self.shake_start_time = time.time()

    def stop_shake(self):
        """Stop the camera shake effect and return to original position."""
        self.shake_intensity = 0
        self.camera.topleft = self.original_position

