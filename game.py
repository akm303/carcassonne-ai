import random
import time
from typing import Optional

from wingedsheep.carcassonne.carcassonne_game import CarcassonneGame
from wingedsheep.carcassonne.objects.actions.action import Action
from wingedsheep.carcassonne.tile_sets.tile_sets import TileSet
from wingedsheep.carcassonne.tile_sets.supplementary_rules import SupplementaryRule

from agents import Agent, RandAgent, QLearnAgent, SarsaAgent
from agents.mcts_agent import MCTSAgent
from agents import SarsaLambdaAgent
from menu import CarcassonneMenu
from scoreboard import drawScoreboard

import cProfile
import pstats


def sort_agents(input, index, iter = 50):
    if input == "Q-Learning":
        # here we need to add the final filepath of already taught algorithm / same for sarsa
        return QLearnAgent(index, param_filepath='agents/params/q_table_1.pkl')
    elif input == "Sarsa":
        return SarsaAgent(index, param_filepath='agents/params/sarsa_table_1.pkl')
    elif input == "Sarsa (Lambda)":
        return SarsaLambdaAgent(index, param_filepath='agents/params/sarsa_table_1.pkl')
    elif input == "MCTS":
        return MCTSAgent(index, iterations=iter, vis_pbar=False)
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
    iterations = input["iterations"]

    game = CarcassonneGame(
        players=num_players,
        tile_sets=[TileSet.BASE],
        supplementary_rules=[],  # e.g. [SupplementaryRule.ABBOTS, SupplementaryRule.FARMERS]
    )

    agentClasses = []
    for i in range(num_players):
        agentClasses.append(sort_agents(agents[i], i, iterations))






    # --- configure game (you can later hook this up to a UI/menu) ---
    #game = CarcassonneGame(
    #    players=2,
    #    tile_sets=[TileSet.BASE],
    #    supplementary_rules=[SupplementaryRule.FARMERS],  # e.g. [SupplementaryRule.ABBOTS, SupplementaryRule.FARMERS]
    #)

    # Example setups:
    # players = [RandAgent(i) for i in range(game.players)]
    # players = [PlayerAgent(0), RandAgent(1)]


    # Q-learning vs random baseline:
    #players: list[Agent] = [
    #    # RandAgent(0),
    #    SarsaAgent(0,param_filepath='agents/params/q_table_0.pkl'),
    #    MCTSAgent(1, iterations=50, vis_pbar=False)
    #]

    # --- main game loop ---
    while not game.is_finished():
        # control speed using time sleep
        if speed > 0:
            time.sleep(speed)

        # draw the board
        game.render()

        # check if scoreboard is allowed, and if so draw it
        if scoreboard:
            # since we draw scoreboard outside the render inside of carcassonne_visualiser everything gets deleted after each turn,
            # which is why it blinks - in order to fix it we need to move this function inside of visualizer.
            drawScoreboard(game, agentClasses)

        game.visualiser.canvas.update()

        print(f"Remaining Tiles: {len(game.state.deck)}")
        player_id: int = game.get_current_player()
        agent: Agent = agentClasses[player_id]

        actions = agent.choice(game)
        if isinstance(actions, Action):
            actions = [actions]
        if actions is not None:
            for action in actions:
                game.step(player_id, action)
                print(f"{agent}: {action}")

        # Notify other agents of the action taken
        # MCTS needs it, not sure about the others -- Keith
        for i, other_agent in enumerate(agentClasses):
            if i != player_id:
                for action in actions:
                    other_agent.notify_action(action)

        game.render()
        if scoreboard:
            drawScoreboard(game, agentClasses)
        game.visualiser.canvas.update()

    print("Game finished. Final scores:", game.state.scores)


if __name__ == "__main__":
    # cProfile.run('main()', 'game_profile.prof')
    # p = pstats.Stats('game_profile.prof')
    # p.sort_stats('cumulative').print_stats(20)
    main()

