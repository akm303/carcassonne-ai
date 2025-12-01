from wingedsheep.carcassonne.objects.actions.action import Action
from wingedsheep.carcassonne.objects.coordinate import Coordinate
from wingedsheep.carcassonne.objects.tile import Tile


class TileAction(Action):
    def __init__(self, tile: Tile, coordinate: Coordinate, tile_rotations: int):
        self.tile = tile
        self.coordinate = coordinate
        self.tile_rotations = tile_rotations

    def __repr__(self):
        return f"T({self.coordinate}, {self.tile_rotations})"
    def __str__(self):
        return str((self.tile.description, str(self.coordinate), self.tile_rotations))

    def __eq__(self, other):
        if not isinstance(other, TileAction):
            return False
        return self.tile == other.tile and \
            self.coordinate == other.coordinate and \
            self.tile_rotations == other.tile_rotations

    def __hash__(self):
        return hash((self.tile, self.coordinate, self.tile_rotations))