
# carcassonne
Carcassonne implementation in python  
- [*CSCI 6511 Project Final Report*](docs/finalreport.md)
- [*CSCI 6511 Milestone 1*](docs/statespace.md)

All documentation formatted to be rendered by Github's built-in viewer


![Example game](https://github.com/wingedsheep/carcassonne/blob/master/example_game.gif)

## Features

* Tilesets 
    * Base game
    * The river
    * Inns and cathedrals
* Abbots
* Farmers

## Quick Setup
#### installing the environment
Updated for python 3.11.*

* Clone the project
* Navigate to the project folder
* Run the following: 

```sh
# sets up local environment
python -m venv venv 

# activates local environment
source venv/bin/activate

# installs required packages (numpy & Pillow)
pip install -r requirements.txt
```

#### playing a game
Once installed, run the following command to start a game:
```sh
python game.py
```
Menu/game running details [here](docs/setup.md)



## API

Code example for a game with two players
```py
import random  
from typing import Optional  
    
from wingedsheep.carcassonne.carcassonne_game import CarcassonneGame  
from wingedsheep.carcassonne.carcassonne_game_state import CarcassonneGameState  
from wingedsheep.carcassonne.objects.actions.action import Action  
from wingedsheep.carcassonne.tile_sets.supplementary_rules import SupplementaryRule  
from wingedsheep.carcassonne.tile_sets.tile_sets import TileSet  
    
game = CarcassonneGame(  
    players=2,  
    tile_sets=[TileSet.BASE, TileSet.THE_RIVER, TileSet.INNS_AND_CATHEDRALS],  
    supplementary_rules=[SupplementaryRule.ABBOTS, SupplementaryRule.FARMERS]  
)  
    
while not game.is_finished():  
    player: int = game.get_current_player()  
    valid_actions: [Action] = game.get_possible_actions()  
    action: Optional[Action] = random.choice(valid_actions)  
    if action is not None:  
        game.step(player, action)  
    game.render() 
```

## CSCI 6511 Info
Link to Final Report: [Final Report](docs/finalreport.md)  
Link to Milestone 1: [milestone 1](docs/statespace.md)  
