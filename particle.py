import pygame
import random
import math


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
        self.dy += 0.05

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
        for _ in range(2):  # Number of particles per spurt
            dx = random.uniform(-7, 7)  # Random horizontal speed
            dy = random.uniform(-1, 3)  # Random vertical speed
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


class ExperienceParticle(Particle):
    def __init__(self, x, y, dx, dy, color, lifespan, player, value):
        super().__init__(x, y, dx, dy, color, lifespan)
        self.player = player
        self.value = value

    def update(self):
        # Calculate attraction toward the player
        player_x, player_y = self.player.position
        distance_x = player_x - self.x
        distance_y = player_y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2)

        if distance != 0:
            # Normalize and apply attraction force
            attraction_strength = 0.1  # How strongly it moves toward the player
            self.dx += (distance_x / distance) * attraction_strength
            self.dy += (distance_y / distance) * attraction_strength

        # Apply velocity
        self.x += self.dx
        self.y += self.dy

        # Age the particle
        self.age += 1

    def on_collect(self):
        # Add experience to the player
        self.player.gain_experience(self.value)
        self.age = self.lifespan  # Mark as "dead"

    def check_collision(self):
        # Simple collision check with the player
        player_rect = pygame.Rect(self.player.position[0], self.player.position[1], self.player.width, self.player.height)
        particle_rect = pygame.Rect(self.x, self.y, 5, 5)
        if player_rect.colliderect(particle_rect):
            self.on_collect()


class ExperienceEffect:
    def __init__(self, player):
        self.player = player
        self.particles = []

    def emit(self, x, y, value, count=1):
        for _ in range(count):  # Number of experience particles per burst
            dx = random.uniform(-1, 1)  # Random initial horizontal speed
            dy = random.uniform(-1, 1)  # Random initial vertical speed
            color = (255, 215, 0)  # Golden yellow for experience
            lifespan = random.randint(60, 120)  # Lifespan in frames
            self.particles.append(ExperienceParticle(x, y, dx, dy, color, lifespan, self.player, value))

    def update(self):
        for particle in self.particles:
            particle.update()
            particle.check_collision()

        # Remove dead particles
        self.particles = [p for p in self.particles if not p.is_dead()]

    def render(self, screen):
        for particle in self.particles:
            particle.render(screen)




