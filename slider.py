import pygame, pygame_widgets

from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox


def initialize_slider(screen, x, y, width, _min=0, _max=2, _step=0.1):
    txt_scl = 50
    slider = pygame_widgets.slider.Slider(screen, x, y, width, 20, min=_min, max=_max, step=_step)
    output = pygame_widgets.textbox.TextBox(screen, x - 100, y, txt_scl + 5, txt_scl // 2, fontSize=10)
    output.disable()
    return slider, output

def draw_slider(slider, output, name):
    events = pygame.event.get()
    output.setText(f"{name}: {slider.getValue()}")
    pygame_widgets.update(events)
