import pygame
import asyncio

import physics
import spritesheet
from config import *

screen = pygame.display.set_mode((PANNING_SCREEN_WIDTH, PANNING_SCREEN_HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF)
pygame.init()
import shader
import numpy as np
import stat_display
import math
import rotate_image
import enemy_data
import player
import state_machine
from ability import SkillMenu
from buttons import start_menu_buttons, ability_menu_buttons, button, pause_menu_buttons, inventory_menu_buttons
import player_ability_controller
import enemy
import menu
import item
import camera
import level_files
import mini_map
import door
import hud
import world_generator
import inventory
import npc

### ============================================== BACKGROUND IMAGES FOR PARALLAX RENDERING =========================================
# background_layers = [(pygame.image.load(f"./game_assets/background_images/layer_{i}.png").convert_alpha(), 0.05*i) for i in range(10,0, -1)] # Farthest layer
# background_layers = [(pygame.transform.scale(layer, (SCREEN_WIDTH,SCREEN_HEIGHT)), parallax) for layer, parallax in background_layers]

def display_tile_sets(screen, tile_set):
    for row in tile_set:
        for tile in row:
            tile.display_tile(screen)

def load_tile_set(level_array):
    return world_generator.WorldGenerator(level_array, GAME_SCALE).world_tiles

def create_abilities(player, game):
    player.abilities = [ability(game=game, caster=player) for ability in player.abilities]

class Game:
    def __init__(self):
        self.running = True
        self.clock = pygame.time.Clock()
        self.screen = screen
        self.fps_cap = 60
        self.time = 0
        self.font = pygame.font.Font(DEFAULT_FONT, 34)
        self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.init_menus()
        self.init_shader()
        self.init_player_and_world()
        self.init_world()
        self.init_mini_map()
        self.init_hud()
        self.init_skill_menus()
        self.load_room()

    def init_shader(self):
        self.game_shader = shader.ShaderManager(_frag_shader=shader.point_glow_shader)
        num_points = 50
        self.random_positions = np.random.rand(num_points, 2) * [SCREEN_WIDTH, SCREEN_HEIGHT]
        self.game_shader.program['point_size'] = 0.001
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
        self.player = player.Player(name="Blart",
                                    sprite_sheet=enemy_data.hooded_avatar,
                                    frame_width=64,
                                    frame_height=64,
                                    game_class=self.start_menu.starting_class,
                                    background=self.start_menu.starting_background,
                                    screen=self.screen,
                                    scale=GAME_SCALE)

        # Camera initialization
        self.camera = camera.Camera(PANNING_SCREEN_WIDTH, PANNING_SCREEN_HEIGHT, self.player, SCREEN_WIDTH, SCREEN_HEIGHT)

        # Create the player's abilities
        create_abilities(self.player, self)

        # Create the player ability controller
        self.player.ability_controller = player_ability_controller.AbilityController(self.player, self)

        # Enemy, tile, and door data for each room in the world
        self.init_world()

        # Player spawn initialization
        self.player.x_spawn, self.player.y_spawn = self.doors[f"room_{self.current_level}"]["door_1"].player_spawn

        # Player state-machine initialization
        self.player.state_machine = state_machine.StateMachine(self.player)

        # Assign collidable tile set
        self.player.tile_set = self.tile_set

        # Player inventory initialization
        self.player.inventory = inventory.Inventory(self.screen, self)

        # Stat display for pause menu UI initialization
        self.stat_display = stat_display.StatUI(self.screen, self.player.display_stats, None, None)


        #======================================== INVENTORY TESTING START ==============================================
        sword = item.Item(name='sword of power', slot='Weapon', stats={'attack': 7}, category='weapons', spritesheet="./game_assets/spritesheets/weapons/sword_12.png", icon='./game_assets/spritesheets/weapons/still_sword.png')
        axe = item.Item(name="axe of power", slot='Weapon', stats={'attack': 8}, category='weapons', spritesheet="./game_assets/spritesheets/weapons/axe_12.png", icon='./game_assets/spritesheets/weapons/still_axe.png')
        # helmet = item.Item(name='Iron Helmet', slot='Helmet', stats={'defense': 10}, category='helmets', icon="./game_assets/concept_art/helmet_drop.png")
        # pants = item.Item(name='Iron Leggings', slot='Leggings', stats={'defense': 5}, category='leggings', icon="./game_assets/concept_art/pants_drop.png")
        # chestplate = item.Item(name='Chestplate', slot='Chestplate', stats={'defense': 5}, category='chestplates', icon="./game_assets/concept_art/chestplate_drop.png")
        #
        # # Add test items to the inventory
        # self.player.inventory.add_item(helmet)
        self.player.inventory.add_item(sword)
        self.player.inventory.add_item(axe)
        # self.player.inventory.add_item(pants)
        # self.player.inventory.add_item(chestplate)
        #======================================== INVENTORY TESTING END =================================================

    # def init_items(self):
    #     self.room_items = [item.Item('gold', None, 'gold', position=(_ * 10, SCREEN_HEIGHT-150)) for _ in range(10)]
    #     self.room_items = [item.Item(name='sword of power', slot='Weapon', stats={'attack': 7}, category='weapons', icon="./game_assets/concept_art/weapon_drop.png", position=(400,SCREEN_HEIGHT-150))]


    def rotate_held_item(self, position, weapon_image):
        rocking_speed = 1  # Speed of oscillation
        rocking_angle_range = 4  # Maximum rotation angle (degrees)
        pivot_point = (0, weapon_image.get_height())

        # Calculate the rocking angle using a sine wave
        self.time += self.clock.get_time() / 1000  # Increment time based on frame duration
        rocking_angle = math.sin(self.time * rocking_speed) * rocking_angle_range

        # Rotate the weapon image around the handle
        rotated_weapon, rotated_weapon_rect = rotate_image.rotate_image(weapon_image, pivot_point, rocking_angle)

        # Position the rotated weapon at the player's position, adjusted for pivot
        rotated_weapon_rect.topleft = (position[0] - pivot_point[0], position[1] - pivot_point[1])

        # Draw the rotated weapon
        return rotated_weapon

    def render_equipped_items(self):
        self.player.sprites['idle'].animation_speed = 0.2
        walking_sprite_position_list = [(53, 20) ,(51, 23), (49, 27),(47, 31),(39, 35),(28, 26),(26, 22),(27, 26),(30, 30),(33, 32),(40, 36),(51,23)]
        jumping_sprite_position_list = [(18, 29), (37, 36), (51, 5) ,(52, 5),(53, 8),(53, 13),(52, 21),(47, 30),(47, 31),(47, 36),(50, 45),(34, 36)]
        casting_sprite_position_list = [(31, 43),(32, 43),(34, 43),(35, 43),(27, 41),(21, 38),(27, 41),(33, 44),(29, 44),(28, 47),(29, 46),(30, 34)]


        for item in self.player.inventory.equipment.values():
            if item and self.player.sprites:
                item.position = self.player.position
                image = item.spritesheet.frame_list[int(self.player.animation_index)]

                if self.player.state == "walking" or self.player.state == "running":
                    image = pygame.image.load(item.icon)
                    item.position = [item.position[0] + walking_sprite_position_list[int(self.player.animation_index)][0] - 4,
                                     item.position[1] + walking_sprite_position_list[int(self.player.animation_index)][1] - image.get_height() + 4]
                    if self.player.direction < 0:
                        item.position = [item.position[0] - image.get_width() - self.player.width_buffer + 6, item.position[1]]
                        image = pygame.transform.flip(image, True, False)

                    image = self.rotate_held_item(item.position, image)


                elif self.player.state == "jumping":
                    image = pygame.image.load(item.icon)
                    item.position = [
                        item.position[0] + jumping_sprite_position_list[int(self.player.animation_index)][0] - 2,
                        item.position[1] + jumping_sprite_position_list[int(self.player.animation_index)][1] - image.get_height() + 2]

                    if self.player.direction < 0:
                        item.position = [item.position[0] - image.get_width() - self.player.width_buffer + 4, item.position[1]]
                        image = pygame.transform.flip(image, True, False)

                elif self.player.state == "casting":
                    image = pygame.image.load(item.icon)
                    item.position = [
                        item.position[0] + casting_sprite_position_list[int(self.player.animation_index)][0] + 3,
                        item.position[1] + casting_sprite_position_list[int(self.player.animation_index)][1] - image.get_height() - 2]

                    if self.player.direction > 0:
                        item.position = [item.position[0] - image.get_width() - self.player.width_buffer + 3, item.position[1] - 8]
                        image = pygame.transform.flip(image, True, False)

                else:
                    if self.player.direction < 0:
                        image = pygame.transform.flip(image, True, False)


                self.background.blit(image, item.position)

    def init_hud(self):
        self.hud = hud.HUD(self.player)

    def init_mini_map(self):
        self.minimap = mini_map.Minimap(world_width=SCREEN_WIDTH, world_height=SCREEN_HEIGHT, minimap_size=(150, 150), player=self.player)

    def init_tile_data(self):
        self.tiles = level_files.level_order

    def init_enemies(self):
        self.enemies = {

            'room_0': [enemy.Enemy(self.background,
                                   self.camera,
                                   sprite_paths=enemy_data.ENEMY_DATA[_enemy]["sprite_paths"],
                                   position=enemy_data.ENEMY_DATA[_enemy]["position"],
                                   width=enemy_data.ENEMY_DATA[_enemy]["width"],
                                   height=enemy_data.ENEMY_DATA[_enemy]["height"],
                                   rescale_x=enemy_data.ENEMY_DATA[_enemy]['rescale_x'],
                                   rescale_y=enemy_data.ENEMY_DATA[_enemy]['rescale_y'],
                                   sound_effects=enemy_data.ENEMY_DATA[_enemy]['sound_effects']) for _enemy in
                       enemy_data.ENEMY_DATA][:3],

            # 'room_0': [],

            # 'room_1': [enemy.Enemy(self.background,
            #                        self.camera,
            #                        sprite_paths=enemy_data.ENEMY_DATA[_enemy]["sprite_paths"],
            #                        position=enemy_data.ENEMY_DATA[_enemy]["position"],
            #                        width=enemy_data.ENEMY_DATA[_enemy]["width"],
            #                        height=enemy_data.ENEMY_DATA[_enemy]["height"],
            #                        rescale_x=enemy_data.ENEMY_DATA[_enemy]['rescale_x'],
            #                        rescale_y=enemy_data.ENEMY_DATA[_enemy]['rescale_y'],
            #                        sound_effects=enemy_data.ENEMY_DATA[_enemy]['sound_effects']) for _enemy in
            #            enemy_data.ENEMY_DATA],

            'room_1': [],

            # 'room_2': [enemy.Enemy(self.background,
            #                        self.camera,
            #                        sprite_paths=enemy_data.ENEMY_DATA[_enemy]["sprite_paths"],
            #                        position=enemy_data.ENEMY_DATA[_enemy]["position"],
            #                        width=enemy_data.ENEMY_DATA[_enemy]["width"],
            #                        height=enemy_data.ENEMY_DATA[_enemy]["height"],
            #                        rescale_x=enemy_data.ENEMY_DATA[_enemy]['rescale_x'],
            #                        rescale_y=enemy_data.ENEMY_DATA[_enemy]['rescale_y'],
            #                        sound_effects=enemy_data.ENEMY_DATA[_enemy]['sound_effects']) for _enemy in
            #            enemy_data.ENEMY_DATA]

            'room_2': [],

        }

    def init_doors(self):
        self.doors = {

            "room_0": {"door_1": door.Door(player=self.player,
                                                                x_position=1500 * TILE_SIZE / 32,
                                                                y_position=(SCREEN_HEIGHT) * TILE_SIZE / 32  - 150,
                                                                game=self,
                                                                door_to_level=1,
                                                                player_spawn=(300, SCREEN_HEIGHT - 150))},

            "room_1": {"door_1":door.Door(player=self.player,
                                                   x_position=100 / 32 * GAME_SCALE,
                                                   y_position=(SCREEN_HEIGHT - 150) / 32 * GAME_SCALE,
                                                   game=self,
                                                   door_to_level=0,
                                                   player_spawn=(1300, SCREEN_HEIGHT - 150)),

                       'door_2': door.Door(player=self.player,
                                                                x_position=1500,
                                                                y_position=SCREEN_HEIGHT - 150,
                                                                game=self,
                                                                door_to_level=2,
                                                                player_spawn=(300, SCREEN_HEIGHT - 150)),},



            "room_2": {"door_1":door.Door(player=self.player,
                                                   x_position=1200,
                                                   y_position=SCREEN_HEIGHT - 150,
                                                   game=self),
                       'door_2': door.Door(player=self.player,
                                                                x_position=1200,
                                                                y_position=SCREEN_HEIGHT - 150,
                                                                game=self)},

            "room_3": {"door_1":door.Door(player=self.player,
                                                   x_position=1200,
                                                   y_position=SCREEN_HEIGHT - 150,
                                                   game=self),

                       'door_2': door.Door(player=self.player,
                                                                x_position=1200,
                                                                y_position=SCREEN_HEIGHT - 150,
                                                                game=self)},
        }
        self.door = self.doors[f"room_{self.current_level}"][f"door_{1}"]

    def init_background_images(self):
        self.background_images = {}

    def init_music_files(self):
        self.music_files = {"room_0": DEFAULT_BACKGROUND_MUSIC_PATH + "/Start_Menu.mp3",
                            "room_1": DEFAULT_BACKGROUND_MUSIC_PATH + "/Village_theme.mp3",
                            "room_2": DEFAULT_BACKGROUND_MUSIC_PATH + "/room_2.mp3",
                            "room_3": DEFAULT_BACKGROUND_MUSIC_PATH + "/boss_lobby_theme.mp3",
                            }

    def init_npcs(self):
        self.npcs = {
            'room_0': [npc.Npc(self, "Idle_4.png", (400, SCREEN_HEIGHT - 96))],
            'room_1': [npc.Npc(self, "Idle_4.png", (1200, SCREEN_HEIGHT - 96))],
            'room_2': [npc.Npc(self, "Idle_4.png", (200, SCREEN_HEIGHT - 96))],
            'room_3': [npc.Npc(self, "Idle_4.png", (1500, SCREEN_HEIGHT - 96))]
        }

    def init_items(self):
        self.world_items = {
            'room_0': [item.Item(name='sword of power', slot='Weapon', stats={'attack': 7}, category='weapons', icon="./game_assets/spritesheets/weapons/still_sword.png", spritesheet= "./game_assets/spritesheets/weapons/sword_12.png",position=(400, SCREEN_HEIGHT - 150))],
            'room_1': [item.Item(name='Iron Helmet', slot='Helmet', stats={'defense': 10}, category='helmets', icon="./game_assets/concept_art/helmet_drop.png", position=(400, SCREEN_HEIGHT - 150))],
            'room_2': [item.Item(name='Iron Leggings', slot='Leggings', stats={'defense': 5}, category='leggings', icon="./game_assets/concept_art/pants_drop.png", position=(400, SCREEN_HEIGHT - 150))],
            'room_3': [item.Item(name='Chestplate', slot='Chestplate', stats={'defense': 5}, category='chestplates', icon="./game_assets/concept_art/chestplate_drop.png", position=(400, SCREEN_HEIGHT - 150))],
        }

    def init_weapons(self):
        self.weapons = {
            'sword': spritesheet.SpriteSheet("./game_assets/spritesheets/weapons/sword_12.png"),
            'axe': spritesheet.SpriteSheet("./game_assets/spritesheets/weapons/axe_12.png")
        }

    def init_world(self):
        self.init_tile_data()
        self.init_enemies()
        self.init_doors()
        self.init_background_images()
        self.init_music_files()
        self.init_npcs()
        self.init_items()

        self.world_data = {
            "tile_data": self.tiles,
            "enemy_data": self.enemies,
            "door_data": self.doors,
            "background_data": self.background_images,
            "music_data": self.music_files,
            "npc_data": self.npcs,
            "item_data": self.world_items,
        }

    def select_music(self):
        pygame.mixer.music.load(self.world_data['music_data'][f"room_{self.current_level}"])
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.0)

    def select_npcs(self):
        self.current_npcs = self.world_data['npc_data'][f"room_{self.current_level}"]

    def select_enemies(self):
        self.enemies = self.world_data['enemy_data'][f"room_{self.current_level}"]
        state_machine.initialize_state_machine(self.enemies)

    def select_items(self):
        self.room_items = self.world_data['item_data'][f"room_{self.current_level}"]

    def load_room(self):
        self.select_enemies()
        self.select_music()
        self.select_npcs()
        self.select_items()

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

            for npc in self.current_npcs:
                npc.event_checker(event)

    def update_game(self):
        self.player.render(self.background)
        self.render_equipped_items()

        #self.background.blit(self.background_image, (0, 0))
        self.render_doors()

        #self.render_shader_effects()

        for _enemy in self.enemies:
            _enemy.render(self.player)

        for projectile in self.player.projectiles:
            projectile.run(self.background, self.enemies)

        display_tile_sets(self.background, self.tile_set)
        # self.hitbox_debugging()
        # self.optimized_tile_display()



        for item in self.room_items:
            if item.is_picked_up(self.player):
                self.room_items.remove(item)
            else:
                collision_set = physics.tile_optimizer(item, self.player.tile_set, TILE_SIZE)
                physics.gravity(item , 0.00001)
                physics.update_kinematics(item)
                physics.resolve_collision(item, collision_set)
                item.display(self.background)

        # self.camera.render_parallax(self.screen, background_layers)
        self.render_npcs()
        self.camera.apply_offset(self.screen, self.background)

        for npc in self.current_npcs:
            npc.interact_with_player(self.player, self.screen)

        self.camera.update()

    def render_npcs(self):
        for npc in self.current_npcs:
            npc.render_npc(self.player, self.background)

    def render_doors(self):
        for door in self.doors[f"room_{self.current_level}"].values():
            door.display_objective(self.background)
            door.check_objective_collision()

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

    def hitbox_debugging(self):
        projected_x = self.player.position[0] + self.player.velocity[0]
        if self.player.direction > 0:
            self.player.x_collision_hitbox = (
            projected_x + self.player.width // 2, self.player.position[1] + 3,
            self.player.width_buffer, self.player.height * .7)
        else:
            self.player.x_collision_hitbox = (
            projected_x + self.player.width // 2 - self.player.width_buffer,
            self.player.position[1] + 3,
            self.player.width_buffer, self.player.height * .7)

        pygame.draw.rect(self.background, (255, 0, 0), self.player.x_collision_hitbox)

    def optimized_tile_display(self):
        player = self.player
        tile_set = self.player.tile_set
        x_index = (player.position[0] + player.width // 2) // TILE_SIZE
        feet_y_index = (player.position[1] + player.height - TILE_SIZE) // TILE_SIZE
        head_y_index = (player.position[1] // TILE_SIZE)
        floor_index = feet_y_index + 1
        projected_y = player.position[1] + player.velocity[1]

        if not tile_set[int(floor_index)][int(x_index)].is_collidable:
            player.is_touching_ground = False

        collidable_set = [tile_set[int(head_y_index + y)][int(x_index + x)] for x in range(-1, 2) for y
                in
                range(-1, int(player.height // TILE_SIZE + 1)) if
                tile_set[int(head_y_index + y)][int(x_index + x)].is_collidable]
        for rect in collidable_set:
            pygame.draw.rect(self.background, (0, 255, 0), rect.rect)


    def render_fps(self):
        fps_text = self.font.render(f"FPS: {self.clock.get_fps():.0f}", True, (255, 255, 255))
        fps_text_rect = fps_text.get_rect()
        self.screen.blit(fps_text, fps_text_rect)

    def run(self):
        while self.running:
            self.background.fill((70,70,70))

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
                self.render_fps()
                self.render_hud()
                # self.game_shader.apply_vignette(0.9)
                self.minimap.render(self.screen, self.enemies, self.room_items)
                self.game_shader.update_textures([self.screen])
                self.game_shader.render()
                pygame.display.flip()

            self.clock.tick(self.fps_cap)
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()