import pygame
import npc_chat_logs
from config import *


class ChatBox:
    def __init__(self,
                 location,
                 character,
                 chat_tree,
                 text_color=(0,0,0),):

        # Font
        self.font = pygame.font.Font(DEFAULT_FONT, 25)
        self.text_color = text_color

        # Dialogue tree
        self.dialogue_index = 0
        self.character_chat_tree = npc_chat_logs.chat_logs[character][chat_tree]
        self.text = self.character_chat_tree[self.dialogue_index]

        # Rolling text effect
        self.text_index = 0
        self.displayed_text = ""
        self.is_displaying = False
        self.last_update_time = 0  # For timing control

        # Dialogue box dimensions
        self.height = 100
        self.width_buffer = 100
        self.height_buffer = 230
        self.location = location

        # Precompute the main surface
        self.main_surface = pygame.Surface((PANNING_SCREEN_WIDTH - self.width_buffer, self.height))
        self.main_surface_rect = self.main_surface.get_rect(
            center=(PANNING_SCREEN_WIDTH / 2, self.height_buffer)
        )

    def render_chat_box(self, surface, delay=50):
        if not self.is_displaying:
            return

        """Renders text progressively with a delay in milliseconds."""
        current_time = pygame.time.get_ticks()  # Use pygame's time
        if current_time - self.last_update_time > delay and self.text_index < len(self.text):
            self.displayed_text += self.text[self.text_index]
            self.text_index += 1
            self.last_update_time = current_time

        # Clear and render the main surface
        self.main_surface.fill((255, 255, 255))
        wrapped_text = self._wrap_text(self.displayed_text)
        text_surface = self.font.render(wrapped_text, True, self.text_color)
        self.main_surface.blit(text_surface, (10, 10))  # Add padding

        # Blit to the main screen
        self.attach_to_target(surface)
        surface.blit(self.main_surface, self.main_surface_rect)

    def _wrap_text(self, text):
        """Helper function to wrap text to fit within the main surface."""
        words = text.split(" ")
        wrapped_text = ""
        line = ""
        max_width = self.main_surface.get_width() - 20  # Account for padding

        for word in words:
            test_line = line + word + " "
            if self.font.size(test_line)[0] <= max_width:
                line = test_line
            else:
                wrapped_text += line.strip() + "\n"
                line = word + " "
        wrapped_text += line.strip()  # Add the last line
        return wrapped_text

    def progress_chat(self):
        """Handles progression of the chat dialogue."""
        if self.text_index < len(self.text) and self.is_displaying:
            # Skip to the end of the current text
            self.displayed_text = self.text
            self.text_index = len(self.text)

        elif self.dialogue_index < len(self.character_chat_tree) - 1 and self.is_displaying:
            # Move to the next dialogue
            self.dialogue_index += 1
            self.text = self.character_chat_tree[self.dialogue_index]
            self.text_index = 0
            self.displayed_text = ""

        else:
            self.escape_chat()

    def attach_to_target(self, surface):
        pygame.draw.polygon(surface, "white", ((self.width_buffer//2, self.height_buffer + self.height//2), (self.width_buffer*2,  self.height_buffer + self.height//2), self.location))

    def escape_chat(self):
        """Ends the chat dialogue."""
        self.is_displaying = False
