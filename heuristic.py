import sys, pygame
from objects import *
#import init_gui
import random

class Heuristic(Player):
    def __init__(self, game, name):
        Player.__init__(self, game, name)
        self.d = 10

    """Calculates the value of the hand"""
    def h(self, hand):
        score = 0
        handDeck = Deck(0)
        handDeck.contents.extend(hand)
        sets = handDeck.find_runs()
        xOfAKind = handDeck.find_x_of_a_kind()
        sets.extend(xOfAKind)
        four = False
        for s in sets:
            if (len(s) > 3 and four == False):
                four = True
                score += 15
            else:
                score += 10

        flattenedSet = []
        for i in sets:
            for j in i:
                flattenedSet.append(j)

        tempHand = []
        for x in hand:
            if x not in flattenedSet:
                tempHand.append(x)

        for x in range(len(tempHand)):
            for y in range(x+1,len(tempHand)):
                if tempHand[x].value == tempHand[y].value:
                    score += 2
                elif (tempHand[x].value == tempHand[y].value - 1 and tempHand[x].suit == tempHand[y].suit):
                    score += 2
                elif (tempHand[x].value == tempHand[y].value + 1 and tempHand[x].suit == tempHand[y].suit):
                    score += 2
                elif (tempHand[x].value == tempHand[y].value - 2 and tempHand[x].suit == tempHand[y].suit):
                    score += 1
                elif (tempHand[x].value == tempHand[y].value + 2 and tempHand[x].suit == tempHand[y].suit):
                    score += 1
        ###haven't done if four = False. Don't know if it makes sense to include
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
        self.d = self.best_draw_option()
        if self.d == 10:
            return self.draw_deck()
        else:
            return self.draw_discard()

    def play_discard(self):
        if self.d != 10:
            c = self.hand.contents[self.d]
            self.discard(c)
            return c

        e = self.best_discard_option()
        c = self.hand.contents[e]
        self.discard(c)
        return c

    def declare_rummy(self):
        self.game_state.check_goal_state(self)
