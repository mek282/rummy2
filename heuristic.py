# greedy best first search, where H(card) = fractional value indicating how many runs you'll have


import sys, pygame
from objects import *
import init_gui
import random

class Heuristic(Player):
    def __init__(self, game, name):
        Player.__init__(self, game, name)

    #self.drawCard
    #self.discardCard



    def play_draw(self):
        self.best_deck_option()
        if self.drawCard == 10:
            return self.draw_deck()
        else:
            return self.draw_discard()

    def play_discard(self):
        self.discard(self.discardCard)
        return self.discardCard

    def declare_rummy(self):
        self.game_state.check_goal_state(self)

    def best_deck_option(self):
        self.drawCard = 10
        current = calculate_hand_value(self.hand.contents)
        for x in range(len(self.hand.contents)):
            tempHand = self.hand.contents[:]
            tempHand[x] = self.game_state.deck.contents[]

    def calculate_hand_value(self):
