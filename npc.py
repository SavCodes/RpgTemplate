import pygame
import spritesheet
import chatbox
from config import *

class Npc:
    def __init__(self, game, animation, position):
        self.position = pygame.math.Vector2(position)
        self.chatbox = chatbox.ChatBox(self.position, "npc_1", "introduction")
        self.idle_sprite = spritesheet.SpriteSheet(DEFAULT_NPC_SPRITESHEET_PATH + animation, scale=GAME_SCALE)
        self.exclamation_sprite = spritesheet.SpriteSheet("./game_assets/animated_tiles/exclamation_point_10.png", scale=GAME_SCALE)
        self.game = game

    def render_npc(self, player, screen):
        self.chatbox.location = pygame.math.Vector2(self.position[0] - self.game.camera.camera.x, self.position[1] - self.game.camera.camera.y)
        screen.blit(self.idle_sprite.basic_animate()[0],self.position)

        if self.chatbox.dialogue_index < len(self.chatbox.character_chat_tree) - 1:
            screen.blit(self.exclamation_sprite.basic_animate()[0], (self.position[0], self.position[1] - 32 * GAME_SCALE))

    def interact_with_player(self, player, screen):
        if (self.position - player.position).magnitude() <= 400:
            if self.chatbox.is_displaying:
                self.chatbox.render_chat_box(self.game.screen)

    def event_checker(self, event):
        if event.type != pygame.KEYDOWN:
            return

        elif event.key == pygame.K_e:
            self.chatbox.is_displaying = True

        elif event.key == pygame.K_ESCAPE:
            self.chatbox.escape_chat()

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.chatbox.progress_chat()