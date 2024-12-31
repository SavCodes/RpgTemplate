import pygame
from config import *
from config import DEFAULT_PLAYER_SPRITESHEET_PATH
from enemy import Boss

purple_guy_sprite_paths = {
    'idle': DEFAULT_PLAYER_SPRITESHEET_PATH + "purple_guy/Idle_4.png",
    'death': DEFAULT_PLAYER_SPRITESHEET_PATH + "purple_guy/Death_8.png",
    'run': DEFAULT_PLAYER_SPRITESHEET_PATH + "purple_guy/Run_6.png",
    'walk': DEFAULT_PLAYER_SPRITESHEET_PATH + "purple_guy/Walk_6.png",
    'attack': DEFAULT_PLAYER_SPRITESHEET_PATH + "purple_guy/Attack1_4.png",
    'jump': DEFAULT_PLAYER_SPRITESHEET_PATH + "purple_guy/Jump_8.png",
    'run_dust': DEFAULT_PLAYER_SPRITESHEET_PATH + "purple_guy/Run_Dust_6.png",
    'double_jump_dust': DEFAULT_PLAYER_SPRITESHEET_PATH + "purple_guy/Double_Jump_Dust_5.png"
}
knight = {
    "idle": DEFAULT_PLAYER_SPRITESHEET_PATH + "knight/idle_8.png",
    "death": DEFAULT_PLAYER_SPRITESHEET_PATH + "purple_guy/Death_8.png",
    "run": DEFAULT_PLAYER_SPRITESHEET_PATH + "knight/walk_8.png",
    "walk": DEFAULT_PLAYER_SPRITESHEET_PATH + "knight/walk_8.png",
    "attack": DEFAULT_PLAYER_SPRITESHEET_PATH + "knight/attack_1_8.png",
    "double_jump": DEFAULT_PLAYER_SPRITESHEET_PATH + "Double_Jump_Dust_5.png",
    "jump": DEFAULT_PLAYER_SPRITESHEET_PATH + "knight/jump_8.png",
    "run_dust": DEFAULT_PLAYER_SPRITESHEET_PATH + "Run_Dust_6.png",

}
custom_avatar = {
    'idle': DEFAULT_PLAYER_SPRITESHEET_PATH + "grey_avatar/walk_12.png",
    'walk': DEFAULT_PLAYER_SPRITESHEET_PATH + "grey_avatar/walk_12.png",
    'run': DEFAULT_PLAYER_SPRITESHEET_PATH + "grey_avatar/walk_12.png",
}
hooded_avatar = {
    'idle': DEFAULT_PLAYER_SPRITESHEET_PATH + "hooded_avatar/idle_12.png",
    'run': DEFAULT_PLAYER_SPRITESHEET_PATH + "hooded_avatar/run_12.png",
    'death': DEFAULT_PLAYER_SPRITESHEET_PATH + "hooded_avatar/idle_12.png",
    'walk': DEFAULT_PLAYER_SPRITESHEET_PATH + "hooded_avatar/run_12.png",
    'attack': DEFAULT_PLAYER_SPRITESHEET_PATH + "hooded_avatar/idle_12.png",
    'jump': DEFAULT_PLAYER_SPRITESHEET_PATH + "hooded_avatar/jump_12.png",
    'run_dust': DEFAULT_PLAYER_SPRITESHEET_PATH + "hooded_avatar/idle_12.png",
    'double_jump_dust': DEFAULT_PLAYER_SPRITESHEET_PATH + "hooded_avatar/idle_12.png",
    'spell_cast': DEFAULT_PLAYER_SPRITESHEET_PATH + "hooded_avatar/spell_cast_12.png",
    'slide': DEFAULT_PLAYER_SPRITESHEET_PATH + "hooded_avatar/slide_12.png",
}


boss_sprite_paths = {
        "walk": DEFAULT_ENEMY_SPRITESHEET_PATH + "horned_shadow_mob/boss_walk_16.png",
        "death": DEFAULT_ENEMY_SPRITESHEET_PATH + "horned_shadow_mob/boss_death_16.png",
        "hit": DEFAULT_ENEMY_SPRITESHEET_PATH + "horned_shadow_mob/boss_is_hit_3.png",
        "attack": DEFAULT_ENEMY_SPRITESHEET_PATH + "horned_shadow_mob/boss_attack_16.png",
        "idle": DEFAULT_ENEMY_SPRITESHEET_PATH + "horned_shadow_mob/boss_idle_16.png",
        "hit": DEFAULT_ENEMY_SPRITESHEET_PATH + "horned_shadow_mob/boss_take_damage_3.png",
    }
boss_sound_effects = {
    'death': pygame.mixer.Sound(DEFAULT_SOUND_FX_PATH + "monster_sounds/monster_death.wav"),
    'attack': pygame.mixer.Sound(DEFAULT_SOUND_FX_PATH + "monster_sounds/monster_attack.mp3")
}

