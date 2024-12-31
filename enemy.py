import pygame
import spritesheet
import physics
import random
from player import LivingEntity
from config import *

class Enemy(physics.KinematicObject, LivingEntity):
    def __init__(self, screen, game_camera, position, sprite_paths, rescale_x, rescale_y, attack_damage=5, max_health=100, width=32, height=32, experience=1000, sound_effects=None):
        physics.KinematicObject.__init__(self, position, width=width, height=height, scale=GAME_SCALE)
        LivingEntity.__init__(self, sprite_paths,frame_width=width, frame_height=height, rescale_x=rescale_x, rescale_y=rescale_y, max_health=max_health, sound_effects=sound_effects)

        self.is_touching_ground = False
        self.is_alive = True
        self.screen = screen
        self.rescale_size = 64
        self.game_camera = game_camera
        self.attack_damage = attack_damage
        self.experience = experience

        # LOADING IN TEST SPRITESHEETS
        self.width = self.rescale_size
        self.height = self.rescale_size
        self.width_buffer = 0
        self.total_tile_height = self.height // TILE_SIZE

        # WANDERING AND PLAYER DETECTION
        self.original_vision_radius = 300
        self.vision_radius = self.original_vision_radius
        self.attack_radius = 50
        self.wander_speed = 1
        self.move_speed = 3
        self.original_move_speed = 3

        self.vision_color = "red"
        self.attack_color = "black"

        # HEALTH INSTANTIATION
        self.max_speed = 7
        self.max_force = 0.1

        # VECTOR INSTANTIATION
        self.spawn_position = pygame.math.Vector2(position)
    # =================================== LOGIC METHODS ==========================================
    def render(self, player):
        # Logic
        self.state_machine.update(player, self.screen)
        collision_tiles = physics.tile_optimizer(self, player.tile_set, 32)
        physics.gravity(self, 0.05)
        physics.update_kinematics(self, 10, 20, 2 ,2)
        physics.resolve_collision(self, collision_tiles)
        # Display
        self.display_health()
        #self.display_debugs()

    # =================================== DISPLAY METHODS ==========================================
    def display_debugs(self):
        self.display_ranges()
        self.display_health()
    def display_ranges(self):
        # VISION RANGE
        center_of_vision = (self.position[0] + self.width // 2, self.position[1] + self.height // 2)
        pygame.draw.circle(self.screen, self.vision_color, center_of_vision, self.vision_radius, 2)

        # ATTACK RANGE
        pygame.draw.circle(self.screen, self.attack_color, center_of_vision, self.attack_radius, 2)
    def display_health(self):
        # Health Bars
        pygame.draw.rect(self.screen, "black", (self.position[0] + self.width//2 - self.stats['max_health'] / 2 - 1, self.position[1] - 1, self.stats['max_health'] + 2, 9))
        pygame.draw.rect(self.screen, "red", (self.position[0] + self.width//2 - self.stats['current_health'] / 2, self.position[1], self.stats['current_health'], 7))

class Boss(Enemy):
    def __init__(self, screen, game_camera, position, sprite_paths, attack_damage=10, max_health=500, width=64, height=64, experience=100, sound_effects=None):
        super().__init__(screen, game_camera, position, sprite_paths, attack_damage, max_health, width, height, experience, sound_effects)
        self.phase_shift_cooldown = 300  # Cooldown in frames (e.g., 5 seconds at 60 FPS)
        self.phase_shift_timer = 0
        self.energy_burst_radius = 100  # Radius of the AoE damage upon reappearing

    def render(self, player):
        print(self.phase_shift_timer)
        if self.phase_shift_timer > 0:
            self.phase_shift_timer -= 1
        else:
            self.phase_shift(player)
        super().render(player)

    def phase_shift(self, player):
        if self.phase_shift_timer <= 0:
            print('casting phase shift')
            # Teleport to a random location within vision radius
            new_position = self.get_random_position_within_radius(self.vision_radius)
            self.position = new_position
            self.phase_shift_timer = self.phase_shift_cooldown

            # Create an energy burst that damages the player
            distance_to_player = pygame.math.Vector2(self.position).distance_to(player.position)
            if distance_to_player <= self.energy_burst_radius:
                damage_modifier = 0 if player.is_shielded else 1
                player.take_damage(self.attack_damage * damage_modifier)

            # Visual feedback for the energy burst
            pygame.draw.circle(self.screen, "purple", (int(self.position[0]), int(self.position[1])), self.energy_burst_radius, 2)

    def get_random_position_within_radius(self, radius):
        # Generate a random position within the boss's vision radius
        x_offset = random.randint(-radius, radius)
        y_offset = random.randint(-radius, radius)
        new_x = max(0, min(self.spawn_position[0] + x_offset, SCREEN_WIDTH - self.width))
        new_y = max(0, min(self.spawn_position[1] + y_offset, SCREEN_HEIGHT - self.height))
        return pygame.math.Vector2(new_x, new_y)



