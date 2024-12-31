import pygame

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
