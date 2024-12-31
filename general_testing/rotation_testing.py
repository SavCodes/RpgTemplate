import pygame
import sys
import math


def rotate_image(image, pivot, angle):
    """
    Rotates an image around a pivot point.

    Args:
        image (pygame.Surface): The image to rotate.
        pivot (tuple): The (x, y) coordinates of the pivot point relative to the image's top-left.
        angle (float): The angle to rotate the image, in degrees.

    Returns:
        pygame.Surface: The rotated image.
        pygame.Rect: The rect of the rotated image, adjusted to keep the pivot in place.
    """
    # Rotate the image
    rotated_image = pygame.transform.rotate(image, angle)

    # Calculate the new rect for the rotated image
    original_rect = image.get_rect(topleft=(0, 0))
    pivot_vector = pygame.Vector2(pivot)
    rotated_pivot = pivot_vector.rotate(-angle)  # Rotate the pivot point (inverse of image rotation)
    new_center = (original_rect.centerx - rotated_pivot.x, original_rect.centery - rotated_pivot.y)
    rotated_rect = rotated_image.get_rect(center=new_center)

    return rotated_image, rotated_rect


# Initialize Pygame
pygame.init()

# Screen setup
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()


# Load a weapon image
weapon_image = pygame.image.load("../game_assets/spritesheets/weapons/still_sword.png").convert_alpha()

# Weapon pivot point (handle at bottom-left corner)
pivot_point = (0, weapon_image.get_height())

# Player position (center of screen for example)
player_position = (400, 300)

# Variables for rocking effect
rocking_speed = 3  # Speed of oscillation
rocking_angle_range = 10  # Maximum rotation angle (degrees)
time = 0  # Time counter for sine wave

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Clear the screen
    screen.fill((30, 30, 30))

    # Calculate the rocking angle using a sine wave
    time += clock.get_time() / 1000  # Increment time based on frame duration
    rocking_angle = math.sin(time * rocking_speed) * rocking_angle_range

    # Rotate the weapon image around the handle
    rotated_weapon, rotated_weapon_rect = rotate_image(weapon_image, pivot_point, rocking_angle)

    # Position the rotated weapon at the player's position, adjusted for pivot
    rotated_weapon_rect.topleft = (player_position[0] - pivot_point[0], player_position[1] - pivot_point[1])

    # Draw the rotated weapon
    screen.blit(rotated_weapon, rotated_weapon_rect.topleft)

    # Update the display
    pygame.display.flip()
    clock.tick(60)
