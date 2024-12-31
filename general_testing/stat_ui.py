import pygame
from pygame.locals import *

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 50, 50)
GREEN = (50, 200, 50)
BLUE = (50, 50, 200)
GREY = (200, 200, 200)

# Stat Display Class
class StatDisplay:
    def __init__(self, screen, stats):
        self.screen = screen
        self.stats = stats
        self.font = pygame.font.SysFont("arial", 20)

    def draw_progress_bar(self, x, y, width, height, current, maximum, color):
        # Background bar
        pygame.draw.rect(self.screen, GREY, (x, y, width, height))
        # Filled portion
        fill_width = int((current / maximum) * width)
        pygame.draw.rect(self.screen, color, (x, y, fill_width, height))
        # Border
        pygame.draw.rect(self.screen, BLACK, (x, y, width, height), 2)

    def render(self):
        y_offset = 50  # Start position

        # Core Stats
        self.screen.blit(self.font.render("Core Stats", True, WHITE), (50, y_offset))
        y_offset += 30
        self.draw_progress_bar(50, y_offset, 200, 20, self.stats["current_experience"], self.stats["max_experience"], BLUE)
        self.screen.blit(self.font.render(f"EXP: {self.stats['current_experience']}/{self.stats['max_experience']}", True, WHITE), (270, y_offset))
        y_offset += 40
        self.draw_progress_bar(50, y_offset, 200, 20, self.stats["current_health"], self.stats["max_health"], RED)
        self.screen.blit(self.font.render(f"Health: {self.stats['current_health']}/{self.stats['max_health']}", True, WHITE), (270, y_offset))
        y_offset += 40
        self.draw_progress_bar(50, y_offset, 200, 20, self.stats["current_mana"], self.stats["max_mana"], BLUE)
        self.screen.blit(self.font.render(f"Mana: {self.stats['current_mana']}/{self.stats['max_mana']}", True, WHITE), (270, y_offset))
        y_offset += 40
        self.screen.blit(self.font.render(f"Skill Points: {self.stats['skill_points']}", True, WHITE), (50, y_offset))
        y_offset += 50

        # Combat Stats
        self.screen.blit(self.font.render("Combat Stats", True, WHITE), (50, y_offset))
        y_offset += 30
        for stat in ["attack", "defense", "speed", "critical_chance", "critical_damage"]:
            self.screen.blit(self.font.render(f"{stat.capitalize()}: {self.stats[stat]}", True, WHITE), (50, y_offset))
            y_offset += 30

        # Special Stats
        self.screen.blit(self.font.render("Special Stats", True, WHITE), (50, y_offset))
        y_offset += 30
        for stat in ["life_steal", "damage_reduction", "mana_regen", "mana_recharge", "poison_damage", "poison_duration", "healing"]:
            self.screen.blit(self.font.render(f"{stat.replace('_', ' ').capitalize()}: {self.stats[stat]}", True, WHITE), (50, y_offset))
            y_offset += 30


# Main Game Loop (Testing the UI)
def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    # Example Stats
    stats = {
        "current_experience": 45,
        "max_experience": 100,
        "skill_points": 3,
        "max_health": 100,
        "current_health": 75,
        "max_mana": 50,
        "current_mana": 30,
        "life_steal": 10,
        "damage_reduction": 5,
        "attack": 12,
        "defense": 8,
        "speed": 15,
        "critical_chance": 20,
        "critical_damage": 50,
        "healing": 5,
        "mana_regen": 2,
        "mana_recharge": 10,
        "poison_damage": 8,
        "poison_duration": 6
    }

    stat_display = StatDisplay(screen, stats)

    running = True
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        stat_display.render()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
