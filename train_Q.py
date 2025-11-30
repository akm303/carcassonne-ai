# Author: Anvay Paralikar – Q-learning agent training script

from __future__ import annotations

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


def main() -> None:
    num_episodes = 20  # adjust for your experiments

    q_agent = QLearnAgent(
        index=0,
        alpha=0.3,
        gamma=0.9,
        epsilon=0.2,
    )

    q_wins = 0
    draws = 0

    for ep in range(1, num_episodes + 1):
        scores = run_episode(q_agent, epsilon=0.2, render=False)
        q_score, rand_score = scores

        if q_score > rand_score:
            q_wins += 1
            result = "Q-win"
        elif q_score < rand_score:
            result = "Rand-win"
        else:
            draws += 1
            result = "Draw"

        print(f"Episode {ep:3d}: scores = {scores} -> {result}")

    # save learned Q-table at the end
    q_agent.save_q_table("q_table.pkl")
    print("Saved trained Q-table to q_table.pkl")

    print("\nTraining summary vs random:")
    print(f"  Q-learning wins : {q_wins}/{num_episodes}")
    print(f"  Draws           : {draws}/{num_episodes}")
    print(f"  Random wins     : {num_episodes - q_wins - draws}")


if __name__ == "__main__":
    main()
