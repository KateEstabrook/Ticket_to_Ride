"""
Computer players
"""

import player
import deck
import cards
import globals as game_globals
import constants as c
import time

class Computer:
    def __init__(self, player):
        self.player = player
        self.cards_needed = {"pink":0, "blue":0, "orange":0, "white":0, "green":0, "yellow":0, "black":0, "red":0, "colorless":0}
        self.routes_needed = []
        self.curr_dest = None
        self.turn_finished = False
        self.taken_card = None

    def get_color(self):
        """Getter for player color"""
        return self.player.get_color()
    
    def get_map(self):
        """Getter for player map"""
        return self.player.get_map()
    
    def get_player(self):
        """Getter for player map"""
        return self.player

    def set_curr_dest(self, dest):
        """Getter for player map"""
        self.curr_dest = dest

    def play(self):

        time.sleep(1.0)

        # use turn finished instead of big if elif else
        self.turn_finished = False
        self.taken_card = None

        # Setting current destination (at the start of game)
        if self.curr_dest == None:
            self.curr_dest = self.player.get_destination_cards().get_cards()[0]
        

        # Player turn decision logic
        # Update whether comp's dest card is completed and draw new card
        elif self.player.get_map().check_completed(self.curr_dest):
            self.curr_dest.complete()
            # Setting current destination if first dest is complete
            if self.player.get_destination_cards().get_uncompleted():
                    self.curr_dest = self.player.get_destination_cards().get_uncompleted()[0]
            else:
                new_card = game_globals.dest_deck.remove(-1)
                self.player.add_card(self.player.get_destination_cards(), new_card)
                self.curr_dest = new_card
                self.turn_finished = True

        print(self.curr_dest)

        # if the curr_dest of the comp is not completed, we must find the weights of paths, and if we can claim one, then claim it and end turn
        if not self.turn_finished:
            self.update_cards_routes_needed()
            # Check if we can claim and claim
            if self.can_claim():
                self.turn_finished = True

        if not self.turn_finished and self.useful_faceup(): # Sees a useful faceup card, draw it
            if not self.turn_finished and self.useful_faceup(): # Sees a useful faceup card (and it didn't draw a faceup rainbow), draw it
                self.turn_finished = True
            elif not self.turn_finished: # Draw from the deck
                self.player.add_card(self.player.get_train_cards(), game_globals.train_deck.remove(-1))
                print('Drew from deck')
                self.turn_finished = True

        elif not self.turn_finished: # Draw from the train card deck if no better options
            self.player.add_card(self.player.get_train_cards(), game_globals.train_deck.remove(-1))
            print('Drew from deck')
            if self.useful_faceup(): # Sees a useful faceup card (and it isn't a faceup rainbow), draw it
                self.turn_finished = True
            else: # Draw from the deck
                self.player.add_card(self.player.get_train_cards(), game_globals.train_deck.remove(-1))
                print('Drew from deck')
                self.turn_finished = True

        time.sleep(1.0)

    def can_claim(self):
        """"Returns boolean whether or not comp can claim a route 
        that helps to complete a destination card"""
        for route in self.routes_needed:
            if self.player.get_train_cards().has_cards(route.get_color(), route.get_weight()):
                game_globals.game_map.remove_route(route.get_cities()[0], route.get_cities()[1])
                self.player.get_map().add_route(route)
                # Remove train cards
                removed = self.player.get_train_cards().remove_cards(route.get_color(), route.get_weight())
                game_globals.discard_deck.add_cards(removed)
                self.turn_finished = True
                self.routes_needed.remove(route)
                return True
        return False
    
    def useful_faceup(self):
        """"Returns boolean for if it successfully drew a useful faceup card"""
        for i in range(game_globals.faceup_deck.get_len()):
            color = game_globals.faceup_deck.cards[i].get_color()
            if color == 'wild':
                color = 'colorless'
            if self.cards_needed[color] > 0:
                # Remove the card from face-up deck
                self.taken_card = game_globals.faceup_deck.get_card_at_index(i)
                if self.taken_card:
                    if color == "colorless":
                        break
                # Remove the card from face-up deck
                self.taken_card = game_globals.faceup_deck.remove(i)
                self.player.get_train_cards().add(self.taken_card)
                if self.taken_card.get_color() == "wild":
                    self.turn_finished = True
                # Replenish the face-up deck
                if game_globals.train_deck.get_len() > 0:
                    new_card = game_globals.train_deck.remove(-1)  # Draw from top
                    # Insert the new card at the same position we removed from
                    game_globals.faceup_deck.cards.insert(i, new_card)
                print('took faceup card')
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
            if cities[0] not in adj:
                adj[cities[0]] = [(cities[1], weight)]
            else:
                adj[cities[0]].append((cities[1], weight))
            if cities[1] not in adj:
                adj[cities[1]] = [(cities[0], weight)]
            else:
                adj[cities[1]].append((cities[0], weight))
                            
        for route in map.get_paths(): # add self paths with weight 0
            cities = route.get_cities()
            if cities[0] not in adj:
                adj[cities[0]] = [(cities[1], 0)]
            else:
                adj[cities[0]].append((cities[1], 0))
            if cities[1] not in adj:
                adj[cities[1]] = [(cities[0], 0)]
            else:
                adj[cities[1]].append((cities[0], 0))

        return adj
    
    def update_cards_routes_needed(self):
        """"Updates the cards needed and routes needed dictionary based on current destination card"""
        self.cards_needed = {"pink":0, "blue":0, "orange":0, "white":0, "green":0, "yellow":0, "black":0, "red":0, "colorless":0}
        self.routes_needed = []

        src = self.curr_dest.get_city_1()
        dest = self.curr_dest.get_city_2()
        dist, route_lists = self.player.get_map().djikstra(src, self.create_adjacency_list_global())

        map = self.player.get_map()

        # iterate through route lists at dest to find cities in path

        prev_city = src
        for cur_city in route_lists[dest]:
            cur_city
            
            routes = game_globals.game_map.get_path_by_cities(prev_city, cur_city)


            for route in routes:
                if map.has_path(prev_city, cur_city) or route == None:
                    prev_city = cur_city
                else:
                    self.cards_needed[route.get_color()] += route.get_weight()
                    if route.get_weight() > 0:
                        self.routes_needed.append(route)
