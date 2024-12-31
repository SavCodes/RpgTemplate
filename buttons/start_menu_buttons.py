from class_data.class_data import game_classes

def test_effect():
    print("EFFECT RAN")

class_selection_button_data = {
    "Blood Mage": {"x":0.13, "y":0.2, "effect": lambda button: select_class(button)},
    "Psionic Mage": {"x":0.13, "y":0.3, "effect": lambda button: select_class(button)},
    "Techno Mage": {"x":0.13, "y":0.4, "effect": lambda button: select_class(button)},
    "Hunter": {"x":0.13, "y":0.5, "effect": lambda button: select_class(button)},
    "Bruiser": {"x":0.13, "y":0.6, "effect": lambda button: select_class(button)},
    "Duelist": {"x":0.13, "y":0.7, "effect": lambda button: select_class(button)},
}

background_selection_button_data = {
    "Background 1": {"x":0.9, "y":0.2, "effect": lambda button: select_background(button)},
    "Background 2": {"x":0.9, "y":0.3, "effect": lambda button: select_background(button)},
    "Background 3": {"x":0.9, "y":0.4, "effect": lambda button: select_background(button)},
    "Background 4": {"x":0.9, "y":0.5, "effect": lambda button: select_background(button)},
    "Background 5": {"x":0.9, "y":0.6, "effect": lambda button: select_background(button)},
    "Background 6": {"x":0.9, "y":0.7, "effect": lambda button: select_background(button)},
}

def select_class(button):
    button.menu.starting_class = game_classes[button.text]

def select_background(button):
    button.menu.starting_background = button.text











