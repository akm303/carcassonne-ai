import random

from wingedsheep.carcassonne.carcassonne_game import CarcassonneGame
from wingedsheep.carcassonne.objects.actions.action import Action

from .base import Agent
from MCTS.algorithm import MCTS

class MCTSAgent(Agent):
    """Agent using Monte-Carlo Tree Search"""
    def __init__(self, index, iterations=150):
        self.index = index
        self.type = "MCTS"
        self.iterations = iterations

    def getAction(self, game: CarcassonneGame) -> Action | None:
        # basic, safe behaviour so the game runs
        valid_actions = game.get_possible_actions()
        if not valid_actions:
            return None

        # TODO: replace this with actual MCTS search
        return random.choice(valid_actions)     