"""
Computer players
"""

import player
import deck
import cards
import globals as game_globals

class Computer:
    def __init__(self, player):
        self.player = player
        self.cards_needed = {"pink":0, "blue":0, "orange":0, "white":0, "green":0, 
                             "yellow":0, "black":0, "red":0, "colorless":0}

    def play(self):
        # Player turn decision logic
        if len(self.player.get_destination_cards().get_uncompleted()) == 0 and game_globals.dest_deck.get_len() != 0: # No dest cards, draw 1
            self.player.add_card(self.player.get_destination_cards(), game_globals.dest_deck.remove(-1))
        elif self.can_claim(): # Can play a route, play it
            0
        elif self.useful_faceup(): # Sees a useful faceup card, draw it
            0
            if self.useful_faceup(): # Sees a useful faceup card (and it didn't draw a faceup rainbow), draw it
                0
            else: # Draw from the deck
                self.player.add_card(self.player.get_train_cards(), game_globals.train_deck.remove(-1))
        else: # Draw from the train card deck if no better options
            self.player.add_card(self.player.get_train_cards(), game_globals.train_deck.remove(-1))
            if False: # Sees a useful faceup card (and it isn't a faceup rainbow), draw it
                0
            else: # Draw from the deck
                self.player.add_card(self.player.get_train_cards(), game_globals.train_deck.remove(-1))
        
        print(f"{self.player} computer played")
        

        # Update whether player's dest cards are completed
        for card in self.player.get_destination_cards().get_uncompleted():
            if self.player.get_map().check_completed(card):
                card.complete()

    def can_claim(self):
        """"Returns boolean whether or not comp can claim a route 
        that helps to complete a destination card"""
        return False
    
    def useful_faceup(self):
        """"Returns boolean whether or not there is a useful faceup card"""
        return False