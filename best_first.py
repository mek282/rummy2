from objects import *
import copy

def heu(hand):
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


class Node():
    def __init__(self, deck, deck_poss):
        self.cards = deck
        self.parent = None
        self.children = []
        self.deck_possibilities = deck_poss
        self.value = self.h(self.cards)


    def add_child(self, deck):
        new_possibilities = Deck(0)
        new_possibilities.contents = self.deck_possibilities.contents[:]
        for card in deck.contents:
            if card in new_possibilities.contents:
                new_possibilities.contents.remove(card)

        child = Node(deck, new_possibilities)
        child.parent = self

        self.children.append(child)

    def h(self, deck):
        if len(deck.contents) == 10:
            return heu(deck.contents)
        else:
            deck_len = len(self.deck_possibilities.contents)
            acc = 0.0
            for d in range(deck_len):
                acc += heu(deck.contents + [self.deck_possibilities.contents[d]])
            return acc / deck_len


class Best_First(Player):
    def __init__(self, game, name):
        Player.__init__(self, game, name)
        self.tree = Node(self.hand, None)
        self.frontier = []
        self.opponent_hand = Deck(0)
        self.best_hand = None


    def process_opponent_move(self):
        if self.game_state.recent_discard() in self.opponent_hand.contents:
            self.opponent_hand.contents.remove(self.game_state.recent_discard())
        if self.game_state.last_draw is not None:
            self.opponent_hand.add(self.game_state.last_draw)


    def populate_tree(self, parent):
        # add all possibilities after drawing discard
        c = self.game_state.recent_discard()
        for i in range(10):
            hand = copy.deepcopy(self.hand)
            hand.contents[i] = c
            parent.add_child(hand)
        # add all possibilities after drawing draw
        for i in range(10):
            hand = copy.deepcopy(self.hand)
            hand.contents.remove(hand.contents[i])
            parent.add_child(hand)


    def play_draw(self):
        self.process_opponent_move()

        # create list of cards that may be in the deck
        deck_possibilities = Deck(0)
        deck_possibilities.contents = self.game_state.deck.contents[:]
        deck_possibilities.contents.extend(self.game_state.player1.hand.contents[:])
        deck_possibilities.contents.extend(self.game_state.player2.hand.contents[:])
        for c in self.hand.contents:
            deck_possibilities.contents.remove(c)
        for c in self.opponent_hand.contents:
            deck_possibilities.contents.remove(c)

        self.tree = Node(self.hand, deck_possibilities)

        #find out who to expand
        self.populate_tree(self.tree)
        for c in self.tree.children:
            # expand all children who increase hand value
            if c.value > self.tree.value:
                self.populate_tree(c)
        # find the max value in the second layer
        max_val = 0
        parent = None
        for c in self.tree.children:
            if c.children != []:
                for ch in c.children:
                    if ch.value > max_val:
                        parent = c
                        max_val = ch.value
        if parent is None:
            return self.draw_deck()
        elif len(parent.cards.contents) == 9:
            return self.draw_deck()
        else:
            self.best_hand = parent.cards.contents # keep track of the hand you want so you know what to discard
            return self.draw_discard()


    def play_discard(self):
        # we already know what to discard if we drew from the discard pile
        if self.best_hand is not None:
            for i in range(10):
                if self.hand.contents[i] not in self.best_hand:
                    self.best_hand = None
                    c = self.hand.contents[i]
                    self.discard(c)
                    return c
        else:
            best_discard = None
            best_val = 0
            for i in range(10):
                hand = self.hand.contents[:10]
                hand[i] = self.hand.contents[10]
                v = heu(hand)
                if v > best_val:
                    best_val = v
                    best_discard = self.hand.contents[i]
            self.discard(best_discard)
            return best_discard
