from MCTS.algorithm import MCTS

def train(episodes, agent_filepath):
    mcts = MCTS()
    for _ in range(episodes):
        mcts.one_iteration()