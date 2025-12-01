from wingedsheep.carcassonne.objects.connection import Connection
from wingedsheep.carcassonne.objects.farmer_connection import FarmerConnection
from wingedsheep.carcassonne.objects.farmer_side import FarmerSide
from wingedsheep.carcassonne.objects.side import Side

SIDE_ORDER = {
    Side.TOP: Side.RIGHT,
    Side.RIGHT: Side.BOTTOM,
    Side.BOTTOM: Side.LEFT,
    Side.LEFT: Side.TOP,
    Side.CENTER: Side.CENTER,
    Side.TOP_LEFT: Side.TOP_RIGHT,
    Side.TOP_RIGHT: Side.BOTTOM_RIGHT,
    Side.BOTTOM_RIGHT: Side.BOTTOM_LEFT,
    Side.BOTTOM_LEFT: Side.TOP_LEFT
}

FARMER_SIDE_ORDER = {
    FarmerSide.TLL: FarmerSide.TRR,
    FarmerSide.TLT: FarmerSide.BLB,
    FarmerSide.TRT: FarmerSide.BRR,
    FarmerSide.TRR: FarmerSide.TLL,
    FarmerSide.BRR: FarmerSide.BLL,
    FarmerSide.BRB: FarmerSide.TRT,
    FarmerSide.BLB: FarmerSide.TLT,
    FarmerSide.BLL: FarmerSide.BRR
}


class SideModificationUtil:

    @classmethod
    def turn_side(cls, source_side: Side, times: int) -> Side:
        for _ in range(times):
            source_side = SIDE_ORDER[source_side]
        return source_side

    @classmethod
    def opposite_side(cls, side: Side):
        return cls.turn_side(side, 2)

    @classmethod
    def turn_sides(cls, sides: [Side], times: int):
        return list(map(lambda side: cls.turn_side(side, times), sides))

    @classmethod
    def turn_farmer_side(cls, source_farmer_side: FarmerSide, times: int) -> FarmerSide:
        for _ in range(times):
            source_farmer_side = FARMER_SIDE_ORDER[source_farmer_side]
        return source_farmer_side

    @classmethod
    def turn_farmer_sides(cls, farmer_sides: [FarmerSide], times: int) -> [FarmerSide]:
        return list(map(lambda farmer_side: cls.turn_farmer_side(farmer_side, times), farmer_sides))

    @classmethod
    def opposite_farmer_side(cls, farmer_side: FarmerSide) -> FarmerSide:
        return FARMER_SIDE_ORDER[farmer_side]

    @classmethod
    def turn_farmer_connection(cls, farmer_connection: FarmerConnection, times: int):
        return FarmerConnection(
            # list(map(lambda side: cls.turn_side(side, times), farmer_connection.farmer_positions))
            farmer_positions=cls.turn_sides(farmer_connection.farmer_positions, times),
            # farmer_positions=list(map(lambda t_side: cls.turn_side(t_side, times), farmer_connection.farmer_positions)),
            tile_connections=cls.turn_farmer_sides(farmer_connection.tile_connections, times),
            # tile_connections=list(map(lambda f_side: cls.turn_farmer_side(f_side, times), farmer_connection.tile_connections)),
            city_sides=cls.turn_sides(farmer_connection.city_sides, times)
            # city_sides=list(map(lambda c_side: cls.turn_side(c_side, times), farmer_connection.city_sides))
        )

    @classmethod
    def turn_connection(cls, connection: Connection, times: int) -> Connection:
        return Connection(cls.turn_side(connection.a, times), cls.turn_side(connection.b, times))
