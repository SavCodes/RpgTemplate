import numpy as np
import pygame
import time
import physics
import shader
import random
import spritesheet
import fireball_effect
import lightning_effect as l_effect

import math

from config import DEFAULT_TEXT_COLOR, DEFAULT_ABILITY_IMAGE_PATH, DEFAULT_FONT, DEFAULT_ABILITY_SOUND_FX_PATH, \
    SCREEN_WIDTH, SCREEN_HEIGHT

pygame.init()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
FONT = pygame.font.Font(DEFAULT_FONT, 20)

# ============================ UPGRADE TREE CLASSES ==========================================
class SkillNode:
    def __init__(self, x, y, name, description, prerequisite=None, effect=None, cost=1):
        self.x = x
        self.y = y
        self.radius = 20
        self.name = name
        self.description = description
        self.prerequisite = prerequisite
        self.unlocked = False
        self.effect = lambda: effect()
        self.cost = cost

    def draw(self, screen, unlocked, hover=False):
        color = GREEN if unlocked else RED
        if hover:
            color = BLUE
        pygame.draw.circle(screen, color, (self.x, self.y), self.radius)
        label = FONT.render(self.name, True, WHITE)
        screen.blit(label, (self.x - label.get_width() // 2, self.y - self.radius - 25))

    def is_hovered(self, mouse_pos):
        return ((self.x - mouse_pos[0]) ** 2 + (self.y - mouse_pos[1]) ** 2) ** 0.5 <= self.radius

class SkillConnection:
    def __init__(self, node1, node2):
        self.node1 = node1
        self.node2 = node2

    def draw(self, screen):
        color = GREEN if self.node1.unlocked and self.node2.unlocked else GRAY
        pygame.draw.line(screen, color, (self.node1.x, self.node1.y), (self.node2.x, self.node2.y), 3)

class SkillMenu:
    def __init__(self,screen, player, ability, background_image="./game_assets/concept_art/enemy_in_the_station.webp"):
        self.player = player
        self.upgrade_nodes = ability.upgrade_nodes
        self.upgrade_connections = ability.upgrade_connections
        self.screen = screen
        self.is_running = False
        self.background_image = pygame.image.load(ability.background_image).convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, self.screen.get_size())

    def run(self, _):
        # Draw connections
        self.is_running = True
        self.event_checker()
        self.screen.blit(self.background_image, (0, 0))
        self.mouse_pos = pygame.mouse.get_pos()
        for connection in self.upgrade_connections:
            connection.draw(self.screen)

        # Draw skill points
        skill_points_label = FONT.render(f"Skill Points: {self.player.stats['skill_points']}", True, WHITE)
        self.screen.blit(skill_points_label, (10, 10))

        # Draw nodes
        hover_list = []
        for node in self.upgrade_nodes:
            hover = node.is_hovered(self.mouse_pos)
            node.draw(self.screen, node.unlocked, hover)

            # Display tooltip on hover
            if hover:
                description_label = FONT.render(node.description, True, WHITE)
                hover_list.append(node)

        if hover_list != []:
            self.screen.blit(description_label, (self.mouse_pos[0] + 15, self.mouse_pos[1] + 15))


    def node_event_handler(self):
        for node in self.upgrade_nodes:
            if node.is_hovered(self.mouse_pos):
                if not node.unlocked and self.player.stats['skill_points'] >= node.cost:
                    if not node.prerequisite or any(n.name == node.prerequisite and n.unlocked for n in self.upgrade_nodes):
                        node.unlocked = True
                        self.player.stats['skill_points'] -= node.cost
                        node.effect()

    def event_checker(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                self.node_event_handler()
        return True

class Ability:
    def __init__(self, name, damage=0, cost=0, cooldown=0, sound_fx=None, activate=None, effect=None):
        self.name = name
        self.font = pygame.font.Font(DEFAULT_FONT, 30)
        self.damage = damage
        self.cost = cost
        self.init_cooldown(cooldown)
        self.level = 0
        self.sound_fx = sound_fx
        self.is_active = False
        self.is_animating = False
        self.effect = effect
        self.activate = activate
        self.render_effect = None

    def init_cooldown(self, cooldown):
        self.cooldown = cooldown
        self.last_used = 0
        self.current_time = 0

    def init_ability_icons(self, name):
        self.icon = pygame.image.load(DEFAULT_ABILITY_IMAGE_PATH + self.ability_class + f"/{name}_icon.png").convert_alpha()
        self.icon = pygame.transform.scale(self.icon, (50, 50))
        self.icon_surface = pygame.Surface(self.icon.get_size())

    def can_use(self):
        """Check if the ability can be used based on cooldown."""
        self.current_time = time.time()
        return self.current_time - self.last_used >= self.cooldown

    def apply(self, player, **kwargs):
        """Activate the ability."""
        # Check mana and cooldown
        if player.current_mana < self.cost:
            print("Not enough mana")
            return
        if not self.can_use():
            print("Ability is on cooldown")
            return

        # Deduct mana and start cooldown
        player.current_mana -= self.cost
        self.last_used = time.time()

        # Play sound and set active state
        if self.sound_fx:
            self.sound_fx.play()

    def update(self):
        """Handle ongoing logic for active abilities."""
        if self.is_active:
            print("I am active")
            # Logic for active state, if needed

    def handle_click(self, player, click_position):
        """Process clicks for interactive abilities."""
        # This can be overridden for abilities requiring click logic
        pass

    def display_icon(self, screen, x, y):
        cooldown_time_remaining = max(self.cooldown - (time.time() - self.last_used), 0)
        overlay_height = int(self.icon.get_height() * cooldown_time_remaining / (self.cooldown + 0.000001))

        # Simplify overlay creation
        overlay_surface = pygame.Surface(self.icon.get_size(), pygame.SRCALPHA)
        overlay_surface.fill((0, 0, 0, 150))  # Semi-transparent black overlay
        overlay_rect = pygame.Rect(0, self.icon.get_height() - overlay_height, self.icon.get_width(), overlay_height)
        overlay_surface.blit(self.icon, (0, 0))
        overlay_surface.fill((0, 0, 0, 150), overlay_rect)

        screen.blit(self.icon, (x, y))
        if cooldown_time_remaining > 0:
            text = self.font.render(f"{cooldown_time_remaining:.1f}", True, DEFAULT_TEXT_COLOR)
            screen.blit(text, (x + 15, y + 15))

    def render_shader_effect(self, _shader, camera):
        shader.frag_coord_shader_effect(_shader, camera)

class AbilityProjectile:
    def __init__(self, ability, spritesheet, x_pos, y_pos, x_vel, y_vel, direction, x_acc=0, y_acc=0, hitbox_width=32, hitbox_height=32, game=None, collision_effect=None):
        self.ability = ability
        self.spritesheet = spritesheet
        self.position = np.array([x_pos, y_pos])
        self.velocity = np.array([x_vel, y_vel]) * direction
        self.acceleration = np.array([x_acc, y_acc])
        self.damage = ability['damage']
        self.cooldown = ability['cooldown']
        self.hitbox_size = hitbox_width, hitbox_height
        self.direction = direction
        self.last_used_time = 0  # For cooldown management
        self.collision_effect = collision_effect
        self.rect = pygame.Rect(self.position, self.hitbox_size)
        self.collided_list = []
        self.game = game
        self.is_dead = False
        self.run_time = 0
        self.delay_time = 0.65

    def run(self, screen, target_list):

        if self.run_time + self.delay_time < time.time():
            physics.update_kinematics(self, 5)
            self.display(screen)


        for target in target_list:
            self.check_collision(target)

    def check_collision(self, target):
        self.rect = pygame.Rect(self.position[0], self.position[1], self.hitbox_size[0], self.hitbox_size[1])
        target.rect = pygame.Rect(target.position[0], target.position[1], target.width, target.height)
        if self.rect.colliderect(target.rect):
            if target not in self.collided_list:
                self.collision_effect(target)
                self.collided_list.append(target)

        if not 0 < self.position[0] < self.game.screen.width and not 0 < self.position[1] < self.game.screen.height:
            self.is_dead = True


    def display(self, screen):
        frame_to_display, self.animation_index = self.spritesheet.basic_animate()
        screen.blit(frame_to_display, (self.position[0], self.position[1]))

# ============================ BLOOD MAGE ABILITIES ========================================
class BloodBurst(Ability):
    """
    Blood Burst - Deals AoE damage around the caster, scaling with the amount of health sacrificed.
    Includes upgrades for customization via skill tree.
    """
    def __init__(self, game, caster):
        super().__init__("Blood_Burst")
        self.ability_class = "blood_mage"
        self.game = game
        self.caster = caster
        self.health_cost = 0.2  # 20% of current HP
        self.base_damage = 50
        self.radius = 200
        self.init_ability_icons(self.name)

        # Upgrades (default values)
        self.damage_multiplier = 2  # Scaling multiplier for sacrificed health
        self.bleed_effect = False
        self.bleed_damage = 0.5  # 50% of initial damage over time
        self.bleed_duration = 5  # Bleed effect duration in seconds
        self.vampiric_heal = False
        self.vampiric_percentage = 0.3  # Heal percentage of total damage dealt
        self.blood_bond = False
        self.background_image = "./game_assets/concept_art/blood_burst.webp"
        self.init_skill_nodes()
        self.init_skill_connections()
        self.render_effect = 'blood_burst'
        self.render_effect = None
        self.render_effect_duration = 0.1

    def init_skill_nodes(self):

        self.skill_nodes = {
            "Amplified Burst": {'name':'Amplified Burst', 'x':200, 'y':150, 'description':"Increase AoE radius by 20%. \n(Unlock cost: 1 skill point)", 'effect':lambda: self.upgrade("Amplified Burst"), 'cost':1, 'prerequisite':None },
            "Efficient Sacrifice": {'name':'Efficient Sacrifice', 'x':400, 'y':150, 'description':"Reduce HP cost to 12% instead of 20% \n(Unlock cost; 2 skill point)", 'effect':lambda: self.upgrade("Efficient Sacrifice"), 'cost':1, 'prerequisite':None},
            "Lingering Pain": {'name':'Lingering Pain', 'x':600, 'y':300, 'description':"Enemies hit by Blood Burst take 50% of the initial damage over 5 seconds as a bleed effect. \n(Unlock cost: 2 skill points)", 'effect':lambda: self.upgrade("Lingering Pain"), 'cost':2, 'prerequisite':'Amplified Burst'},
            "Focused Blast": {'name':'Focused Blast', 'x':200, 'y':450, 'description':'Increase damage scaling from 2x to 3x HP sacrificed but reduce radius by 30%. \n(Unlock cost: 2 skill points)', 'effect':lambda: self.upgrade("Focused Blast"), 'cost':2, 'prerequisite':'Amplified Burst'},
            "Blood Bond": {'name':'Blood Bond', 'x':500, 'y':450, 'description':'Allies in the AoE heal for 50% of the HP sacrificed by the caster. \n(Unlock cost: 3 skill points)', 'effect':lambda: self.upgrade("Blood Bond"), 'cost':3, 'prerequisite':'Focused Blast'},
            "Vampiric Burst": {'name':'Vampiric Burst', 'x':450, 'y':475, 'description':'The caster heals for 30% of the damage dealt to enemies. \n(Unlock cost: 3 skill points)', 'effect':lambda: self.upgrade("Vampiric Burst"), 'cost':3, 'prerequisite':'Focused Blast'},
        }

        self.upgrade_nodes = [SkillNode(x=node['x'],
                                        y=node['y'],
                                        description=node['description'],
                                        effect=node['effect'],
                                        cost=node['cost'],
                                        prerequisite=node['prerequisite'],
                                        name=node['name']) for node in self.skill_nodes.values()]



    def init_skill_connections(self):
        self.upgrade_connections = [
            SkillConnection(self.upgrade_nodes[0], self.upgrade_nodes[2]),
            SkillConnection(self.upgrade_nodes[0], self.upgrade_nodes[3]),

            # SkillConnection(self.upgrade_nodes[1], self.upgrade_nodes[3]),
            # SkillConnection(self.upgrade_nodes[1], self.upgrade_nodes[4]),

            SkillConnection(self.upgrade_nodes[3], self.upgrade_nodes[4]),
            SkillConnection(self.upgrade_nodes[3], self.upgrade_nodes[5]),
        ]

    def apply(self):
        # Check if caster has enough health
        health_to_sacrifice = self.caster.stats['current_health'] * self.health_cost
        self.draw_hitbox()
        if self.caster.stats['current_health'] > health_to_sacrifice:
            # Reduce caster's health
            self.caster.stats['current_health'] -= health_to_sacrifice

            # Calculate damage
            damage = self.base_damage + health_to_sacrifice * self.damage_multiplier
            self.deal_aoe_damage(damage, self.radius, self.caster)

            print(f"{self.caster.name} used Blood Burst, sacrificing {health_to_sacrifice:.1f} HP for {damage:.1f} AoE damage!")

            # Apply vampiric healing if unlocked
            if self.vampiric_heal:
                total_damage_dealt = self.calculate_total_damage(damage, self.radius)
                heal_amount = total_damage_dealt * self.vampiric_percentage
                self.caster.stats['current_health'] += heal_amount
                print(f"{self.caster.name} healed for {heal_amount:.1f} HP from Vampiric Burst!")

        else:
            print(f"{self.caster.name} does not have enough health to use Blood Burst.")

    def deal_aoe_damage(self, damage, radius, caster):
        """Deals AoE damage to all enemies within a given radius."""
        caster_position = caster.position  # (x, y) coordinates of the caster

        for enemy in self.game.enemies:  # Access the list of enemies in the game
            distance = ((enemy.position[0] - caster_position[0]) ** 2 +
                        (enemy.position[1] - caster_position[1]) ** 2) ** 0.5
            if distance <= radius:
                enemy.take_damage(damage)
                print(f"Dealt {damage} damage to {enemy.name} at distance {distance:.2f}.")

                # Apply bleed effect if unlocked
                if self.bleed_effect:
                    enemy.apply_status_effect("bleed", damage * self.bleed_damage, duration=self.bleed_duration)
                    print(f"{enemy.name} is bleeding for {damage * self.bleed_damage:.1f} damage over {self.bleed_duration} seconds.")

    def calculate_total_damage(self, base_damage, radius):
        """Calculate total damage dealt to all enemies in the radius."""
        total_damage = 0
        caster_position = self.caster.position

        for enemy in self.game.enemies:
            distance = ((enemy.position[0] - caster_position[0]) ** 2 +
                        (enemy.position[1] - caster_position[1]) ** 2) ** 0.5
            if distance <= radius:
                total_damage += base_damage

        return total_damage

    def upgrade(self, upgrade_type):
        """Applies upgrades to Blood Burst based on the skill tree."""
        if upgrade_type == "Amplified Burst":
            self.radius *= 1.2
            print(f"Upgrade Applied: Radius increased to {self.radius:.1f}.")
        elif upgrade_type == "Efficient Sacrifice":
            self.health_cost = 0.15  # Reduce health cost to 15%
            print("Upgrade Applied: Health cost reduced to 15%.")
        elif upgrade_type == "Lingering Pain":
            self.bleed_effect = True
            print("Upgrade Applied: Bleed effect unlocked.")
        elif upgrade_type == "Focused Blast":
            self.damage_multiplier = 3  # Increase scaling multiplier
            self.radius *= 0.7  # Reduce radius
            print("Upgrade Applied: Damage multiplier increased, radius decreased.")
        elif upgrade_type == "Vampiric Burst":
            self.vampiric_heal = True
            print("Upgrade Applied: Vampiric healing unlocked.")
        elif upgrade_type == "Blood Bond":
            self.blood_bond = True
            print("Upgrade Applied: Blood Bond unlocked.")

    def draw_hitbox(self):
        pygame.draw.circle(self.game.background, (255, 0, 0), self.caster.position, self.radius,)

class CrimsonPact(Ability):
    """
    Crimson Pact - Empowers the caster with blood magic to enhance abilities and survival through health sacrifice.
    Includes upgrades for customization via a skill tree.
    """

    def __init__(self, game, caster):
        super().__init__("Crimson_Pact")
        self.ability_class = "blood_mage"
        self.game = game
        self.caster = caster
        self.health_cost = 0.001  # 20% of max HP
        self.base_duration = 600  # 10 seconds
        self.cooldown = 1200  # 20 seconds cooldown
        self.active = False

        # Base buffs
        self.damage_bonus = 1.2  # 20% increase
        self.life_steal_percentage = 0.1  # 10% lifesteal
        self.damage_reduction = 0.1  # 10% damage reduction

        # Upgrade defaults
        self.enhanced_life_steal = False
        self.damage_boost = False
        self.sacrificial_strength = False
        self.health_regen_boost = False
        self.longer_duration = False
        self.increased_resilience = False
        self.is_active = False

        self.background_image = "./game_assets/concept_art/crimson_pact.webp"
        self.init_skill_nodes()
        self.init_skill_connections()
        self.init_ability_icons(self.name)
        self.effect = lambda: self.effects()

    def init_skill_nodes(self):
        self.skill_nodes = {
            # Tree one
            'Enhanced Lifesteal': {'name': 'Enhanced Lifesteal', 'x': 200, 'y': 150,
                                   'description': 'Increase lifesteal by 10%.',
                                   'effect': lambda: self.upgrade("Enhanced Lifesteal"), 'cost': 1,
                                   'prerequisite': None},
            'Life Surge': {'name': 'Life Surge', 'x': 400, 'y': 150,
                           'description': 'Gain a health regeneration buff during Crimson Pact.',
                           'effect': lambda: self.upgrade("Life Surge"), 'cost': 2,
                           'prerequisite': 'Enhanced Lifesteal'},

            # Tree two
            'Sacrificial Strength': {'name': 'Sacrificial Strength', 'x': 200, 'y': 250,
                                     'description': 'Sacrifice an additional 5% HP to increase damage bonus to 40%.',
                                     'effect': lambda: self.upgrade("Sacrificial Strength"), 'cost': 2,
                                     'prerequisite': None},
            'Unyielding Might': {'name': 'Unyielding Might', 'x': 400, 'y': 250,
                                 'description': 'Duration increased by 5 seconds.',
                                 'effect': lambda: self.upgrade("Unyielding Might"), 'cost': 2,
                                 'prerequisite': 'Sacrificial Strength'},

            # Tree three
            'Crimson Resilience': {'name': 'Crimson Resilience', 'x': 200, 'y': 350,
                                   'description': 'Increase damage reduction by 15%.',
                                   'effect': lambda: self.upgrade("Crimson Resilience"), 'cost': 2,
                                   'prerequisite': None},
            'Shield of Blood': {'name': 'Shield of Blood', 'x': 400, 'y': 350,
                                'description': 'On activation, gain a shield equal to 20% of max HP.',
                                'effect': lambda: self.upgrade("Shield of Blood"), 'cost': 3,
                                'prerequisite': 'Crimson Resilience'},
        }

        self.upgrade_nodes = [SkillNode(x=node['x'],
                                        y=node['y'],
                                        description=node['description'],
                                        effect=node['effect'],
                                        cost=node['cost'],
                                        prerequisite=node['prerequisite'],
                                        name=node['name']) for node in self.skill_nodes.values()]

    def init_skill_connections(self):
        self.upgrade_connections = [
            SkillConnection(self.upgrade_nodes[0], self.upgrade_nodes[1]),
            SkillConnection(self.upgrade_nodes[2], self.upgrade_nodes[3]),
            SkillConnection(self.upgrade_nodes[4], self.upgrade_nodes[5]),
        ]

    def apply(self):
        if self.is_active:
            self.is_active = False

        else:
            self.is_active = True
            self.start_time = time.time()

    def effects(self):
        health_to_sacrifice = self.caster.stats['max_health'] * self.health_cost
        if self.caster.stats['current_health'] > health_to_sacrifice:
            self.caster.stats['current_health'] -= health_to_sacrifice
            self.caster.stats['damage_multiplier'] *= self.damage_bonus
            self.caster.stats["life_steal"] += self.life_steal_percentage
            self.caster.stats['damage_reduction'] += self.damage_reduction
            print(
                f"{self.caster.name} activated Crimson Pact, sacrificing {health_to_sacrifice:.1f} HP for enhanced power!")

        if self.start_time + self.base_duration < time.time():
            self.end_crimson_pact()

    def end_crimson_pact(self):
        self.is_active = False
        self.caster.stats["damage_multiplier"] /= self.damage_bonus
        self.caster.stats["life_steal"] -= self.life_steal_percentage
        self.caster.stats["damage_reduction"] -= self.damage_reduction
        print(f"{self.caster.name}'s Crimson Pact has ended.")

    def upgrade(self, upgrade_type):
        if upgrade_type == "Enhanced Lifesteal":
            self.life_steal_percentage += 0.1
            self.enhanced_life_steal = True
            print(f"Upgrade Applied: Lifesteal increased to {self.life_steal_percentage * 100:.1f}%.")

        elif upgrade_type == "Life Surge":
            self.health_regen_boost = True
            print("Upgrade Applied: Health regeneration active during Crimson Pact.")

        elif upgrade_type == "Sacrificial Strength":
            self.health_cost += 0.05
            self.damage_bonus = 1.4
            self.sacrificial_strength = True
            print(
                f"Upgrade Applied: Damage bonus increased to {self.damage_bonus * 100:.1f}%, health cost increased to {self.health_cost * 100:.1f}%.")

        elif upgrade_type == "Unyielding Might":
            self.base_duration += 500
            self.longer_duration = True
            print(f"Upgrade Applied: Duration increased to {self.base_duration / 100:.1f} seconds.")

        elif upgrade_type == "Crimson Resilience":
            self.damage_reduction += 0.15
            self.increased_resilience = True
            print(f"Upgrade Applied: Damage reduction increased to {self.damage_reduction * 100:.1f}%.")

        elif upgrade_type == "Shield of Blood":
            self.caster.shield = self.caster.stats['max_health'] * 0.2
            print(f"Upgrade Applied: Shield of Blood grants {self.caster.shield:.1f} HP shield on activation.")

class SanguineChains(Ability):
    """
    Sanguine Chains - Roots enemies and deals damage over time, consuming a percentage of the caster's max HP.
    Includes upgrades for customization via skill tree.
    """
    def __init__(self, game, caster):
        super().__init__("Sanguine_Chains")
        self.ability_class = "blood_mage"
        self.game = game
        self.caster = caster
        self.health_cost = 0.1  # 10% of max HP
        self.base_damage = 0.1  # Damage per second
        self.duration = 600  # Default duration in frames
        self.radius = 800  # Effect radius
        self.init_ability_icons(self.name)

        # Upgrades starting booleans
        self.extended_duration = False
        self.chain_radius_increase = False
        self.multiple_targets = False
        self.life_siphon = False
        self.critical_strike = False
        self.slow = False

        # Upgrade stat increases
        self.damage_increase_per_second = 0.0  # Damage increase each second
        self.slow_duration = 800 # Default duration in frames
        self.critical_strike_multiplier = 2 # 2x Critical hit damage multiplier
        self.critical_strike_chance = 0.2 # 20% Critical strike chance
        self.siphon_percentage = 0.1  # Heal percentage of total damage dealt

        self.background_image = "./game_assets/concept_art/sanguine_chains.webp"
        self.animation = spritesheet.SpriteSheet("./game_assets/concept_art/vine_root_spritesheet_16.png", frame_height=48, frame_width=48)
        self.init_skill_nodes()
        self.init_skill_connections()
        self.render_effect = None
        self.render_effect_duration = 0.1


    def init_skill_nodes(self):
        self.skill_nodes = {
            # Tree One
            'Extended Bind': {'name':'Extended Bind', 'x':200, 'y':150, 'description':'Increase the root duration by 2 seconds. (Unlock cost: 1 skill point)', 'effect':lambda: self.upgrade("Extended Bind"), 'cost':1, 'prerequisite': None},
            'Constriction Slow': {'name':'Constriction Slow', 'x':400, 'y':150, 'description':'Chains slow by 20% for 3 seconds after root ends.', 'effect':lambda: self.upgrade("Constriction Slow"), 'cost':2, 'prerequisite': 'Extended Bind'},
            'Inescapable Bind': {'name':'Inescapable Bind', 'x':600, 'y':300, 'description':'Chains hit multiple targets within range. (Unlock cost: 3 skill points)', 'effect':lambda: self.upgrade("Inescapable Bind"), 'cost':3, 'prerequisite': 'Constriction Slow'},

            # Tree two
            'Enhanced Bleed': {'name':'Enhanced Bleed', 'x':200, 'y':450, 'description':'Bleed damage is increased by 50%. (Unlock cost: 1 skill points)', 'effect':lambda: self.upgrade("Enhanced Bleed"), 'cost':1, 'prerequisite': None},
            'Critical Bleed': {'name':'Critical Bleed', 'x':300, 'y':450, 'description':'Critical Bleed. (Unlock cost: 2 skill points)', 'effect':lambda: self.upgrade("Critical Bleed"), 'cost':2, 'prerequisite': 'Enhanced Bleed'},
            'Chain Pull': {'name':'Chain Pull', 'x':400, 'y':450, 'description':'Chains pull enemies towards a central location. (Unlock cost: 3 skill points)', 'effect':lambda: self.upgrade("Chain Pull"), 'cost':3, 'prerequisite': 'Critical Bleed'},

            # Tree three
            'Life Siphon': {'name':'Life Siphon', 'x':400, 'y':550, 'description':'Chains heal for 10% of damage dealt. (Unlock cost: 1 skill point)', 'effect':lambda: self.upgrade("Life Siphon"), 'cost':1, 'prerequisite': None },
            'Energy Refund': {'name':'Energy Refund', 'x':500, 'y':550, 'description':'Refunds 50% of energy cost if all chains hit their target. (Unlock cost: 2 skill points)', 'effect':lambda: self.upgrade("Energy Refund"), 'cost':2, 'prerequisite': 'Life Siphon'},
            'Ally Link': {'name':'Ally Link', 'x':600, 'y':650, 'description':'Chains can attach to allies healing them instead of damaging them. (Unlock cost: 3 skill points)', 'effect':lambda: self.upgrade("Ally Link"), 'cost':3, 'prerequisite': 'Chain Pull'},
        }

        self.upgrade_nodes = [SkillNode(x=node['x'],
                                        y=node['y'],
                                        description=node['description'],
                                        effect=node['effect'],
                                        cost=node['cost'],
                                        prerequisite=node['prerequisite'],
                                        name=node['name']) for node in self.skill_nodes.values()]


    def init_skill_connections(self):
        self.upgrade_connections = [
            SkillConnection(self.upgrade_nodes[0], self.upgrade_nodes[1]),
            SkillConnection(self.upgrade_nodes[1], self.upgrade_nodes[2]),

            SkillConnection(self.upgrade_nodes[3], self.upgrade_nodes[4]),
            SkillConnection(self.upgrade_nodes[4], self.upgrade_nodes[5]),

            SkillConnection(self.upgrade_nodes[6], self.upgrade_nodes[7]),
            SkillConnection(self.upgrade_nodes[7], self.upgrade_nodes[8]),
        ]

    def apply(self):
        health_to_sacrifice = self.caster.stats['max_health'] * self.health_cost
        if self.caster.stats['current_health'] > health_to_sacrifice:
            self.is_animating = True
            self.caster.stats['current_health'] -= health_to_sacrifice
            print(f"{self.caster.name} used Sanguine Chains, sacrificing {health_to_sacrifice:.1f} HP!")


            if not self.multiple_targets:
                distance_sorted_enemy = [(((enemy.position[0] - self.caster.position[0]) ** 2 + (
                            enemy.position[1] - self.caster.position[1]) ** 2) ** 0.5, ind) for ind, enemy in
                                         enumerate(self.game.enemies)]
                distance_sorted_enemy.sort()

                if distance_sorted_enemy:
                    target_list = [self.game.enemies[distance_sorted_enemy[0][1]]]
                else:
                    target_list = []

            else:
                target_list = self.game.enemies

            for enemy in target_list:
                distance = ((enemy.position[0] - self.caster.position[0]) ** 2 + (enemy.position[1] - self.caster.position[1]) ** 2) ** 0.5
                if distance <= self.radius:
                    enemy.state_machine.apply_effect("rooted", duration=self.duration)
                    print(f"{enemy.name} is rooted for {self.duration} seconds!")

                    total_damage = self.base_damage * self.duration

                    if self.critical_strike and random.randint(0,100) / 100 > self.critical_strike_chance:
                        total_damage *= self.critical_strike_multiplier
                        print(f'{self.caster.name} has a critical strike!')

                    if self.extended_duration:
                        total_damage += self.damage_increase_per_second * self.duration

                    enemy.take_damage(total_damage)
                    self.animate(enemy.position)
                    print(f"Dealt {total_damage:.1f} damage to {enemy.name}!")

                    if self.life_siphon:
                        heal_amount = total_damage * self.siphon_percentage
                        self.caster.stats['current_health'] += heal_amount
                        print(f"{self.caster.name} healed for {heal_amount:.1f} HP from Bloodflow Bind!")


                    if self.slow:
                        enemy.state_machine.apply_effect("slowed", duration=self.slow_duration)

    def animate(self, position):
        self.game.background.blit(self.animation.basic_animate()[0], (position))



    def upgrade(self, upgrade_type):
        if upgrade_type == "Extended Bind":
            self.duration += 2
            self.extended_duration = True
            print(f"Upgrade Applied: Duration increased to {self.duration} seconds.")

        elif upgrade_type == "Constriction Slow":
            self.slow = True
            print("Upgrade Applied: Now slows after root effect ends.")

        elif upgrade_type == "Inescapable Bind":
            self.multiple_targets = True
            print("Upgrade Applied: Target chaining unlocked for Sanguine Chains.")

        elif upgrade_type == "Enhanced Bleed":
            self.base_damage *= 1.5
            print(f"Upgrade Applied: Damage increased to {self.base_damage * self.duration:.1f}.")

        elif upgrade_type == "Critical Bleed":
            self.critical_strike = True
            print(f"Upgrade Applied: Bleed can now critically strike.")

        elif upgrade_type == "Chain Pull":
            self.radius *= 1.3
            print(f"Upgrade Applied: Radius increased to {self.radius:.1f}.")

        elif upgrade_type == "Life Siphon":
            self.life_siphon = True
            print(f"Upgrade Applied: Now heals {self.siphon_percentage * 100:.1f}% of damage dealt.")

class Hemorrhage(Ability):
    """
    Hemorrhage - Applies a bleed effect to enemies, healing the caster for a portion of the damage dealt.
    """
    def __init__(self, game, caster):
        super().__init__("Hemorrhage", caster)
        self.ability_class = "blood_mage"
        self.bleed_damage = 5  # Damage per second
        self.duration = 5
        self.healing_factor = 0.5  # Heal for 50% of damage dealt
        self.activation_skill = self.activate
        self.caster = caster
        self.game = game
        self.init_skill_nodes()
        self.init_skill_connections()
        self.init_ability_icons(self.name)
        self.background_image = "./game_assets/concept_art/hemorrhage.webp"


    def init_skill_nodes(self):
        self.upgrade_nodes = [
            SkillNode(200, 150, "Node 1", "This is Node 1"),
            SkillNode(400, 150, "Node 2", "This is Node 2", prerequisite="Node 1"),
            SkillNode(600, 300, "Node 3", "This is Node 3", prerequisite="Node 2"),
            SkillNode(200, 450, "Node 4", "This is Node 4", prerequisite="Node 1"),
        ]

    def init_skill_connections(self):
        self.upgrade_connections = [
            SkillConnection(self.upgrade_nodes[0], self.upgrade_nodes[1]),
            SkillConnection(self.upgrade_nodes[1], self.upgrade_nodes[2]),
            SkillConnection(self.upgrade_nodes[0], self.upgrade_nodes[3]),
        ]

    def apply(self):
        total_healing = 0
        for target in self.game.enemies:
            total_damage = self.bleed_damage * self.duration
            target.take_damage(total_damage)
            healing = total_damage * self.healing_factor
            total_healing += healing
        self.caster.stats['current_health'] = min(self.caster.stats['max_health'], self.caster.stats['current_health'] + total_healing)
        print(f"{self.caster.name} used Hemorrhage, dealing bleed damage and healing for {total_healing:.1f} HP.")
# ============================ BLOOD MAGE ABILITIES ========================================

class ArcaneMissile(Ability):
    """
    Arcane Missile - Fires a projectile that seeks the clicked target location, dealing damage on impact.
    Includes upgrades for customization via skill tree.
    """
    def __init__(self, game, caster):
        super().__init__("Arcane_Missile")
        self.ability_class = "arcane_mage"
        self.game = game
        self.caster = caster
        self.mana_cost = 25  # Mana cost to cast
        self.base_damage = 100  # Damage on impact
        self.speed = 20  # Speed of the projectile
        self.range = 1200  # Maximum range of the projectile
        self.init_ability_icons(self.name)

        # Upgrades starting booleans
        self.piercing_projectile = False
        self.explosive_impact = False
        self.critical_strike = False
        self.mana_efficiency = False
        self.homing_projectile = False
        self.damage_over_time = False

        # Upgrade stat increases
        self.critical_multiplier = 2.0  # Critical hit damage multiplier
        self.critical_chance = 0.2  # 20% chance to critically strike
        self.explosion_radius = 300  # Radius for explosive impact
        self.dot_damage = 10  # Damage over time per second
        self.dot_duration = 3  # Duration of the damage over time effect

        self.background_image = "./game_assets/concept_art/blood_burst.webp"
        # self.animation = spritesheet.SpriteSheet("./game_assets/abilities/icons/fireball_sheet_10.png", height=32, width=32)
        self.animation = None
        self.init_skill_nodes()
        self.init_skill_connections()
        self.effect = lambda: self.effects()
        self.render_effect = None
        self.render_effect_duration = 0.2
        self.sound_effect = pygame.mixer.Sound(DEFAULT_ABILITY_SOUND_FX_PATH + "fireball_woosh.mp3")

    def init_skill_nodes(self):
        self.skill_nodes = {
            # Tree One
            'Piercing Bolt': {'name': 'Piercing Bolt', 'x': 200, 'y': 150, 'description': 'Missile pierces through enemies, hitting multiple targets. (Unlock cost: 1 skill point)', 'effect': lambda: self.upgrade("Piercing Bolt"), 'cost': 1, 'prerequisite': None},
            'Explosive Impact': {'name': 'Explosive Impact', 'x': 400, 'y': 150, 'description': 'Missile explodes on impact, dealing damage in an area. (Unlock cost: 2 skill points)', 'effect': lambda: self.upgrade("Explosive Impact"), 'cost': 2, 'prerequisite': 'Piercing Bolt'},
            'Critical Surge': {'name': 'Critical Surge', 'x': 600, 'y': 300, 'description': 'Missile can critically strike, dealing double damage. (Unlock cost: 3 skill points)', 'effect': lambda: self.upgrade("Critical Surge"), 'cost': 3, 'prerequisite': 'Explosive Impact'},

            # Tree Two
            'Homing Arc': {'name': 'Homing Arc', 'x': 200, 'y': 450, 'description': 'Missile slightly homes in on targets. (Unlock cost: 1 skill point)', 'effect': lambda: self.upgrade("Homing Arc"), 'cost': 1, 'prerequisite': None},
            'Greater Range': {'name': 'Greater Range', 'x': 400, 'y': 450, 'description': 'Increases missile range by 25%. (Unlock cost: 2 skill points)', 'effect': lambda: self.upgrade("Greater Range"), 'cost': 2, 'prerequisite': 'Homing Arc'},
            'Swift Barrage': {'name': 'Swift Barrage', 'x': 600, 'y': 450, 'description': 'Reduces cooldown by 20%. (Unlock cost: 3 skill points)', 'effect': lambda: self.upgrade("Swift Barrage"), 'cost': 3, 'prerequisite': 'Greater Range'},

            # Tree Three
            'Mana Efficiency': {'name': 'Mana Efficiency', 'x': 200, 'y': 550, 'description': 'Reduces mana cost by 10%. (Unlock cost: 1 skill point)', 'effect': lambda: self.upgrade("Mana Efficiency"), 'cost': 1, 'prerequisite': None},
            'Arcane Burn': {'name': 'Arcane Burn', 'x': 400, 'y': 550, 'description': 'Adds damage-over-time effect to missile hits. (Unlock cost: 2 skill points)', 'effect': lambda: self.upgrade("Arcane Burn"), 'cost': 2, 'prerequisite': 'Mana Efficiency'},
            'Empowered Arcana': {'name': 'Empowered Arcana', 'x': 600, 'y': 550, 'description': 'Increases base damage by 25%. (Unlock cost: 3 skill points)', 'effect': lambda: self.upgrade("Empowered Arcana"), 'cost': 3, 'prerequisite': 'Arcane Burn'},
        }

        self.upgrade_nodes = [SkillNode(x=node['x'],
                                        y=node['y'],
                                        description=node['description'],
                                        effect=node['effect'],
                                        cost=node['cost'],
                                        prerequisite=node['prerequisite'],
                                        name=node['name']) for node in self.skill_nodes.values()]

    def init_skill_connections(self):
        self.upgrade_connections = [
            SkillConnection(self.upgrade_nodes[0], self.upgrade_nodes[1]),
            SkillConnection(self.upgrade_nodes[1], self.upgrade_nodes[2]),

            SkillConnection(self.upgrade_nodes[3], self.upgrade_nodes[4]),
            SkillConnection(self.upgrade_nodes[4], self.upgrade_nodes[5]),

            SkillConnection(self.upgrade_nodes[6], self.upgrade_nodes[7]),
            SkillConnection(self.upgrade_nodes[7], self.upgrade_nodes[8]),
        ]

    def run_projectile(self):
        if self.projectile.run_time + self.projectile.delay_time < time.time():
            physics.update_kinematics(self.projectile, 10)
            self.projectile.display(self.game.background)
            self.projectile.fireball.update()
            self.projectile.fireball.draw(self.game.background)

            for target in self.game.enemies:
                self.projectile.check_collision(target)

    def effects(self):
        self.run_projectile()

    def collision_effect(self, target):
        target.take_damage(self.base_damage)
        self.projectile.fireball.trigger_explosion()

    def apply(self):
        """Implementation of the projectile firing and effects logic."""
        # Logic to fire the projectile toward the clicked location, apply upgrades, and damage enemies
        self.is_active = True
        self.caster.is_spell_casting = True
        x_vel, y_vel = pygame.math.Vector2(pygame.mouse.get_pos() - pygame.math.Vector2(self.caster.position) + pygame.math.Vector2(self.game.camera.camera.x, self.game.camera.camera.y)).clamp_magnitude(0, 5)
        self.projectile = AbilityProjectile(ability=ABILITY_DATA['Fireball'],
                                               spritesheet=fire_ball_spritesheet,
                                               x_pos=self.caster.position[0],
                                               y_pos=self.caster.position[1],
                                               x_vel=x_vel,
                                               y_vel=y_vel,
                                               direction=1,
                                               collision_effect=self.collision_effect,
                                               game=self.game)



        self.projectile.fireball = fireball_effect.Fireball(self.projectile)

        self.projectile.run_time = time.time()

        self.caster.projectiles.append(self.projectile)

        self.sound_effect.play()

        print("Total projectile count: ", len(self.caster.projectiles))
    def upgrade(self, upgrade_type):
        """Applies the effects of an upgrade."""
        if upgrade_type == "Piercing Bolt":
            self.piercing_projectile = True
            print("Upgrade Applied: Missile can pierce through enemies.")

        elif upgrade_type == "Explosive Impact":
            self.explosive_impact = True
            print("Upgrade Applied: Missile explodes on impact.")

        elif upgrade_type == "Critical Surge":
            self.critical_strike = True
            print("Upgrade Applied: Missile can critically strike.")

        elif upgrade_type == "Homing Arc":
            self.homing_projectile = True
            print("Upgrade Applied: Missile homes in on enemies.")

        elif upgrade_type == "Greater Range":
            self.range *= 1.25
            print(f"Upgrade Applied: Range increased to {self.range} units.")

        elif upgrade_type == "Swift Barrage":
            self.cooldown *= 0.8
            print(f"Upgrade Applied: Cooldown reduced by 20%.")

        elif upgrade_type == "Mana Efficiency":
            self.mana_cost *= 0.9
            print(f"Upgrade Applied: Mana cost reduced to {self.mana_cost}.")

        elif upgrade_type == "Arcane Burn":
            self.damage_over_time = True
            print(f"Upgrade Applied: Missile inflicts {self.dot_damage} damage per second for {self.dot_duration} seconds.")

        elif upgrade_type == "Empowered Arcana":
            self.base_damage *= 1.25
            print(f"Upgrade Applied: Base damage increased to {self.base_damage}.")

class LightningStrike(Ability):
    """
    Lightning Strike - Strikes a clicked target location with a lightning effect, dealing damage on impact.
    Includes upgrades for customization via a skill tree.
    """
    def __init__(self, game, caster):
        super().__init__("Lightning_Strike")
        self.ability_class = "arcane_mage"
        self.game = game
        self.caster = caster
        self.mana_cost = 30  # Mana cost to cast
        self.base_damage = 150  # Damage on impact
        self.range = 1000  # Maximum range of the strike
        self.lightning_effect_duration = 1.5  # Duration of the lightning effect
        self.init_ability_icons(self.name)

        # Upgrades starting booleans
        self.chain_lightning = False
        self.stun_effect = False
        self.critical_strike = False
        self.mana_efficiency = False

        # Upgrade stat increases
        self.critical_multiplier = 2.0  # Critical hit damage multiplier
        self.critical_chance = 0.2  # 20% chance to critically strike
        self.stun_duration = 2.0  # Stun duration in seconds
        self.chain_targets = 3  # Number of targets the lightning chains to

        self.background_image = "./game_assets/concept_art/blood_burst.webp"
        self.animation = None
        self.init_skill_nodes()
        self.init_skill_connections()
        self.render_effect = None
        self.is_active = False
        self.effect = lambda: self.effects()
        self.render_effect_duration = self.lightning_effect_duration
        self.sound_effect = pygame.mixer.Sound(DEFAULT_ABILITY_SOUND_FX_PATH + "fireball_woosh.mp3")
        self.lightning_manager = l_effect.LightningManager()


    def init_skill_nodes(self):
        self.skill_nodes = {
            'Chain Lightning': {'name': 'Chain Lightning', 'x': 200, 'y': 150, 'description': 'Lightning chains to nearby enemies. (Unlock cost: 1 skill point)', 'effect': lambda: self.upgrade("Chain Lightning"), 'cost': 1, 'prerequisite': None},
            'Stunning Strike': {'name': 'Stunning Strike', 'x': 400, 'y': 150, 'description': 'Lightning stuns targets. (Unlock cost: 2 skill points)', 'effect': lambda: self.upgrade("Stunning Strike"), 'cost': 2, 'prerequisite': 'Chain Lightning'},
            'Critical Voltage': {'name': 'Critical Voltage', 'x': 600, 'y': 300, 'description': 'Lightning can critically strike. (Unlock cost: 3 skill points)', 'effect': lambda: self.upgrade("Critical Voltage"), 'cost': 3, 'prerequisite': 'Stunning Strike'},
        }

        self.upgrade_nodes = [SkillNode(x=node['x'],
                                        y=node['y'],
                                        description=node['description'],
                                        effect=node['effect'],
                                        cost=node['cost'],
                                        prerequisite=node['prerequisite'],
                                        name=node['name']) for node in self.skill_nodes.values()]

    def init_skill_connections(self):
        self.upgrade_connections = [
            SkillConnection(self.upgrade_nodes[0], self.upgrade_nodes[1]),
            SkillConnection(self.upgrade_nodes[1], self.upgrade_nodes[2]),
        ]

    def apply(self):
        print("successfully cast Lightning Strike")
        self.is_active = True
        # self.caster.sprites['spell_cast'].animation_speed = 1
        for enemy in self.game.enemies:
            distance = ((enemy.position[0] - self.caster.position[0]) ** 2 +
                        (enemy.position[1] - self.caster.position[1]) ** 2) ** 0.5

            if distance <= self.range:
                cast_location = (self.caster.position[0] + self.caster.width / 2, self.caster.position[1] + self.caster.height / 3)
                self.lightning_manager.trigger(cast_location, enemy.position)
                enemy.take_damage(self.base_damage)
                print(f"Dealt {self.base_damage} damage to {enemy.name} at distance {distance:.2f}.")


            # Apply stun if unlocked
            if self.stun_effect:
                enemy.apply_status_effect("stun", self.stun_duration)

           # Apply chaining if unlocked
            if self.chain_lightning:
                self.chain_to_additional_targets(enemy)

    def chain_to_additional_targets(self, initial_target):
        """Chains lightning to additional nearby targets."""
        nearby_targets = self.game.get_nearby_enemies(initial_target.position, range=300)
        for target in nearby_targets[:self.chain_targets]:
            target.take_damage(self.base_damage)
            if self.stun_effect:
                target.apply_status_effect("stun", self.stun_duration)

    def calculate_damage(self):
        """Calculates the damage of the lightning strike, including critical strikes."""
        if self.critical_strike and random.random() < self.critical_chance:
            return self.base_damage * self.critical_multiplier
        return self.base_damage


    def upgrade(self, upgrade_type):
        """Applies the effects of an upgrade."""
        if upgrade_type == "Chain Lightning":
            self.chain_lightning = True
            print("Upgrade Applied: Lightning can chain to multiple targets.")

        elif upgrade_type == "Stunning Strike":
            self.stun_effect = True
            print("Upgrade Applied: Lightning stuns targets.")

        elif upgrade_type == "Critical Voltage":
            self.critical_strike = True
            print("Upgrade Applied: Lightning can critically strike.")

    def effects(self):
        self.lightning_manager.update(self.game.clock.get_time())
        self.lightning_manager.draw(self.game.background)


# ================================= FIREBALL SKILL FUNCTIONS ====================================================

# class Hemorrhage:
#     def __init__(self, game, caster):
#         self.base_damage = 1  # Damage dealt per tick
#         self.duration = 600  # Duration of the bleed effect
#         self.bleed_effect = bleed_effect  # Tracks applied bleeds
#         self.crit_chance = crit_chance  # Critical hit chance
#         self.caster = caster  # Reference to the caster/player
#         self.upgrades = {
#             "HemorrhagicWave": False,
#             "SanguineCountdown": False,
#             "Exsanguinate": False,
#             "CrimsonSynergy": False,
#             "HemorrhagicEcho": False,
#             "LingeringAgony": False,
#             "VitalSacrifice": False,
#             "BloodlustSurge": False,
#         }
#         self.stacks = {}  # Tracks stacks of bleed per target
#
#     def apply_bleed(self, target):
#         """Applies the bleed effect to the target."""
#         is_crit = self.roll_crit()
#         bleed_damage = self.base_damage * (2 if is_crit else 1)
#
#         # Upgrade: BloodlustSurge
#         if self.upgrades["BloodlustSurge"]:
#             bleed_damage *= 1 + 0.02 * target.get_bleed_duration()
#
#         if target not in self.bleed_effect:
#             self.bleed_effect[target] = self.duration
#         else:
#             # Upgrade: LingeringAgony
#             if not self.upgrades["LingeringAgony"]:
#                 self.bleed_effect[target] = self.duration
#
#         # Apply bleed damage
#         target.apply_effect("bleed", bleed_damage, self.duration)
#
#         # Upgrade: HemorrhagicWave
#         if self.upgrades["HemorrhagicWave"]:
#             self.apply_aoe_bleed(target)
#
#     def apply_aoe_bleed(self, target):
#         """Applies a weakened bleed effect to nearby enemies."""
#         nearby_enemies = target.get_nearby_enemies(radius=5)
#         for enemy in nearby_enemies:
#             if enemy not in self.bleed_effect:
#                 enemy.apply_effect("bleed", self.base_damage * 0.5, self.duration // 2)
#
#     def roll_crit(self):
#         """Determines whether the attack is a critical hit."""
#         crit_chance = self.crit_chance
#
#         # Upgrade: CrimsonSynergy
#         if self.upgrades["CrimsonSynergy"]:
#             crit_chance += 5 * min(len(self.get_bleeding_enemies()), 4)
#
#         return random.random() < crit_chance / 100
#
#     def get_bleeding_enemies(self):
#         """Returns a list of enemies currently bleeding."""
#         return [target for target, duration in self.bleed_effect.items() if duration > 0]
#
#     def on_bleed_expire(self, target):
#         """Handles effects when the bleed expires."""
#         # Upgrade: SanguineCountdown
#         if self.upgrades["SanguineCountdown"]:
#             final_burst_damage = 0.5 * self.base_damage * self.duration
#             target.take_damage(final_burst_damage, self.caster)
#
#         # Upgrade: HemorrhagicEcho
#         if self.upgrades["HemorrhagicEcho"] and target.is_dead():
#             self.chain_bleed(target)
#
#     def chain_bleed(self, source):
#         """Chains Hemorrhage to a nearby enemy."""
#         nearby_enemies = source.get_nearby_enemies(radius=10)
#         if nearby_enemies:
#             next_target = nearby_enemies[0]  # Choose the first enemy (can be random)
#             self.apply_bleed(next_target)
#
#     def modify_healing(self, target):
#         """Modifies healing effects on bleeding targets."""
#         # Upgrade: Exsanguinate
#         if self.upgrades["Exsanguinate"]:
#             target.reduce_healing(50)
#
#     def provide_healing(self, damage_dealt):
#         """Provides healing to the caster or allies."""
#         # Upgrade: VitalSacrifice
#         if self.upgrades["VitalSacrifice"]:
#             allies = self.caster.get_nearby_allies(radius=10)
#             for ally in allies:
#                 ally.heal(damage_dealt * 0.2)
#         else:
#             self.caster.heal(damage_dealt * 0.2)
#
#     def tick(self, delta_time):
#         """Handles the tick logic for all bleeding enemies."""
#         for target, time_left in list(self.bleed_effect.items()):
#             time_left -= delta_time
#             if time_left <= 0:
#                 self.on_bleed_expire(target)
#                 del self.bleed_effect[target]
#             else:
#                 self.bleed_effect[target] = time_left
#                 damage = self.base_damage * delta_time
#                 target.take_damage(damage, self.caster)
#                 self.modify_healing(target)



fire_ball_spritesheet = spritesheet.SpriteSheet(DEFAULT_ABILITY_IMAGE_PATH + 'fireball_sheet_10.png')
def activate_fireball(ability, player):
    print("Fireball activated")
    ability.is_active = True
    ability.projectile = AbilityProjectile(ability=ABILITY_DATA['Fireball'],
                                           spritesheet=fire_ball_spritesheet,
                                           x_pos=player.position[0],
                                           y_pos=player.position[1],
                                           x_vel=6,
                                           y_vel=0,
                                           direction=player.direction,
                                           collision_effect=fireball_collision_effect)
    player.projectiles.append(ability.projectile)
def run_fireball(ability, screen):
    # ADD COLLISION CHECKS RIGHT HERE LATER
    physics.update_kinematics(ability.projectile, 5)
    ability.projectile.display(screen)
def fireball_collision_effect(self, target):
    target.take_damage(self.damage)

# ================================= INVISIBILITY SKILL FUNCTIONS ====================================================
def activate_invisibility(ability, player):
    ability.player = player

    if not ability.is_active:
        ability.is_active = True

    else:
        ability.player.alpha = 255
        ability.is_active = False
def run_invisibility(ability, screen):
    if ability.is_active and  ability.player.alpha > 0:
        ability.player.alpha = max(ability.player.alpha - 5, 0)

# ================================= SHIELD SKILL FUNCTIONS ====================================================
def activate_shield(ability, player):
    ability.player = player
    if ability.is_active:
        ability.is_active = False
        ability.player.is_shielded = False
    else:
        ability.is_active = True
        ability.projectile = AbilityProjectile(ability=ABILITY_DATA['Lightning_Wall'],
                                               spritesheet=fire_ball_spritesheet,
                                               x_pos=player.position[0],
                                               y_pos=player.position[1],
                                               x_vel=0,
                                               y_vel=0,
                                               hitbox_height=80,
                                               hitbox_width=80,
                                               direction=player.direction,
                                               collision_effect=shield_collision_effect)
        player.projectiles.append(ability.projectile)
        ability.start_time = time.time()
def run_shield(ability, screen):
    ability.player.is_shielded = True
    ability.projectile.position = ability.player.position
    pygame.draw.rect(screen, "green", (ability.projectile.position, ability.projectile.hitbox_size))
    if cancel_on_timer(ability, 3):
        ability.is_active = False
        ability.player.projectiles.remove(ability.projectile)
        ability.player.is_shielded = False

def shield_collision_effect(self, target):
    print("shield collision detected")
    target.is_touching_ground = False
    target.velocity[1] -= 20

# ================================= LIGHTNING WALL SKILL FUNCTIONS ====================================================
def activate_lightning_wall(ability, player):
    ability.player = player
    if ability.is_active:
        ability.is_active = False
    else:
        ability.is_active = True
        ability.start_time = time.time()
        ability.projectile = AbilityProjectile(ability=ABILITY_DATA['Lightning_Wall'],
                                               spritesheet=fire_ball_spritesheet,
                                               x_pos=player.position[0] + 60 * player.direction,
                                               y_pos=player.position[1],
                                               x_vel=0,
                                               y_vel=0,
                                               hitbox_height=100,
                                               hitbox_width=50,
                                               direction=player.direction,
                                               collision_effect=lightning_wall_collision_effect)
        player.projectiles.append(ability.projectile)
def run_lightning_wall(ability, screen):
    pygame.draw.rect(screen, "blue", (ability.projectile.rect))
    physics.update_kinematics(ability.projectile, 5)
    if cancel_on_timer(ability, 3):
        ability.is_active = False
        ability.player.projectiles.remove(ability.projectile)
def lightning_wall_collision_effect(self, target):
    print("collision detected")
    target.take_damage(self.damage)

# ================================= TELEPORT SKILL FUNCTIONS ====================================================
def activate_teleport(ability, player):
    ability.player = player
    if ability.is_active:
        ability.is_active = False
    else:
        ability.is_active = True
def run_teleport(ability, screen):
    ability.player.teleport_range = 500
    pygame.draw.circle(screen, "blue", (ability.player.position[0], ability.player.position[1]), ability.player.teleport_range, 1)
    if pygame.mouse.get_pressed()[0]:
        ability.player.position = [pygame.mouse.get_pos()[0] + ability.player.position[0], pygame.mouse.get_pos()[1] - ability.player.position[1]]
        ability.is_active = False

    print("Running teleport")

# ================================= LEVITATE SKILL FUNCTIONS ====================================================
def activate_levitate(ability, player):
    ability.player = player
    if ability.is_active:
        ability.player.jump_height = 5
        ability.player.gravity_value = 0.02
        ability.is_active = False

    else:
        ability.this_frames_health = ability.player.stats['current_health']
        ability.player.gravity_value = 0.0
        ability.player.jump_height = 1
        ability.is_active = True
def run_levitate(ability, screen):
    if ability.this_frames_health < ability.player.stats['current_health']:
        print("lost health mid air")
        ability.player.jump_height = 5
        ability.player.gravity_value = 0.02
        ability.is_active = False

# ================================= STAND-IN TESTING FUNCTIONS ====================================================
def test_active_skill(self, player):
    self.is_active = True
    print("I am now active!")
def test_run_skill(self):
    print("I am running!")

def dash(player):
    if player.is_touching_ground:
        player.velocity[0] += 10 * player.direction

def cancel_on_timer(ability, duration):
    print('start time:', ability.start_time)
    print('end time:', ability.start_time + duration)
    return ability.start_time + duration < time.time()

# Centralized repository of abilities
ABILITY_DATA = {
    "Levitate": {"damage": 0, "cost": 0, "cooldown": 0, "sound_fx": 'fireball_woosh.mp3', "activation_skill": lambda self, player: activate_levitate(self, player), 'effect': lambda self, screen: run_levitate(self, screen)},
    "Heal": {"damage": -30, "cost": 15, "cooldown": 5, "sound_fx": 'fireball_woosh.mp3', "activation_skill": lambda self, player: test_active_skill(self, player=player), 'effect': lambda self, player: test_active_skill(self, player=player)},
    "Dash": {"damage": 0, "cost": 5, "cooldown": 5, "sound_fx": 'fireball_woosh.mp3', "activation_skill": lambda player: dash(player), 'effect': lambda self, player: test_active_skill(self, player=player)},
    "Fireball": {"damage": 500, "cost": 20, "cooldown": 3, "sound_fx": 'fireball_woosh.mp3', "activation_skill": lambda self, player: activate_fireball(self, player=player), 'effect': lambda self, player, **kwargs: run_fireball(self, player, **kwargs)},
    "Teleport": {"damage": 0, "cost": 0, "cooldown": 5, "sound_fx": 'fireball_woosh.mp3', "activation_skill": lambda self, player: activate_teleport(self, player=player), 'effect': lambda self, screen: run_teleport(self, screen)},
    "Invisibility": {"damage": 0, "cost": 50, "cooldown": 8, "sound_fx": 'invisibility.mp3', "activation_skill": lambda self, player: activate_invisibility(self, player), 'effect': lambda self, screen: run_invisibility(self, screen)},
    "Shield": {"damage": 0, "cost": 0, "cooldown": 5, "sound_fx": 'shield.mp3', "activation_skill": lambda self, player: activate_shield(self, player),'effect': lambda self, player, **kwargs: run_shield(self, player, **kwargs)},
    "Lightning_Wall": {"damage": 50, "cost": 0, "cooldown": 5, "sound_fx": 'lightning_wall.wav', "activation_skill": lambda self, player: activate_lightning_wall(self, player), 'effect': lambda self, screen: run_lightning_wall(self, screen)},
}


def create_ability_from_data(name):
    data = ABILITY_DATA[name]
    return Ability(name=name,
                   damage=data["damage"],
                   cost=data["cost"],
                   cooldown=data["cooldown"],
                   sound_fx=pygame.mixer.Sound(DEFAULT_ABILITY_SOUND_FX_PATH + data["sound_fx"]),
                   activate=data["activation_skill"],
                   effect=data['effect'])
