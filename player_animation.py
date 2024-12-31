# player_animation.py
import pygame

class PlayerAnimation:
    def __init__(self, sprite_sheet, animation_speed=0.2):
        self.sprite_sheet = sprite_sheet
        self.animation_speed = animation_speed
        self.current_animation = "idle"
        self.current_frame_index = 0
        self.animations = {}
        self.image = None

    def load_animations(self, animations):
        """Load animations from a dictionary mapping state names to lists of frames."""
        self.animations = animations
        self.image = self.animations[self.current_animation][0]

    def set_animation(self, animation_name):
        """Switch to a new animation."""
        if animation_name != self.current_animation:
            self.current_animation = animation_name
            self.current_frame_index = 0

    def update(self):
        """Update the current animation frame."""
        frames = self.animations[self.current_animation]
        self.current_frame_index += self.animation_speed
        if self.current_frame_index >= len(frames):
            self.current_frame_index = 0
        self.image = frames[int(self.current_frame_index)]

    def get_current_image(self):
        """Return the current frame image."""
        return self.image
