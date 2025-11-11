import random
from typing import Optional

from wingedsheep.carcassonne.carcassonne_game import CarcassonneGame
from wingedsheep.carcassonne.carcassonne_game_state import CarcassonneGameState
from wingedsheep.carcassonne.objects.actions.action import Action
from wingedsheep.carcassonne.tile_sets.supplementary_rules import SupplementaryRule
from wingedsheep.carcassonne.tile_sets.tile_sets import TileSet

from agents.agent import GameAgent

game = CarcassonneGame(
    players=2,
    tile_sets=[TileSet.BASE, TileSet.THE_RIVER, TileSet.INNS_AND_CATHEDRALS],
    supplementary_rules=[SupplementaryRule.ABBOTS, SupplementaryRule.FARMERS],
)

players = [GameAgent(i) for i in range(game.players)]
while not game.is_finished():
    player_id: int = game.get_current_player()
    playerAgent: GameAgent = players[player_id]
    action: Optional[Action] = playerAgent.choice(game)
    if action is not None:
        game.step(player_id, action)
    game.render()
