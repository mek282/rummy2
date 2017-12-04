from objects import *
import copy

def heu(hand):
    score = 0
    handDeck = Deck(0)
    handDeck.contents.extend(hand)
    sets = handDeck.find_runs()
    xOfAKind = handDeck.find_x_of_a_kind()
    sets.extend(xOfAKind)

    maxScoreOfSets = 0
    bestSetOfSets = [] ##list of lists

    for i in range(len(sets)):
        tmp = sets[i]
        count = 0
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
                tmp = sets[i] + sets[j] + sets[k] ##what if length of sets not at least 3? problem?
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
                new_possibilities.contents.remove(card) #TODO - think about this

        child = Node(deck, new_possibilities)
        #print(child.value)
        child.parent = self
        self.children.append(child)


    def h(self, deck):
        if len(deck.contents) == 10:
            return heu(deck.contents)
        elif len(deck.contents) == 9:
            deck_len = len(self.deck_possibilities.contents)
            acc = 0.0
            for d in range(deck_len):
                acc += heu(deck.contents + [self.deck_possibilities.contents[d]])
            return acc / deck_len
        else:
            deck_len = len(self.deck_possibilities.contents)
            acc = 0.0
            count = 0
            for d in range(deck_len):
                for e in range(d+1, deck_len):
                    count += 1
                    acc += heu(deck.contents + [self.deck_possibilities.contents[d]]
                        + [self.deck_possibilities.contents[e]])
            return acc / count


class Best_First(Player):
    def __init__(self, game, name):
        Player.__init__(self, game, name)
        self.tree = Node(self.hand, None)
        #self.frontier = []
        self.opponent_hand = Deck(0)
        self.best_hand = None


    def process_opponent_move(self):
        if self.game_state.recent_discard() in self.opponent_hand.contents:
            self.opponent_hand.contents.remove(self.game_state.recent_discard())
        if self.game_state.last_draw is not None:
            self.opponent_hand.add(self.game_state.last_draw)


    def populate_tree(self, parent, layer):
        # add all possibilities after drawing discard
        if layer == 1:
            #print("Layer 1 Nodes")
            c = self.game_state.recent_discard()
            for i in range(10):
                hand = copy.deepcopy(parent.cards)
                hand.contents[i] = c
                parent.add_child(hand)
            # add all possibilities after drawing deck
            for i in range(10):
                hand = copy.deepcopy(parent.cards)
                hand.contents.remove(hand.contents[i])
                parent.add_child(hand)
        else:
            #print("Layer 2 Nodes")
            for i in range(len(parent.cards.contents)):
                hand = copy.deepcopy(parent.cards)
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
        #print("Current hand: " + str(self.tree.value))
        #find out who to expand
        self.populate_tree(self.tree, 1) # TODO - add a check if we've won before expanding
        for c in self.tree.children:
            # expand all children who increase hand value
            if c.value > self.tree.value:
                self.populate_tree(c, 2)
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
