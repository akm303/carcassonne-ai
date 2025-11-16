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
    """rename based on reinforcement learning agent we choose to implement"""
    def __init__(self, index):
        self.index = index
        self.type = "Qlearn"

    def getAction(self, game: CarcassonneGame):
        pass