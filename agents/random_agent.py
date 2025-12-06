import random

from wingedsheep.carcassonne.carcassonne_game import CarcassonneGame
from wingedsheep.carcassonne.objects.actions.action import Action

from .base import Agent


class RandAgent(Agent):
    """Agent that selects random moves"""
    def __init__(self, index):
        self.index = index
        self.type = "Random"

    def getAction(self, game: CarcassonneGame):
        """
        Basic agent selects action at random
        """
        valid_actions: list[Action] = game.get_possible_actions()
        action = random.choice(valid_actions)
        return action
