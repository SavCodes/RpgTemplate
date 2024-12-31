import pygame
import random
import time


class Camera:
    def __init__(self, width, height, player, world_width, world_height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.viewport = pygame.Rect(0, 0, width, height)
        self.player = player
        self.world_width = world_width
        self.world_height = world_height
        self.screen_width = width
        self.screen_height = height
        self.shake_intensity = 0
        self.shake_duration = 0
        self.shake_start_time = 0

    def update(self):
        """Update the camera position based on the player's position."""
        x = self.player.rect[0] + self.player.rect[2] // 2 - self.viewport.width // 2
        y = self.player.rect[1] + self.player.rect[3] // 2 - self.viewport.height // 2

        # Keep the camera within the world bounds
        x = min(max(x, 0), self.world_width - self.viewport.width)
        y = min(max(y, 0), self.world_height - self.viewport.height)

        # Apply shake effect if active
        if self.shake_intensity > 0:
            x += random.randint(-self.shake_intensity, self.shake_intensity)
            y += random.randint(-self.shake_intensity, self.shake_intensity)
            if time.time() - self.shake_start_time > self.shake_duration:
                self.shake_intensity = 0  # Stop shaking after duration has passed

        self.camera = pygame.Rect(x, y, self.viewport.width, self.viewport.height)

    def apply(self, entity):
        """Apply the camera's offset to a given entity."""
        return entity.rect.move(self.camera.topleft)


class ParallaxLayer:
    def __init__(self, image, parallax_factor, world_width, world_height):
        """
        Initialize a parallax layer with pre-rendered optimization.
        :param image: The background image for this layer.
        :param parallax_factor: A float (0 to 1) determining how much this layer moves relative to the camera.
        :param world_width: The width of the world in pixels.
        :param world_height: The height of the world in pixels.
        """
        self.parallax_factor = parallax_factor
        self.image = pygame.transform.scale(
            image, (image.get_width() // 2, image.get_height() // 2)
        )  # Low-res optimization
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        # Pre-render the layer
        self.rendered_layer = pygame.Surface((world_width, world_height))
        for x in range(0, world_width, self.width):
            for y in range(0, world_height, self.height):
                self.rendered_layer.blit(self.image, (x, y))

    def render(self, screen, camera):
        """Render the pre-rendered portion of the layer based on the camera viewport."""
        viewport_x = camera.camera.x * self.parallax_factor
        viewport_y = camera.camera.y * self.parallax_factor
        viewport_rect = pygame.Rect(viewport_x, viewport_y, camera.screen_width, camera.screen_height)

        # Blit only the visible portion
        screen.blit(self.rendered_layer, (0, 0), viewport_rect)
