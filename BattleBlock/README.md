zhura_Block
===========
This bot is the current version of my bot on theaigames Block Battle game.
It uses a simple search algorithm that bases its own moves based off a heuristic that weighs different features negatively or positively.
This bot was based off of the Python 3 starter bot provided by rbtcs, which can be found under the Getting Started page for the Block Battle game.

Running the bot
---------------
In terms of running it locally, through the terminal or command line change the directory to where the file "BotRun.py" is.
Then use the command "python BotRun.py".
This will give room for the user to type commands to the bot, and the bot will parse these commands in the Parser.py file.
Once you give it all the commands necessary, type the command "action moves x" where x is how much time the bot has to give a set of moves in milliseconds.

Strategy descriptions
---------------------
GeneticStrategy.py was originally supposed to use a genetic strategy to select the best moves out of a population and continue mutating it, but that was scrapped for the new strategy in place there.
The actual strategy in this file searches the field left and right for the best spot to place the piece being operated on for all the rotations the piece can do.
It judges the positions by features the field contains, such as bumpiness, holes, aggregate height, lines cleared, etc.. 
Weights were tested based off the many matches the bot participated in the competition.
This bot is more on the aggressive side versus a more passive bot that can keep the number of blocks on the field to a minimum.

HeightStrategy.py was similar to the current implementation, but much using less features to base the move off of. This strategy only based the set of moves to choose based off of the column's height.
This doesn't take into consideration the maximum height of the pieces below it.

RLStrategy.py was going to try to implement a reinforcement learning strategy for the bot, but after much thought the plan for the strategy was abandoned.
This is documented within the document that's attached to this repository. 
All it contains right now is a bare minimum to calculate features and their base weights.
The choose function would reward the bot after some state->action,but is obviouslly not implemented completely to do that.

