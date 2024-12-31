import pygame

from config import DEFAULT_FONT


class StatUI:
    def __init__(self, screen, stats, themes, icons):
        self.screen = screen
        self.stats = stats
        self.current_theme = None
        self.themes = themes
        self.icons = icons
        self.font = pygame.font.Font(DEFAULT_FONT, 20)
        self.collapsed_sections = {}

    def draw_gradient_bar(self, x, y, width, height, current, maximum, start_color, end_color):
        try:
            progress = current / maximum
        except ZeroDivisionError:
            progress = 0

        for i in range(int(width * progress)):
            color = (
                min(start_color[0] + (end_color[0] - start_color[0]) * (i / width),255),
                min(start_color[1] + (end_color[1] - start_color[1]) * (i / width), 255),
                min(start_color[2] + (end_color[2] - start_color[2]) * (i / width), 255),
            )
            pygame.draw.line(self.screen, color, (x + i, y), (x + i, y + height))
        pygame.draw.rect(self.screen, (0, 0, 0), (x, y, width, height), 2)

    def display_tooltip(self, text, x, y):
        tooltip = self.font.render(text, True, (255, 255, 255))
        tooltip_rect = tooltip.get_rect(topleft=(x, y))
        pygame.draw.rect(self.screen, (0, 0, 0), tooltip_rect.inflate(10, 10))
        self.screen.blit(tooltip, (x + 5, y + 5))

    def toggle_section(self, section):
        self.collapsed_sections[section] = not self.collapsed_sections.get(section, False)

    def render(self):
        y_offset = 10
        bar_width = self.screen.get_width() * 0.25
        bar_height = 20

        for section, stats in self.stats.items():
            # Render Section Header
            section_title = self.font.render(section.upper(), True, (255, 255, 255))
            section_rect = section_title.get_rect(topleft=(10, y_offset))
            pygame.draw.rect(self.screen, (0, 0, 0), section_rect.inflate(10, 10))
            self.screen.blit(section_title, (10, y_offset))

            # Click to Toggle Section
            if pygame.mouse.get_just_pressed()[0] and section_rect.collidepoint(pygame.mouse.get_pos()):
                self.toggle_section(section)

            y_offset += 40

            if self.collapsed_sections.get(section, False):
                continue

            # Render Stats
            for stat, value in stats.items():
                # icon = pygame.image.load(self.icons[stat]).convert_alpha() if stat in self.icons else None
                # if icon:
                #     self.screen.blit(icon, (10, y_offset))

                stat_text = f"{stat}: {value}"
                stat_render = self.font.render(stat_text, True, (255, 255, 255))
                self.screen.blit(stat_render, (50, y_offset))

                # Render Gradient Bars for relevant stats
                if "current_" in stat and "max_" + stat.split("current_")[1] in stats:
                    max_stat = stats["max_" + stat.split("current_")[1]]
                    self.draw_gradient_bar(200, y_offset, bar_width, bar_height, value, max_stat, (255, 0, 0),
                                           (0, 255, 0))

                # Display tooltip on hover
                stat_rect = stat_render.get_rect(topleft=(50, y_offset))
                if stat_rect.collidepoint(pygame.mouse.get_pos()):
                    self.display_tooltip(f"Description of {stat}", stat_rect.right + 10, stat_rect.top)

                y_offset += 40
