# Agent Design/API

Agent design inspired by Berkeley CS188 Pacman AI Project's Agent implementation ([course page](https://inst.eecs.berkeley.edu/~cs188/fa25/)).

An Agent will:
- observe the game state (ie. take the game state as input)
- select from a set of legal actions (action pairs):
    1. current tile rotation and placement coordinates
    2. optional meeple placement on meeple-less feature of current tile

We first define an abstract agent. Any subclass will need to implement a `getAction()` method which will choose an action based on the current `game.state`.

From there, we implement the following agents:
- Stochastic Agent
- MCTS Agent
- Q-Learning Agent
- Sarsa Agent
- Sarsa($\lambda$) Agent

---
### Stochastic Agent
Chooses action from legal moves at random

### MCTS Agent
At each round of play, this agent generates a tree that it uses to inform its action selection.
To select a move, it loops:
- generates a successor state based on a potential action
- simulates the rest of the game by randomly selecting moves (rollout)
- backpropogates results up the tree

After a fixed number of ndoes are added to the tree, the action with the highest potential score is selected. After the next player takes their turn, this agent shifts its root to the appropriate next node (based on the action it selected) and continues generating the tree, generating a fixed number of nodes each turn.

<!-- There are a number of potential optimizations that could be made -->


### Q-Learning Agent

Over multiple games, this agent generates a table of Q-values for each state,action pair using an epsilon-greedy exploration strategy. These agents learn based on evaluating the "optimal" actions of future states rather than actual actions taken (ie. off-policy)



### Sarsa Agent
Similar in design to Q-learning agent, except these agents evaluate  the actual actions taken from a future state (ie. on-policy).