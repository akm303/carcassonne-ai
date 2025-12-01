# Author: Anvay Paralikar – Q-learning agent training script

import os, pickle
from wingedsheep.carcassonne.carcassonne_game import CarcassonneGame
from wingedsheep.carcassonne.tile_sets.tile_sets import TileSet

from agents import QLearnAgent, RandAgent


def run_episode(q_agent: QLearnAgent, epsilon: float, render: bool = False):
    """
    Run a single self-contained episode:
    - new CarcassonneGame
    - q_agent vs random agent
    - returns final scores [q_score, rand_score]
    """
    game = CarcassonneGame(
        players=2,
        tile_sets=[TileSet.BASE],
        supplementary_rules=[],
    )

    opp_agent = RandAgent(1)
    players = [q_agent, opp_agent]

    # Reset only per-episode memory, keep learned Q-table
    q_agent.reset_episode()
    q_agent.epsilon = epsilon

    while not game.is_finished():
        player_id = game.get_current_player()
        agent = players[player_id]
        action = agent.choice(game)
        if action is not None:
            game.step(player_id, action)

        if render:
            game.render()

    return game.state.scores  # [score_Q, score_rand]


def train(episodes,agent_filepath) -> None:
    # init agent
    q_agent = QLearnAgent(
        index=0,
        param_filepath=agent_filepath
    )

    # load prior q_table/data if it exists
    q_agent.load_q_table(agent_filepath)

    q_wins = 0
    q_draws = 0

    for ep in range(1, episodes + 1):
        scores = run_episode(q_agent, epsilon=0.2, render=False)
        q_score, rand_score = scores

        if q_score > rand_score:
            q_wins += 1
            result = "Q-win"
        elif q_score < rand_score:
            result = "Rand-win"
        else:
            q_draws += 1
            result = "Draw"

        print(f"Episode {ep:3d}: scores = {scores} -> {result}")
    
    q_losses = episodes - q_wins - q_draws


    # save learned Q-table at the end
    q_agent.save_q_table(agent_filepath)
    print("Saved trained Q-table to q_table.pkl")

    # return wdl for current training run
    return q_wins,q_draws,q_losses

if __name__ == "__main__":
    train()
