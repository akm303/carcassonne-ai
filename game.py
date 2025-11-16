import random
from typing import Optional

from wingedsheep.carcassonne.carcassonne_game import CarcassonneGame
from wingedsheep.carcassonne.carcassonne_game_state import CarcassonneGameState
from wingedsheep.carcassonne.objects.actions.action import Action
from wingedsheep.carcassonne.tile_sets.supplementary_rules import SupplementaryRule
from wingedsheep.carcassonne.tile_sets.tile_sets import TileSet


# import menu
from agents.agent import Agent
from agents.agent import RandAgent
from agents.agent import PlayerAgent
# from agents.agent import MCTSAgent
# from agents.agent import QLearnAgent

def main():

    #todo: setup menu goes here

    #todo: adjust game init based on setup-menu selections
    # * select agents to play
    game = CarcassonneGame(
        players=2,
        tile_sets=[TileSet.BASE],
        supplementary_rules=[],
    )

    # * test game setup (has examples of options)
    # game = CarcassonneGame(
    #     players=2,
    #     tile_sets=[TileSet.BASE, TileSet.THE_RIVER, TileSet.INNS_AND_CATHEDRALS],
    #     supplementary_rules=[SupplementaryRule.ABBOTS, SupplementaryRule.FARMERS],
    # )

    #todo: adjust to init agents based on game setup
    players = [RandAgent(i) for i in range(game.players)] 

    # game loop
    while not game.is_finished():
        player_id: int = game.get_current_player()
        playerAgent: Agent = players[player_id]
        action: Optional[Action] = playerAgent.choice(game)
        if action is not None:
            game.step(player_id, action)
        game.render()


if __name__ == "__main__":
    main()
