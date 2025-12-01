import random

from wingedsheep.carcassonne.carcassonne_game import CarcassonneGame
from wingedsheep.carcassonne.objects.actions.action import Action

from .base import Agent
from MCTS.node import MCTSNode

from tqdm import tqdm

class MCTSAgent(Agent):
    """Agent using Monte-Carlo Tree Search"""
    def __init__(self, index, iterations=150, vis_pbar=True):
        self.index = index
        self.type = "MCTSch"
        self.iterations = iterations
        self.vis_pbar = vis_pbar

        self.mcts_root = None
        self.opponent_agent_actions = []

    def getAction(self, game: CarcassonneGame) -> Action | None:
        # basic, safe behaviour so the game runs
        valid_actions = game.get_possible_actions()
        if not valid_actions:
            return None # TODO: This shouldn't happen actually

        if self.mcts_root is None:
            self.mcts_root = MCTSNode(state=game.state, exploration_rate=0.3)
        if len(self.opponent_agent_actions) % 2 != 0:
            raise ValueError("Opponent actions should be in pairs of (tile_action, meeple_action)")

        while self.opponent_agent_actions:
            tile_action = self.opponent_agent_actions.pop(0)
            meeple_action = self.opponent_agent_actions.pop(0)
            action_pair = (tile_action, meeple_action)
            if action_pair in self.mcts_root.children:
                self.mcts_root = self.mcts_root.children[action_pair]
                self.mcts_root.parent = None
            else:
                # Reinitialize the MCTS tree if the action pair is not found (not explored yet)
                self.mcts_root = MCTSNode(state=game.state, exploration_rate=0.3)
                self.opponent_agent_actions.clear()
        if self.vis_pbar:
            for _ in tqdm(range(self.iterations)):
                self._one_iteration()
        else:
            for _ in range(self.iterations):
                self._one_iteration()

        # Select the best action based on win rate
        best_actions = None
        best_win_rate = -1.0
        for action_pair, child in self.mcts_root.children.items():
            win_rate = child.wins / child.visits if child.visits > 0 else 0
            if win_rate > best_win_rate:
                best_win_rate = win_rate
                best_actions = action_pair

        return best_actions

    def _one_iteration(self):
        node_gen: MCTSNode = None
        try:
            node_gen = self.mcts_root.select_expand()
            terminal_state = node_gen.rollout()
            node_gen.update(
                win=terminal_state.scores[self.index] > terminal_state.scores[1 - self.index],
                result=terminal_state.scores[self.index] - terminal_state.scores[1 - self.index]
            )
        except AttributeError as e:
            print(f"[MCTSAgent] AttributeError during MCTS iteration: {e}")
            if node_gen is not None:
                for k, v in node_gen.parent.children.items():
                    if v is node_gen:
                        del node_gen.parent.children[k]
                        break
    def notify_action(self, action: Action):
        """notify agent of an action taken in the game (by any player)"""
        self.opponent_agent_actions.append(action)
