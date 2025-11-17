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

# State Space:
#### Version 4
The state space for Carcassonne is the set of unique boards and meeple placements that can be generated over the course of the game.  
*_Note:  
Due to the game implementation, there are a few changes & limitations that don't exist in the original game [1]  
(eg. board size limitations, no starting tiles so first tile placed by first player, etc.)_

- Pile of undrawn tiles $t\in$ pile $P=\{t_1,t_2,...,t_{72}\}$ is non-uniformly distributed.  
- For Board $B$
    - Let Board $B$ be a 30x30 matrix*
    - Let $i,j$ be indices such that $\forall i,j: 1 ≤ i,j ≤ 30$*  
    - For each $b_{ij}\in B$:
$$
b_{ij} = 
\begin{cases} 
    0 & \text{if no tile at position }i,j \\
    t_{s} & \text{if tile $t_s$ at position }i,j \\
\end{cases}
$$  
ie. Board B is:
$$
B=
\begin{bmatrix}
    b_{1,1} & b_{1,2} & b_{1,3} & \dots  & b_{1,30} \\
    b_{2,1} & b_{2,2} & b_{2,3} & \dots  & b_{2,30} \\
    \vdots & \vdots & \vdots & \ddots & \vdots \\
    b_{30,1} & b_{30,2} & b_{30,3} & \dots  & b_{30,30}
\end{bmatrix}
$$
and let $|B|$ be the set of tiles currently in $B$



---

At each step $s$, where $0 ≤ s ≤ 72$  
(where s=0 represents the board setup before the first action).  
State $x_s$ at step $s$ is defined by:
- Let $B_s$ be the board state at s (ie. $|B_s|=\{t_0,...,t_{s-1}\}$)
- Let $P_s$ be the remaining undrawn tiles @ s (ie. $P_s = P-|B_s|$)
- Let $t_s$ be the tile drawn at step $s$


<!-- Commented out bc we havent really defined these...?
- Transition matrix $T_{s}$ 
- Action $a_s$ is a 30x30 matrix, where:
$$
a_{ij} = 
\begin{cases} 
    1 & \text{if tile $t_s$ is to be placed at position }i,j \\
    0 & \text{otherwise} \\
\end{cases}
$$
 -->
Step $s=0$ is the initial game state.  
$x_0$:
- The set of remaining tiles $P_0=\{t_1,t_1,t_2,...,t_{72}\}$ 
- so $|B_0|=\{\}$, and
$$
B_0=
\begin{bmatrix}
    0 & 0 & 0 & \dots  & 0 \\
    0 & 0 & 0 & \dots  & 0 \\
    \vdots & \vdots & \vdots & \ddots & \vdots \\
    0 & 0 & 0 & \dots  & 0 \\
\end{bmatrix}
$$
  

At each step $s$:  
$x_s$:  
- Player draws and places tile $t_s$
- The set of remaining tiles $P_1=\{t_{s+1},...,t_{72}\}$ 
- The current board $B_1=\{t_0,t_1\}$

---



<!-- idk if we need this -->
**Tile Model**  
We enumerate the directions of each tile $t_{ij}\in B_s$ as a square matrix (where each $e_{direction}$ represents an edge of tile $t$):
$$
t_{ij} = 
\begin{bmatrix}
   e_{west} & e_{north}\\
   e_{south} & e_{east}\\
\end{bmatrix}
=
\begin{bmatrix}
   00 & 01 \\
   10 & 11 \\
\end{bmatrix}
$$

---
---
---
---


<!-- 
**State Space**:  
#### version 2
$T$ is the total set of tiles

At each state $x_s,\ \forall$ steps $s, 0≤s≤72$:  
Let $B_s$ be the set of tiles currently placed on the board.  
Let $T_s$ be the set of remaining tiles ($T_s=T-B_s$).  
Let $i,j$ indicate row and column indices respectively ($\forall i,j: 1≤i,j≤72$).  

**Board Model**  
Max row or column-length of a Carcassonne board would be 72.  
This is a certain overestimate, due to the inclusion of tiles with bending features (eg. a tile with a road connecting west and north), but the area coverage as of $s_{72}$ will always be 72 tiles.
Therefore, lets represent board $B_s$ as a 72x72 matrix, initialized to 0s (representing no tile placement):
$$
B=
\begin{bmatrix}
    t_{1,1} & t_{1,2} & t_{1,3} & \dots  & t_{1,72} \\
    t_{2,1} & t_{2,2} & t_{2,3} & \dots  & t_{2,72} \\
    \vdots & \vdots & \vdots & \ddots & \vdots \\
    t_{72,1} & t_{72,2} & t_{72,3} & \dots  & t_{72,72}
\end{bmatrix}
=
\begin{bmatrix}
    0 & 0 & 0 & \dots  & 0 \\
    0 & 0 & 0 & \dots  & 0 \\
    \vdots & \vdots & \vdots & \ddots & \vdots \\
    0 & 0 & 0 & \dots  & 0
\end{bmatrix}
$$

**Tile Model**  
We enumerate the directions of each tile $t_{ij}\in B_s$ as a square matrix (where each $e_{direction}$ represents an edge of tile $t$):
$$
t_{ij} = 
\begin{bmatrix}
   e_{west} & e_{north}\\
   e_{south} & e_{east}\\
\end{bmatrix}
=
\begin{bmatrix}
   00 & 01 \\
   10 & 11 \\
\end{bmatrix}
$$ -->



### Branching Factor
Considering meeples further increase branching factor; Each action may optional include the usage of a meeple




<!-- # version 1
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





<!-- #### Version 0
State Space Size
This is very difficult to compute the number of board configurations precisely due to a number of factors, but especially the variety of board shapes and placement restrictions, which results in a massive discrete state space.   

- After the starting tile $t_0$, each tile $t_s$ is drawn randomly from a non-uniformly distributed set $T=\{t_1,t_2,...,t_{71}\}$. 
- Tile placement is constrainted since each placed tile must "continue the landscape", which is dependent on:
    - the current board's shape
    - its current open sides/features
    - the current tile to be placed
- Meeple placement is dependent on:
    - the current placed tile
    - previous meeple placements


According to this [thesis](https://project.dke.maastrichtuniversity.nl/games/files/msc/MasterThesisCarcassonne.pdf), a lower bound on the state space can be calculated based on unique board shapes (called polyominoes), at $\approx 3\cdot10^{41}$


We compute board shapes for each tile on the board, where $1 ≤ s ≤ |T|=72$.  
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

--- -->


A Lower limit can be computed by estimating the number of board shapes:



---


### Milestone 2: 
#### Per Proposal:
- Complete the implementation of the model and training
- test-run the training, make sure it works.

#### State Space Implementation:





---
## Sources:
Carcassonne Implementation
[1] https://wingedsheep.com/programming-carcassonne/

polyominoes
[2] https://www.math.cmu.edu/~bkell/21110-2010s/polyominoes.html
[3] https://epubs.siam.org/doi/10.1137/1.9781611977929.10