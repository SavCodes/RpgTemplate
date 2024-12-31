import pygame
import time

class AbilityController:
    def __init__(self, player, game):
        self.player = player
        self.game = game
        self.camera = game.camera
        self.shader = game.game_shader
        self.active_effects = []

    def ability_event_checker(self, game_event):
        if game_event.type == pygame.KEYDOWN:
            if game_event.key == self.player.config["controls"][2]:
                self.player.change_state('jumping')
                self.player.jump_player()

            elif game_event.key == pygame.K_1:
                self.player.abilities[0].apply()
                self.active_effects.append((self.player.abilities[0], time.time()))

            elif game_event.key == pygame.K_2 and len(self.player.abilities) >= 2:
                self.player.abilities[1].apply()
                self.active_effects.append((self.player.abilities[1], time.time()))

            elif game_event.key == pygame.K_3 and len(self.player.abilities) >= 3:
                self.player.abilities[2].apply()
                self.active_effects.append((self.player.abilities[2], time.time()))

            elif game_event.key == pygame.K_4 and len(self.player.abilities) >= 4:
                self.player.abilities[3].apply()
                self.active_effects.append((self.player.abilities[3], time.time()))


            elif game_event.key == pygame.K_5 and len(self.player.abilities) >= 5:
                self.player.abilities[4].apply()
                self.active_effects.append((self.player.abilities[4], time.time()))
                self.player.change_state('casting')

            elif game_event.key == pygame.K_6 and len(self.player.abilities) >= 6:
                self.player.abilities[5].apply()
                self.active_effects.append((self.player.abilities[5], time.time()))
                self.player.change_state('casting')

            elif game_event.key == pygame.K_q and self.player.state != 'sliding':
                self.player.change_state('sliding')


            elif game_event.key == pygame.K_q and not self.player.is_attacking:
                self.player.change_state('attacking')

            elif game_event.key == pygame.K_ESCAPE:
                self.player.stats['current_health'] -= 10

        self.render_shader_effects()

    def render_shader_effects(self):
        for effect in self.active_effects:
            ability, time_used = effect
            effect = ability.render_effect

            if ability.render_effect:
                if time.time() - time_used > ability.render_effect_duration:
                    self.shader.program[effect] = 0

                else:
                    self.shader.program['origin'] = (self.player.position[0] - self.camera.x) / self.camera.screen_width, self.player.position[1] / self.camera.world_height
                    self.shader.program[effect] = 3

    def animate_abilities(self, position):
        for ability in self.player.abilities:
            if ability.is_animating:
                ability.animation.basic_animate()