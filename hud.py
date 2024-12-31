import pygame
from config import DEFAULT_FONT


# class HUD:
#     def __init__(self, player):
#         self.player = player
#         self.font = pygame.font.Font(DEFAULT_FONT, 16)
#         self.icon_font = pygame.font.Font(DEFAULT_FONT, 20)  # For icons
#
#     def render(self, screen):
#         self._display_health(screen)
#         self._display_mana(screen)
#         self._display_experience(screen)
#
#     def _draw_bar(self, screen, x, y, current, maximum, color, border_color, label):
#         # Bar dimensions
#         width = 200
#         height = 20
#         border_radius = 5
#
#         # Draw border
#         pygame.draw.rect(screen, border_color, (x - 2, y - 2, width + 4, height + 4), border_radius, border_radius)
#
#         # Draw background
#         pygame.draw.rect(screen, "black", (x, y, width, height), border_radius, border_radius)
#
#         # Calculate fill percentage
#
#         try:
#             fill_width = max(0, int((current / maximum) * width))
#         except ZeroDivisionError:
#             fill_width = 0
#
#         # Draw gradient fill
#         fill_rect = pygame.Surface((fill_width, height))
#         fill_rect.fill(color)
#         screen.blit(fill_rect, (x, y))
#
#         # Draw text label
#         label_text = self.font.render(label, True, "white")
#         screen.blit(label_text, (x - 50, y))
#
#         # Draw numerical values
#         value_text = self.font.render(f"{current}/{maximum}", True, "white")
#         screen.blit(value_text, (x + width + 10, y))
#
#     def _display_health(self, screen):
#         self._draw_bar(
#             screen,
#             x=55,
#             y=30,
#             current=self.player.current_health,
#             maximum=self.player.max_health,
#             color="red",
#             border_color="darkred",
#             label="Health"
#         )
#
#     def _display_mana(self, screen):
#         self._draw_bar(
#             screen,
#             x=55,
#             y=55,
#             current=self.player.current_mana,
#             maximum=self.player.max_mana,
#             color=self.player.mana_color,
#             border_color="blue",
#             label="Mana"
#         )
#
#     def _display_experience(self, screen):
#         self._draw_bar(
#             screen,
#             x=55,
#             y=80,
#             current=self.player.current_experience,
#             maximum=self.player.max_experience,
#             color="green",
#             border_color="darkgreen",
#             label="EXP"
#         )
#
#         if self.player.current_experience == self.player.max_experience:
#             level_up_text = self.font.render("LEVEL UP AVAILABLE!", True, "yellow")
#             screen.blit(level_up_text, (100, 110))


import pygame
from config import DEFAULT_FONT

class HUD:
    def __init__(self, player):
        self.player = player
        self.font = pygame.font.Font(DEFAULT_FONT, 16)
        self.large_font = pygame.font.Font(DEFAULT_FONT, 20)
        self.icon_font = pygame.font.Font(DEFAULT_FONT, 20)  # For icons

        # Load icons (placeholders for now, replace with actual image files)
        self.health_icon = pygame.image.load("./game_assets/concept_art/health.png").convert_alpha()
        self.mana_icon = pygame.image.load("./game_assets/concept_art/mana.png").convert_alpha()
        self.exp_icon = pygame.image.load("./game_assets/concept_art/experience.png").convert_alpha()

    def render(self, screen):
        self._display_health(screen)
        self._display_mana(screen)
        self._display_experience(screen)

    def _draw_bar(self, screen, x, y, current, maximum, color, border_color, icon=None):
        # Bar dimensions
        width = 200
        height = 20
        border_radius = 5

        # Draw border
        pygame.draw.rect(screen, border_color, (x - 2, y - 2, width + 4, height + 4), border_radius, border_radius)

        # Draw background
        pygame.draw.rect(screen, "black", (x, y, width, height), border_radius, border_radius)

        # Calculate fill percentage
        try:
            fill_width = max(0, int((current / maximum) * width))
        except ZeroDivisionError:
            fill_width = 0

        # Draw gradient fill
        for i in range(fill_width):
            gradient_color = pygame.Color(color)
            gradient_color.r = min(255, gradient_color.r + i // 2)
            gradient_color.g = min(255, gradient_color.g + i // 2)
            pygame.draw.line(screen, gradient_color, (x + i, y), (x + i, y + height - 1))

        # Draw icon (if available)
        if icon:
            screen.blit(icon, (x - 40, y - 5))

        # Draw numerical values
        value_text = self.font.render(f"{current:.1f}/{maximum:.1f}", True, "white")
        screen.blit(value_text, (x + width + 10, y - 5))

    def _display_health(self, screen):
        self._draw_bar(
            screen,
            x=35,
            y=30,
            current=self.player.stats['current_health'],
            maximum=self.player.stats['max_health'],
            color="red",
            border_color="darkred",
            icon=self.health_icon
        )

    def _display_mana(self, screen):
        self._draw_bar(
            screen,
            x=35,
            y=60,
            current=self.player.stats['current_mana'],
            maximum=self.player.stats['max_mana'],
            color="blue",
            border_color="darkblue",
            icon=self.mana_icon
        )

    def _display_experience(self, screen):
        self._draw_bar(
            screen,
            x=35,
            y=90,
            current=self.player.stats['current_experience'],
            maximum=self.player.stats['max_experience'],
            color="green",
            border_color="darkgreen",
            icon=self.exp_icon
        )

        if self.player.stats['current_experience'] == self.player.stats['max_experience']:
            # Glow effect for "Level Up"
            glow_color = pygame.Color("yellow")
            glow_color.a = 100  # Semi-transparent
            pygame.draw.circle(screen, glow_color, (150, 130), 50)
            level_up_text = self.large_font.render("LEVEL UP AVAILABLE!", True, "yellow")
            screen.blit(level_up_text, (100, 120))
