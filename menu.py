import pygame
import math
from buttons import button
import sys
from config import *

class Menu:
    def __init__(self, screen, _button_data, _image=None, text="Testing", game=None):
        self.screen = screen
        self.image = _image
        self.bob_index = 0
        self.text = text
        self.game = game


        self.is_running = False

        self.button_data = _button_data
        self.init_buttons()
        self.init_dimensions_and_background()

    def init_buttons(self):
        self.button_list = {}
        button.create_buttons(_button_data=self.button_data, button_list=self.button_list, screen=self.screen, menu=self, game=self.game)

    def init_dimensions_and_background(self):
        self.width, self.height = pygame.display.get_window_size()
        self.image = self.image if None else pygame.transform.scale(pygame.image.load(self.image), self.screen.get_size())
        self.my_font = pygame.font.Font(DEFAULT_FONT, self.width // 8)

    def event_checker(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return False
        return True

    def display_text(self, text_location, text_to_display="Testing"):
        text_surface = self.my_font.render(text_to_display, True, "white")
        pause_rect = text_surface.get_rect(center=(text_location[0], text_location[1]))
        self.screen.blit(text_surface, pause_rect)

    def bob_text(self):
        if self.bob_index < math.pi * 100:
            self.bob_index += 1
        else:
            self.bob_index = 0

    def run(self):
        self.display_image()
        self.display_text((self.width // 2, 25), self.text)
        button.all_buttons_display(self.button_list)
        button.all_buttons_check_press(self.button_list)

    def display_image(self):
        if self.image:
            self.screen.blit(self.image, (0, 0))
