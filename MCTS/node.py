import copy

from wingedsheep.carcassonne.carcassonne_game import CarcassonneGame
from wingedsheep.carcassonne.carcassonne_game import CarcassonneGameState
from wingedsheep.carcassonne.objects.actions.action import Action
from wingedsheep.carcassonne.objects.actions.tile_action import TileAction
from wingedsheep.carcassonne.tile_sets.tile_sets import TileSet
from wingedsheep.carcassonne.utils.action_util import ActionUtil
from wingedsheep.carcassonne.utils.state_updater import StateUpdater

from typing import Dict, Tuple

import random
import math


class MCTSNode:
    def __init__(self, state: CarcassonneGameState, exploration_rate: 0.3, parent: 'MCTSNode' = None):
        self.state: CarcassonneGameState = state
        self.exploration_rate = exploration_rate
        self.parent: MCTSNode = parent
        self.children: Dict[Tuple[Action, Action], 'MCTSNode'] = {}
        self.visits = 0
        self.wins = 0

    def is_fully_expanded(self):
        return len(self.children) == len(self.get_possible_actions())

    def get_possible_actions(self):
        return ActionUtil.get_possible_actions(self.state)

    def select_expand(self):
        # Generate possible action pairs
        action_pairs = []
        # Tile action
        tile_actions = [action for action in self.get_possible_actions()]
        # verification
        for x in tile_actions:
            if not isinstance(x, TileAction):
                print(type(x))
                raise ValueError("Expected TileAction in tile_actions")
        for tile_action in tile_actions:
            # Placement actions
            new_state = StateUpdater.apply_action(self.state, tile_action)
            meeple_actions = [action for action in ActionUtil.get_possible_actions(new_state)]
            # verification
            for x in meeple_actions:
                if isinstance(x, TileAction):
                    raise ValueError("Expected MeepleAction, got TileAction")
            if meeple_actions:
                for meeple_action in meeple_actions:
                    action_pairs.append((tile_action, meeple_action))
            else:
                action_pairs.append((tile_action, None))

        selected_path = None

        curr_max_q = float('-inf')

        for action_pair in action_pairs:
            if action_pair in self.children:
                state = self.children[action_pair]
                q = state.wins / state.visits + (2 * (2 * math.log(self.visits + 1) / (state.visits + 1))) ** 0.5
            else:
                q = 0.5 + (2 * (2 * math.log(self.visits + 1) / 1)) ** 0.5

            if q > curr_max_q:
                curr_max_q = q
                selected_path = action_pair

        if selected_path not in self.children:
            # Gen new node
            tile_action, meeple_action = selected_path
            new_state = StateUpdater.apply_action(self.state, tile_action)
            if meeple_action is not None:
                new_state = StateUpdater.apply_action(new_state, meeple_action)
            new_node = MCTSNode(state=new_state, exploration_rate=self.exploration_rate, parent=self)
            self.children[selected_path] = new_node
            return new_node
        else:
            curr_node = self.children[selected_path]
            return curr_node.select_expand()

    def rollout(self):
        current_state = copy.deepcopy(self.state)
        # pbar = tqdm(total=len(current_state.deck), desc="Processing items")
        count = len(current_state.deck)
        while not current_state.is_terminated():
            possible_actions = ActionUtil.get_possible_actions(current_state)
            action = random.choice(possible_actions)
            current_state = StateUpdater.apply_action(current_state, action, need_copy=False)
            count -= 1
            # pbar.update(1)
        # pbar.close()
        return current_state

    def update(self, win: bool, result: int):
        self.visits += 1
        # TODO: update wins based on result
        if win:
            self.wins += 1
            # TODO: complex scoring
        if self.parent:
            p_actions = self.parent.get_possible_actions()
            if p_actions[0] is TileAction:
                self.parent.update(not win, -result)
            else:
                self.parent.update(win, result)


def train():
    game = CarcassonneGame(
        players=2,
        tile_sets=[TileSet.BASE],
        supplementary_rules=[],
    )

    mcts_root = MCTSNode(state=game.state, exploration_rate=0.3)

    for _ in range(10):
        node_gen = mcts_root.select_expand()
        terminal_state = node_gen.rollout()
        node_gen.update(
            win=terminal_state.scores[game.get_current_player()] > terminal_state.scores[1 - game.get_current_player()],
            result=terminal_state.scores[game.get_current_player()] - terminal_state.scores[
                1 - game.get_current_player()]
        )


if __name__ == '__main__':
    # cProfile.run('train()', 'mcts_profile.prof')
    #
    # p = pstats.Stats('mcts_profile.prof')
    # p.sort_stats('cumulative').print_stats(10)
    train()
