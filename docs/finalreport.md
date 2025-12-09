# AI Agents for Carcassonne
### CSCI 6511 AI Algorithms Project  
### Authors:
- Keith Zhang
- Anvay Paralikar
- Alex Frolov
- Ari Majumdar

---
### Project Document Links
Below are a set of hyperlinks to different documents submitted for our project:
- [Problem Description (Proposal in Google Doc)](https://docs.google.com/document/d/1PEDPkamepkVnma3u2gy3hDgGm40ObsuCCUwDg2AMZo8/edit?usp=sharing)
- [Milestone 1 (State Space Descripton)](statespace.md)
- [Solution Method](solutions.md)


### Project Setup/Run:
- Documents uses Markdown with KaTeX math rendering.  
  Use a viewer that supports math rendering to see formulas correctly.

- Base Project/Game Setup and Run instructions in root level [README.md](../README.md)

- Software requirements
    - Python Interpreter Version 3.12.*
    - Python Module Requirements in [`requirements.txt`](../requirements.txt)

- Setup instructions
    - project setup instructions: [README.md](../README.md)
    - agent setup instructions: []
    - running instructions: (wip)


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
Defined here: [milestone 1](../docs/statespace.md)



## Implementation
- Source Code: [(`github repo`)](https://github.com/akm303/carcassonne-ai)
- Setup Documentation: [(`setup doc`)](../README.md)
- Agent Code Directory: [(`agents/`)](../agents/)

## Design
Game implemented by Wingedsheep (details on design and implementation [here](https://wingedsheep.com/programming-carcassonne/))  
Basic Agent design and implementation details [here](agents.md)



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
- Ari Majumdar
    - project setup, structure, and architecture
    - agent design & implementation
        - abstract agent
        - stochastic agent
    - Reports, Milestones, and Group Coordination
    - Game-engine QoL improvements

