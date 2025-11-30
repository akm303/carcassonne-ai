import copy

from wingedsheep.carcassonne.carcassonne_game import CarcassonneGameState
from wingedsheep.carcassonne.objects.actions.action import Action
from wingedsheep.carcassonne.objects.actions.tile_action import TileAction
from wingedsheep.carcassonne.utils.action_util import ActionUtil
from wingedsheep.carcassonne.utils.state_updater import StateUpdater

from typing import Dict, Tuple
from tqdm import tqdm

import random
import math

class MCTSNode:
    def __init__(self, state: CarcassonneGameState, exploration_rate: 0.3, parent: 'MCTSNode' =None):
        self.state: CarcassonneGameState = state
        self.exploration_rate = exploration_rate
        self.parent: MCTSNode = parent
        self.children: Dict[Tuple[Action, Action], state] = {}
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
                raise ValueError("Expected TileAction in tile_actions")
        for tile_action in tile_actions:
            # Placement actions
            new_state = StateUpdater.apply_action(self.state, tile_action)
            meeple_actions = [action for action in ActionUtil.get_possible_actions(new_state)]
            # verification
            for x in meeple_actions:
                if isinstance(x, TileAction):
                    raise ValueError("Expected non-TileAction in placement_actions")
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
                q = state.wins / state.visits + (2 * (2 * math.log(self.visits + 1) / (state.visits + 1)) ) ** 0.5
            else:
                q = 0.5 + (2 * (2 * math.log(self.visits + 1) / 1) ) ** 0.5

            if q > curr_max_q:
                curr_max_q = q
                selected_path = action_pair

        o1 = selected_path
        o2 = list(self.children.keys())[0] if self.children else None
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
        pbar = tqdm(total=len(current_state.deck), desc="Processing items")
        count = len(current_state.deck)
        while not current_state.is_terminated():
            # print(f"Remaining tiles: {len(current_state.deck)}")
            possible_actions = ActionUtil.get_possible_actions(current_state)
            action = random.choice(possible_actions)
            current_state = StateUpdater.apply_action(current_state, action, need_copy=False)
            count -= 1
            pbar.update(1)
        pbar.close()
        return current_state

    def update(self, win: bool, result: int):
        self.visits += 1
        # TODO: update wins based on result
        if win:
            self.wins += 1
            # TODO: complex scoring
        if self.parent:
            if self.get_possible_actions()[0] is TileAction:
                self.parent.update(not win, -result)
            else:
                self.parent.update(win, result)