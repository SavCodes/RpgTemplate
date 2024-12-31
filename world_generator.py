import game_tile

class WorldGenerator:
    def __init__(self, world_array_2d, scale=1):
        self.world_array = world_array_2d
        self.scale = scale
        self.world_tiles = self.create_world_tiles()

    def create_world_tiles(self):
        _temp_array = []
        for y_index, layer in enumerate(self.world_array):
            _temp_row = []
            for x_index, tile in enumerate(layer):
                _temp_row.append(game_tile.Platform(tile, x_index * 32 * self.scale,
                                    y_index * 32 * self.scale, scale=self.scale, is_collidable=True if tile.split(".")[-2][-2:] != "00" else False))
            _temp_array.append(_temp_row)
        return _temp_array

def generate_all_world_layers(full_tile_set, scale=1, current_level=0):
    background = WorldGenerator(full_tile_set[0][current_level], scale=scale).world_tiles
    level_tiles = WorldGenerator(full_tile_set[1][current_level], scale=scale).world_tiles
    foreground = WorldGenerator(full_tile_set[2][current_level], scale=scale).world_tiles
    return background, level_tiles, foreground

