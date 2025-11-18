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

### State Space:
#### Version 5
The state space $\mathcal{S}$ for Carcassonne is the set of unique boards and meeple placements that can be generated over the course of the game.  

*_Note: Due to the game implementation, there are a few changes & limitations that differ from the original game [1]  
(includes: board size limited to 30x30, no starting tile, first tile placed by first player)_

---
#### State Model
---
Let pile $P$ represent the set of undrawn tiles $t$.  
$t\in P=\{t_1,t_2,...,t_{72}\}$ is non-uniformly distributed.  

---
Let $B$ represent the Board state:
- Let Board $B$ be a 30x30 matrix*
- Let $i,j$ be indices such that $\forall i,j: 1 ≤ i,j ≤ 30$*  
- For each $b_{ij}\in B$:
$$
b_{ij} = 
\begin{cases} 
    0 & \text{if no tile at position }(i,j) \\
    t_{s} & \text{if tile $t_s$ at position }(i,j) \\
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
Let $|B|$ be the set of tiles currently in $B$

---
Each tile $t\in P$ is a square where each edge contains a feature type.  
We will enumerate the four edges as relative north, south, east, and west.  
ie. Tile $t$'s edges can be represented as an enumeration:
<!-- todo: enumerate feature types, so can define Pr[e = f and e=e' | x_{s-1}] or smth? -->
$$
t = 
\left[
\begin{matrix}
   e_{west} & e_{north} \cr
   e_{south} & e_{east} \cr
\end{matrix}
\right]
=
\left[
\begin{matrix}
   00 & 01 \cr
   10 & 11 \cr
\end{matrix}
\right]
$$
When drawn, the tile may be rotated by $\theta\in\{0º,90º,180º,270º\}$, and is then placed on the board at some selected $(i,j)$

$\therefore$

At each step $s$, where $0 ≤ s ≤ 72$  
(where s=0 represents the board setup before the first action).  
State $x_s$ at step $s$ is defined by:
- Let $B_s$ be the board state at s (ie. $|B_s|=\{t_1,...,t_{s-1}\}$)
- Let $P_s$ be the remaining undrawn tiles @ s (ie. $P_s = P-|B_s|$)
- Let $t_s$ be the tile drawn at step $s$

#### Initial State (ie. $s=0$):
$x_0$:
- $P_0=P$ 
- $B_0$ is an empty board; ie. 
$$
B_0=
\begin{bmatrix}
    0 & 0 & 0 & \dots  & 0 \\
    0 & 0 & 0 & \dots  & 0 \\
    \vdots & \vdots & \vdots & \ddots & \vdots \\
    0 & 0 & 0 & \dots  & 0 \\
\end{bmatrix},\ \ 
|B_0|=\{\}
$$
  
#### For each step (ie. $\forall s,\ 0 < s ≤ 72$):
$x_s$:  
- $t_s \leftarrow P_{s-1}$  (ie. Player draws tile from pile)
- $\theta = rotate(t_s)$
- $P_s = P_{s-1} - \{t_s\} =\{t_{s+1},...,t_{72}\}$ (ie. Set of remaining tiles in pile)

Agent takes action $a_s$ which includes:
- coordinates $i,j$, and orientation $\theta$ to place tile $t_s$ (ie. to set $b_{ij}=t_s$)
- coordinates i,j and to place tile $t_s$ (ie. to set $b_{ij}=t_s$)
:  
Policy $\pi(x_s,a_s)$:
- Phase 1:
    - The current board $B_s=\{t_1,t_2,...,t_s\}$
    - Player will place tile $t_s\rightarrow B_{s-1}$ at some $b_{ij}$ (per policy $\pi$)


---
---
---
---
---

---
- f


---


---



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