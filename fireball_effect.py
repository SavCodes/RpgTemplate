import pygame
import random
import math

# Initialize Pygame
# Screen settings
WIDTH, HEIGHT = 800, 600

# Colors
BLACK = (0, 0, 0)
RED = (255, 69, 0)
ORANGE = (255, 140, 0)
YELLOW = (255, 215, 0)

# Particle classes
class Particle:
    def __init__(self, x, y, color, lifetime, velocity):
        self.x = x
        self.y = y
        self.color = color
        self.lifetime = lifetime
        self.velocity = velocity
        self.age = 0

    def update(self):
        # Move particle
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.age += 1

    def is_dead(self):
        return self.age >= self.lifetime

    def draw(self, surface):
        if not self.is_dead():
            # Fade effect as particle ages
            alpha = max(255 - int((self.age / self.lifetime) * 255), 0)
            particle_surface = pygame.Surface((6, 6), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, (*self.color, alpha), (3, 3), 3)
            surface.blit(particle_surface, (self.x - 3, self.y - 3))


class Fireball:
    def __init__(self, projectile):
        self.projectile = projectile
        self.x = projectile.position[0] + projectile.hitbox_size[0]
        self.y = projectile.position[1] + projectile.hitbox_size[1]
        self.direction = projectile.direction
        self.trail_particles = []
        self.explosion_particles = []
        self.is_exploded = False

    def move(self):
        if not self.is_exploded:
            self.x = self.projectile.position[0] + self.projectile.hitbox_size[0] // 2
            self.y = self.projectile.position[1] + self.projectile.hitbox_size[1] // 2
            self.generate_trail()

    def generate_trail(self):
        for _ in range(3):  # Create multiple trail particles
            velocity = (random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5))
            color = random.choice([RED, ORANGE, YELLOW])
            particle = Particle(self.x, self.y, color, lifetime=30, velocity=velocity)
            self.trail_particles.append(particle)

    def trigger_explosion(self):
        self.is_exploded = True
        for _ in range(50):  # Explosion generates more particles
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 5)
            velocity = (math.cos(angle) * speed, math.sin(angle) * speed)
            color = random.choice([RED, ORANGE, YELLOW])
            particle = Particle(self.x, self.y, color, lifetime=60, velocity=velocity)
            self.explosion_particles.append(particle)

    def update(self):
        if not self.is_exploded:
            self.move()

        # Update particles
        self.trail_particles = [p for p in self.trail_particles if not p.is_dead()]
        self.explosion_particles = [p for p in self.explosion_particles if not p.is_dead()]
        for particle in self.trail_particles + self.explosion_particles:
            particle.update()

    def draw(self, surface):
        # Draw particles
        for particle in self.trail_particles + self.explosion_particles:
            particle.draw(surface)

        # Draw fireball itself if not exploded
        if not self.is_exploded:
            pygame.draw.circle(surface, ORANGE, (int(self.x), int(self.y)), 10)