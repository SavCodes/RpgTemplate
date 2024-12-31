import pygame
import random

class StateMachine:
    def __init__(self, owner):
        self.owner = owner
        self.state = "idling"
        self.effects = {}

    def update(self, player, screen):
        # Handle external states like dying
        self.get_external_based_states()

        # Process active effects
        self.update_effects()

        # Process states
        if self.state == 'dying':
            self.death_behaviour(player)
        elif self.state == "rooted":
            self.rooted_behavior()
        elif self.state == "slowed":
            self.slowed_behavior()
        self.animate()

    def change_state(self, new_state):
        if self.state != new_state:
            #print(f"State changed from {self.state} to {new_state}")
            self.state = new_state

    def apply_effect(self, effect_name, duration):
        """Apply a temporary effect to the enemy."""
        self.effects[effect_name] = duration
        if effect_name == "slowed":
            self.change_state("slowed")
        if effect_name == "rooted":
            self.change_state("rooted")

    def update_effects(self):
        """Update and manage the durations of active effects."""
        effects_to_remove = []
        for effect, duration in self.effects.items():
            if duration > 0:

                self.effects[effect] -= 1
            else:
                effects_to_remove.append(effect)

        for effect in effects_to_remove:
            del self.effects[effect]
            if not self.effects:
                if effect == "slowed":
                    self.change_state('idling')
                if effect == "rooted":
                    self.change_state("idling")  # Resume normal behavior when the root effect ends
            else:
                print("Changing state to: ", list(self.effects.items())[0][0])
                self.change_state(list(self.effects.items())[0])

    def animate(self):
        animation_map = {
            "idling": "walk",
            "chasing": "walk",
            "attacking": "attack",
            "dying": "death",
            "rooted": "idle",  # Use idle animation for the rooted state
            "slowed": "walk" # Use the walk animation when put into a slowed state
        }
        anim_key = animation_map.get(self.state)
        if anim_key:
            self.frame_to_display, self.animation_index = self.owner.sprites[anim_key].basic_animate()

        # Flip and blit the frame
        if self.owner.direction < 0:
            self.frame_to_display = pygame.transform.flip(self.frame_to_display, True, False)
        self.owner.screen.blit(self.frame_to_display, self.owner.position)

    def rooted_behavior(self):
        """Behavior for the 'Rooted' state."""
        self.owner.velocity = [0, 0]  # Halt movement immediately
        pass

    def slowed_behavior(self):
        """Behavior for the 'Slowed' state."""
        print("Enemy velocity changed from: ", self.owner.velocity)
        self.owner.velocity = [self.owner.original_move_speed * 0.4 , self.owner.original_move_speed * 0.4]
        print("To: ", self.owner.velocity)

    def death_behaviour(self, player):
        if self.owner.sprites['death'].animation_index >= self.owner.sprites['death'].number_of_animations - 1:
            self.owner.respawn(self.owner.spawn_position)
            self.owner.sprites['death'].reset_animation()
            self.change_state("idling")

        # Emit experience particles when an enemy dies
        elif self.owner.sprites['death'].animation_index == 1:
            player.experience_effect.emit(self.owner.position[0], self.owner.position[1], self.owner.experience, count=15)
            player.effects['blood'].emit(self.owner.position[0], self.owner.position[1])
            self.owner.game_camera.shake()

    def get_external_based_states(self):
        if self.owner.stats['current_health'] <= 0:
            self.change_state('dying')
            self.owner.is_alive = False




