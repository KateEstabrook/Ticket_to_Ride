# Ticket to Ride
### CS 3050 (Software Engineering) Final Project
### Group #1 – Elisabeth, Kate, Mateo, Oliver

---

## Project Description
We recreated the classic board game *Ticket to Ride* using Python Arcade.  
This is a 4-player game with 1 human player and 3 computer-controlled players.

---

## Requirements
You will need the following Python packages:

- `platform`
- `arcade`
- `heapq`

You can install missing packages using pip:

ex: `pip install arcade`

## How to Run
Open a terminal (or IDE) and run 
`python board.py`
or
`python3 board.py`

## Instructions for Playing
### Objective
Score the most points by:

- Completing destination tickets (connecting cities with continuous train routes)
- Building the longest continuous route
- Placing trains on the board

### Setup
1. Color Selection: Choose your player color at the start
2. Instruction Menu: Review game rules or click "Exit" if familiar
3. Destination Cards: Select your initial destination tickets

You will start with 4 random train cards and 45 train pieces. 

### Gameplay
One each turn, choose **ONE** of these actions:
1. Draw Train Cards
- Take 2 train cards from the face-up deck or draw pile (click the deck or the card you want)
- If you take a face-up locomotive (wild) card, it counts as one of your two cards
- You may draw destination cards instead (see below)

2. Claim a Route
- Spend train cards matching the color and quantity needed for a route
- Place your colored trains on the claimed route by selecting the two adjacent cities
- Score points based on route length:
  - 1 train = 1 point
  - 2 trains = 2 points
  - 3 trains = 4 points
  - 4 trains = 7 points
  - 5 trains = 10 points
  - 6 trains = 15 points

3. Draw Destination Cards
- Select the destination card deck to draw 4 destination tickets
- Keep at least 1
- Destination cards show two cities you need to connect with your trains
- Completed destinations score points at game end
- Uncompleted destinations deduct points

### Special Rules
- Gray Routes: Can be claimed with any single color of cards
- Locomotive Cards: Wild cards that can substitute for any color
- Double Routes: Some cities have parallel routes that can be claimed by different players

### Game End
- Trigger: When any player has 3 or fewer trains remaining
- Final Round: All other players get one more turn
- Scoring:
  - Points for claimed routes
  - Points for completed destination tickets
  - Minus points for uncompleted destination tickets
  - 10 bonus points for longest continuous route

### Winning
- The player with the highest total score wins!
- Press ESC to exit the win screen

Enjoy your journey across the country!
