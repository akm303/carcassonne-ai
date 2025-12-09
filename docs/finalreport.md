# AI Agents for Carcassonne
### CSCI 6511 AI Algorithms Project  
### Authors:
- Keith Zhang
- Anvay Paralikar
- Alex Frolov
- Ari Majumdar

---
*Note regarding Documentation*
- Project documentation use Markdown with KaTeX math rendering.  
  Use a viewer that supports math rendering to see formulas correctly.  
  eg. VS-Code's default Markdown Viewer
  *note, currently porting to work using github's built in markdown viewer, which uses Mathjax instead of KaTeX.  
  Currently, Matrix and font-based rendering broken on github's default markdown viewere*

---
### Project Document Links
Below are a set of links to different documents submitted for and describing our work:
- [Project Proposal (Google Docs)](https://docs.google.com/document/d/1PEDPkamepkVnma3u2gy3hDgGm40ObsuCCUwDg2AMZo8/edit?usp=sharing)
- [Milestone 1 (State Space Descripton)](statespace.md)
- [Agent Information](agents.md)

------

## Problem Statement
Carcassonne is a 2-5 player tile-placement game with an intractibly large state space.  
We want to build and compare a set of agents using a variety of cutting-edge AI algorithms  
(such as MCTS, Q-Learning, and Sarsa) to play a two-player game of Carcassonne with the goal  
of scoring more points than their opponent.

The game is played in turns, where a player draws a random tile from a deck of 72 tiles, and  
places it adjacent to any number of previously placed tiles as long as the features on adjacent  
edges match. The player may then optionally place a meeple on a meeple-less feature, which acts  
as a point multiplier once a feature is extended and completed. 

There are a number of complexities that makes solving this problem non-trivial:
- A balance must be struck between short-term and long-term rewards,  
  complicated by feature extensions and meeple placements.
- The game is non-deterministic due to the tile drawing mechanic.  
  Tiles are drawn at random from a set with a non-uniform distribution.
- Each tile may be rotated (4 placement variations per tile), and may  
  have multiple positions in which they can be placed on the board.

The game's complete rules and pieces are defined here: [Carcassonne - base game](https://wikicarpedia.com/car/Base_game)  
We modeled the state space in [milestone 1](statespace.md)



## Related Solutions to Similar Problems
Solutions for Carcassonne:
1. [*Implementing a Computer Player for Carcassonne (Cathleen Heyden, 2009)*](https://project.dke.maastrichtuniversity.nl/games/files/msc/MasterThesisCarcassonne.pdf)  
A master's thesis analyzing the game of Carcassonne, and attempting an implementation of the game and of AI players. 

2. [*Playing Carcassone with Monte Carlo Tree Search (Ameneyro et al., 2020)*](https://arxiv.org/abs/2009.12974)  
An exploration into the use of Monte-Carlo Tree Search algorithms (MCTS & MCTS-RAVE) to play Carcassonne.

3. [*Monte Carlo Tree Search for Carcassonne - (Max Jappert, 2022)*](https://ai.dmi.unibas.ch/papers/theses/jappert-bachelor-22.pdf)  
A bachelor's thesis working on improving the performance of the MCTS algorithms used by Ameneyro et al.

Other Related Work:
4. [*Programming Carcassonne - (Vincent Bons (Wingedsheep), 2020)*](https://wingedsheep.com/programming-carcassonne/)  
The design and implementation document written by the author of the game engine we are using.  
Provided insight on how the game and state space were modeled, as well as some differences  
between the original game and the implementation.

State Space Modeling:
5. [CMU Document on Polyominoes](https://www.math.cmu.edu/~bkell/21110-2010s/polyominoes.html)
6. [Paper Counting Polyominoes up to 70 terms](https://epubs.siam.org/doi/10.1137/1.9781611977929.10)

## Model
State Space, Action space, transitions, and ovservations defined here: [milestone 1 (statespace.md)](../docs/statespace.md)

## Solution Method
We chose to solve the problem by implementing agents using the following algorithms:
- Monte Carlo Tree Search (MCTS)
- Q-Learning
- Sarsa
- Sarsa($\lambda$)

We also implemented a random-choice agent (refered to in other documentation as random or stochastic agent)  
that we use as an adversary to train reinforcement-learning (RL) based agents.

#### MCTS Method
Since every tile placement has many legal positions and orientations, its impossible to do an exhaustive search on the entire state space.
Additionally, the action space is similarly difficult to predict due to its dependence on the board state and remaining deck state.

#### RL Methods
We understood early on that reinforcement learning methods may be less effective in this game, for a couple reasons:
- the state space is influenced by the board state; its unlikely to have the exact same board into two playthroughs of the game
- actions are influenced by board state and a randomly selected tile, exponentially increasing the size of the set of state-action pairs
Because rewards are sparse, we suspect eligibility-trace based solutions, like Sarsa($\lambda$), will fare slightly better than Q-learning and Sarsa, but the enormous state space is still problematic. 
<!-- That being said, we wanted to experiment with it, since RL-methods could potentially learn the behaviors of particular opponents. For example, if we spent enough time and resources training an RL-based agent against MCTS, which uses a stochastic rollout policy (similar to the random agent), it may be possible to_______idk blanking here     -->


## Implementation
- Source Code: [(`github repo`)](https://github.com/akm303/carcassonne-ai)
- Setup Documentation: [(`setup doc`)](../README.md)
- Agent Code Directory: [(`agents/`)](../agents/)

## Design
Game implemented by Wingedsheep (details on design and implementation [here](https://wingedsheep.com/programming-carcassonne/))  
Basic Agent design and implementation details [here](agents.md)



### Project Setup/Run:
- Base Project/Game Setup and Run instructions in root level [README.md](../README.md)
- Software requirements
    - Python Interpreter Version 3.12.*
    - Python Module Requirements in [`requirements.txt`](../requirements.txt)

- Setup instructions
    - project setup instructions: [README.md](../README.md)
    - agent setup instructions: []
    - running instructions: (wip)


---


## Team Contributions
- Keith Zhang:
    - agent design & implementation
        - MCTS agent
    - Game-engine functional optimizations
- Anvay Paralikar
    - agent design & implementation
        - Q-Learning
        - Sarsa($\lambda$)
    - Project structuring & architectural improvements
- Alex Frolov
    - agent design & implementation
        - Sarsa 
        - Sarsa($\lambda$)
    - Menu & UI implementation 
    - Game-engine QoL improvements
    - (*note: had to do some manual migrations for Alex's work, as such our repo may be  
       missing some of his commit history; if so, please see his repo for implementation history ([linked here](https://github.com/Frolov-Alexander/carcassonne-ai/tree/master)))
- Ari Majumdar
    - project setup, structure, and architecture
    - agent design & implementation
        - abstract agent
        - stochastic agent
    - Reports, Milestones, and Group Coordination
    - Game-engine QoL improvements

