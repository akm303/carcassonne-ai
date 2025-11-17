# GWU - CSCI 6511 AI Algorithms Project
### Group:
- Keith Zhang
- Anvay Paralikar
- Alex Frolov
- Ari Majumdar

### [Link to Proposal](https://docs.google.com/document/d/1PEDPkamepkVnma3u2gy3hDgGm40ObsuCCUwDg2AMZo8/edit?usp=sharing)

### Project Setup/Run:
Setup instructions in README.md at root level

---
---

## Game
Carcassone is a turn-based tile-placement game. Though the game allows for 2-5 players and game expansions, we will be focusing on 2 player games with a base set of landscape tiles and non-farmer meeples.

0. The game starts with a starting tile, $t_0$, placed on the board
1. On each player’s turn, they will:
- 1.1 expand the board by placing a square tile randomly drawn from a set of 71 tiles, and placing it on the existing board such that:
    - at least one edge is in contact with a tile on the board
    - all edges of the placed tile in contact with other tiles match in feature types
- 1.2 The player will then optionally place a Meeple on the placed tile, if the feature does not currently have a meeple in it
2. A game ends once all 72 tiles are placed.

---
## Milestone 1 (Nov 16): 

#### Per Proposal:
- Setting up the environment/game engine
- implementing API to interact with the game engine for later use in training

#### State Space Description:
The state space for Carcassonne is the set of unique boards that can be formed over the course of the game. 
This is difficult to compute exactly due to a number of factors, but especially the variety of board shapes and placement restrictions, which results in a very large discrete state space.   

- After the starting tile $t_0$, each tile $t_s$ is drawn randomly from a non-uniformly distributed set $T=\{t_1,t_2,...,t_{71}\}$. 
- Tile placement is constrainted since each placed tile must "continue the landscape", which is dependent on:
    - the current board's shape
    - its current open sides/features
    - the current tile to be placed
- Meeple placement is dependent on:
    - the current placed tile
    - previous meeple placements


According to this [thesis](https://project.dke.maastrichtuniversity.nl/games/files/msc/MasterThesisCarcassonne.pdf), a lower bound on the state space can be calculated based on unique board shapes (called polyominoes), at $\approx 3\cdot10^{41}$


We compute boad shapes for each n tiles on the board, where $1 ≤ s ≤ |T|=72$.  
We consider mirrored or rotated polyominoes to be the same board state



To compute the number of board shapes at each step of play:  

0. $x_0$: Board starts with $t_0$ (aka $t_s$)  
    - 1 tile placed
    - 1 possible shape
    - 4 open edges

1. $x_1$: Tile $t_1$ is placed from remaining 71 tiles in $T$
    - 2 tiles placed
    - result is 1 possible shape
    - 6 open edges

2. $x_2$: Tile $t_2$ is placed from remaining 70 tiles in $T$
    - 3 tiles placed
    - result is 2 possible shapes (a line or corner)
    - 8 open edges

From here, shapes begin to get complicated.  
3. $x_3$: Tile $t_3$ is placed from remaining 69 tiles in $T$
    - 4 tiles placed
    - results in several possible shapes:  
        - if $s_2=Corner$, 7 possible $s_3$ shapes  
        - if $s_2=Line$, 8 possible $s_3$ shapes  
...  

70. Tile is placed from remaining 2 tiles
    - 71 tiles placed
71. Tile is placed from remaining 1 tile  
    - 72 tiles placed

---
**Model**:  
# version 3
At each state $x_s,\ \forall x, 0≤x≤72$:  
Let $B_s$ be the set of tiles on the board  
Let $T_s$ be the set of remaining tiles  
Let $i,j$ indicate row and column indices respectively.  
Let $l,w$ indicate board length and width respectively.

**Tile Model**  
At state $x_s$, each tile $t_{ij}\in B_s$ is a square matrix:
$$
t_s = 
\left[
\begin{matrix}
   e_{west} & e_{north} \cr
   e_{south} & e_{east} \cr
\end{matrix}
\right]
=
\left[
\begin{matrix}
   e_{00} & e_{01} \cr
   e_{10} & e_{11} \cr
\end{matrix}
\right]
$$

**Board Model**  
Max row or column-length of a Carcassonne board would be 72.  
This is a certain overestimate, due to the inclusion of tiles with bending features (eg. a tile with a road connecting west and north), but the area coverage as of $s_{72}$ will always be 72 tiles:


<!-- # version 2
At state $s$, each tile $t_s$ is defined as a square matrix:
$$
t_s = 
\left[
\begin{matrix}
   e_{w} & e_{n} \cr
   e_{s} & e_{e} \cr
\end{matrix}
\right]
=
\left[
\begin{matrix}
   e_{00} & e_{01} \cr
   e_{10} & e_{11} \cr
\end{matrix}
\right]
$$
where $w=west, n=north, s=south, e=east$.  
$t_{s}=e_{ij}$  -->




<!-- ---
# version 3
**Action-Value Function**
$$Q^π(s,a)=E^π[R_t+1+γQ^π(S_t+1,A_t+1)\ |\ S_t=s,A_t=a]$$

**State Space**
$$
\left[
\begin{matrix}
   a & b \cr
   c & d \cr
   e & f
\end{matrix}
\right]
$$


**Transition Matrix**
$$
P=
\left[
\begin{matrix}
   a & b \cr
   c & d
\end{matrix}
\right]
$$

**Transition Matrix**
$$
\left[
\begin{matrix}
   a & b \cr
   c & d
\end{matrix}
\right]
$$

**Value Function**:
$$

$$

 -->



A Lower limit can be computed by estimating the number of board shapes:



---


### Milestone 2: 
#### Per Proposal:
- Complete the implementation of the model and training
- test-run the training, make sure it works.

#### State Space Implementation: