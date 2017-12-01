import sys, pygame
from objects import *
import init_gui
import random

class Heuristic(Player):
    def __init__(self, game, name):
        Player.__init__(self, game, name)

    """Calculates the value of the hand"""
    def h(self, hand):
        score = 0

        for x in range(len(hand)):
            for y in range(x+1,len(hand)):
                if x.value == y.value:
                    score += 2
                elif (x.value == y.value - 1 and x.suit == y.suit):
                    score += 3
                elif (x.value == y.value + 1 and x.suit == y.suit):
                    score += 3
                elif (x.value == y.value - 2 and x.suit == y.suit):
                    score += 2
                elif (x.value == y.value + 2 and x.suit == y.suit):
                    score += 2
                elif (x.value == y.value - 3 and x.suit == y.suit):
                    score += 0.5
                elif (x.value == y.value + 3 and x.suit == y.suit):
                    score += 0.5

        return score

    """Determines whether to draw from the discard pile or the deck
    based on the h value of all possible hands with the card from the
    discard pile"""
    def best_draw_option(self):
        currentH = self.h(self.hand.contents)
        d = 10
        for x in range(len(self.hand.contents)):
            tempHand = self.hand.contents[:]
            tempHand[x] = self.game_state.recent_discard()
            newH = self.h(tempHand)
            if newH > currentH:
                currentH = newH
                d = x
        return d

    """Determines which card to discard based on the h value of all
    possible hands after getting rid of a card"""
    def best_discard_option(self):
        tempHand = self.hand.contents[:10]
        newCard = self.hand.contents[10]
        currentH = self.h(tempHand)
        d = 10
        for x in range(len(tempHand)):
            tempHand = self.hand.contents[:10]
            tempHand[x] = newCard
            newH = self.h(tempHand)
            if newH > currentH:
                currentH = newH
                d = x
        return d


    def play_draw(self):
        d = self.best_deck_option()
        if d == 10:
            return self.draw_deck()
        else:
            return self.draw_discard()

    def play_discard(self):
        d = self.best_deck_option()
        if d != 10:
            c = self.hand.contents[d]
            self.discard(c)
            return c

        e = self.best_discard_option()
        c = self.hand.contents[e]
        return c

    def declare_rummy(self):
        self.game_state.check_goal_state(self)
