"""
import training function
"""

import os, pickle, argparse
from agents import Agent, RandAgent, QLearnAgent, MCTSAgent, SarsaAgent, SarsaLambdaAgent
from agents.training.train_Q import train

# from agents.training.train_Sarsa import train as s_train

AGENT_DIR = "agents"
PARAM_DIR = f"{AGENT_DIR}/params"

# training function to select agent to train
DEFAULT_ADVERSARY = "random"

# keys for load/store training statistics/history
EPISODES = "episodes"
WINS = "wins"
LOSSES = "losses"
DRAWS = "draws"


def load_wdl(filepath: str) -> None:
    """Load score data"""
    if not os.path.exists(filepath):
        print(
            f"[WARN] win/draw/loss history file '{filepath}' not found. Initializing."
        )
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


def main():
    # agent types that can be trained
    valid_models = {
        "qlearn": QLearnAgent,
        "sarsa": SarsaAgent,
        "sarsalambda":SarsaLambdaAgent
    }

    def valid_model(model):
        if not model in valid_models:
            raise argparse.ArgumentDefaultsHelpFormatter()
        return model

    # agent types that can be used to train another agent
    # note, currently have not implemented using learning-based agents as adversary
    valid_adversaries = {
        "random": RandAgent,
        "mcts": MCTSAgent, # ! very slow
    }

    def valid_adversary(adversary):
        if not adversary in valid_adversaries:
            raise argparse.ArgumentDefaultsHelpFormatter()
            # return DEFAULT_ADVERSARY
        return adversary

    print("AGENT TRAINER")
    parser = argparse.ArgumentParser(prog="trainer", description="Trains an agent")
    parser.add_argument(
        "-i", "--iterations", type=int, required=True, help="training iterations"
    )
    parser.add_argument(
        "-m", "--model", type=valid_model, required=True, help=f"agent model to train ({valid_models})"
    )
    parser.add_argument(
        "-a",
        "--adversary",
        type=valid_adversary,
        default='random',
        required=False,
        help=f"model to train against ({valid_adversaries})",
    )
    parser.add_argument("-u", "--uid", required=False, help="agent name/id")

    # parse arguments; if empty, print arg options and exit
    args = parser.parse_args()
    if not args:
        parser.print_help()
        print()
        return

    # otherwise,
    episodes = int(args.iterations)
    player = args.model
    adversary = args.adversary
    agent_id = args.uid
    print(
        f"training {player} agent '{agent_id}' for {episodes} iterations against {adversary}\n"
    )

    param_filepath = f"{PARAM_DIR}/{player}_table_{agent_id}.pkl"
    wdl_filepath = f"{PARAM_DIR}/{player}_wdl_{agent_id}.pkl"  # wld = win/draw/loss
    print(f"params file: '{param_filepath}'")
    print(f" wld   file: '{wdl_filepath}'")

    # load scores
    allscores = load_wdl(wdl_filepath)

    # train player against adversary
    wins, draws, losses = train(episodes, valid_models[player], valid_adversaries[adversary], param_filepath)
    print("\nTraining summary vs random:")

    total_episodes = episodes + allscores[EPISODES]
    total_wins = wins + allscores[WINS]
    total_draws = draws + allscores[DRAWS]
    total_losses = losses + allscores[LOSSES]

    print(
        f"  Q-learning:   current : {episodes:5d} episodes : wins/draws/losses : {wins}/{draws}/{losses}"
    )
    print(
        f"  Q-learning: aggregate : {total_episodes:5d} episodes : wins/draws/losses : {total_wins}/{total_draws}/{total_losses}"
    )

    allscores[EPISODES] = total_episodes
    allscores[WINS] = total_wins
    allscores[DRAWS] = total_draws
    allscores[LOSSES] = total_losses
    save_wdl(allscores, wdl_filepath)
    return


if __name__ == "__main__":
    main()
