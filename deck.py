"""
Train Cards Deck (essential, hard)
- Amount of each card remaining
- Shuffle
- Add card
- Remove card
- Name (Draw, Discard, Faceup, Player, …)
- Deck sprites (not yet)

Route Card Deck (30 routes) (essential, hard)
- Amount of cards remaining
- Shuffle
- Add card
- Remove card                                  
- Name (Draw, Discard, Faceup, Player, …)
- Deck sprites (not yet)
"""

import operator
import random
#import cards

STARTING_NUM_CARDS = 0

class Deck:
    """Deck class"""
    def __init__(self, name):
        self.num_cards = STARTING_NUM_CARDS
        self.name = name
        self.cards = []

    def shuffle(self):
        """Shuffles the deck"""
        random.shuffle(self.cards)

    def remove(self, index):
        """Removes a card from the deck at a certain index and return it"""
        return self.cards.pop(index)

    def remove_cards(self, color, count):
        """Remove a list of cards of a color + wild cards to make up for the count"""
        if self.has_cards(color, count):
            discarded = []
            i = 0
            while i < count:
                try:
                    discarded.append(self.remove(self.get_card_index(color)))
                except TypeError:
                    discarded.append(self.remove(self.get_card_index("wild")))
                i += 1
            return discarded

    def add(self, card):
        """Adds a card to the deck"""
        self.cards.append(card)

    def add_cards(self, cards_list):
        for card in cards_list:
            self.add(card)

    def clear(self):
        self.num_cards = STARTING_NUM_CARDS
        self.cards = []

    def has_cards(self, color, count):
        """Checks if the passed cards are in the deck including wild cards"""
        if self.get_count(color) >= count:
            return True
        if self.get_count("wild") + self.get_count(color) >= count and color != "wild":
            return True
        return False

    def sort(self):
        """Sorts the deck"""
        self.cards.sort(key=operator.attrgetter('color'))

    def refresh_deck(self, input_deck):
        for card in input_deck.get_cards():
            self.add(card)
        input_deck.clear()
        self.shuffle()

    def get_count(self, color):
        """Gets the number of cards with that color"""
        count = 0
        for card in self.cards:
            if card.get_color() == color:
                count += 1
        return count

    def get_card_index(self, color):
        """Returns the index of a train card of a certain color"""
        for card in self.cards:
            if card.get_color() == color:
                return int(self.cards.index(card))
        return None

    def get_card_at_index(self, index):
        """Returns the card at a certain index in the deck"""
        lst = []
        for card in self.cards:
            lst.append(card)
        return lst[index]

    def get_len(self):
        """Returns length of deck"""
        count = 0
        for _ in self.cards:
            count += 1
        return count
    
    def get_cards(self):
        return self.cards

    def __str__(self):
        """To String"""
        s = ""
        for card in self.cards:
            s += str(card) + '\n'
        return f"{s}"

    def __eq__(self, other):
        """Equals function"""
        # It's good practice to first check if 'other' is an instance of the same class
        if not isinstance(other, Deck):
            return NotImplemented  # Or raise TypeError("Can only compare with MyClass instances")
        # Define the equality logic based on the attributes
        return self.cards == other.cards
