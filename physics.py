import pygame

def update_kinematics(object, x_vel_cap=100, y_vel_cap=100, x_acc_cap=100, y_acc_cap=100):
    """Update the position, velocity,acceleration, and the direction of movement of an object"""
    if object.velocity[0] > 0:
        object.direction = 1
    elif object.velocity[0] < 0:
        object.direction = -1

    # Set a cap on accelerations, 100 pixels per frame per frame by default
    object.acceleration[0] = min(object.acceleration[0], x_acc_cap)
    object.acceleration[1] = min(object.acceleration[1], y_acc_cap)

    # Set a cap on velocities, 100 pixels per frame by default
    object.velocity[0] = min(object.acceleration[0] + object.velocity[0], x_vel_cap)
    object.velocity[1] = min(object.acceleration[1] + object.velocity[1], y_vel_cap)



    # Update position based on movement vectors
    object.position[0] += object.velocity[0]
    object.position[1] += object.velocity[1]

def gravity(sprite, gravity_value=0.01):
    if sprite.is_touching_ground:
        sprite.acceleration[1] = 0
        sprite.velocity[1] = 0

    elif not sprite.is_touching_ground and sprite.velocity[1] < 0:
        sprite.acceleration[1] += gravity_value * 0.7

    else:
        sprite.acceleration[1] += gravity_value

def friction(sprite, friction_value=0.05):
    if sprite.velocity[0] != 0:
        sprite.velocity[0] *= (1 - friction_value)

def tile_optimizer(player, tile_set, TILE_SIZE):
    x_index = (player.position[0] + player.width // 2) // TILE_SIZE
    feet_y_index = (player.position[1] + player.height - TILE_SIZE) // TILE_SIZE
    head_y_index = (player.position[1] // TILE_SIZE)
    floor_index = feet_y_index + 1
    projected_y = player.position[1] + player.velocity[1]

    if not tile_set[int(floor_index)][int(x_index)].is_collidable:
        player.is_touching_ground = False

    # Find neighboring walls that are collidable
    return [tile_set[int(head_y_index + y)][int(x_index + x)] for x in range(-1, 2) for y
                            in
                            range(-1, int(player.height // TILE_SIZE + 1)) if
                            tile_set[int(head_y_index + y)][int(x_index + x)].is_collidable]

# ============================== COLLISION DETECTION FRAMEWORK =====================================
def colliderect(rect_1, rect_2):
    x_range_1 = set(range(int(rect_1[0]), int(rect_1[0]) + int(rect_1[2]) + 1))
    x_range_2 = set(range(int(rect_2[0]), int(rect_2[0]) + int(rect_2[2]) + 1))
    y_range_1 = set(range(int(rect_1[1]), int(rect_1[1]) + int(rect_1[3]) + 1))
    y_range_2 = set(range(int(rect_2[1]), int(rect_2[1]) + int(rect_2[3]) + 1))


    return True if x_range_1 & x_range_2 and y_range_1 & y_range_2 else False

def resolve_y_collision(resolving_object, wall):
    projected_y = resolving_object.velocity[1] + resolving_object.position[1]

    resolving_object.y_collision_head_hitbox = (resolving_object.position[0] + resolving_object.width // 2 - resolving_object.width_buffer + 2,
                                               projected_y, 2 * resolving_object.width_buffer - 4, resolving_object.height // 2)

    resolving_object.y_collision_foot_hitbox = (resolving_object.position[0] + resolving_object.width // 2,
                                                projected_y + resolving_object.height - resolving_object.height // 2 + 1, 2, resolving_object.height)

    # Y-Axis collision handling
    if wall.is_collidable and colliderect(resolving_object.y_collision_head_hitbox, wall.rect) and resolving_object.velocity[1] <= 0:
        # Rising collision handling
        resolving_object.position[1] = wall.rect[1] + wall.rect[3]
        resolving_object.velocity[1] = 0
        resolving_object.acceleration[1] = 0

    if wall.is_collidable and colliderect(resolving_object.y_collision_foot_hitbox, wall.rect) and resolving_object.velocity[1] > 0:
        # Landing collision handling
        resolving_object.position[1] = wall.rect[1] - resolving_object.height
        resolving_object.is_touching_ground = True

def resolve_x_collision(resolving_object, wall, width_buffer=16):
    projected_x = resolving_object.position[0] + resolving_object.velocity[0]

    if resolving_object.direction > 0:
        resolving_object.x_collision_hitbox = (projected_x + resolving_object.width // 2, resolving_object.position[1] + 3,
                                              resolving_object.width_buffer, resolving_object.height * .7)
    else:
        resolving_object.x_collision_hitbox = (projected_x + resolving_object.width // 2 - resolving_object.width_buffer,
                                              resolving_object.position[1] + 3,
                                              resolving_object.width_buffer, resolving_object.height * .7)

    # X-Axis collision handling
    if wall.is_collidable and colliderect(resolving_object.x_collision_hitbox, wall.rect):
        # Right sided collision handling
        if resolving_object.velocity[0] > 0 and resolving_object.position[0] + resolving_object.width // 2 < wall.position[0] + wall.width - width_buffer:
            resolving_object.position[0] = wall.position[0] - resolving_object.width //2 - resolving_object.width_buffer
            resolving_object.acceleration[0] = 0
            resolving_object.velocity[0] = 0

        # Left sided collision handling
        elif resolving_object.velocity[0] < 0 and resolving_object.position[0] + resolving_object.width // 2 > wall.position[0] + width_buffer:
            resolving_object.position[0] = wall.position[0] + wall.width - resolving_object.width_buffer
            resolving_object.acceleration[0] = 0
            resolving_object.velocity[0] = 0

def resolve_collision(player, tile_set):
    for wall in tile_set:
        resolve_y_collision(player, wall)
        resolve_x_collision(player, wall)

class KinematicObject:
    def __init__(self, position, width, height, width_buffer=16, scale=1.0):
        self.position = [position[0], position[1]]
        self.velocity = [0, 0]
        self.acceleration = [0, 0]
        self.direction = 1

        self.width_buffer = width_buffer * scale
        self.width = width * scale
        self.height = height * scale

        self.x_speed_cap = 3 * scale
        self.y_speed_cap = 3 * scale
        self.rect =  (self.position[0], self.position[1], self.width, self.height)

        self.is_touching_ground = False