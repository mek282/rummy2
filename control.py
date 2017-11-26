"""
This is the control AI, which plays somewhat randomly. It exists for the purpose
of allowing us to conclude that our other AIs are at least better than random.
"""

"""
Plays randomly
Look at its hand, and select a card to play at random
Randomly decide which deck to draw from
Make sure, can't discard if it drew from the open deck
"""

import sys, pygame
from objects import *
import init_gui
import random

class Control(Player):
    def __init__(self, game, name):
        Player.__init__(self, game, name)

    def play_draw(self):
        i = random.randint(0,1)
        #if i == 0, draw from the closed deck
        if i == 0:
            self.draw_deck()
        #if i == 1, draw from the discard pile
        else:
            self.draw_discard()

    def play_discard(self):
        i = random.randint(0,10)
        self.discard(self.hand.contents[i])

    def declare_rummy(self):
        self.game_state.check_goal_state(self)