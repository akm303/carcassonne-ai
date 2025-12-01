import random
import time
from typing import Optional

from wingedsheep.carcassonne.carcassonne_game import CarcassonneGame
from wingedsheep.carcassonne.objects.actions.action import Action
from wingedsheep.carcassonne.tile_sets.tile_sets import TileSet
from wingedsheep.carcassonne.tile_sets.supplementary_rules import SupplementaryRule

from agents import Agent, RandAgent, QLearnAgent
from agents.mcts_agent import MCTSAgent

import cProfile
import pstats

def main() -> None:
    # --- configure game (you can later hook this up to a UI/menu) ---
    game = CarcassonneGame(
        players=2,
        tile_sets=[TileSet.BASE],
        supplementary_rules=[SupplementaryRule.FARMERS],  # e.g. [SupplementaryRule.ABBOTS, SupplementaryRule.FARMERS]
    )

    # Example setups:
    # players = [RandAgent(i) for i in range(game.players)]
    # players = [PlayerAgent(0), RandAgent(1)]

       
    # Q-learning vs random baseline:
    players: list[Agent] = [
        RandAgent(0),
        # QLearnAgent(1,param_filepath='agents/params/q_table_0.pkl')
        MCTSAgent(1, iterations=50, vis_pbar=False)
    ]

    # --- main game loop ---
    while not game.is_finished():
        print(len(game.state.deck))
        player_id: int = game.get_current_player()
        agent: Agent = players[player_id]

        actions = agent.choice(game)
        if isinstance(actions, Action):
            actions = [actions]
        if actions is not None:
            for action in actions:
                game.step(player_id, action)
                print(f"{agent}: {action}")

        # Notify other agents of the action taken
        # MCTS needs it, not sure about the others -- Keith
        for i, other_agent in enumerate(players):
            if i != player_id:
                for action in actions:
                    other_agent.notify_action(action)

        game.render()
        if isinstance(agent, RandAgent):
            time.sleep(0.5)  # slow down for better observation

    print("Game finished. Final scores:", game.state.scores)


if __name__ == "__main__":
    # cProfile.run('main()', 'game_profile.prof')
    # p = pstats.Stats('game_profile.prof')
    # p.sort_stats('cumulative').print_stats(20)
    main()

