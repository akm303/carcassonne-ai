from .node import MCTSNode

from wingedsheep.carcassonne.carcassonne_game import CarcassonneGame
from wingedsheep.carcassonne.tile_sets.tile_sets import TileSet


class MCTS:
    def __init__(self):
        self.root = None
        self.c = 9999

        new_game = CarcassonneGame(
            players=2,
            tile_sets=[TileSet.BASE],
            supplementary_rules=[],
        )

        self.root = MCTSNode(state=new_game.state, exploration_rate=0.3)

    def run(self):
        pass

    def one_iteration(self):
        node_gen = self.root.select_expand()
        terminal_state = node_gen.rollout()
        node_gen.update(
            win=terminal_state.scores[0] > terminal_state.scores[1],
            result=terminal_state.scores[0] - terminal_state.scores[1]
        )

        self.visualize()

    def visualize(self):
        def helper(node: MCTSNode, level: int, src_actions):
            print(f"{' '*level}Actions: {src_actions} Node: Visits={node.visits}, Wins={node.wins}")
            for action, child in node.children.items():
                helper(child, level + 1, action)
        # DFS print
        print("===========================================")
        print("Tree Visualization:")
        helper(self.root, 0, None)
        print("===========================================")

