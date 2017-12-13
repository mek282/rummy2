"""
This file defines classes that will be used to structure the game as follows:

Game: represents a single game, tracking its current state
Player: abstract class representing a computer player. AIs will implement Player
Card: represents a card in the deck
Deck: a collection of Card objects

"""

import random
from operator import attrgetter

random.seed()


""" Represents the current state of the game. """
class Game:
    def  __init__(self, game_deck, player1=None, player2=None):
        self.player1 = player1
        self.player2 = player2

        self.last_draw = None # None if unknown, else the card that the most recent player picked up

        self.deck = game_deck
        self.discard_pile = Deck(0)
        self.discard_pile.add(self.deck.contents.pop())
        self.turn = player1

    def recent_discard(self):
        return self.discard_pile.contents[len(self.discard_pile.contents)-1]

    """ Returns the match if a player has Rummy, else None """
    def check_goal_state(self, player):
        # check player 1's hand
        matches = player.hand.find_runs()
        matches.extend(player.hand.find_x_of_a_kind())

        for i in range(len(matches)):
            for j in range(i+1, len(matches)):
                for k in range(i+2, len(matches)):
                    tmp = matches[i] + matches[j] + matches[k]
                    if len(tmp) != 10:
                        continue
                    count = 0
                    for card in tmp:
                        if tmp.count(card) == 1:
                            count +=1
                    if count == 10:
                        return tmp
        return None



""" Abstract class representing a Player."""
class Player:
    def __init__(self, game, name):
        self.name = name
        self.hand = Deck(0)
        self.game_state = game
        for i in range(10):
            self.draw_deck()
        self.hand.contents = sorted(self.hand.contents, key=attrgetter('suit', 'value'))


    """ Removes a card from deck and add it to Player's hand. """
    def draw_deck(self):
        c = self.game_state.deck.contents.pop()
        self.hand.add(c)
        if len(self.game_state.deck.contents) == 0:
            recentCard = self.game_state.discard_pile.contents.pop()
            self.game_state.deck = self.game_state.discard_pile
            random.shuffle(self.game_state.deck.contents)
            self.game_state.discard_pile = Deck(0)
            self.game_state.discard_pile.add(recentCard)
        self.game_state.last_draw = None
        return c

    """ Removes a card from discard_pile and add it to Player's hand. Returns
        the card if successful, else returns None. """
    def draw_discard(self):
        if len(self.game_state.discard_pile.contents) > 0:
            c = self.game_state.discard_pile.contents.pop()
            self.hand.add(c)
            self.game_state.last_draw = c
            return c
        else:
            self.game_state.last_draw = None
            return None

    """ Removes and returns a specific card from this Deck. Returns its index."""
    def discard(self, card):
        i = self.hand.contents.index(card)
        c = self.hand.contents.pop(i)
        self.game_state.discard_pile.add(c)
        self.hand.contents = sorted(self.hand.contents, key=attrgetter('suit', 'value'))
        return i

    """ Should return the card the player just drew """
    def play_draw(self):
        raise NotImplementedError("play has not been implemented")

    """ Returns the card the player just discarded """
    def play_discard(self):
        raise NotImplementedError("play has not been implemented")


""" Represents a single Card object. If value = 1, it is an ace; 2-10 are the
equivalently numbered cards; 11 is a jack, 12 a queen, and 13 a king.
Suit is a string representing the suit: it is either Hearts, Spades, Clubs,
or Diamonds. """
class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit


""" Represents a collection of Card objects. Default is to initialize a
standard shuffled deck of 52 cards. If num_cards != 52, the Deck will be
initialized as empty.
The LAST item in the list is considered to be the 'top' of the Deck.
"""
class Deck:
    def __init__(self, num_cards=52):
        self.contents = []
        if num_cards == 52:
            for suit in ["Hearts", "Clubs", "Spades", "Diamonds"]:
                for i in range(1, 14):
                    self.contents.append(Card(i, suit))
            random.shuffle(self.contents)

    def add(self, card):
        self.contents.append(card)

    """ Returns a list of all runs in the deck of length 3 or 4 and the
        same suit """
    def find_runs(self):
        runs = []
        h = sorted(self.contents, key=attrgetter('suit', 'value'))
        # runs of length 3
        for i in range(len(h)-2):
            if ((h[i].value + 1 == h[i+1].value) and (h[i+1].value + 1 == h[i+2].value)
            and (h[i].suit == h[i+1].suit) and (h[i+1].suit == h[i+2].suit)):
                runs.append([h[i], h[i+1], h[i+2]])
        # runs of length 4
        for i in range(len(h)-3):
            if ((h[i].value + 1 == h[i+1].value) and (h[i+1].value + 1 == h[i+2].value)
                and (h[i+2].value + 1 == h[i+3].value) and (h[i].suit == h[i+1].suit)
                and (h[i+1].suit == h[i+2].suit) and (h[i+2].suit == h[i+3].suit)):
                runs.append([h[i], h[i+1], h[i+2], h[i+3]])
        return runs

    """ Returns a list of all 3 or 4 of a kind matches in the deck """
    def find_x_of_a_kind(self):
        x_of_a_kind = []
        h = sorted(self.contents, key=attrgetter('value'))
        for i in range(len(h)-3):
            # 4 of a kind - also add all 3 of a kind combos
            if (h[i].value == h[i+1].value and h[i+1].value == h[i+2].value
                and h[i+2].value == h[i+3].value):
                x_of_a_kind.append([h[i], h[i+1], h[i+2], h[i+3]])
                x_of_a_kind.append([h[i], h[i+1], h[i+2]])
                x_of_a_kind.append([h[i], h[i+1], h[i+3]])
                x_of_a_kind.append([h[i], h[i+2], h[i+3]])
                x_of_a_kind.append([h[i+1], h[i+2], h[i+3]])
            # ONLY 3 of a kind
            elif h[i].value == h[i+1].value and h[i+1].value == h[i+2].value:
                x_of_a_kind.append([h[i], h[i+1], h[i+2]])
            # missing final index
            elif (i == len(h)-4 and h[i+1].value == h[i+2].value
                and h[i+2].value == h[i+3].value):
                x_of_a_kind.append([h[i+1], h[i+2], h[i+3]])
        return x_of_a_kind
