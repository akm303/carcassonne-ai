# GWU - CSCI 6511 AI Algorithms Project
### Group:
- Keith Zhang
- Anvay Paralikar
- Alex Frolov
- Ari Majumdar

### [Link to Proposal (Google Docs)](https://docs.google.com/document/d/1PEDPkamepkVnma3u2gy3hDgGm40ObsuCCUwDg2AMZo8/edit?usp=sharing)

### Project Setup/Run:
- Setup instructions in [README.md](../README.md) (at root level)


---
---

## Game
Carcassone is a turn-based tile-placement game.  
Though the game allows for 2-5 players and game  
expansions, we will be focusing on 2 player games  
with a base set of landscape tiles and non-farmer meeples.  

- 1: The game starts with a starting tile, $t_0$, placed on the board.
- 2: On each player’s turn, they will:
- 2.1: expand the board by placing a square tile randomly drawn from  
       a set of 72 tiles, and placing it on the existing board such that:
    - at least one edge is in contact with a tile  
      on the board.
    - all tiles adjacent to the newly placed tile  
      share a feature type along shared edges.
- 2.2: The player will then optionally place a Meeple on that tile,  
       if the feature does not currently have a meeple on it.
- 3: A game ends once all 72 tiles are placed.

---
# Milestone 1 (Nov 16): 
## State Space Model
The state space $\mathcal{S}$ for Carcassonne is the set of unique boards (including both  
tile and meeple placements) that can be generated over the course of the game.  

The environment implementation generates a state consisting of the current tile to be  
placed, and a set of "feature planes" [1] compiled to represent:
- the current board
- all tiles currently on the board
- all meeple placements on those tiles. 

We use the state for our state-space model, but describe it mathematically below.

*_Note:  
Due to the game implementation, there are a few changes & limitations that differ from the original game [1]   
This includes: board size limited to 30x30, no starting tile, first tile placed by first player_


---
### Base Game
- Players $\mathbb P_0,\mathbb P_1$, each with a supply of 7 meeples
- A set $\mathcal{T}$ of 72 landscape tiles (non-uniformally distributed across 24  
tile types, but constant and consistent across runs of the base game)
- An empty 30x30 board $B$ *


---
### Game Objects
We define the following objects that make up a game state, and define them below:
- Tiles
- Deck (of tiles)
- Board
- Meeple


---
#### Tiles
Each landscape tile $t\in\mathcal{T}$ is a square with:
- Five positions, four of which are edges
    - $E=\{n, s, e, w\}$
        - Edges `north, south, east, west`  
        (represented as $n,s,e,w$ respectively)
    - $P=E +\{c\}$
        - These four edges and position `center`  
        (represented by $c$)
    - Notation:
        - $t^E, t^P$ denote the set of all edges and all positions of tile $t$ respectively
            - note that $t^E\subset t^P$
        - $t^e,t^p$ denote an edge $e\in t^E$ and position $p\in t^P$, respectively
            - note that $e$ is a special type of position $p$

        - Two positions $p,p'$ are 'connected' if:
            - $p,p'$ are adjacent within a tile  
                - For any two $p,p'\in t^P, p≠p'$, if  
                  set $\{p,p'\} ≠ \{n,s\}$ and $\{p,p'\} ≠ \{e,w\}$,  
                  then $p,p'$ are connected.  
                - these pairs of positions $p\in t^P$ are connected:  
                  $(n,e),(n,w),(s,e),(s,w),(n,c),(s,c),(e,c),(w,c)$  
            - $p,p'$ are adjacent along the shared edge of two adjacent tiles $t,t'$
                - $\exists$ edges $p\in t^E,p'\in t'^E$ st. $p,p'$ are adjacent

- Each position $p\in P$ displays a feature of type $f$ (denoted as $p_f$):
    - Every position has a feature.
    - Edge feature types include: 
        - `{fields, city, road}` enumerated as $f_1,f_2,f_3$
        - $\forall p\in E,$ all edge positions $p$ contains a feature from set $\mathcal{F}_E = \{f_1,f_2,f_3\}$ 
        - All edges have a feature from the set $\mathcal{F}_E = \{f_1,f_2,f_3\}$
        - these features are expanded by placing an adjacent tile with the matching feature on the shared edge. 
    
    - Other feature types include:
        - `{village, monastery}` enumerated as $f_4,f_5$
        - these features ($f_4,f_5$) may only exist in $c$ positions of a tile, and mark the starts/ends of features like roads.
        - $\forall p\in P,$ all positions $p$ contain a feature from set $\mathcal{F}_P=\mathcal{F}_E+\{f_4,f_5\}$ 
        
- Features are created and expanded by placing tiles that connect positions of shared feature types.
    - A feature $F=\{p_1,p_2,...,p_n\}$ is a run of connected positions that all share the same feature type.  
    ie. $\forall p,p'\in F, p_f=p_f'=f$.