small_mob_sprite_paths = {
        "walk": DEFAULT_ENEMY_SPRITESHEET_PATH + "tentacle_shadow_mob/small_mob_walk_8.png",
        "idle": DEFAULT_ENEMY_SPRITESHEET_PATH + "tentacle_shadow_mob/small_mob_idle_8.png",
        "attack": DEFAULT_ENEMY_SPRITESHEET_PATH + "tentacle_shadow_mob/small_mob_attack_14.png",
        "death": DEFAULT_ENEMY_SPRITESHEET_PATH + "tentacle_shadow_mob/small_mob_death_14.png",
        "hit": DEFAULT_ENEMY_SPRITESHEET_PATH + "tentacle_shadow_mob/small_mob_take_damage_5.png",
    }
small_mob_sound_effects = {
    'death': pygame.mixer.Sound(DEFAULT_SOUND_FX_PATH + "monster_sounds/monster_death.wav"),
    'attack': pygame.mixer.Sound(DEFAULT_SOUND_FX_PATH + "monster_sounds/monster_attack.mp3")
}

ENEMY_DATA = {
    "boss": {'sprite_paths': boss_sprite_paths, 'health':100, 'position': (600,75), 'width': 80, 'height': 64, 'rescale_x':64, 'rescale_y':64, 'sound_effects': boss_sound_effects},
    "mob": {'sprite_paths': small_mob_sprite_paths, 'health':100, 'position': (600,75), 'width': 32, 'height': 32, 'rescale_x':64, 'rescale_y':64, 'sound_effects': small_mob_sound_effects},
    "mob_1": {'sprite_paths': small_mob_sprite_paths, 'health': 100, 'position': (600, 75), 'width': 32, 'height': 32,'rescale_x':64, 'rescale_y':64,
            'sound_effects': small_mob_sound_effects},
    "mob_2": {'sprite_paths': small_mob_sprite_paths, 'health': 100, 'position': (600, 75), 'width': 32, 'height': 32,'rescale_x':64, 'rescale_y':64,
            'sound_effects': small_mob_sound_effects},
    "mob_3": {'sprite_paths': small_mob_sprite_paths, 'health': 100, 'position': (600, 75), 'width': 32, 'height': 32,'rescale_x':64, 'rescale_y':64,
            'sound_effects': small_mob_sound_effects},
    "mob_4": {'sprite_paths': small_mob_sprite_paths, 'health': 100, 'position': (600, 75), 'width': 32, 'height': 32,
            'rescale_x': 64, 'rescale_y': 64, 'sound_effects': small_mob_sound_effects},
    "mob_5": {'sprite_paths': small_mob_sprite_paths, 'health': 100, 'position': (600, 75), 'width': 32, 'height': 32,
            'rescale_x': 64, 'rescale_y': 64, 'sound_effects': small_mob_sound_effects},
    "mob_6": {'sprite_paths': small_mob_sprite_paths, 'health': 100, 'position': (600, 75), 'width': 32, 'height': 32,
            'rescale_x': 64, 'rescale_y': 64, 'sound_effects': small_mob_sound_effects},
    "mob_7": {'sprite_paths': small_mob_sprite_paths, 'health': 100, 'position': (600, 75), 'width': 32, 'height': 32,
            'rescale_x': 64, 'rescale_y': 64, 'sound_effects': small_mob_sound_effects},
    "mob_8": {'sprite_paths': small_mob_sprite_paths, 'health': 100, 'position': (600, 75), 'width': 32, 'height': 32,
            'rescale_x': 64, 'rescale_y': 64, 'sound_effects': small_mob_sound_effects},
    "mob_9": {'sprite_paths': small_mob_sprite_paths, 'health': 100, 'position': (600, 75), 'width': 32, 'height': 32,
            'rescale_x': 64, 'rescale_y': 64, 'sound_effects': small_mob_sound_effects},
    "mob_10": {'sprite_paths': small_mob_sprite_paths, 'health': 100, 'position': (600, 75), 'width': 32, 'height': 32,
            'rescale_x': 64, 'rescale_y': 64, 'sound_effects': small_mob_sound_effects},
    "mob_11": {'sprite_paths': small_mob_sprite_paths, 'health': 100, 'position': (600, 75), 'width': 32, 'height': 32,
            'rescale_x': 64, 'rescale_y': 64, 'sound_effects': small_mob_sound_effects},
    "mob_12": {'sprite_paths': small_mob_sprite_paths, 'health': 100, 'position': (600, 75), 'width': 32, 'height': 32,
            'rescale_x': 64, 'rescale_y': 64, 'sound_effects': small_mob_sound_effects},
    "mob_13": {'sprite_paths': small_mob_sprite_paths, 'health': 100, 'position': (600, 75), 'width': 32, 'height': 32,
            'rescale_x': 64, 'rescale_y': 64, 'sound_effects': small_mob_sound_effects},
    "mob_14": {'sprite_paths': small_mob_sprite_paths, 'health': 100, 'position': (600, 75), 'width': 32, 'height': 32,
            'rescale_x': 64, 'rescale_y': 64, 'sound_effects': small_mob_sound_effects},
    "mob_15": {'sprite_paths': small_mob_sprite_paths, 'health': 100, 'position': (600, 75), 'width': 32, 'height': 32,
            'rescale_x': 64, 'rescale_y': 64, 'sound_effects': small_mob_sound_effects},
    "mob_16": {'sprite_paths': small_mob_sprite_paths, 'health': 100, 'position': (600, 75), 'width': 32, 'height': 32,
            'rescale_x': 64, 'rescale_y': 64, 'sound_effects': small_mob_sound_effects},
    "mob_17": {'sprite_paths': small_mob_sprite_paths, 'health': 100, 'position': (600, 75), 'width': 32, 'height': 32,
            'rescale_x': 64, 'rescale_y': 64, 'sound_effects': small_mob_sound_effects},
    "mob_18": {'sprite_paths': small_mob_sprite_paths, 'health': 100, 'position': (600, 75), 'width': 32, 'height': 32,
            'rescale_x': 64, 'rescale_y': 64, 'sound_effects': small_mob_sound_effects},
    "mob_19": {'sprite_paths': small_mob_sprite_paths, 'health': 100, 'position': (600, 75), 'width': 32, 'height': 32,
            'rescale_x': 64, 'rescale_y': 64, 'sound_effects': small_mob_sound_effects},
    "mob_20": {'sprite_paths': small_mob_sprite_paths, 'health': 100, 'position': (600, 75), 'width': 32, 'height': 32,
            'rescale_x': 64, 'rescale_y': 64, 'sound_effects': small_mob_sound_effects},
    "mob_21": {'sprite_paths': small_mob_sprite_paths, 'health': 100, 'position': (600, 75), 'width': 32, 'height': 32,
            'rescale_x': 64, 'rescale_y': 64, 'sound_effects': small_mob_sound_effects},
    "mob_22": {'sprite_paths': small_mob_sprite_paths, 'health': 100, 'position': (600, 75), 'width': 32, 'height': 32,
            'rescale_x': 64, 'rescale_y': 64, 'sound_effects': small_mob_sound_effects},
    "mob_23": {'sprite_paths': small_mob_sprite_paths, 'health': 100, 'position': (600, 75), 'width': 32, 'height': 32,
            'rescale_x': 64, 'rescale_y': 64, 'sound_effects': small_mob_sound_effects},
    "mob_24": {'sprite_paths': small_mob_sprite_paths, 'health': 100, 'position': (600, 75), 'width': 32, 'height': 32,
            'rescale_x': 64, 'rescale_y': 64, 'sound_effects': small_mob_sound_effects},
    "mob_25": {'sprite_paths': small_mob_sprite_paths, 'health': 100, 'position': (600, 75), 'width': 32, 'height': 32,
            'rescale_x': 64, 'rescale_y': 64, 'sound_effects': small_mob_sound_effects},
    "mob_26": {'sprite_paths': small_mob_sprite_paths, 'health': 100, 'position': (600, 75), 'width': 32, 'height': 32,
            'rescale_x': 64, 'rescale_y': 64, 'sound_effects': small_mob_sound_effects},
    "mob_27": {'sprite_paths': small_mob_sprite_paths, 'health': 100, 'position': (600, 75), 'width': 32, 'height': 32,
            'rescale_x': 64, 'rescale_y': 64, 'sound_effects': small_mob_sound_effects},
    "mob_28": {'sprite_paths': small_mob_sprite_paths, 'health': 100, 'position': (600, 75), 'width': 32, 'height': 32,
            'rescale_x': 64, 'rescale_y': 64, 'sound_effects': small_mob_sound_effects},
    "mob_29": {'sprite_paths': small_mob_sprite_paths, 'health': 100, 'position': (600, 75), 'width': 32, 'height': 32,
            'rescale_x': 64, 'rescale_y': 64, 'sound_effects': small_mob_sound_effects},
    "mob_30": {'sprite_paths': small_mob_sprite_paths, 'health': 100, 'position': (600, 75), 'width': 32, 'height': 32,
            'rescale_x': 64, 'rescale_y': 64, 'sound_effects': small_mob_sound_effects},
    "mob_31": {'sprite_paths': small_mob_sprite_paths, 'health': 100, 'position': (600, 75), 'width': 32, 'height': 32,
            'rescale_x': 64, 'rescale_y': 64, 'sound_effects': small_mob_sound_effects},
    "mob_32": {'sprite_paths': small_mob_sprite_paths, 'health': 100, 'position': (600, 75), 'width': 32, 'height': 32,
            'rescale_x': 64, 'rescale_y': 64, 'sound_effects': small_mob_sound_effects},
    "mob_33": {'sprite_paths': small_mob_sprite_paths, 'health': 100, 'position': (600, 75), 'width': 32, 'height': 32,
               'rescale_x': 64, 'rescale_y': 64, 'sound_effects': small_mob_sound_effects},
    "mob_34": {'sprite_paths': small_mob_sprite_paths, 'health': 100, 'position': (600, 75), 'width': 32, 'height': 32,
               'rescale_x': 64, 'rescale_y': 64, 'sound_effects': small_mob_sound_effects},
    "mob_35": {'sprite_paths': small_mob_sprite_paths, 'health': 100, 'position': (600, 75), 'width': 32, 'height': 32,
               'rescale_x': 64, 'rescale_y': 64, 'sound_effects': small_mob_sound_effects},
    "mob_36": {'sprite_paths': small_mob_sprite_paths, 'health': 100, 'position': (600, 75), 'width': 32, 'height': 32,
               'rescale_x': 64, 'rescale_y': 64, 'sound_effects': small_mob_sound_effects},
    "mob_37": {'sprite_paths': small_mob_sprite_paths, 'health': 100, 'position': (600, 75), 'width': 32, 'height': 32,
               'rescale_x': 64, 'rescale_y': 64, 'sound_effects': small_mob_sound_effects},
    "mob_38": {'sprite_paths': small_mob_sprite_paths, 'health': 100, 'position': (600, 75), 'width': 32, 'height': 32,
               'rescale_x': 64, 'rescale_y': 64, 'sound_effects': small_mob_sound_effects},
    "mob_39": {'sprite_paths': small_mob_sprite_paths, 'health': 100, 'position': (600, 75), 'width': 32, 'height': 32,
               'rescale_x': 64, 'rescale_y': 64, 'sound_effects': small_mob_sound_effects},
    "mob_40": {'sprite_paths': small_mob_sprite_paths, 'health': 100, 'position': (600, 75), 'width': 32, 'height': 32,
               'rescale_x': 64, 'rescale_y': 64, 'sound_effects': small_mob_sound_effects},
    "mob_41": {'sprite_paths': small_mob_sprite_paths, 'health': 100, 'position': (600, 75), 'width': 32, 'height': 32,
               'rescale_x': 64, 'rescale_y': 64, 'sound_effects': small_mob_sound_effects},
    "mob_42": {'sprite_paths': small_mob_sprite_paths, 'health': 100, 'position': (600, 75), 'width': 32, 'height': 32,
               'rescale_x': 64, 'rescale_y': 64, 'sound_effects': small_mob_sound_effects},
    "mob_43": {'sprite_paths': small_mob_sprite_paths, 'health': 100, 'position': (600, 75), 'width': 32, 'height': 32,
               'rescale_x': 64, 'rescale_y': 64, 'sound_effects': small_mob_sound_effects},
    "mob_44": {'sprite_paths': small_mob_sprite_paths, 'health': 100, 'position': (600, 75), 'width': 32, 'height': 32,
               'rescale_x': 64, 'rescale_y': 64, 'sound_effects': small_mob_sound_effects},
    "mob_45": {'sprite_paths': small_mob_sprite_paths, 'health': 100, 'position': (600, 75), 'width': 32, 'height': 32,
               'rescale_x': 64, 'rescale_y': 64, 'sound_effects': small_mob_sound_effects},
    "mob_46": {'sprite_paths': small_mob_sprite_paths, 'health': 100, 'position': (600, 75), 'width': 32, 'height': 32,
               'rescale_x': 64, 'rescale_y': 64, 'sound_effects': small_mob_sound_effects},
    "mob_47": {'sprite_paths': small_mob_sprite_paths, 'health': 100, 'position': (600, 75), 'width': 32, 'height': 32,
               'rescale_x': 64, 'rescale_y': 64, 'sound_effects': small_mob_sound_effects},
    "mob_48": {'sprite_paths': small_mob_sprite_paths, 'health': 100, 'position': (600, 75), 'width': 32, 'height': 32,
               'rescale_x': 64, 'rescale_y': 64, 'sound_effects': small_mob_sound_effects},
    "mob_49": {'sprite_paths': small_mob_sprite_paths, 'health': 100, 'position': (600, 75), 'width': 32, 'height': 32,
               'rescale_x': 64, 'rescale_y': 64, 'sound_effects': small_mob_sound_effects},
    "mob_50": {'sprite_paths': small_mob_sprite_paths, 'health': 100, 'position': (600, 75), 'width': 32, 'height': 32,
               'rescale_x': 64, 'rescale_y': 64, 'sound_effects': small_mob_sound_effects},


}




