def exit_menu(self):
    self.menu.game.inventory_menu.is_running = False

inventory_button_data = {
    "Use": {"x": 0.80, "y": 0.15, "effect": lambda self: self.menu.game.player.inventory.equip_item(self)},
    "Equip": {"x": 0.8, "y": 0.25, "effect": lambda self: self.menu.game.player.inventory.equip_item(self)},
    "Unequip": {"x": 0.80, "y": 0.35, "effect": lambda self: self.menu.game.player.inventory.unequip_item(self)},
    "Drop": {"x": 0.80, "y": 0.45, "effect": lambda self: self.menu.game.player.inventory.drop_item(self)},
    "Back": {"x": 0.80, "y": 0.55, "effect": lambda self: exit_menu(self)},
}