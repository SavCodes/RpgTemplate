import pygame
from PIL import Image, ImageFilter, ImageEnhance

from config import DEFAULT_ENEMY_SPRITESHEET_PATH, GAME_SCALE

ANIMATION_SPEED = 0.1

class SpriteSheet:
    def __init__(self, sprite_sheet, scale=1.0, frame_width=32, frame_height=32, x_offset=0, y_offset=0):
        self.sprite_sheet = sprite_sheet
        self.width = frame_width
        self.height = frame_height
        self.sprites = pygame.image.load(sprite_sheet).convert_alpha()
        self.number_of_animations = int(sprite_sheet[sprite_sheet.rfind("_")+1:sprite_sheet.rfind(".")])
        self.scale = scale
        self.frame_list = [self.sprites.subsurface((self.width*index+x_offset,0 , self.width, self.height- y_offset)) for index in range(self.number_of_animations)]
        self.frame_list = [pygame.transform.scale_by(frame, scale) for frame in self.frame_list]
        self.animation_index = 0
        self.animation_speed = 0.25

    def __repr__(self):
        return f"{self.sprite_sheet}"

    def load_spritesheets(self, sprite_paths, width, height, x_offset=0, y_offset=0, rescale_x=64, rescale_y=64):
        self.animations = {
            key: SpriteSheet(path, frame_width=width, frame_height=height, scale=GAME_SCALE, y_offset=y_offset, x_offset=x_offset)
            for key, path in sprite_paths.items()
        }

        if rescale_x is not None and rescale_y is not None:
            for animation in self.animations.values():
                animation.rescale_frames(rescale_x, rescale_y)

    def basic_animate(self, dampener=1):
        if self.animation_index < self.number_of_animations - 1:
            self.animation_index += self.animation_speed * dampener
        else:
            self.animation_index = 0

        return self.frame_list[int(self.animation_index)], self.animation_index

    def reset_animation(self):
        self.animation_index = 0

    def rescale_frames(self, x_rescale, y_rescale):
        self.frame_list = [pygame.transform.scale(frame, (x_rescale, y_rescale)) for frame in self.frame_list]

class AnimatedTileManager:
    def __init__(self):
        self.animated_background_tiles = []
        self.animated_foreground_tiles = []

    def add_tile(self, sprite_sheet, location, tile_set, animation_speed=ANIMATION_SPEED):
        """Add a new animated tile."""
        tile_set.append({
            "sprite_sheet": sprite_sheet,
            "location": location,
            "animation_speed": animation_speed
        })

    def draw_tiles(self, surface, tile_set, dampener_speed=1):
        """Draw all animated tiles to the surface."""
        for tile in tile_set:
            frame = tile["sprite_sheet"].basic_animate(dampener_speed)
            surface.blit(frame, tile["location"])


def load_spritesheets(self, sprite_paths, width, height, x_offset=0, y_offset=0, rescale_x=64, rescale_y=64):
    self.animations = {
        key: SpriteSheet(path, width=width, height=height, scale=GAME_SCALE, y_offset=y_offset, x_offset=x_offset)
        for key, path in sprite_paths.items()
        }

    if rescale_x is not None and rescale_y is not None:
        for animation in self.animations.values():
            animation.rescale_frames(rescale_x, rescale_y)

def sheet_to_row(file_path, split_height, x_offset=0, y_offset=0):
    image = Image.open(file_path)
    width, height = image.size
    rows = height // split_height
    for i in range(rows):
        image = Image.open(file_path)
        image.crop((0+x_offset, i*split_height+y_offset, width, (i+1)*split_height)).save(f"{file_path[:file_path.rfind('.', 2)]}_{i}.png")

def images_to_sheet(file_list, save_name, width=32, height=32, add_reverse=False):
    frames = [Image.open(file).resize((width,height)) for file in file_list]

    # Combine frames into a spritesheet
    length = 2 * width * len(frames) if add_reverse else width * len(frames)
    spritesheet = Image.new("RGBA", (length, height))

    for i, frame in enumerate(frames):
        spritesheet.paste(frame, (i * width, 0))

        if add_reverse:
            spritesheet.paste(frame, ((2 * len(frames) - 1 - i) * width, 0))

    # Save the spritesheet
    spritesheet.save("./"+save_name)
    print(f'File saved as ./{save_name}')

