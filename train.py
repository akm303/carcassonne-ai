"""
import training function
"""

import os, pickle

from agents.training.train_MCTS import train as mcts_train
from agents.training.train_Q import train as q_train

AGENT_DIR = "agents"
PARAM_DIR = f"{AGENT_DIR}/params"

# training function to select agent to train
train = q_train

# load/store training statistics
AGENT_ID = 0
AGENT_TYPE = 'q' # 'mcts'
TRAINING_ITERATIONS = 5

EPISODES = "episodes"
WINS = "wins"
LOSSES = "losses"
DRAWS = "draws"


def load_wdl(filepath: str) -> None:
    """Load score data"""
    if not os.path.exists(filepath):
        print(f"[WARN] win/draw/loss history file '{filepath}' not found. Initializing.")
        return {EPISODES: 0, WINS: 0, DRAWS: 0, LOSSES: 0}
    data = None
    with open(filepath, "rb") as f:
        data = pickle.load(f)
    print(f"[INFO] Loaded win/draw/loss history from '{filepath}'")
    return data


def save_wdl(data, filepath: str) -> None:
    """Save the learned win/draw/loss history to disk."""
    with open(filepath, "wb") as f:
        pickle.dump(data, f)


if __name__ == "__main__":
    episodes = TRAINING_ITERATIONS
    # use storage for particular agent type
    if AGENT_TYPE == 'q':
        agent_param = 'table'
    elif AGENT_TYPE == 'mcts':
        agent_param = 'nodes'
    # else:
    #     print(f'invalid agent type: {AGENT_TYPE}')
    #     exit(1)

    param_filepath = f"{PARAM_DIR}/{AGENT_TYPE}_{agent_param}_{AGENT_ID}.pkl"
    wdl_filepath = f"{PARAM_DIR}/{AGENT_TYPE}_wdl_{AGENT_ID}.pkl"  # wld = win/draw/loss

    allscores = load_wdl(wdl_filepath)
    wins, draws, losses = train(episodes, param_filepath)
    print("\nTraining summary vs random:")

    total_episodes = episodes + allscores[EPISODES]
    total_wins = wins + allscores[WINS]
    total_draws = draws + allscores[DRAWS]
    total_losses = losses + allscores[LOSSES]

    print(f"  Q-learning:   current : {episodes:5d} episodes : wins/draws/losses : {wins}/{draws}/{losses}")
    print(f"  Q-learning: aggregate : {total_episodes:5d} episodes : wins/draws/losses : {total_wins}/{total_draws}/{total_losses}")

    allscores[EPISODES] = total_episodes
    allscores[WINS] = total_wins
    allscores[DRAWS] = total_draws
    allscores[LOSSES] = total_losses
    save_wdl(allscores,wdl_filepath)
