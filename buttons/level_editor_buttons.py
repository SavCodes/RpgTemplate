import copy

def test_effect():
    print("EFFECT RAN")

level_editor_button_data = {
    "Set Spawn": {"x": 0.05, "y": 0.50, "effect": lambda button: spawn_button_effect(button)},
    "Set Objective": {"x": 0.18, "y": 0.50, "effect": test_effect},

    "Player One": {"x": 0.05, "y": 0.70, "effect": lambda button: player_one_button_effect(button)},

    "Save Level": {"x": 0.05, "y": 0.80, "effect": lambda button: level_editor_save_button_effect(button)},
    "Reset Level": {"x": 0.18, "y": 0.70, "effect": lambda button: reset_button_effect(button)},

    "Edit Background": {"x": 0.05, "y": 0.90, "effect": lambda button: edit_background_button_effect(button)},
    "Edit Foreground": {"x": 0.18, "y": 0.80, "effect": lambda button: edit_foreground_button_effect(button)},
}
def level_editor_save_button_effect(button):
    print("im going to save the level editor")
    with open("./new_levels.md", "w") as file:
        file.write("###")
        file.write(f"player_{button.menu.selected_player}_{button.menu.editing_array[1].split()[0]}_{button.menu.current_level} = [ \n")
        for row in button.menu.editing_array[0]:
            file.write(f'{row},')
        file.write("] \n")
def player_one_button_effect(button):
        print("Player One selected")
        button.menu.selected_player = "one"
        # button.menu.level_title_button.display_button()
        # button.menu.editing_array =  [button.menu.player_tile, "Player Level Tiles"]
        # button.menu.level_title_button.set_text(f"Editing: Player {button.menu.selected_player} Level {button.menu.current_level} \n Layer: {button.menu.editing_array[1]}")ec
def spawn_button_effect(button):
    button.menu.player_spawn_selected = True
    print("spawn button pressed")
def reset_button_effect(button):
    button.menu.editing_array[0] = copy.deepcopy(button.menu.original_level)
    print("reset button pressed")
def edit_foreground_button_effect(button):
    button.menu.editing_array = [button.menu.foreground, "Foreground Layer"]
    # button.menu.level_title_button.set_text(
    #     f"Editing: Player {button.menu.selected_player} Level {button.menu.current_level} \n Layer: {button.menu.editing_array[1]}")
def edit_background_button_effect(button):
    button.menu.editing_array = [button.menu.background, "Background Layer"]
    # button.menu.level_title_button.set_text(
    #     f"Editing: Player {button.menu.selected_player} Level {button.menu.current_level} \n Layer: {button.menu.editing_array[1]}")

