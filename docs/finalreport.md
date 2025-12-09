# AI Agents for Carcassonne
### CSCI 6511 AI Algorithms Final Project  
### Authors:
- Keith Zhang
- Anvay Paralikar
- Alex Frolov
- Ari Majumdar

---
*_Notes:_

###### ***Regarding Game Implementation***:  
Due to the game implementation, there are a few changes & limitations that differ from the original game.   
This includes the following: 
- board size limited to 30x30
- no starting tile, first tile placed by first player

See [original author's implementation document](#4-programming-carcassonne---vincent-bons-wingedsheep-2020) for more details.

###### ***Regarding Documentation and Math Rendering***:  
Math rendering currently using KaTeX. Effort currently under way to format  
using MathJAX, for reading documentation with github's markdown viewer.  
Currently, Matrix expressions and fonts appear broken on github's default markdown viewer.

---
### Quick Links
Links to important documentation:
- [Source Code (Github Repo)](https://github.com/akm303/carcassonne-ai)
- [Project Proposal (Google Docs)](https://docs.google.com/document/d/1PEDPkamepkVnma3u2gy3hDgGm40ObsuCCUwDg2AMZo8/edit?usp=sharing)
- [Quick Setup Information](../README.md)
- [Detailed Setup Information](setup.md)
- [Milestone 1 (State Space Descripton)](statespace.md)
- [Team Contributions](contributions.md)

More included at the bottom [(click here)](#project-links).


---
## Contents
1. [Problem Statement](#1-problem-statement)
2. [Game Modeling](#2-game-modeling)
3. [Our Solution Method](#3-solution-method)
4. [Related Solutions](#4-related-solutions-to-similar-problems)
5. [All Project Links](#5-all-project-links)


---
## 1. Problem Statement
Carcassonne is a 2-5 player tile-placement game with an intractibly large state space.  
We want to build and compare a set of agents using a variety of cutting-edge AI algorithms  
(including MCTS, Q-Learning, Sarsa, and Sarsa($\lambda$)) to play a two-player game of Carcassonne  
with the goal of scoring more points than their opponent.

The game is played in turns, where a player draws a random tile from a deck of 72 tiles, and  
places it adjacent to any number of previously placed tiles on the board as long as the features on adjacent  
edges match. The player may then optionally place a meeple on a meeple-less feature, which acts  
as a point multiplier once a feature is extended and completed. 

There are a number of complexities that makes solving this problem non-trivial:
- A balance must be struck between short-term and long-term rewards,  
  complicated by feature extensions and (optional) meeple placements.
- The game is non-deterministic due to the tile drawing mechanic.  
  Tiles are drawn at random from a set with a non-uniform distribution.
- Each tile may be rotated (4 placement variations per tile), and may  
  have multiple positions in which they can be placed on the board.
- Multiple runs of the game are very unlikely to repeat game states, due  
  to the massive state space and non-deterministic nature of tile drawing.

The original game's complete rules and pieces are defined here: [Carcassonne Wiki - base game](https://wikicarpedia.com/car/Base_game)  
See note [regarding game implementation](#regarding-game-implementation) for differences between original game and game-engine implementation 


---
## 2. Game Modeling
State Space, Action space, transitions, and ovservations defined here: [milestone 1 (statespace.md)](../docs/statespace.md)

---
## 3. Solution Method
Per our proposal, we chose to solve the problem by implemented Agents to play  
Carcassonne using a MCTS and several Reinforcement Learning (RL) algorithms.  

We implemented the following algorithms and integrated them into agents:
- Stochastic (Random)
- Monte Carlo Tree Search (MCTS)
- Q-Learning
- Sarsa
- Sarsa($\lambda$)

Monte-Carlo Tree Search would play the game dynamically, constructing a partial tree based on a fixed number of action-selections, expansion, simulation, and backpropagation loops. Though slow, these agents were expected to generally do better than the RL-based agents.  
The RL algorithms (Q-Learning, Sarsa, and Sarsa($\lambda$)) could be run completely out-of-the-box, but could potentialy improve their gameplay with a pre-trained set of Q-values.  
Though not explicitly included in our proposal, we wanted to see if we could potentially use RL algorithms to either be better than, or to specifically counter, an MCTS agent. More details to follow.


#### MCTS Method
##### Concept
Since every tile placement has many legal positions and orientations, its impossible to do an exhaustive search on the entire state space.
Similarly, its infeasible to predict the action space due to its dependence on the board state and distribution of remaining tiles.
This makes MCTS-based Carcassonne players particularly promising, since they had been used with much success in other games with massive state spaces.

#### RL Methods
##### Concept
We understood early on that reinforcement learning methods may be significantly less effective in this game, for a couple reasons relating to the (s,a) pairs:
- the state space includes the board state; its unlikely to have the exact same board into two playthroughs of the game
- actions are influenced by board state and a randomly selected tile, exponentially increasing the size of the set of state-action pairs
Because rewards are sparse, we suspect eligibility-trace based solutions, like Sarsa($\lambda$), will fare slightly better than Q-learning and Sarsa, but the enormous state space is still problematic. 
That being said, we wanted to experiment with it, since RL-methods could learn the "behaviors" of particular opponents. For example, training an RL-based agent to provide a challenge specifically against MCTS agents may be possible. 
Additionally, due to our MCTS Agent's rollout implementation, which selects random-actions every turn simulate the game (ie. essentially the same behavior as the stochastic agent), it may be possible to train our RL models using stochastic agents, which operate much faster than MCTS and essentially behave the same in the early-game.


#### Additional Components
- along



---
## 4. Related Solutions to Similar Problems
### Solutions for Carcassonne:
###### 1. [*Implementing a Computer Player for Carcassonne (Cathleen Heyden, 2009)*](https://project.dke.maastrichtuniversity.nl/games/files/msc/MasterThesisCarcassonne.pdf)  
- A master's thesis analyzing the game of Carcassonne, and attempting an implementation of the game and of AI players. 

###### 2. [*Playing Carcassone with Monte Carlo Tree Search (Ameneyro et al., 2020)*](https://arxiv.org/abs/2009.12974)  
- An exploration into the use of Monte-Carlo Tree Search algorithms (MCTS & MCTS-RAVE) to play Carcassonne.

###### 3. [*Monte Carlo Tree Search for Carcassonne - (Max Jappert, 2022)*](https://ai.dmi.unibas.ch/papers/theses/jappert-bachelor-22.pdf)
- A bachelor's thesis working on improving the performance of the MCTS algorithms used by Ameneyro et al.

### Other Related Work:
#### Game Engine Implementation
###### 4. [*Programming Carcassonne - (Vincent Bons (Wingedsheep), 2020)*](https://wingedsheep.com/programming-carcassonne/)  
- The design and implementation document written by the author of the game engine we are using.  
Provided insight on how the game and state space were modeled, as well as some differences  
between the original game and the implementation.

#### State Space Modeling
###### 5. [CMU Document on Polyominoes](https://www.math.cmu.edu/~bkell/21110-2010s/polyominoes.html)
###### 6. [Paper Counting Polyominoes up to 70 terms](https://epubs.siam.org/doi/10.1137/1.9781611977929.10)



---
## 5. all Project Links
Full set of project links (to all directories and documentation)

#### Implementation Links
- Source Code Repository: [(`github repo`)](https://github.com/akm303/carcassonne-ai)
- Detailed Setup Information: [(`setup doc`)](../README.md)
- Team Contributions: [(`contributions doc)](contributions.md)

#### Final Project Source Files/Directories (Project Organization)
These are links to files and directories where we implemented  
and documented our code per the CSCI-6511 final project spec.

- Documentation: [(maintained in `docs/`)](../docs/)
- Agent Implementations: [(in `agents/`)](../agents/)
    - RL Q-tables: [(loaded/stored from `agents/params/`)](../agents/params/)
- MCTS Implementation: [(`MCTS/`)](../MCTS/)
- Main Game Script: [game.py](../game.py)
- Training Script: [train.py](../train.py)
- Menu Script: [menu.py](../menu.py)
- Scoreboard Script: [scoreboard.py](../scoreboard.py)

#### Design Docs
Original game implemented by Wingedsheep (details on design and implementation [here](https://wingedsheep.com/programming-carcassonne/))  
Basic Agent design and implementation details [here](agents.md)
