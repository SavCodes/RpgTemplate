import pygame
import random
import math

class LightningBoltEffect:
    def __init__(self, start_pos, end_pos, color=(255, 255, 0), thickness=2, duration=100):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.color = color
        self.thickness = thickness
        self.duration = duration
        self.timer = duration
        self.segments = self.generate_segments()
        self.discharge_particles = []

    def generate_segments(self):
        """Generate the zig-zag pattern for the lightning bolt."""
        segments = [self.start_pos]
        num_segments = random.randint(5, 10)
        for i in range(1, num_segments):
            lerp_factor = i / num_segments
            x = self.start_pos[0] + lerp_factor * (self.end_pos[0] - self.start_pos[0])
            y = self.start_pos[1] + lerp_factor * (self.end_pos[1] - self.start_pos[1])
            offset_x = random.randint(-15, 15)
            offset_y = random.randint(-15, 15)
            segments.append((x + offset_x, y + offset_y))
        segments.append(self.end_pos)
        return segments

    def update(self, dt):
        """Update the effect timer and manage discharge particles."""
        self.timer -= dt

        # Update particle positions
        for particle in self.discharge_particles:
            particle["lifetime"] -= dt
            particle["pos"][0] += particle["velocity"][0] * dt / 1000
            particle["pos"][1] += particle["velocity"][1] * dt / 1000
            particle["velocity"][1] += particle["gravity"] * dt / 1000  # Gravity effect

        # Remove expired particles
        self.discharge_particles = [p for p in self.discharge_particles if p["lifetime"] > 0]

        # Create discharge particles when the bolt expires
        if self.timer <= 0 and not self.discharge_particles:
            self.create_discharge_particles()

    def create_discharge_particles(self):
        """Create burst particles that fall with gravity."""
        # for _ in range(random.randint(15, 25)):
        #     angle = random.uniform(0, 2 * math.pi)
        #     speed = random.uniform(50, 150)
        #     velocity = [speed * math.cos(angle), speed * math.sin(angle)]
        #     lifetime = random.uniform(400, 800)
        #     self.discharge_particles.append({
        #         "pos": list(self.end_pos),
        #         "velocity": velocity,
        #         "gravity": random.uniform(300, 500),
        #         "lifetime": lifetime,
        #         "color": (
        #             random.randint(200, 255),
        #             random.randint(200, 255),
        #             random.randint(100, 200),
        #         ),
        #     })
        pass

    def draw(self, screen):
        """Draw the lightning bolt and discharge particles."""
        if self.timer > 0:
            for i in range(len(self.segments) - 1):
                pygame.draw.line(screen, self.color, self.segments[i], self.segments[i + 1], self.thickness)

        for particle in self.discharge_particles:
            pygame.draw.circle(screen, particle["color"], (int(particle["pos"][0]), int(particle["pos"][1])), 2)

class LightningManager:
    def __init__(self):
        self.effects = []

    def trigger(self, start_pos, end_pos, count=3):
        """Trigger multiple lightning bolts with varying colors."""
        for _ in range(count):
            color_variation = (
                random.randint(200, 255),
                random.randint(200, 255),
                random.randint(150, 255),
            )
            self.effects.append(LightningBoltEffect(start_pos, end_pos, color=color_variation))

    def update(self, dt):
        """Update all active effects."""
        for effect in self.effects:
            effect.update(dt)
        # Remove expired effects
        self.effects = [effect for effect in self.effects if effect.timer > 0 or effect.discharge_particles]

    def draw(self, screen):
        """Draw all active effects."""
        for effect in self.effects:
            effect.draw(screen)

# Example usage in a game loop
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    lightning_manager = LightningManager()

    running = True
    while running:
        dt = clock.tick(60)  # Milliseconds since the last frame
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Trigger lightning bolts on mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                lightning_manager.trigger(pygame.mouse.get_pos(), (800, 300))

        # Update and draw effects
        lightning_manager.update(dt)
        lightning_manager.draw(screen)

        pygame.display.flip()

    pygame.quit()
