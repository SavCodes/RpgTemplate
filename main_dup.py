import pygame
import asyncio
from config import *

screen = pygame.display.set_mode((PANNING_SCREEN_WIDTH, PANNING_SCREEN_HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF)
pygame.init()
import shader
import numpy as np
import stat_display
import enemy_data
import player
from ability import SkillMenu
from buttons import start_menu_buttons, ability_menu_buttons, button, pause_menu_buttons, inventory_menu_buttons
import player_ability_controller
import enemy
import menu
import item
import camera
import level_files
import particle
import mini_map
import level_objective
import hud
import world_generator
import inventory
import npc

def display_tile_sets(screen, tile_set):
    for row in tile_set:
        for tile in row:
            tile.display_tile(screen)

def load_tile_set(level_array):
    return world_generator.WorldGenerator(level_array, GAME_SCALE).world_tiles

def create_abilities(player, game):
    player.abilities = [ability(game=game, caster=player) for ability in player.abilities]

background_layers = [(pygame.image.load(f"./game_assets/background_images/layer_{i}.png").convert_alpha(), 0.05*i) for i in range(10,0, -1)] # Farthest layer
background_layers = [(pygame.transform.scale(layer, (SCREEN_WIDTH,SCREEN_HEIGHT)), parallax) for layer, parallax in background_layers]


class Game:
    def __init__(self):
        self.running = True
        self.clock = pygame.time.Clock()
        self.screen = screen
        self.font = pygame.font.Font(DEFAULT_FONT, 34)
        self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.init_menus()
        self.init_shader()
        self.init_music()
        self.init_player_and_world()
        self.init_enemies()
        self.init_npcs()
        self.init_items()
        self.init_mini_map()
        self.init_hud()
        self.init_doors()
        self.init_skill_menus()

    def init_shader(self):
        self.game_shader = shader.ShaderManager(_frag_shader=shader.point_glow_shader)
        num_points = 50
        self.random_positions = np.random.rand(num_points, 2) * [SCREEN_WIDTH, SCREEN_HEIGHT]
        self.game_shader.program['point_size'] = 0.001
        self.game_shader.program['resolution'] = [self.screen.width, self.screen.height]
        self.game_shader.program['positions'] = self.random_positions

    def init_skill_menus(self):
        self.player.skill_trees = [SkillMenu(self.screen, self.player, ability) for ability in self.player.abilities]

    def init_menus(self):
        # Pause menu
        self.pause_menu = menu.Menu(self.screen, _button_data=pause_menu_buttons.pause_button_data, text="Pause Screen", _image="./game_assets/concept_art/enclave_background.webp", game=self)
        button.all_buttons_set_size(self.pause_menu.button_list, width=200, height=30)

        # Start menu
        self.start_menu = menu.Menu(self.screen, _button_data=start_menu_buttons.class_selection_button_data, text="Choose Your Class", _image="./game_assets/concept_art/start_menu_2.png", game=self)
        button.create_buttons(_button_data=start_menu_buttons.background_selection_button_data, button_list=self.start_menu.button_list, screen=self.screen, menu=self.start_menu, game=self)
        button.all_buttons_set_size(self.start_menu.button_list, width=200, height=30)

        # Skill menu
        self.skill_menu = menu.Menu(self.screen, _button_data=ability_menu_buttons.ability_button_data, text="Upgrade Your Abilities", _image="./game_assets/concept_art/start_menu_3.png", game=self)
        self.skill_menu.button_list_2 = {}
        button.create_buttons(_button_data=ability_menu_buttons.upgrade_tree_button_data, button_list=self.skill_menu.button_list_2, screen=self.screen, menu=self.skill_menu, game=self)
        button.all_buttons_set_size(self.skill_menu.button_list, 350, 30)

        # Inventory Menu
        self.inventory_menu = menu.Menu(self.screen, _button_data=inventory_menu_buttons.inventory_button_data, text="Inventory", _image="./game_assets/concept_art/start_menu_3.png", game=self)
        button.all_buttons_set_size(self.inventory_menu.button_list, width=200, height=30)

    def init_player_and_world(self):
        # Background load and scale
        self.current_level = 0
        self.background_image = pygame.image.load("./game_assets/background_images/backround.webp").convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.tile_set = load_tile_set(level_files.level_order[self.current_level])
        self.start_menu.starting_class = None
        self.start_menu.starting_background = None
        self.run_start_menu()

        # Player initialization
        self.player = player.Player(self.start_menu.starting_class, self.start_menu.starting_background, screen=self.screen, scale=GAME_SCALE)
        self.player.name = "Blart"
        self.player.tile_set = self.tile_set
        self.player.inventory = inventory.Inventory(self.screen, self)
        self.stat_display = stat_display.StatUI(self.screen, self.player.display_stats, None, None)

        # Make test items
        sword = item.Item(name='sword of power', slot='Weapon', stats={'attack': 7}, category='weapons', icon="./game_assets/concept_art/weapon_drop.png")
        helmet = item.Item(name='Iron Helmet', slot='Helmet', stats={'defense': 10}, category='helmets', icon="./game_assets/concept_art/helmet_drop.png")
        pants = item.Item(name='Iron Leggings', slot='Leggings', stats={'defense': 5}, category='leggings', icon="./game_assets/concept_art/pants_drop.png")
        chestplate = item.Item(name='Chestplate', slot='Chestplate', stats={'defense': 5}, category='chestplates', icon="./game_assets/concept_art/chestplate_drop.png")

        # Add test items to the inventory
        self.player.inventory.add_item(helmet)
        self.player.inventory.add_item(sword)
        self.player.inventory.add_item(pants)
        self.player.inventory.add_item(chestplate)

        # Create the player's abilities
        create_abilities(self.player, self)

        # Create the game camera
        self.camera = camera.Camera(PANNING_SCREEN_WIDTH, PANNING_SCREEN_HEIGHT, self.player, SCREEN_WIDTH, SCREEN_HEIGHT)

        # Create the player ability controller
        self.player.ability_controller = player_ability_controller.AbilityController(self.player, self)

    def init_enemies(self):
        self.enemy_list = [enemy.Enemy(self.background,
                                       self.camera,
                                       sprite_paths=enemy_data.ENEMY_DATA[_enemy]["sprite_paths"],
                                       position=enemy_data.ENEMY_DATA[_enemy]["position"],
                                       width=enemy_data.ENEMY_DATA[_enemy]["width"],
                                       height=enemy_data.ENEMY_DATA[_enemy]["height"],
                                       sound_effects=enemy_data.ENEMY_DATA[_enemy]['sound_effects']) for _enemy in enemy_data.ENEMY_DATA]

        # self.enemy_list = []
        # self.enemy_list.append(enemy.Boss(self.background,
        #                                   self.camera,
        #                                   sprite_paths=enemy_data.small_mob_sprite_paths,
        #                                   position=(600,75),
        #                                   width=32,
        #                                   height=32))

        enemy.initialize_state_machine(self.enemy_list)

    def init_npcs(self):
        self.npc_1 = npc.Npc("Idle_4.png", (400, SCREEN_HEIGHT - 96))

    def init_items(self):
        self.world_items = [item.Item('gold', None, 'gold', position=(_ * 10, SCREEN_HEIGHT-150)) for _ in range(10)]
        self.world_items = []

    def init_hud(self):
        self.hud = hud.HUD(self.player)

    def init_mini_map(self):
        self.minimap = mini_map.Minimap(world_width=SCREEN_WIDTH, world_height=SCREEN_HEIGHT, minimap_size=(150, 150), player=self.player)

    def init_doors(self):
        self.door = level_objective.LevelObjective(player=self.player,
                                                   x_position=1200,
                                                   y_position=SCREEN_HEIGHT - 150,
                                                   game=self)

    def init_music(self):
        pygame.mixer.music.load(DEFAULT_SOUND_FX_PATH + "/Start_Menu.mp3")
        #pygame.mixer.music.play(-1)

    def run_start_menu(self):
        while self.start_menu.starting_class is None or self.start_menu.starting_background is None:
            self.start_menu.run()
            self.start_menu.event_checker()
            # self.game_shader.program['vignette_strength'] = 10
            # self.game_shader.program['perlin_toggle'] = 10
            self.game_shader.update_textures([self.screen])
            self.game_shader.render()
            pygame.display.flip()

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                self.pause_menu.is_running = not self.pause_menu.is_running
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.player.inventory.handle_item_interaction(event.pos)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_k:
                self.skill_menu.is_running = not self.skill_menu.is_running

            if event.type == pygame.KEYDOWN and event.key == pygame.K_i:
                self.inventory_menu.is_running = not self.inventory_menu.is_running

            self.player.ability_controller.ability_event_checker(event)
            self.npc_1.event_checker(event)

    def update_game(self):

        # Update game logic here (camera, player, enemies, items)
        self.background.blit(self.background_image, (0, 0))

        self.render_npcs()
        self.render_level_objectives()
        self.player.render(self.background)

        #self.render_shader_effects()

        for _enemy in self.enemy_list:
            _enemy.render(self.player)
            for projectile in self.player.projectiles:
                projectile.check_collision(_enemy)

        display_tile_sets(self.background, self.tile_set)

        for item in self.world_items:
            if item.is_picked_up(self.player):
                self.world_items.remove(item)
            else:
                item.display(self.background)

        # self.camera.render_parallax(self.screen, background_layers)
        self.camera.apply_offset(self.screen, self.background)
        self.camera.update()


    def render_npcs(self):
        self.npc_1.render_npc(self.player, self.background)

    def render_level_objectives(self):
        self.door.display_objective(self.background)
        self.door.check_objective_collision()

    def render_hud(self):
        self.hud.render(self.screen)
        for index, ability in enumerate(self.player.abilities):
            start_index = PANNING_SCREEN_WIDTH // 2 - 60 + index * 60
            ability.display_icon(self.screen, start_index, 0 )

    def render_pause_menu(self):
        self.pause_menu.run()
        self.player.update_display_stats()
        self.stat_display.stats = self.player.display_stats
        self.stat_display.render()
        print("ATTACK: ", self.player.stats['attack'])

    def render_inventory_menu(self):
        self.inventory_menu.run()
        self.player.inventory.run()

    def render_skill_menu(self):
        self.skill_menu.run()

        # Set skill menu text
        level_text = self.font.render(f"Level: {self.player.level}", True, (255, 255, 255))
        skill_point_text = self.font.render(f"Unspent Skill Points: {self.player.stats['skill_points']}", True, (255, 255, 255))

        screen.blit(level_text, (0, self.screen.height - 100))
        screen.blit(skill_point_text, (0, screen.height - 50))

        self.game_shader.update_textures([self.screen])
        self.game_shader.render()
        pygame.display.flip()

    def render_shader_effects(self):
        for ability in self.player.abilities:
            if ability.is_active:
                ability.render_shader_effect(self.game_shader, self.camera)

    def run_ability_tree(self):
        for skill_menu in self.player.skill_trees:
            while skill_menu.is_running:
                skill_menu.run("_")
                skill_menu.event_checker()
                button.all_buttons_display(self.skill_menu.button_list_2)
                button.all_buttons_check_press(self.skill_menu.button_list_2)
                self.game_shader.update_textures([self.screen])
                self.game_shader.render()
                pygame.display.flip()
            else:
                self.render_skill_menu()

    def render_fps(self):
        fps_text = self.font.render(f"FPS: {self.clock.get_fps():.0f}", True, (255, 255, 255))
        fps_text_rect = fps_text.get_rect()
        self.screen.blit(fps_text, fps_text_rect)

    def run(self):
        while self.running:
            # Handle all game events
            self.handle_events()

            # Run skill menu
            if self.skill_menu.is_running:
                self.run_ability_tree()

            # Run inventory menu
            elif self.inventory_menu.is_running:
                self.render_inventory_menu()
                self.game_shader.update_textures([self.screen])
                self.game_shader.render()
                pygame.display.flip()

            # Run pause menu
            elif self.pause_menu.is_running:
                self.render_pause_menu()
                self.game_shader.update_textures([self.screen])
                self.game_shader.render()
                pygame.display.flip()

            # Run main game
            else:
                self.update_game()
                shader.particle_drifter(self.game_shader, self.screen, self.random_positions, camera=self.camera)
                self.render_hud()
                # self.game_shader.apply_vignette(0.9)
                self.minimap.render(self.screen, self.enemy_list, self.world_items)
                self.game_shader.update_textures([self.screen])
                self.game_shader.render()
                pygame.display.flip()





            self.render_fps()
            self.clock.tick(60)
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()