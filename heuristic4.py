import sys, pygame
from objects import *
#import init_gui
import random

class Heuristic4(Player):
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

        maxScoreOfSets = 0
        bestSetOfSets = [] ##list of lists
        ##what about 3 sets of 3; how do you improve? how to keep track of a set of 4 in this case
        for i in range(len(sets)):
            tmp = sets[i]
            val = 0
            if len(tmp) == 3:
                val = 10
            if len(tmp) == 4:
                val = 15
            if val > maxScoreOfSets:
                maxScoreOfSets = val
                bestSetOfSets = [tmp]

        for i in range(len(sets)):
            for j in range(i+1, len(sets)):
                tmp = sets[i] + sets[j]
                count = 0
                val = 0
                for card in tmp:
                    if tmp.count(card) == 1:
                        count += 1
                if count == len(tmp):
                    if len(tmp) == 6:
                        val = 20
                    if len(tmp) == 7:
                        val = 25
                    if val > maxScoreOfSets:
                        maxScoreOfSets = val
                        bestSetOfSets = [sets[i],sets[j]]

        for i in range(len(sets)):
            for j in range(i+1, len(sets)):
                for k in range(i+2, len(sets)):
                    tmp = sets[i] + sets[j] + sets[k]
                    count = 0
                    val = 0
                    if len(tmp) != 10:
                        continue
                    for card in tmp:
                        if tmp.count(card) == 1:
                            count +=1
                    if count == 10:
                        val = 35
                        if val > maxScoreOfSets:
                            maxScoreOfSets = val
                            bestSetOfSets = [sets[i], sets[j], sets[k]]

        score += maxScoreOfSets

        for b in bestSetOfSets:
            if len(b) == 4:
                four = True

        firstlast = []
        for i in bestSetOfSets:
            if len(i) == 3:
                firstlast.append(i[0])
                firstlast.append(i[2])


        flattenedSet = []
        for i in bestSetOfSets:
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

        if not four:
            for x in range(len(tempHand)):
                for y in firstlast:
                    if tempHand[x].value == y.value:
                        score += 2
                    elif (tempHand[x].value == y.value - 1 and tempHand[x].suit == y.suit):
                        score += 2
                    elif (tempHand[x].value == y.value + 1 and tempHand[x].suit == y.suit):
                        score += 2
                    elif (tempHand[x].value == y.value - 2 and tempHand[x].suit == y.suit):
                        score += 1
                    elif (tempHand[x].value == y.value + 2 and tempHand[x].suit == y.suit):
                        score += 1

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
