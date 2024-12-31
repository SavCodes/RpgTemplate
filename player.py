import pygame
import spritesheet
import physics
import particle
from class_data import background_data
from config import *
from physics import KinematicObject

blood_effect = particle.BloodSpurtEffect()


class LivingEntity:
    def __init__(self, sprite_sheet_paths, frame_width, frame_height, max_health=100, max_mana=100, rescale_x=None, rescale_y=None, sound_effects=None, name="TEST_NAME", scale=GAME_SCALE):

        self.config = {
            "scale": scale,
            "controls": [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s],
            "sprint_speed": 3,
            "gravity_value": 0.02,
            "x_move_acceleration": 0.08 * scale,
            "x_speed_cap": 3 * scale,
            "y_speed_cap": 3 * scale,
            "max_jumps": 2,
        }
        self.init_starting_states()
        self.init_stats(max_health, max_mana)
        self.damage_multiplier = 1
        self.debuff_effects = []
        self.sound_effects = sound_effects
        self.alpha = 255
        self.jump_height = 5
        self.level = 0
        self.name = name
        self.load_sprite_sheets(sprite_sheet_paths,
                                frame_width=frame_width,
                                frame_height=frame_height,
                                rescale_x=rescale_x,
                                rescale_y=rescale_y)
        try:
            self.sprites['spell_cast'].animation_speed = 0.15
        except KeyError as e:
            print(e)


    def load_sprite_sheets(self, paths, frame_width, frame_height, x_offset=0, y_offset=0, rescale_x=64, rescale_y=64):
        self.sprites = {
            name: spritesheet.SpriteSheet(path,
                                          frame_width=frame_width,
                                          frame_height=frame_height,
                                          scale=GAME_SCALE,
                                          y_offset=y_offset,
                                          x_offset=x_offset)

            for name, path in paths.items()
        }
        if rescale_x is not None and rescale_y is not None:
            for animation in self.sprites.values():
                animation.rescale_frames(rescale_x, rescale_y)

    def init_stats(self, max_health, max_mana):
        self.stats = {
            # RAW ATTRIBUTES
            'strength': 0,
            'dexterity': 0,
            'intelligence': 0,

            # EXPERIENCE
            "current_experience": 0,
            "max_experience": 100,
            "skill_points": 0,

            # HEALTH
            "max_health": max_health,
            "current_health": max_health,
            "life_steal": 0,

            # MANA
            "max_mana": max_mana,
            "current_mana": max_mana,
            "mana_regen": 0,
            "mana_recharge": 0,

            # COMBAT
            "speed": 0,
            "attack": 0,
            "defense": 0,
            "damage_multiplier": 1,
            "damage_reduction": 0,
            "critical_chance": 0,
            "critical_damage": 0,
            "poison_damage": 0,
            "poison_duration": 0,
            "healing": 0,
                }
        self.update_display_stats()

    def update_display_stats(self):
        self.display_stats = {
            "Attributes":{
                'current_health': self.stats['current_health'],
                'current_mana': self.stats['current_mana'],
                'current_experience': self.stats['current_experience'],
                "Strength": self.stats['strength'],
                "Dexterity": self.stats['dexterity'],
                "Intelligence": self.stats['intelligence'],
                'max_health': self.stats['max_health'],
                'max_mana': self.stats['max_mana'],
                'max_experience': self.stats['max_experience'],
            },
            "Combat": {
                'attack': self.stats['attack'],
                'defense': self.stats['defense'],
                'speed': self.stats['speed'],
            }
        }

    def init_starting_states(self):
        self.is_alive = True
        self.is_shielded = False
        self.is_attacking = False
        self.is_spell_casting = False
        self.is_sliding = False

    def take_damage(self, damage):
        self.stats['current_health'] = max(self.stats['current_health'] - damage, 0)
        #self.state_machine.state = 'hit'

    def regenerate_mana(self, regenerated_mana):
        self.stats['current_mana'] = min(self.stats['current_mana'] + regenerated_mana, self.stats['max_mana'])

    def respawn(self, spawn_position):
            self.stats['current_health'] = self.stats['max_health']
            self.position[0], self.position[1] = spawn_position
            self.acceleration[0], self.acceleration[1] = 0, 0

    def apply_status_effect(self, effect, damage, duration):
        if effect == "bleed":
            print("I am bleeding")

    def die(self):
        self.is_alive = False
        self.velocity = [0, 0]
        self.acceleration = [0, 0]
        self.acceleration = [0, 0]
        blood_effect.update()
        blood_effect.render(self.screen)

        try:
            if self.sound_effects is not None and self.sprites['death'].animation_index == 1:
                self.sound_effects['death'].play()
                blood_effect.emit(self.position[0] + self.width // 2 , self.position[1] + self.height // 2)
        except AttributeError as e:
            print("Error: ", e)

    def gain_experience(self, experience):
        self.stats['current_experience'] += experience
        self.level_up()

    def level_up(self):
        if self.stats['current_experience'] >= self.stats['max_experience']:
            self.level += 1
            self.stats['current_experience'] -= self.stats['max_experience']
            self.stats['max_experience'] = self.stats['max_experience'] * 1.25
            self.stats['skill_points'] += 1
            self.stats['max_health'] += 10
            self.stats['max_mana'] += 10

            self.init_starting_states()
            if self.sound_effects is not None:
                self.sound_effects['levelup'].play()

class Player(physics.KinematicObject, LivingEntity):
    def __init__(self, sprite_sheet, frame_width, frame_height, game_class, background, scale=GAME_SCALE, screen=None, name='PLAYER_ONE'):
        KinematicObject.__init__(self, (300, 300), width=frame_width, height=frame_height, scale=scale)
        LivingEntity.__init__(self,
                              sprite_sheet,
                              frame_width=frame_width,
                              frame_height=frame_height,
                              max_health=game_class['health'],
                              max_mana=game_class['mana'],)

        # Player configurations
        self.config = {
            "scale": scale,
            "controls": [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s],
            "sprint_speed": 3,
            "gravity_value": 0.02,
            "x_move_acceleration": 0.08 * scale,
            "x_speed_cap": 3 * scale,
            "y_speed_cap": 3 * scale,
            "max_jumps": 2,
        }

        # Game data
        self.screen = screen
        self.name = name
        self.game_class = game_class
        self.background = background_data.backgrounds[background]
        self.abilities = game_class['abilities']
        self.mana_color = game_class['mana_color']
        self.mana_regen = game_class['mana_regen']
        # Initialize player dimensions
        self.width_buffer = self.width // 4
        self.total_tile_height = self.height // TILE_SIZE

        # State and effects
        self.image = None
        self.is_touching_ground = False
        self.level_completed = False
        self.projectiles = []
        self.current_level = 1
        self.jump_count = 0
        self.max_jumps = 2
        self.state = 'jumping'
        self.sound_effects = {
            'levelup': pygame.mixer.Sound('./game_assets/sound_assets/level_up.mp3'),
        }
        self.effects = {
            'experience': particle.ExperienceEffect(self),
            'blood': particle.BloodSpurtEffect(),
        }


    def render(self, screen):
        self.handle_logic()
        self.handle_display(screen)

    def jump_player(self):
        self.is_touching_ground = False
        if self.jump_count < self.max_jumps:
            self.jump_count += 1
            self.acceleration[1] = 0
            self.velocity[1] = -self.jump_height * self.config['scale']

    def jump_behavior(self):
        # Animate rising part of jump
        if self.velocity[1] < 0 and self.sprites['jump'].animation_index > 6:
            self.sprites['jump'].animation_index = 6

        # Animate falling part of jump
        elif self.velocity[1] > 0 and self.sprites['jump'].animation_index >= self.sprites['jump'].number_of_animations - 1:
            self.sprites['jump'].animation_index = self.sprites['jump'].number_of_animations - 1

        elif self.is_touching_ground:
            self.jump_count = 0
            self.change_state("idling")

    def handle_logic(self):
        self.get_player_movement()
        self.update()
        self.regenerate_mana(self.mana_regen)

        collision_set = physics.tile_optimizer(self, self.tile_set, TILE_SIZE)
        physics.gravity(self, self.config["gravity_value"])
        physics.update_kinematics(self, 10, 10, 5, 2)
        physics.resolve_collision(self, collision_set)

    def handle_display(self, screen):
        self.animate(screen)
        self.display_abilities(screen)

    def update(self):
        # Process states
        self.rect = pygame.Rect(self.position[0], self.position[1], self.width, self.height)

        if self.state == 'dying':
            self.death_behavior()
        elif self.state == 'casting':
            self.casting_behavior()
        elif self.state == "jumping":
            self.jump_behavior()
        elif self.state == 'sliding':
            self.slide_behavior()
        elif self.state == 'walking':
            self.walking_behavior()
        elif self.state == 'running':
            self.running_behavior()


        if self.is_touching_ground:
            self.sprites['jump'].animation_index = 0

    def animate(self, screen):
        self.animation_map = {
            "idling": "idle",
            'walking': 'walk',
            'running': 'run',
            "attacking": "attack",
            "dying": "death",
            "rooted": "idle",  # Use idle animation for the rooted state
            "slowed": "walk", # Use the walk animation when put into a slowed state
            "sliding": "slide",
            "casting": "spell_cast",
            "jumping": "jump",
        }
        anim_key = self.animation_map.get(self.state)
        if anim_key:
            self.frame_to_display, self.animation_index = self.sprites[anim_key].basic_animate()

        # Flip and blit the frame
        if self.direction < 0:
            self.frame_to_display = pygame.transform.flip(self.frame_to_display, True, False)

        screen.blit(self.frame_to_display, self.position)

    def death_behavior(self):
        if self.sprites["death"].animation_index >= self.sprites["death"].number_of_animations - 1:
            self.respawn([self.x_spawn, self.y_spawn])
            self.change_state("idling")

        self.velocity = [0,0]
        self.acceleration = [0,0]

    def slide_behavior(self):
        if self.sprites['slide'].animation_index >= self.sprites['slide'].number_of_animations - 1:
            self.change_state("walking")
            self.velocity[0] = 6 * self.direction
            self.sprites['slide'].reset_animation()
        else:
            self.velocity[0] = 0
            self.position[0] += 6 * self.direction

    def walking_behavior(self):
        if abs(self.velocity[0]) > self.config['sprint_speed']:
            self.change_state("running")

        if self.is_touching_ground and self.velocity[0] == 0:
            self.change_state("idling")

    def running_behavior(self):
        if abs(self.velocity[0]) < self.config['sprint_speed']:
            self.change_state("walking")

    def casting_behavior(self):
        if self.sprites['spell_cast'].animation_index >= self.sprites['spell_cast'].number_of_animations - 1:
            self.change_state("idling")

    def display_abilities(self, screen):
        for ability in self.abilities:
            if ability.is_active:
                ability.effect()

    def change_state(self, state):
        if self.state != state:
            self.sprites[self.animation_map[state]].reset_animation()
            print(f"State changed from {self.state} to {state}")
            self.state = state

    def get_player_movement(self):
        keys = pygame.key.get_pressed()
        self.jump_count = 0 if self.is_touching_ground else self.jump_count

        if keys[self.config["controls"][0]] and self.velocity[0] <= 0:
            self.acceleration[0] = -self.config["x_move_acceleration"]
            if self.is_touching_ground and self.state != "sliding" and self.state != "running":
                self.change_state("walking")

        elif keys[self.config["controls"][1]] and self.velocity[0] >= 0:
            self.acceleration[0] = self.config["x_move_acceleration"]
            print("Fill in a slide to stop animation here")
            if self.is_touching_ground and self.state != "sliding" and self.state != "running":
                self.change_state("walking")

        else:
            self.slide_on_stop()

    def slide_on_stop(self):
        slide_strength = 0.3
        if abs(self.velocity[0]) < 1:
            self.velocity[0] = 0
            self.acceleration[0] = 0
            # if self.is_touching_ground and self.state != "sliding" and self.state != "casting":
            #     self.change_state("idling")

        elif self.velocity[0] > 0:
            self.acceleration[0] = -slide_strength
        elif self.velocity[0] < 0:
            self.acceleration[0] = slide_strength
