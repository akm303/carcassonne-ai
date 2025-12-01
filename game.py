import random
from typing import Optional

from wingedsheep.carcassonne.carcassonne_game import CarcassonneGame
from wingedsheep.carcassonne.objects.actions.action import Action
from wingedsheep.carcassonne.tile_sets.tile_sets import TileSet
from wingedsheep.carcassonne.tile_sets.supplementary_rules import SupplementaryRule

from agents import Agent, RandAgent, QLearnAgent
from agents.mcts_agent import MCTSAgent

from menu import CarcassonneMenu

import time

from scoreboard import drawScoreboard

def sort_agents(input, index):
    '''elif input == "Sarsa":
            return SarsaAgent(index)'''
    if input == "Q-Learning":
        return QLearnAgent(index, param_filepath='')
    elif input == "MCTS":
        return MCTSAgent(index)
    elif input == "Random":
        return RandAgent(index)
    else:
        print("This agent is not implemented yet.")
        print("Try again later...")
        return RandAgent(index)


def main() -> None:
    # run the menu and get input first
    menu = CarcassonneMenu()
    input = menu.run()

    if input is None:
        print("The user did not provide any information.")
        print("Exiting...")
        return

    # get the values from input
    num_players = input["num_players"]
    speed = input["speed"]
    scoreboard = input["scoreboard"]
    agents = input["agents"]

    game = CarcassonneGame(
        players=num_players,
        tile_sets=[TileSet.BASE, TileSet.THE_RIVER, TileSet.INNS_AND_CATHEDRALS],
        supplementary_rules=[SupplementaryRule.ABBOTS, SupplementaryRule.FARMERS]
    )

    agentClasses = []
    for i in range(num_players):
        agentClasses.append(sort_agents(agents[i], i))



    # Example setups:
    # players = [RandAgent(i) for i in range(game.players)]
    # players = [PlayerAgent(0), RandAgent(1)]
    '''
        # Q-learning vs random baseline:
    players: list[Agent] = [
        RandAgent(0),
        QLearnAgent(1, param_filepath='agents/params/q_table_0.pkl')
    ]
    '''


    # --- main game loop ---
    while not game.is_finished():
        # control speed using time sleep
        if speed > 0:
            time.sleep(speed)

        # draw the board
        game.render()

        # check if scoreboard is allowed, and if so draw it
        if scoreboard:
            drawScoreboard(game, agentClasses)

        game.visualiser.canvas.update()

        player_id: int = game.get_current_player()
        agent: Agent = agentClasses[player_id]

        action: Optional[Action] = agent.choice(game)
        if action is not None:
            game.step(player_id, action)

        game.render()
        if scoreboard:
            drawScoreboard(game, agentClasses)
        game.visualiser.canvas.update()
    print("Game finished. Final scores:", game.state.scores)


if __name__ == "__main__":
    main()