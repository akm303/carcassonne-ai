---
layout: default
---
# Project Setup
*Quick setup instructions in root level [README.md](../README.md)*  
This document is for more detailed setup instructions

---
## Contents
0. [Prerequisites](#1-prerequisites)
1. [Environment Setup](#2-environment-setup)
2. [Running a Game](#3-running-a-game)
3. [Training an Agent](#4-training-an-agent)


---
## 1. Prerequisites
- Software Requirements
    - Python Interpreter Version 3.12.*
    - Python Module Requirements in [`requirements.txt`](../requirements.txt)

- Hardware Requirements
    - System was developed and tested on MacOS and Windows


## 2. Environment Setup
Navigate to the root directory, and run the following commands:
```sh
# sets up local environment
python -m venv venv 

# activates local environment
source venv/bin/activate

# installs required packages
pip install -r requirements.txt
```
To verify correct installation, try running a game


## 3. Running a Game
In the root directory, run the following command to start a game:
```sh
python game.py
```

A menu should appear, on which you can make the following adjustments:
- viewing options
    - adjust game speed
    - choose whether or not to display a scoreboard
- game setup options
    - select number of players
        - *implementation well tested for two agents*
    - choose your two agents
        - if MCTS chosen, adjust iterations (number of nodes to generate per action)  

simply make your selections and hit start



## 4. Training an Agent
We weren't able to fully training and playing with individually trained agents during runtime.
However, we prepared a training script and setup the basic back-end infrastructure to be able  
to train unique agents, and (eventually) play specific RL agents against each other.

Use the following command to generate or train Q-table with id `U` using an agent running learning algorithm `M` against an adversary running non-learning algorithm `A` for `I` iterations:
```sh
python train.py -i {I} -m {M} [-a {A}] [-u {U}]
```
`M` can be 'qlearn', 'sarsa', or 'sarsalambda'
`A` can be 'random' or 'mcts' (but defaults to 'random' for invalid inputs)


For example:
```sh
python train.py -m sarsa -i 30 -a mcts
```

Additional details [here](training.md)