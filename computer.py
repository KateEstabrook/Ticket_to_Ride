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
        self.cards_needed = {"pink":0, "blue":0, "orange":0, "white":0, "green":0, "yellow":0, "black":0, "red":0, "wild":0}
        self.routes_needed = []
        self.curr_dest = None

    def play(self):
        # use turn finished instead of big if elif else
        turn_finished = False
        # Player turn decision logic

        # Update whether comp's dest card is completed and draw new card
        if self.player.get_map().check_completed(self.curr_dest):
            self.curr_dest.complete()
            new_card = game_globals.dest_deck.remove(-1)
            self.player.add_card(self.player.get_destination_cards(), new_card)
            self.curr_dest = new_card
            turn_finished = True

        # if the curr_dest of the comp is not completed, we must find the weights of paths, and if we can claim one, then claim it and end turn
        if self.curr_dest != None and not turn_finished:
            src = self.curr_dest.get_city_1()
            dist, route_lists = self.djikstra(src)
            for city in route_lists[self.curr_dest.get_city_2()]:
                # smt smth

                if self.can_claim():
                    # claim it
                    turn_finished = True
                    break

        if self.useful_faceup() and not turn_finished: # Sees a useful faceup card, draw it
            if self.useful_faceup() and not turn_finished: # Sees a useful faceup card (and it didn't draw a faceup rainbow), draw it
                0
            elif not turn_finished: # Draw from the deck
                self.player.add_card(self.player.get_train_cards(), game_globals.train_deck.remove(-1))
                turn_finished = True

        if not turn_finished: # Draw from the train card deck if no better options
            self.player.add_card(self.player.get_train_cards(), game_globals.train_deck.remove(-1))
            if self.useful_faceup(): # Sees a useful faceup card (and it isn't a faceup rainbow), draw it
                0
            else: # Draw from the deck
                self.player.add_card(self.player.get_train_cards(), game_globals.train_deck.remove(-1))
        
        print(f"{self.player} computer played")

    def can_claim(self):
        """"Returns boolean whether or not comp can claim a route 
        that helps to complete a destination card"""
        return False
    
    def useful_faceup(self):
        """"Returns boolean for if it successfully drew a useful faceup card"""
        for i in range(game_globals.faceup_deck.get_len()):
            if self.cards_needed[game_globals.faceup_deck[i].get_color()] > 0:
                # Remove the card from face-up deck
                taken_card = game_globals.faceup_deck.remove(i)
                game_globals.self.player.get_train_cards().add(taken_card)
                if taken_card.get_color() == "wild":
                    self.turn_finished = True
                # Replenish the face-up deck
                if game_globals.train_deck.get_len() > 0:
                    new_card = game_globals.train_deck.remove(-1)  # Draw from top
                    # Insert the new card at the same position we removed from
                    game_globals.faceup_deck.cards.insert(i, new_card)
                return True
        return False