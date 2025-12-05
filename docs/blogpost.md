# AI Agents for Carcassonne
### CSCI 6511 AI Algorithms Project  
### Authors:
- Keith Zhang
- Anvay Paralikar
- Alex Frolov
- Ari Majumdar

---
## Motivation
Carcassonne is a game with an intractibly large state space. 
The game rules and pieces are defined here: [Carcassonne - base game](https://wikicarpedia.com/car/Base_game)


## Problem Statement
We want to build and compare a set of agents using a variety of cutting-edge AI algorithms (such as MCTS, Q-Learning, and Sarsa) to play a two-player game of Carcassonne with the goal of scoring more points than their opponent.


## Related Work

1. [*Implementing a Computer Player for Carcassonne (Cathleen Heyden, 2009)*](https://project.dke.maastrichtuniversity.nl/games/files/msc/MasterThesisCarcassonne.pdf)  
A master's thesis analyzing the game of Carcassonne, and attempting an implementation of the game and of AI players. 
2. [*Playing Carcassone with Monte Carlo Tree Search (Ameneyro et al., 2020)*](https://arxiv.org/abs/2009.12974)  
An exploration into the use of Monte-Carlo Tree Search algorithms (MCTS & MCTS-RAVE) to play Carcassonne.
3. [*Monte Carlo Tree Search for Carcassonne - (Max Jappert, 2022)*](https://ai.dmi.unibas.ch/papers/theses/jappert-bachelor-22.pdf)  
A bachelor's thesis working on improving the performance of the MCTS algorithms used by Ameneyro et al.
4. [*Programming Carcassonne - (Vincent Bons (Wingedsheep), 2020)*](https://wingedsheep.com/programming-carcassonne/)  
The design and implementation document written by the author of the game engine we are using. Provided insight on how the game and state space were modeled, as well as some differences between the original game and the implementation.

## State Space
Defined here: [milestone 1](../agents/milestones.md)

<!-- ## Solution Method -->

## Implementation
- Source Code: [(`github repo`)](https://github.com/akm303/carcassonne-ai)
- Setup Documentation: [(`setup doc`)](../README.md)
- Agent Code Directory: [(`agents/`)](../agents/)

## Design
Game implemented by Wingedsheep (details on design and implementation [here](https://wingedsheep.com/programming-carcassonne/))  
Basic Agent design inspired by Berkeley CS188 Pacman AI Project Implementation ([course page](https://inst.eecs.berkeley.edu/~cs188/fa25/)).




## Evaluation
- Results

## Reproducibility
- Software requirements
- Hardware requirements
- Setup instructions
- Data links

## Team Contributions
- Keith Zhang:
    - MCTS implementation
    - Major game-engine QoL improvements & optimizations
- Anvay Paralikar
    - Q-Learning implementation
    - Project structuring & improvements
- Alex Frolov
    - Sarsa implementation (based on Q-Learning implementation)
    - Menu & UI implementation and related game-engine QoL improvements
    - Inclusion of human player (wip)
- Ari Majumdar
    - project setup and structuring
    - Base agent implementation (including random-choice agent)
    - Reports, Milestones, and Group Coordination
    - Minor game engine QoL improvements

