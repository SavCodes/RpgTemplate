import pygame
from config import DEFAULT_FONT, DEFAULT_TEXT_COLOR, PANNING_SCREEN_WIDTH, PANNING_SCREEN_HEIGHT


class Button:
    def __init__(self, screen, x, y, menu=None, effect=None, width=200, height=100, text_color=DEFAULT_TEXT_COLOR, text="testing", font_size=12, game=None):
        #================ DIMENSION ATTRIBUTES =====================
        self.x_position = x
        self.y_position = y
        self.width = width
        self.height = height
        self.is_pressed = False
        self.is_hovering = False
        self.effect = effect
        self.menu = menu

        #================ DISPLAY ATTRIBUTES =======================
        self.screen = screen
        self.text_color = text_color
        self.text = text
        self.font_size = font_size
        self.font = pygame.font.Font(DEFAULT_FONT, self.font_size)

    def display_button(self, color=(50,50,50)):
        button_text = self.font.render(self.text, True, self.text_color)
        button_rect = pygame.Rect(0, 0, self.width, self.height)
        button_rect.center = (self.x_position, self.y_position)
        pygame.draw.rect(self.screen, color, button_rect)
        self.screen.blit(button_text, button_rect)

    def check_pressed(self, mouse_x, mouse_y):
        if self.x_position - self.width / 2 < mouse_x < self.x_position + self.width / 2:
            if self.y_position - self.height / 2 < mouse_y < self.y_position + self.height / 2:
                self.display_hover_effect()
                if pygame.mouse.get_pressed()[0] and not self.is_pressed:
                    self.is_pressed = True
                    self.effect(self)
                    print("Pressed: ", self.text)
        else:
            self.is_pressed = False

    def display_hover_effect(self):
        button_rect = pygame.Rect(0, 0, self.width * 1.05, self.height * 1.05)
        button_rect.center = (self.x_position, self.y_position)
        pygame.draw.rect(self.screen, (255,0,0), button_rect, int(self.width * 0.05))

    def set_text(self, text):
        self.text = text

    def set_size(self, width, height):
        self.width = width
        self.height = height

def all_buttons_display(button_list):
    for button in button_list.values():
        button.display_button()

def all_buttons_check_press(button_list):
    mouse_x, mouse_y = pygame.mouse.get_pos()

    try:
        for game_class, _button in button_list.items():
            _button.check_pressed(mouse_x, mouse_y)
    except RuntimeError as e:
        print(e)

def all_buttons_set_size(button_list, width, height):
    for button in button_list.values():
        button.set_size(width, height)

def create_buttons(_button_data, button_list, screen, menu=None, font_size=34, game=None, does_return=False):
    for _button in _button_data:
        button_list[_button] = Button(screen,
                                    PANNING_SCREEN_WIDTH * _button_data[_button]["x"],
                                    PANNING_SCREEN_HEIGHT * _button_data[_button]["y"],
                                    effect = _button_data[_button]["effect"],
                                    menu=menu,
                                    text=_button,
                                    text_color=DEFAULT_TEXT_COLOR,
                                    font_size=font_size,
                                    game=game)

    if does_return:
        return button_list