def crop(image, width, height, save_name=None, start_x=0, start_y=0):
    if save_name is None:
        save_name = image.split(".")[0] + "cropped.png"

    _image = pygame.image.load(image, "r")
    pygame.image.save(_image.subsurface((start_x, start_y, width, height)), save_name)

def convert_terrilbly_arranged_spritesheets(spritesheet, start_x=0, start_y=0, save_name=DEFAULT_ENEMY_SPRITESHEET_PATH + "cropped_images/", frames=8):
    width = 32
    height = 32
    rows = pygame.image.load(spritesheet).get_height() // height
    for j in range(rows):
        file_list = []
        for i in range(frames):
            print("cropping sheet starting at: ", height*j + start_y)
            crop(spritesheet, width, height, start_x=width*i + start_x, start_y=height*j +start_y, save_name=DEFAULT_ENEMY_SPRITESHEET_PATH + f"cropped_images/{i}_{j}.png")
            file_list.append(save_name + f"{i}_{j}.png")
        images_to_sheet(file_list, DEFAULT_ENEMY_SPRITESHEET_PATH + f"./new_sheet_{i}_{j}.png")


if __name__ == "__main__":
    # CREATE SPRITESHEETS FROM MAIN PACK
    #sheet_to_row(DEFAULT_ENEMY_SPRITESHEET_PATH+"spritesheet_pack.png", 64)

    # SMALL MOB IDLE
    #convert_terrilbly_arranged_spritesheets(DEFAULT_ENEMY_SPRITESHEET_PATH+"small_mob_attack_14_uncropped.png", start_x=16, start_y=16, frames=14)

    # SMALL MOD WALK
    #convert_terrilbly_arranged_spritesheets(DEFAULT_ENEMY_SPRITESHEET_PATH+"small_mob_walk_8.png", start_x=16, start_y=16, frames=8)

    # SMALL MOD DEATH
    #convert_terrilbly_arranged_spritesheets(DEFAULT_ENEMY_SPRITESHEET_PATH+"small_mob_death_14.png", start_x=16, start_y=16, frames=14)

    # SMALL MOD WALK
    convert_terrilbly_arranged_spritesheets(DEFAULT_ENEMY_SPRITESHEET_PATH+"tentacle_shadow_mob/small_mob_take_damage_3_uncropped.png", start_x=16, start_y=16, frames=6)
    take_damage = ["./game_assets/spritesheets/enemy_spritesheets/cropped_images/0_0.png",
                   "./game_assets/spritesheets/enemy_spritesheets/cropped_images/0_1.png",
                   "./game_assets/spritesheets/enemy_spritesheets/cropped_images/0_2.png",
                   "./game_assets/spritesheets/enemy_spritesheets/cropped_images/0_3.png",
                   "./game_assets/spritesheets/enemy_spritesheets/cropped_images/0_4.png",
                   "./game_assets/spritesheets/enemy_spritesheets/cropped_images/0_5.png"
                   ]
    images_to_sheet(take_damage, "tentacle_shadow_mob/small_mob_take_damage_3.png")

    #crop("./game_assets/abilities/Lightning_Wall_icon.png", 32, 32)

    # hit =  ["./game_assets/abilities/B500-2.PNG", "./game_assets/abilities/B500-3.PNG", "./game_assets/abilities/B500-4.PNG"]
    # images_to_sheet(hit, "fireball_hit_sheet_3.png")

    # convert_terrilbly_arranged_spritesheets("./game_assets/concept_art/adventurer-1.3-Sheet.png", frames=8)

    # pygame.transform(pygame.image.load("game_assets/spritesheets/player_spritesheets/walk_12.png", "r"), (1786, 32))

    pass