# =========================== GAME CONSTANT DECLARATIONS  ===============================
GAME_SCALE = 1
TILE_SIZE = 32 * GAME_SCALE
PANNING_SCREEN_WIDTH = 960
PANNING_SCREEN_HEIGHT = 640
X_WINDOW_PANNING_INDEX = PANNING_SCREEN_WIDTH // (TILE_SIZE * 2) + 1
Y_WINDOW_PANNING_INDEX = PANNING_SCREEN_HEIGHT // (TILE_SIZE * 2) + 1
SCREEN_WIDTH, SCREEN_HEIGHT = PANNING_SCREEN_WIDTH * 2 * GAME_SCALE, PANNING_SCREEN_HEIGHT * 2 * GAME_SCALE
PLAYER_OFFSET_Y = 400
BACKGROUND_SCROLL_FACTOR = 0.1
DEFAULT_TEXT_COLOR = (255,255,255)  # Black

# ========================= DEFAULT PATH DECLARATIONS  ============================================
DEFAULT_FONT = "C:/Users/Josep/PycharmProjects/AlienAndArtifacts/game_assets/fonts/ByteBounce.ttf"
DEFAULT_TILE_PATHS = "C:/Users/Josep/PycharmProjects/AlienAndArtifacts/game_assets/tile_sets/"
DEFAULT_BACKGROUND_IMAGE_PATH = "C:/Users/Josep/PycharmProjects/AlienAndArtifacts/game_assets/background_images/"
DEFAULT_NPC_SPRITESHEET_PATH = "C:/Users/Josep/PycharmProjects/AlienAndArtifacts/game_assets/spritesheets/npc_spritesheets/"
DEFAULT_PLAYER_SPRITESHEET_PATH = "C:/Users/Josep/PycharmProjects/AlienAndArtifacts/game_assets/spritesheets/player_spritesheets/"
DEFAULT_ENEMY_SPRITESHEET_PATH = "C:/Users/Josep/PycharmProjects/AlienAndArtifacts/game_assets/spritesheets/enemy_spritesheets/"
DEFAULT_ABILITY_IMAGE_PATH = "C:/Users/Josep/PycharmProjects/AlienAndArtifacts/game_assets/abilities/icons/"
DEFAULT_SOUND_FX_PATH = "C:/Users/Josep/PycharmProjects/AlienAndArtifacts/game_assets/sound_assets/"
DEFAULT_ABILITY_SOUND_FX_PATH = "C:/Users/Josep/PycharmProjects/AlienAndArtifacts/game_assets/sound_assets/abilities/"
DEFAULT_BACKGROUND_MUSIC_PATH = "C:/Users/Josep/PycharmProjects/AlienAndArtifacts/game_assets/sound_assets/background_music/"
