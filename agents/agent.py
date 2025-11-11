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
    Agent must define a getAction method
    """

    def __init__(self, index=0):
        self.index = index

    def choice(self, game):
        return self.getAction(game)

    def getAction(self, state):
        raise NotImplementedError()


class GameAgent(Agent):
    def __init__(self, index):
        self.index = index

    def getAction(self, game: CarcassonneGame):
        """
        Basic agent selects action at random
        """
        valid_actions: list[Action] = game.get_possible_actions()
        action = random.choice(valid_actions)
        print(f"Agent_{self.index}: {action}")
        return action
