import pygame

class GameLoop:
    def __init__(self, game):
        self.game = game

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False
            self.game.handle_events()

    def update(self):
        self.game.update_game()

    def render(self):
        self.game.screen.fill("black")
        self.game.render_game()
        pygame.display.flip()

def run(game):
    game_loop = GameLoop(game)
    while game.running:
        game_loop.handle_events()
        game_loop.update()
        game_loop.render()
        game.clock.tick(60)
    pygame.quit()
