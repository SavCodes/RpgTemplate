import sys

def test_effect():
    print("EFFECT RAN")

def level_editor_button_effect(button):
    pass

def launch_ability_menu(self):
    self.menu.game.skill_menu.is_running = True

def launch_inventory_menu(self):
    self.menu.game.inventory_menu.is_running = True

def return_to_game(self):
    self.menu.is_running = False

def quit_game():
    sys.exit()


pause_button_data = {
    "Save": {"x": 0.80, "y": 0.15, "effect": test_effect},
    "Load": {"x": 0.80, "y": 0.25, "effect": test_effect},
    "Quit": {"x": 0.80, "y": 0.35, "effect": lambda: quit_game},
    "Ability Menu":  {"x": 0.80, "y": 0.45, "effect": lambda self: launch_ability_menu(self)},
    "Inventory": {"x": 0.80, "y": 0.55, "effect": lambda self: launch_inventory_menu(self)},
    "Return to Game": {"x": 0.80, "y": 0.65, "effect": lambda self: return_to_game(self)},

}

