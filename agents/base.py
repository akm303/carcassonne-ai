from typing import List

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

    def getAction(self, game: CarcassonneGame):
        """based on game state, return a single action"""
        raise NotImplementedError()

    def notify_action(self, actions: List[Action]):
        """notify agent of an action taken in the game (by any player)"""
        pass

    def __str__(self):
        return f"Agent_{self.index} ({self.type})"

    def __repr__(self):
        return f"Agent_{self.index} ({self.type})"

class PlayerAgent(Agent):
    """Agent that takes human inputs to select next move"""
    def __init__(self, index):
        self.index = index
        self.type = "Player"

    def getAction(self, game: CarcassonneGame):
        pass
