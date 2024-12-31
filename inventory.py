import pygame
from config import DEFAULT_FONT
import item as item_lib

# Initialize Pygame
font = pygame.font.Font(DEFAULT_FONT, 24)
item_font = pygame.font.Font(DEFAULT_FONT, 18)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
GOLD = (255, 215, 0)
HIGHLIGHT = (100, 100, 255)

class Inventory:
    def __init__(self, screen, game):
        self.content = {
            'gold': 10,
            'weapons': [],
            'helmets': [],
            'chestplates': [],
            'leggings': []
        }
        self.selected_item = None
        self.EQUIPMENT_SLOTS = ["Helmet", "Armor", "Weapon", "Leggings"]
        self.equipment = {slot: None for slot in self.EQUIPMENT_SLOTS}
        self.screen = screen
        self.button_x_offset = 40
        self.game = game

    def display_gold_count(self):
        """Display the amount of gold in the inventory."""
        gold_text = font.render(f"Gold: {self.content['gold']}", True, GOLD)
        self.screen.blit(gold_text, (20, 20))

    def display_items(self):
        """Display items in the inventory (weapons, helmets, etc.)."""
        y_offset = 100
        for category, items in self.content.items():
            if category != 'gold':
                self._display_category_header(category, y_offset)
                y_offset += 30
                y_offset = self._display_items_in_category(items, y_offset)

    def _display_category_header(self, category, y_offset):
        """Helper method to display the category header."""
        header_text = font.render(f"{category.capitalize()}:", True, WHITE)
        self.screen.blit(header_text, (20, y_offset))

    def _display_items_in_category(self, items, y_offset):
        """Helper method to display the items in each category."""
        for item in items:
            color = HIGHLIGHT if item == self.selected_item else WHITE
            item_text = item_font.render(item.name, True, color)
            item_rect = item_text.get_rect(center=(self.button_x_offset + 20, y_offset + 10))

            # Collision detection for item selection
            if item_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_just_pressed()[0]:
                self.select_item(item)
            self.screen.blit(item_text, (self.button_x_offset, y_offset))
            y_offset += 30
        return y_offset

    def add_item(self, item):
        """Add an item to the inventory in the specified category."""
        if item.category in self.content:
            self.content[item.category].append(item)

    def select_item(self, item):
        """Select an item for interaction."""
        self.selected_item = item

    def equip_item(self, _):
        """Equip an item."""
        item = self.selected_item
        slot = item.slot
        if self.equipment[slot]:
            self.unequip_item('_')
        self.equipment[slot] = item
        self.remove_item(item)
        self.game.player.inventory.equipment[slot] = item
        self._update_player_stats(item, add=True)

    def unequip_item(self, _):
        """Unequip an item."""
        item = self.equipment[self.selected_item.slot]
        self.add_item(item)
        self._update_player_stats(item, add=False)
        self.equipment[self.selected_item.slot] = None

    def drop_item(self, _):
        """Drop an item."""
        item = self.game.player.inventory.selected_item
        if item:
            self.content[item.category].remove(item)
            self.game.room_items.append(item_lib.Item(name=item.name,
                                                           category=item.category,
                                                           slot=item.slot,
                                                           stats=item.stats,
                                                           icon=item.icon,
                                                           position=[self.game.player.position[0] + 80,
                                                                     self.game.player.position[1]]))

    def _update_player_stats(self, item, add=True):
        """Update player stats based on the item's stats."""
        multiplier = 1 if add else -1
        for stat, value in item.stats.items():
            self.game.player.stats[stat] += value * multiplier

    def remove_item(self, item):
        """Remove an item from the inventory."""
        self.content[item.category].remove(item)

    def display_equipment(self):
        """Display the currently equipped items."""
        x_offset = 300
        y_offset = 50
        for slot in self.EQUIPMENT_SLOTS:
            slot_rect = pygame.Rect(x_offset, y_offset, 200, 50)
            pygame.draw.rect(self.screen, GRAY, slot_rect)
            item = self.equipment[slot]
            item_name = item.name if item else 'Empty'
            text = font.render(f"{slot}: {item_name}", True, WHITE)
            self.screen.blit(text, (x_offset + 10, y_offset + 10))
            y_offset += 60

            if slot_rect.collidepoint(pygame.mouse.get_pos()):
                if item and pygame.mouse.get_just_pressed()[0]:
                    self.select_item(item)

    def handle_item_interaction(self, mouse_pos):
        """Handle item interactions when the player clicks an item."""
        y_offset = 100
        for category, items in self.content.items():
            if category != 'gold':
                for item in items:
                    item_rect = pygame.Rect(40, y_offset, 200, 30)
                    if item_rect.collidepoint(mouse_pos):
                        self.select_item(item)
                        return
                    y_offset += 30

    def run(self):
        self.display_gold_count()
        self.display_items()
        self.display_equipment()
