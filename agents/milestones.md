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
# Milestone 1 (Nov 16): 


<!-- ! Trying to model how getting the next move -->
## State Space Model

The state space $\mathcal{S}$ for Carcassonne is the set of unique boards and meeple placements that can be generated over the course of the game.  

*_Note:  
Due to the game implementation, there are a few changes &  
limitations  that differ from the original game [1]  
(includes: board size limited to 30x30, no starting tile, first tile placed by first player)_

---
### Game Setup
- Players $A_0,A_1$, each with a supply of 7 meeples
- A set of 72 landscape tiles $\mathcal{T}$
- An empty 30x30* board $B$


---
### Tiles
Each landscape tile $t\in\mathcal{T}$ is a square with:
- four edges 
    - north, south, east, west (enumerated as 'n','s','e','w')
    - $E=\{n, s, e, w\}$
- five meeple positions
    - the four edges and 'center' ('center' represented by 'c')
    - $P=E +\{c\}$
- each position $p\in P$ displays a feature:
    - Edge feature types include: 
        - {grass, city, road}  
        - enumerated as $f_1,f_2,f_3$
    - Other feature types include:
        - {village, monastery, garden, farmhouse, cowshed, watertower, highwaymen, pigsty, stables}
        - (enumerated as $f_4,...,f_{12}$)
    - in other words:
        - $\mathcal{F}_x$ denotes the features available to $x$
        - $\mathcal{F}_E \in \{f_1,f_2,f_3\}$
        - $\mathcal{F}_P \in \mathcal{F}_E+\{f_4...,f_{12}\}$   <!-- ! double check -->

There are 24 unique tile types. Across all games (restrited to the base game),  
tile types are constant, consistent, and non-uniformly distributed amongst the 72 tiles.

<!-- Tile placement on the board is constrained:
- all adjacent edges must have matching features
-  -->

Each tile, when drawn, may be rotated.

Let $D$ be a queue of undrawn tiles  
$D$ will be referred to as the 'pile' or 'deck'.  
$D$ has methods:
- $push()$: to enqueu a tile 
- $pop()$: to dequeue a tile
- $top()$: to view top of stack

$\forall t\in\mathcal{T}$ are pushed onto $D$ in a random order.  
$t\in D=\{t_1,t_2,...,t_{72}\}$ where $t_s$ is the tile drawn at step $s$.  


---
### Board State
Let $B$ represent the Board:
- $B$ is a 30x30 matrix
- Let $i,j$ be indices such that $\forall i,j: 1 ≤ i,j ≤ 30$*  
- For each $b_{i,j}\in B$:
$$
b_{i,j} = 
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
Let $tiles(B)$ return the set of tiles currently in $B$  
Let $meeples(B)$ return the set of meeples currently in $B$  


---
### Time Step
At each step $s$, where $0 ≤ s ≤ 72$  
(where s=0 represents the initial board state before the first action).  

- Let $B_s$ be the board state at step s 
    - ie. $tiles(B_s)=\{t_1,...,t_{s-1}\}$
- Let $D_s$ be the remaining undrawn tiles
    - ie. $D_s = D-tiles(B_s)$
    - $\therefore D_s = [t_{s},...,t_{72}]$
- Let $t_s$ be the next tile drawn
    - ie. $t_s=D.top()$
<!-- - Let $t_s$ be the tile drawn next from $D$ at step $s$ -->

Let $X$ be the set of all possible game states.  
State $x\in X$ at step $s$ is defined as $x_s = [B_s,D_s,t_s]$ <!-- M_s]$ to model meeples? -->

---
#### Initial State (ie. $s=0$):
$x_0$:
<!-- - $P_0=D \implies t_0 =$  -->
- $D_0=D$ 
- $B_0$ is an empty board; ie. 
$$
B_0=
\begin{bmatrix}
    0 & 0 & 0 & \dots  & 0 \\
    0 & 0 & 0 & \dots  & 0 \\
    \vdots & \vdots & \vdots & \ddots & \vdots \\
    0 & 0 & 0 & \dots  & 0 \\
\end{bmatrix},\ \ 
tiles(B_0)=\{\}
$$
- no tile drawn at $s=0$

ie. $x_0 = [D, B_0, \empty]$
<!-- ie. $x_0 = [D, B_0, t_0]$ -->
  
---
#### Helper Functions
For board $B$, 
drawn tile $t$,  
tile rotation $\theta\in\{0º, 90º, 180º, 270º\}$  
and position (x,y) where $b_{x,y}\in B$ and $b_{x,y}=0$

Let function $is\_valid\_placement(B,t,\theta,(x,y))$ return true if:
- tile $t$ rotated by $\theta$ and placed at $b_{x,y}\in B$
- $\forall$ tiles $b'\in J=\{b_{x+1,y},b_{x-1,y},b_{x,y+1},b_{x,y-1} | b_{i,j} ≠ 0\}$ (adjacent board positions containing tiles)
    - $matching\_features(b',b_{x,y})$ is True
- adjacent to $b_{x,y}$, the adjacent edges have the same feature type
    <!-- - if $\forall e\in t_E$, and $\forall e'\in j, \forall j \in J$ where $J$ is the set of tiles  -->


For $b_1,b_2\in B$,  
Let function $matching\_features(b_1,b_2)$ return true if:
- $\exists$ edge $e\in b_1\land e\in b_2$ (adjacent edge)
- $\exists$ tiles $t_p$ on $b_1\land t_q$ on $b_2$ (there are tiles $t_p$ and $t_q$ on positions $b_1$ and $b_2$)
- and $t_p.e.f = t_q.e.f$ ($t_p$'s feature matches $t_q$'s feature on that edge)

---



For each step (ie. $\forall s,\ 0 < s ≤ 72$):
$x_s$:  
- $t_s \leftarrow P_{s-1}.pop()$  (ie. Player draws random tile from top of pile)
- $\theta = rotate(t_s)$
- $P_s = P_{s-1} - \{t_s\} =\{t_{s+1},...,t_{72}\}$ (ie. Set of remaining tiles in pile)

#### Action
<!-- Agent takes action $a_s$ which includes information for the two move phases   -->
Let $A' = A_s\mod2$ (ie. A' denotes the current player)  
$A_{s\% 2}$ takes action $a_s$ in two phases:
<!-- (tile placement, meeple placement): -->
- Phase 1:
    - A' draws tile $t_s$

- coordinates $i,j$, and orientation $\theta$ to place tile $t_s$ (ie. to set $b_{ij}=t_s$)
- coordinates i,j and to place tile $t_s$ (ie. to set $b_{ij}=t_s$):  
Policy $\pi(x_s,a_s)$:
- Phase 1:
    - The current board $B_s=\{t_1,t_2,...,t_s\}$
    - Player will place tile $t_s\rightarrow B_{s-1}$ at some $b_{ij}$ (per policy $\pi$)


When drawn, the tile may be rotated by $\theta\in\{0º,90º,180º,270º\}$, then placed on the board $B$ at some selected $(i,j)$

---


Each edge must be placed adjacent to an edge on the board such that
 adjacent edges share the same feature
 contains a feature type.  
We will enumerate the four edges as relative north, south, east, and west.  
ie. Tile $t$'s edges can be represented as an enumeration:
<!-- todo: enumerate feature types, so can define Pr[e = f and e=e' | x_{s-1}] or smth? -->

---
---
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

Markov Modeling  
[4] https://ml-lectures.org/docs/reinforcement_learning/ml_reinforcement-learning-2.html