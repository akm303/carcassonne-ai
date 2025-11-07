
# carcassonne
Carcassonne implementation in python

![Example game](https://github.com/wingedsheep/carcassonne/blob/master/example_game.gif)

## Features

* Tilesets 
    * Base game
    * The river
    * Inns and cathedrals
* Abbots
* Farmers

## Installation
Updated for python 3.11.5

* Clone the project
* Go to the project folder
* Run the following: 
```sh
# sets up local environment
python -m venv venv 

# activates local environment
source .venv/bin/activate

# installs required packages (numpy & Pillow)
pip install -r requirements.txt
```

You can now use the API in other projects.

## API

Code example for a game with two players

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