- Each tile may be rotated for placement.
    - Let $rotate(t,\theta)$ be a function that rotates $t$ by $\theta\in\{0º, 90º, 180º, 270º\}$  


---
#### Deck
Let $D$ be a queue of undrawn tiles  
$D$ will be referred to as the 'pile' or 'deck'.  
$D$ has methods:
- $push()$: to enqueue a tile 
- $pop()$: to dequeue a tile 
- $next()$: to view next tile in queue (aka the 'top' of the deck) 
$\forall t\in\mathcal{T}$ are pushed onto $D$ in a random order.  
$t\in D=\{t_1,t_2,...,t_{72}\}$ where $t_s$ is the tile drawn at step $s$.  


---
#### Board
Let $B$ represent the Board:
- $B$ is a 30x30 matrix *
- Let $i,j$ be indices such that $\forall i,j: 1 ≤ i,j ≤ 30$
- $b_{i,j}$ represents the position on $B$ at coordinates $(i,j)$
- For each $b_{i,j}\in B$:
$$
b_{i,j} = 
\begin{cases} 
    0 & \text{if no tile at position }(i,j) \\
    t_{s} & \text{if tile $t_s$ at position }(i,j) \\
\end{cases}
$$  
- ie. Board $B$ is:
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
Let $|B|$ return the number of tiles currently in $B$


---
#### Meeple
Meeples provide a point-multiplying mechanism in Carcassonne.  
After a tile is placed, the player has the option to also place  
a meeple on a feature of that tile, as long as it is the first  
and only meeple of that feature.  
(eg. if the current tile is placed to extend a road that already  
has a meeple, a new meeply may not be placed.)

Each player has 7 meeples that they may place at any step during the game.  
We can think of this as a set of meeples $M$ where $0≤|M|≤7$.  
A player $\mathbb P$'s meeple set is denoted as $\mathbb P_M$.

Because a player can only place a meeple $m$ on a tile when that tile is placed on the board,  
we associate a placed meeple with the tile and feature it was placed on.  
That is, each meeple $m_{t_s,p}\in M$ denotes the meeple $m$ placed on tile $t_s$ in position  
$p\in t_{p}$ at time step $s$. An unplaced meeple is denoted as $m\in M$.

- Let $meeples(t)$ return 
    - None if there is no meeple on $t$
    - Otherwise, the meeple and its position $p\in t^p$
- Let $meeples(B)$ return the set of meeples currently in $B$  
    - ie. for each tile in $B$ with meeples, return the set of meeples placed on board $B$


