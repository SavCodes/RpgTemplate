import pygame
import random


class Particle:
    def __init__(self, x, y, dx, dy, color, lifespan):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.color = color
        self.lifespan = lifespan
        self.age = 0

    def update(self):
        # Move the particle
        self.x += self.dx
        self.y += self.dy

        # Apply gravity for a more realistic effect
        self.dy += 0.1

        # Age the particle
        self.age += 1

    def render(self, screen):
        # Fade the particle based on its age
        alpha = max(0, 255 - int((self.age / self.lifespan) * 255))
        particle_color = (*self.color, alpha)

        surface = pygame.Surface((5, 5), pygame.SRCALPHA)
        pygame.draw.circle(surface, particle_color, (2, 2), 2)
        screen.blit(surface, (self.x, self.y))

    def is_dead(self):
        return self.age >= self.lifespan


class BloodSpurtEffect:
    def __init__(self):
        self.particles = []

    def emit(self, x, y):
        for _ in range(30):  # Number of particles per spurt
            dx = random.uniform(-3, 3)  # Random horizontal speed
            dy = random.uniform(-3, 3)  # Random vertical speed
            color = (139, 0, 0)  # Blood red color
            lifespan = random.randint(30, 60)  # Lifespan in frames
            self.particles.append(Particle(x, y, dx, dy, color, lifespan))

    def update(self):
        for particle in self.particles:
            particle.update()

        # Remove dead particles
        self.particles = [p for p in self.particles if not p.is_dead()]

    def render(self, screen):
        for particle in self.particles:
            particle.render(screen)


# Example usage
if __name__ == "__main__":
    pygame.init()

    # Screen setup
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Blood Spurt Effect")
    clock = pygame.time.Clock()

    # Blood effect instance
    blood_effect = BloodSpurtEffect()

    running = True
    while running:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Emit blood on mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                blood_effect.emit(x, y)

        # Update and render the blood effect
        blood_effect.update()
        blood_effect.render(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
