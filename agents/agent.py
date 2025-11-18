"""
Author: Ari Majumdar
Updated: 11/11/25
Version1

Based on wingedsheep's Carcassonne game implementation, Pacman project implementations,
and [MCTS paper](https://arxiv.org/pdf/2009.12974) (Ameneyro et. al.)
We define a player agent and player state.


"""

import random

from wingedsheep.carcassonne.carcassonne_game import CarcassonneGame
from wingedsheep.carcassonne.objects.actions.action import Action


class Agent:
    """
    Abstract Agent class
    Agent must define a getAction method
    """

    def __init__(self, index=0):
        self.index = index
        self.type = "Abstract"

    def choice(self, game):
        return self.getAction(game)

    def getAction(self, state):
        raise NotImplementedError()


class RandAgent(Agent):
    """Agent that selects random moves"""
    def __init__(self, index):
        self.index = index
        self.type = "Rand"

    def getAction(self, game: CarcassonneGame):
        """
        Basic agent selects action at random
        """
        valid_actions: list[Action] = game.get_possible_actions()
        action = random.choice(valid_actions)
        print(f"Agent({self.type}) {self.index}: {action}")
        return action


class PlayerAgent(Agent):
    """Agent that takes human inputs to select next move"""
    def __init__(self, index):
        self.index = index
        self.type = "Player"

    def getAction(self, game: CarcassonneGame):
        pass


class MCTSAgent(Agent):
    """Agent using Monte-Carlo Tree Search"""
    def __init__(self, index):
        self.index = index
        self.type = "MCTS"

    def getAction(self, game: CarcassonneGame):
        pass


class QLearnAgent(Agent):
    """
    Tabular Q-learning agent.

    - Keeps a Q-table: key = (state_key, action_key)
    - Uses epsilon-greedy policy over valid actions
    - Reward = change in this player's score since its last move
    """

    def __init__(self, index, alpha=0.3, gamma=0.9, epsilon=0.2):
        self.index = index
        self.type = "Qlearn"

        # Q[(state_key, action_key)] -> value
        self.q_table: dict[tuple, float] = {}

        # hyperparameters
        self.alpha = alpha      # learning rate
        self.gamma = gamma      # discount factor
        self.epsilon = epsilon  # exploration rate

        # memory of previous transition (for Q update)
        self.last_state_key = None
        self.last_action_key = None
        self.last_score = 0

    # ---------- helpers to encode state / action ----------

    def _encode_state(self, game: CarcassonneGame) -> tuple:
        """Turn the big game state into a compact, hashable key."""
        state = game.state

        # 1) tile in hand
        next_tile = getattr(state, "next_tile", None)

        # --- SAFE tile identifier (no str(next_tile)) ---
        if next_tile is None:
            tile_name = "NO_TILE"
        else:
            # try the most informative attributes first
            tile_name = getattr(next_tile, "name", None)
            if tile_name is None:
                # some codebases use other IDs
                tile_name = getattr(next_tile, "id", None) or getattr(next_tile, "tile_id", None)
            if tile_name is None:
                # last resort: just use the class name (never calls to_json)
                tile_name = type(next_tile).__name__

        # 2) score difference bucketed
        my_score = state.scores[self.index]
        opp_index = 1 - self.index  # assumes 2-player for now
        opp_score = state.scores[opp_index]
        diff = my_score - opp_score
        if diff < -5:
            score_bucket = -1
        elif diff > 5:
            score_bucket = 1
        else:
            score_bucket = 0

        # 3) how many meeples left
        meeples_left = state.meeples[self.index]

        # 4) game phase (tiles vs meeples etc.)
        phase_obj = getattr(state, "phase", None)
        if phase_obj is None:
            phase_name = "UNKNOWN_PHASE"
        else:
            # avoid str(phase_obj) just in case it does something fancy
            phase_name = getattr(phase_obj, "name", type(phase_obj).__name__)

        return (tile_name, score_bucket, meeples_left, phase_name)

    def _encode_action(self, action: Action) -> str:
        # repr() is stable and already used in printing
        return repr(action)

    # ---------- main RL logic ----------

    def getAction(self, game: CarcassonneGame):
        """
        Called once per turn.

        1) Use current game.state to update Q for the *previous*
           (state, action) pair based on score change.
        2) Choose next action with epsilon-greedy policy.
        3) Store (state, action, score) to update on the next turn.
        """
        valid_actions: list[Action] = game.get_possible_actions()
        if not valid_actions:
            return None

        # --- 1) compute current state key ---
        current_state_key = self._encode_state(game)
        current_score = game.state.scores[self.index]

        # --- 2) update Q for previous transition, if any ---
        if self.last_state_key is not None and self.last_action_key is not None:
            # reward = change in my score since my last move
            reward = current_score - self.last_score

            # estimate max future Q from current state over all valid actions
            max_future_q = 0.0
            for act in valid_actions:
                a_key = self._encode_action(act)
                max_future_q = max(
                    max_future_q,
                    self.q_table.get((current_state_key, a_key), 0.0),
                )

            old_q = self.q_table.get(
                (self.last_state_key, self.last_action_key), 0.0
            )
            new_q = (1 - self.alpha) * old_q + self.alpha * (
                reward + self.gamma * max_future_q
            )
            self.q_table[(self.last_state_key, self.last_action_key)] = new_q
            
            # --- DEBUG: print Q-table size occasionally ---
            if len(self.q_table) % 200 == 0:  # print every 200 updates
                print(f"[DEBUG] Agent {self.index} Q-table size: {len(self.q_table)}")
    
        # --- 3) epsilon-greedy action selection for *current* state ---
        import random

        if random.random() < self.epsilon:
            # explore
            chosen_action = random.choice(valid_actions)
        else:
            # exploit best-known action
            best_q = float("-inf")
            chosen_action = None
            for act in valid_actions:
                a_key = self._encode_action(act)
                q_val = self.q_table.get((current_state_key, a_key), 0.0)
                if q_val > best_q:
                    best_q = q_val
                    chosen_action = act

            # if we somehow never set chosen_action (all zero & -inf), fall back to random
            if chosen_action is None:
                chosen_action = random.choice(valid_actions)

        # --- 4) remember current state/action/score for next update ---
        self.last_state_key = current_state_key
        self.last_action_key = self._encode_action(chosen_action)
        self.last_score = current_score

        print(f"Agent({self.type}) {self.index}: {chosen_action}")
        return chosen_action
    
    def reset_episode(self):
        """Clear per-episode memory (but keep learned Q-table)."""
        self.last_state_key = None
        self.last_action_key = None
        self.last_score = 0
