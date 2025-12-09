# Author: Anvay Paralikar – Q-learning agent training script

import os, pickle
from wingedsheep.carcassonne.carcassonne_game import CarcassonneGame
from wingedsheep.carcassonne.tile_sets.tile_sets import TileSet

from agents import Agent, QLearnAgent, RandAgent


def run_episode(trainee: QLearnAgent, adversary: Agent, epsilon: float, render: bool = False):
    """
    Run a single self-contained episode:
    - new CarcassonneGame
    - trainee vs adversary agent
    - returns final scores [q_score, rand_score]
    """
    game = CarcassonneGame(
        players=2,
        tile_sets=[TileSet.BASE],
        supplementary_rules=[],
    )

    players = [trainee, adversary]

    # Reset only per-episode memory, keep learned Q-table
    trainee.reset_episode()
    trainee.epsilon = epsilon

    while not game.is_finished():
        player_id = game.get_current_player()
        agent = players[player_id]
        action = agent.choice(game)
        if action is not None:
            game.step(player_id, action)

        if render:
            game.render()

    return game.state.scores  # [score_Q, score_rand]


def train(episodes, traineeClass, adversaryClass, agent_filepath) -> None:
    # init agent
    trainee = traineeClass(
        index=0,
        param_filepath=agent_filepath
    )

    adversary = adversaryClass(index = 1)

    # load prior q_table/data if it exists
    trainee.load_q_table(agent_filepath)

    t_wins = 0
    t_draws = 0

    for ep in range(1, episodes + 1):
        scores = run_episode(trainee, adversary, epsilon=0.2, render=False)
        q_score, rand_score = scores

        if q_score > rand_score:
            t_wins += 1
            result = "Player-win"
        elif q_score < rand_score:
            result = "Adversary-win"
        else:
            t_draws += 1
            result = "Draw"

        print(f"Episode {ep:3d}: scores = {scores} -> {result}")
    
    t_losses = episodes - t_wins - t_draws


    # save learned Q-table at the end
    trainee.save_q_table(agent_filepath)
    print("Saved trained Q-table to q_table.pkl")

    # return wdl for current training run
    return t_wins,t_draws,t_losses

if __name__ == "__main__":
    train()
