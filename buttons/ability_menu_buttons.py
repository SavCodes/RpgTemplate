from buttons.button import create_buttons

ability_button_data = {
    'Blood Burst Upgrade Tree': {"x":0.80, "y":0.6, "effect": lambda self: activate_skill_tree_0(self)},
    'Crimson Pact Upgrade Tree': {"x":0.80, "y":0.7, "effect": lambda self: activate_skill_tree_1(self)},
    'Sanguine Chains Upgrade Tree': {"x":0.80, "y":0.8, "effect": lambda self: activate_skill_tree_2(self)},
    'Hemorrhage Upgrade Tree': {"x":0.80, "y":0.9, "effect": lambda self: activate_skill_tree_3(self)},
    'Back': {"x":0.18, "y":0.8, "effect": lambda self: exit_menu(self)}
}

upgrade_tree_button_data = {
    'Confirm Upgrade': {"x":0.80, "y":0.10, "effect": lambda self: print("Confirm Upgrade button works") },
    'Back': {"x":0.80, "y":0.30, "effect": lambda self: exit_tree(self)}
}

upgrade_tree_buttons = create_buttons(_button_data=upgrade_tree_button_data, button_list={}, screen=None, menu=None, game=None, does_return=True)

def activate_skill_tree_0(self):
    self.menu.game.player.skill_trees[0].is_running = not self.menu.game.player.skill_trees[0].is_running

def activate_skill_tree_1(self):
    self.menu.game.player.skill_trees[1].is_running = True

def activate_skill_tree_2(self):
    self.menu.game.player.skill_trees[2].is_running = True

def activate_skill_tree_3(self):
    self.menu.game.player.skill_trees[3].is_running = True

def exit_tree(self):
    for skill_tree in self.menu.game.player.skill_trees:
        skill_tree.is_running = False

def exit_menu(self):
    self.menu.game.skill_menu.is_running = False