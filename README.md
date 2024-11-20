# FAI-Checkers
Course Project
Course: Foundations of AI
Instructors: Prof. Neeldhara Mishra
Prof. Manisha Padala

Team Members:
Deepanjali Kumari- 22110069
Anura Mantri- 22110144
Bhanu Repalle- 22110221
Saloni Shinde- 22110242
Thumma Ushashree- 22110272


Project Overview
This project is a Python implementation of the classic board game Checkers using the pygame module. It features:

Two-Player Mode: Players can play against each other locally.
Human vs AI Mode: A single player can play against an AI opponent.
The AI uses the Minimax Algorithm with Alpha-Beta Pruning to optimize decision-making and includes an Epsilon-Greedy Strategy for introducing variability in its moves.


How to Play:
Launching the Game: After running the script, you'll be presented with a menu to choose the game mode:
Two-Player Mode
Human vs AI Mode

Controls: Use the mouse to select and move pieces. Valid moves will be highlighted on the board. Pieces can capture opponent pieces by jumping over them diagonally to an empty square.  Regular pieces move diagonally forward while kings move diagonally forward and backward. Kings are created when a piece reaches the opponent’s back row. Multiple captures in one turn are allowed if conditions permit.

Objective:
Capture all of your opponent's pieces or block their moves.

*Customization:
AI Depth: Modify the depth of the Minimax tree in ai.py to control the difficulty level of the AI.
Epsilon Value: Adjust the epsilon parameter in ai.py to control the randomness of the AI’s moves.

Enjoy playing Checkers! 🎮