class EnemyStateMachine:
    def __init__(self, enemy, vision_radius=200):
        self.state = "idling"
        self.enemy = enemy
        self.original_vision_radius = vision_radius
        self.vision_radius = vision_radius
        self.effects = {}

    def update(self, player, screen):
        # Handle external states like dying
        self.get_external_based_states()

        # Process active effects
        self.update_effects()

        # Process states
        if self.state == 'dying':
            self.death_behaviour(player)
        elif self.state == "rooted":
            self.rooted_behavior()
        elif self.state == 'hit':
            self.hit_behavior()
        elif self.state == "idling":
            self.idle_behavior(player, screen)
        elif self.state == "chasing":
            self.chase_behaviour(player, screen)
        elif self.state == "attacking":
            self.attack(player)
        elif self.state == "slowed":
            self.slowed_behavior()
        self.animate()

    def change_state(self, new_state):
        if self.state != new_state:
            print(f"State changed from {self.state} to {new_state}")
            self.state = new_state

    def apply_effect(self, effect_name, duration):
        """Apply a temporary effect to the enemy."""
        self.effects[effect_name] = duration
        if effect_name == "rooted":
            self.change_state("rooted")
        if effect_name == "slowed":
            self.change_state("slowed")


    def update_effects(self):
        """Update and manage the durations of active effects."""
        effects_to_remove = []
        for effect, duration in self.effects.items():
            if duration > 0:

                self.effects[effect] -= 1
            else:
                effects_to_remove.append(effect)

        for effect in effects_to_remove:
            del self.effects[effect]
            if not self.effects:
                if effect == "slowed":
                    self.change_state('idling')
                if effect == "rooted":
                    self.change_state("idling")  # Resume normal behavior when the root effect ends
            else:
                print("Changing state to: ", list(self.effects.items())[0][0])
                self.change_state(list(self.effects.items())[0])

    def animate(self):
        animation_map = {
            "idling": "walk",
            "chasing": "walk",
            "attacking": "attack",
            "dying": "death",
            "rooted": "idle",  # Use idle animation for the rooted state
            "slowed": "walk", # Use the walk animation when put into a slowed state
            "hit" : "hit"
        }
        anim_key = animation_map.get(self.state)
        if anim_key:
            self.frame_to_display, self.animation_index = self.enemy.sprites[anim_key].basic_animate()

        # Flip and blit the frame
        if self.enemy.direction < 0:
            self.frame_to_display = pygame.transform.flip(self.frame_to_display, True, False)
        self.enemy.screen.blit(self.frame_to_display, self.enemy.position)

    def hit_behavior(self):
        self.velocity = [0, 0]

        if self.enemy.sprites['hit'].animation_index >= self.enemy.sprites['hit'].number_of_animations - 1:
            self.change_state("idling")
            self.enemy.sprites['hit'].reset_animation()

    def rooted_behavior(self):
        """Behavior for the 'Rooted' state."""
        print("I have been rooted!")
        self.enemy.velocity = [0, 0]  # Halt movement immediately
        pass

    def slowed_behavior(self):
        """Behavior for the 'Slowed' state."""
        # print("Enemy velocity changed from: ", self.enemy.velocity)
        # self.enemy.velocity = [self.enemy.original_move_speed * 0.4 , self.enemy.original_move_speed * 0.4]
        # print("To: ", self.enemy.velocity)
        pass

    def idle_behavior(self, player, screen):
        if self.target_in_range(player, screen, vision_radius=200) and player.alpha == 255:
            self.change_state("chasing")
        else:
            self.enemy.is_attacking = False
            self.idle_wander(range=200, speed=self.enemy.move_speed)

    def chase_behaviour(self, player, screen):
        self.move_towards(player, speed=self.enemy.move_speed)
        if self.target_in_range(player, screen, vision_radius=50) and player.alpha == 255:
            self.change_state("attacking")

        elif self.target_in_range(player, screen, vision_radius=50):
            self.change_state("idle")

    def death_behaviour(self, player):
        if self.enemy.sprites['death'].animation_index >= self.enemy.sprites['death'].number_of_animations - 1:
            self.enemy.respawn(self.enemy.spawn_position)
            self.enemy.sprites['death'].reset_animation()
            self.change_state("idling")

        # Emit experience particles when an enemy dies
        elif self.enemy.sprites['death'].animation_index == 1:
            player.effects["experience"].emit(self.enemy.position[0], self.enemy.position[1], self.enemy.experience, count=15)
            player.effects['blood'].emit(self.enemy.position[0], self.enemy.position[1])
            self.enemy.game_camera.shake()

        else:
            player.effects['experience'].update()
            player.effects['experience'].render(self.enemy.screen)

            player.effects['blood'].update()
            player.effects['blood'].render(self.enemy.screen)

            self.enemy.velocity = [0, 0]
            self.enemy.acceleration = [0, 0]
            self.enemy.die()

    def idle_wander(self, range, speed):
        if random.random() < 0.01:  # 1% chance to switch direction per frame
            self.enemy.direction *= -1

        if self.enemy.spawn_position[0] - range < self.enemy.position[0] < self.enemy.spawn_position[0] + range:
            self.enemy.velocity[0] = speed * self.enemy.direction
        else:
            self.enemy.direction *= -1
            self.enemy.velocity[0] = speed * self.enemy.direction

    def attack(self, player):
        """Handle the attack logic for the enemy."""
        # If the attack animation is complete, reset and switch state
        if self.enemy.sprites['attack'].animation_index >= self.enemy.sprites['attack'].number_of_animations - 1:
            self.enemy.sprites['attack'].reset_animation()
            self.enemy.is_attacking = False
            self.change_state(
                "chasing" if self.target_in_range(player, self.enemy.screen, vision_radius=50) else "idling")
            return

        # Execute the attack and check for damage to the player
        if not self.enemy.is_attacking:
            self.enemy.is_attacking = True
            if self.target_in_range(player, self.enemy.screen, vision_radius=50):
                damage_modifier = 0 if player.is_shielded else 1
                player.take_damage(self.enemy.attack_damage * damage_modifier)
                #self.enemy.sound_effects['attack'].play()

        # Halt movement during the attack
        self.enemy.velocity = [0, 0]

    def target_in_range(self, target, screen, vision_radius=200, angle=60):
        center_of_vision = pygame.math.Vector2(self.enemy.position[0] + self.enemy.width // 2,
                                               self.enemy.position[1] + self.enemy.height // 2)
        direction = pygame.math.Vector2(self.enemy.direction, 0)
        target_vector = pygame.math.Vector2(target.position[0] + target.width // 2,
                                            target.position[1] + target.height // 2) - center_of_vision

        in_range = vision_radius > target_vector.magnitude()
        within_angle = direction.angle_to(target_vector) < angle / 2
        return in_range and within_angle

    def move_towards(self, target, speed=2):
        x_direction = 1 if target.position[0] - self.enemy.position[0] > 0 else -1
        y_direction = 1 if target.position[0] - self.enemy.position[0] > 0 else -1
        self.enemy.velocity[0] = x_direction * speed

    def get_external_based_states(self):
        if self.enemy.stats['current_health'] <= 0:
            self.change_state('dying')
            self.enemy.is_alive = False

class BossStateMachine(EnemyStateMachine):
    def __init__(self, boss, vision_radius=400):
        super().__init__(boss, vision_radius)
        self.phase_shift_chance = 0.05  # 5% chance per frame to use Phase Shift

    def update(self, player, screen):
        super().update(player, screen)

        # Additional logic for Phase Shift
        if self.state != 'dying' and random.random() < self.phase_shift_chance:
            self.enemy.phase_shift(player)

    def animate(self):
        print("using boss animate path")
        animation_map = {
            "idling": "hover",
            "chasing": "hover",
            "attacking": "smash",
            "dying": "disintegrate",
            "rooted": "hover",
        }
        anim_key = animation_map.get(self.state)
        if anim_key:
            self.frame_to_display, self.animation_index = self.enemy.sprites[anim_key].basic_animate()

        # Flip and blit the frame
        if self.enemy.direction < 0:
            self.frame_to_display = pygame.transform.flip(self.frame_to_display, True, False)
        self.enemy.screen.blit(self.frame_to_display, self.enemy.position)

def initialize_state_machine(enemy_list):
    for enemy in enemy_list:
        enemy.state_machine = EnemyStateMachine(enemy)
