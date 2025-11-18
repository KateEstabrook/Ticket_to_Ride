"""
Computer players
"""

import player
import deck
import cards
import globals as game_globals
import constants as c

class Computer:
    def __init__(self, player):
        self.player = player
        self.cards_needed = {"pink":0, "blue":0, "orange":0, "white":0, "green":0, "yellow":0, "black":0, "red":0, "wild":0}
        self.routes_needed = []
        self.curr_dest = None

    def get_color(self):
        """Getter for player color"""
        return self.player.get_color()
    
    def get_map(self):
        """Getter for player map"""
        return self.player.get_map()
    
    def get_player(self):
        """Getter for player map"""
        return self.player

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
            self.update_cards_routes_needed()
            if self.can_claim():
                turn_finished = True

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

    def can_claim(self):
        """"Returns boolean whether or not comp can claim a route 
        that helps to complete a destination card"""
        for route in self.routes_needed:
            if self.player.get_train_cards().has_cards(route.get_color(), route.get_weight()):
                game_globals.game_map.remove_route(route.get_cities()[0], route.get_cities()[1])
                self.player.get_map().add_route(route)
                return True
        return False
    
    def useful_faceup(self):
        """"Returns boolean for if it successfully drew a useful faceup card"""
        for i in range(game_globals.faceup_deck.get_len()):
            if self.cards_needed[game_globals.faceup_deck.cards[i].get_color()] > 0:
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
    
    # For creating the adjacency list for the computer player's claimed routes and the global map
    def create_adjacency_list_global(self):
        """"Creates an adjacency list of the routes the computer player has claimed"""
        adj = {}
        map = self.player.get_map()

        for route in game_globals.game_map.get_paths():
            cities = route.get_cities()
            weight = route.get_weight()
            adj[cities[0]].append((cities[1], weight))
            adj[cities[1]].append((cities[0], weight))
                            
        for route in map.get_paths(): # add self paths with weight 0
            cities = route.get_cities()
            adj[cities[0]].append((cities[1], 0))
            adj[cities[1]].append((cities[0], 0))

        return adj
    
    def update_cards_routes_needed(self):
        """"Updates the cards needed and routes needed dictionary based on current destination card"""
        self.cards_needed = {"pink":0, "blue":0, "orange":0, "white":0, "green":0, "yellow":0, "black":0, "red":0, "wild":0}

        src = self.curr_dest.get_city_1()
        dest = self.curr_dest.get_city_2()
        dist, route_lists = self.player.get_map().djikstra(src, self.create_adjacency_list_global())

        map = self.player.get_map()

        # iterate through route lists at dest to find cities in path

        prev_city = src
        for cur_city in route_lists[dest]:
            cur_city
            
            if map.has_path(prev_city, cur_city):
                prev_city = cur_city
            else:
                route = game_globals.game_map.get_path_by_cities(prev_city, cur_city)
                self.cards_needed[route.get_color()] += route.get_weight()
                self.routes_needed.append(route)
