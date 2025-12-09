import os, pickle, random

from wingedsheep.carcassonne.carcassonne_game import CarcassonneGame
from wingedsheep.carcassonne.objects.actions.action import Action

from .base import Agent


# Author: Alexander Frolov. Sarsa algorithm implementation.
# The code was originally taken from Anvay Paralikar and modified to fit chosen-Q approach for Sarsa instead of finding max-Q.
class SarsaAgent(Agent):
    """
    Tabular Sarsa agent.

    - Keeps a Q-table: key = (state_key, action_key)
    - Uses epsilon-greedy policy over valid actions
    - Reward = change in this player's score since its last move
    - Uses Q(s', a') of the next action which is chosen by epsilon-greedy policy (instead of looping to find max from all the next actions)
    """

    def __init__(
        self,
        index,
        params={"alpha": 0.3, "gamma": 0.9, "epsilon": 0.2},
        param_filepath=None,
    ):
        self.index = index
        self.type = "Sarsa"

        # Q[(state_key, action_key)] -> value
        self.q_table: dict[tuple, float] = {}
        if param_filepath:
            self.load_q_table(param_filepath)

        self.alpha = params["alpha"]  # learning rate
        self.gamma = params["gamma"]  # discount factor
        self.epsilon = params["epsilon"]  # exploration rate

        # memory of previous transition
        self.last_state_key = None # s
        self.last_action_key = None # a
        self.last_score = 0

    def _encode_state(self, game: CarcassonneGame) -> tuple:
        """Turn the big game state into a compact, hashable key."""
        state = game.state

        # 1) tile in hand
        next_tile = getattr(state, "next_tile", None)

        if next_tile is None:
            tile_name = "NO_TILE"
        else:
            tile_name = getattr(next_tile, "name", None)
            if tile_name is None:
                tile_name = getattr(next_tile, "id", None) or getattr(
                    next_tile, "tile_id", None
                )
            if tile_name is None:
                tile_name = type(next_tile).__name__

        # 2) score difference bucket
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

        # 3) no of meeples left
        meeples_left = state.meeples[self.index]

        # 4) game(tile vs meeple)
        phase_obj = getattr(state, "phase", None)
        if phase_obj is None:
            phase_name = "UNKNOWN_PHASE"
        else:
            phase_name = getattr(phase_obj, "name", type(phase_obj).__name__)

        return (tile_name, score_bucket, meeples_left, phase_name)

    def _encode_action(self, action: Action) -> str:
        return repr(action)

    # ---------- main RL logic ----------

    def getAction(self, game: CarcassonneGame):
        """
        Called once per turn.

        1) Look at the current state to get the new s' and current score
        2) Choose next action with epsilon-greedy policy, which is chosen from the new state.
        3) we use reward as the score difference
        4) Update Q for the previous (s, a) using r + gamma * Q(s', a')
        5) Store (new state, new action, score) to update on the next turn.
        """
        valid_actions: list[Action] = game.get_possible_actions()
        if not valid_actions:
            return None

        # compute current state key
        current_state_key = self._encode_state(game)
        current_score = game.state.scores[self.index]

        # epsilon-greedy action
        if random.random() < self.epsilon:
            chosen_action = random.choice(valid_actions)
        else:
            best_q = float("-inf")
            chosen_action = None
            for act in valid_actions:
                a_key = self._encode_action(act)
                q_val = self.q_table.get((current_state_key, a_key), 0.0)
                if q_val > best_q:
                    best_q = q_val
                    chosen_action = act

            if chosen_action is None:
                chosen_action = random.choice(valid_actions)
        #Q(s', a')
        a_next = self._encode_action(chosen_action)
        q_next = self.q_table.get((current_state_key, a_next), 0.0)

        # update Q for previous transition,
        if self.last_state_key is not None and self.last_action_key is not None:
            # change in my score since last score
            reward = current_score - self.last_score

            old_q = self.q_table.get((self.last_state_key, self.last_action_key), 0.0)
            new_q = (1 - self.alpha) * old_q + self.alpha * (
                reward + self.gamma * q_next
            )
            self.q_table[(self.last_state_key, self.last_action_key)] = new_q

            # printing the Q-table size
            if len(self.q_table) % 200 == 0:  # print every 200 updates
                print(f"[DEBUG] Agent {self.index} Q-table size: {len(self.q_table)}")

        #  Take current state/action/score for next update
        self.last_state_key = current_state_key # s'
        self.last_action_key = self._encode_action(chosen_action) # a'
        self.last_score = current_score

        print(f"{self}: {chosen_action}")
        return chosen_action

    def reset_episode(self):
        """Clear per-episode memory (but keep learned Q-table)."""
        self.last_state_key = None
        self.last_action_key = None
        self.last_score = 0

    def save_q_table(self, filepath: str) -> None:
        """Save the learned Q-table to disk."""
        with open(filepath, "wb") as f:
            pickle.dump(self.q_table, f)

    def load_q_table(self, filepath: str) -> None:
        """Load a previously saved Q-table"""
        if not os.path.exists(filepath):
            print(f"[WARN] Q-table file '{filepath}' not found. Starting again.")
            return
        with open(filepath, "rb") as f:
            self.q_table = pickle.load(f)
        print(f"[INFO] Loaded Q-table from '{filepath}', entries = {len(self.q_table)}")