---
### State Space ($\mathbb X$)
#### Game States
Let $\mathbb X$ be the state space of the Carcassonne base game.  
At each step $s$, where $1 ≤ s ≤ 72$:  
We define the current game state $x_s\in\mathbb X$ as an aggregate of the object states $x_s = [\mathbb P',B_s, D_s]$, where:

- $\mathbb P'$ denotes the current player (player whose turn it is on step $s$)
    - $\mathbb P' = \mathbb P_{(s-1)\mod 2}$ in a two player game
    - $\mathbb P_M'$ denotes that player's set of unplaced meeples
    - ie.
$$
    s=1: \mathbb P' =\mathbb P_0 \\ 
    s=2: \mathbb P' =\mathbb P_1 \\ 
    s=3: \mathbb P' =\mathbb P_0 \\ 
    ...\\
    s=72: \mathbb P' =\mathbb P_1 \\
$$
- $B_s$ is the board state at step s 
    - ie. $tiles(B_s)=\{t_1,...,t_{s-1}\}$
- $D_s$ is the remaining undrawn tiles
    - ie. $D_s = D-tiles(B_s)$
    - $\therefore D_s = [t_{s},...,t_{72}]$
    - Let $t_s$ be the next tile drawn from $D_s$
        - ie. $t_s=D_s.next()$  
_*Note: because $t_s$ is implicitly defined in $D_s$, its not included separately in the game state,  
        though it will be referred to here as the 'current' or 'active' tile_
        - Only $t_s$ is observable in $D_s$  


---
#### Initial State (ie. $s=1$):
$x_1$: the following assignments are made:
- $\mathbb P'=\mathbb P_0$ 
- $D_1=D$ 
- $B_1$ is an empty board;   
$\forall b_{i,j}\in B_1, b_{i,j}=0$, so: 
$$
\begin{matrix}
B_1=
\begin{bmatrix}
    0 & 0 & 0 & \dots  & 0 \\
    0 & 0 & 0 & \dots  & 0 \\
    \vdots & \vdots & \vdots & \ddots & \vdots \\
    0 & 0 & 0 & \dots  & 0 \\
\end{bmatrix} \\
\\ 
\begin{matrix}
ie. & tiles(B_1)=\{\} \\ 
\therefore & meeples(B_1)=\{\}
\end{matrix}
\end{matrix}
$$
$\therefore x_1 = [\mathbb P'=\mathbb P_0, B_1,D_1=D]$


---
### Action space ($\mathcal A$)
The action space $\mathcal A$ is defined as the set of all possible tile and meeple placements  
for $t_s,B_s\in x_s$ that produces a legal $B_{s+1}\in x_{s+1}$  
(ie. producing a valid transition from $x_s \to x_{s+1}$).

At game state $x_s=[\mathbb P',B_s, D_s]$, player $\mathbb P'$ chooses an action $a_s\in\mathcal{A}$.

First, the player selects a board location and rotation for current tile $t_s$ to place the tile.   
Second, the player chooses whether or not to place a meeple on a feature of the tile they just placed;  
meeple placement is valid as long as the feature doesn't already contain another meeple.

Actions $a_s\in\mathcal A$ are defined as tuples:
$$
\begin{array}{l}
    a_s = ((b_{i,j},\theta),p), \text{ where:} \\
    \begin{array}{l}
        \text{position }b_{i,j}\in B_s\land b_{i,j}=0, \\
        \text{rotation } \theta \text{ is selected st. }is\_valid\_placement(B_s, b_{i,j}=rotate(t_s,\theta))\text{ returns True}, \\
        \text{and position } p\in t_s \text{ is selected st. }is\_valid\_meeple(B_s, b_{i,j}, p) \\
    \end{array}
\end{array}
$$
The two helper functions, $is\_valid\_placement()$ and $is\_valid\_meeple()$ are defined below.


---
#### Helper Functions
Adjacent tiles must share the same feature type on adjacent edges.  

For board $B_s$, board position $b_{i,j}$, and tile $t_s$ rotated by $\theta$ to be assigned to $b_{i,j}$,  
(ie. $b_{i,j} = t_s = rotate(t_s,\theta)$)

Let function $is\_valid\_placement(B,b_{i,j})$ return true if all adjacent tile edges share the same feature $f$:

- For each board positions with tiles $b'\in B$ (where $b'$ is assigned tile $t'$),  
and $b'$ is adjacent to $b_{i,j}$ (ie. all $b'\in\{b_{i+1,j}, b_{i-1,j}, b_{i,j+1}, b_{i,j-1}\}$),  
- Let edges $e\in t_s$ and $e'\in t'$ refer to the adjacent edge of tiles $t$ and $t'$ (ie. $e=e'$)  
- If $\exists\ b'\text{ st. } e_f≠e_f'$, return $False$.  
- Otherwise return $True$.

Let function $features\_with\_meeple(B,t_s)$ return the set of all  
features on, and extended by, tile $t_s$ that currently have a meeple.  

Let function $is\_valid\_meeple(B,t_s,p)$ return true if  
$p_f \cup features\_with\_meeple(B,t_s)=\empty$.  

(ie. the feature $f$ at position $p\in t^p_s$ does not extend a feature that currently has a meeple)

---
<!-- ###### Version 2 of legal_meeple_placements function definition
Let function $legal\_meeple\_placements(B_s,t_s)$ be a function that returns all legal meeple placements $m_s$:
$$
m_s = 
\begin{cases}
None \\
\text{all valid positions $p\in t^p_s$ where assigning $p=m_s$}\\
\text{ won't conflict with $m_i$ ($1 ≤ i ≤ s-1)$}
\end{cases}
$$ -->

---

---
<!-- ##### (old version - only get legal actions, rather than check for validity) 
Let $legal\_board\_placements(B_s,t_s)$ be a function that returns all valid board positions $b_{ij}\in B_s$ and rotations $\theta\in\{0º, 90º, 180º, 270º\}$ on $t_s$ such that assigning $b_{i,j}=rotate(t_s,\theta)$ results in a valid board $B_{s+1}$

Let $legal\_meeple\_placements(B_s,t_s)$ be a function that returns all legal meeple placements $m_s$:
$$
m_s = 
\begin{cases}
None \\
\text{all valid tile positions $p\in t^p_s$ on which assigning $p=m_s$ results in a valid board $B_{s+1}$}
\end{cases}
$$ -->

---



### Milestone 2: 
#### State Space Implementation:
The state space was implemented in the original project, which provided methods for accessing the game state, retrieving legal actions, and applying those actions.

As such, our focus was on implementing agents.

Our original goal was to implement an agent to utilize the Monte Carlo Tree Search.





---
## Sources:
Carcassonne Implementation:
- [1] (https://wingedsheep.com/programming-carcassonne/)

Polyominoes:
- [2] (https://www.math.cmu.edu/~bkell/21110-2010s/polyominoes.html)
- [3] (https://epubs.siam.org/doi/10.1137/1.9781611977929.10)

Markov Modeling:
- [4] (https://ml-lectures.org/docs/reinforcement_learning/ml_reinforcement-learning-2.html)