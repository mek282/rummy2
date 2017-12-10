"""
    The "Strategy" AI is a combination of features of both Heuristic and
    Adversarial, attempting to simulate a more sophisticated strategy similar to
    how a human with perfect memory would play the game.

    It maintains a list of cards the other player definitely has in their hand,
    as well as a list of "undesirable cards", i.e. cards the other player
    either discarded or did not pick up from the discard pile.

    It prioritizes the strategy of [winning AI], but will consider the heuristic
    used by [other AI] when relevant.

"""
from heuristic3 import *
from objects import *

class SAStrategy(Heuristic3):
    def __init__(self, game, name):
        Heuristic3.__init__(self, game, name)
        self.opponent_hand = Deck(0)
        self.opponent_dislikes = Deck(0)
        self.deck_possibilities = Deck(0)
        self.discard = Deck(0)
        self.drew_deck = 0
        self.stuck = 0


    def adversarial_h(self, card):
        h = 0
        # add 10 points for every new run it would give the opponent
        current_matches = self.opponent_hand.find_runs()
        current_matches.extend(self.opponent_hand.find_x_of_a_kind())
        new_hand = Deck(0)
        new_hand.contents = self.opponent_hand.contents[:]
        new_hand.add(card)
        new_matches = new_hand.find_runs()
        new_matches.extend(new_hand.find_x_of_a_kind())
        h += 10*(len(new_matches) - len(current_matches))

        if h >= 10:
            return h

        # subtract 1 point if same value as a card they dislike
        # subtract 1 point if right next to a card they dislike
        for dislike in self.opponent_dislikes.contents:
            if card.value == dislike.value:
                h -= 1
            elif (card.value == dislike.value - 1 and card.suit == dislike.suit):
                h -= 1
            elif (card.value == dislike.value + 1 and card.suit == dislike.suit):
                h -= 1
        # add 2 points if same value as a card they have
        # add 2 points if right next to a card they have
        # add 1 point if 1 away from a card they have
        for like in self.opponent_hand.contents:
            if card.value == like.value:
                h += 2
            elif (card.value == like.value - 1 and card.suit == like.suit):
                h += 2
            elif (card.value == like.value + 1 and card.suit == like.suit):
                h += 2
            elif (card.value == like.value - 2 and card.suit == like.suit):
                h += 1
            elif (card.value == like.value + 2 and card.suit == like.suit):
                h += 1

        return h


    """ Updates the opponent_hand and opponent_dislikes attributes based on the
        opponent's most recent move. """
    def process_opponent_move(self):
        if self.game_state.recent_discard() in self.opponent_hand.contents:
            self.opponent_hand.contents.remove(self.game_state.recent_discard())
        self.opponent_dislikes.add(self.game_state.recent_discard())
        if self.game_state.last_draw is None:
            d = self.game_state.discard_pile.contents
            self.opponent_dislikes.add(d[len(d) - 2])
        else:
            self.opponent_hand.add(self.game_state.last_draw)


    """Determines the order in which we want to discard all cards in our hand"""
    def best_discard_option(self):
        tempHand = self.hand.contents[:10]
        newCard = self.hand.contents[10]
        currentH = self.h(tempHand)
        h_vals = []
        for x in range(len(tempHand)):
            tempHand = self.hand.contents[:10]
            tempHand[x] = newCard
            newH = self.h(tempHand)
            h_vals.append(newH)
        h_vals.append(currentH)
        return h_vals


    def play_draw(self):
        self.process_opponent_move()
        dis = self.game_state.recent_discard()
        c = Heuristic3.play_draw(self)
        self.drew_deck = (dis != c)
        return c


    def play_discard(self):
        #print("opponent hand")
        #print([(c.value, c.suit) for c in self.opponent_hand.contents])
        discard_options = self.hand.contents[:]
        my_h_vals = self.best_discard_option()
        best_ind = my_h_vals.index(max(my_h_vals))

        # can't discard if we just drew from disc pile
        if not self.drew_deck:
            del my_h_vals[10]
            del discard_options[10]
            best_ind = my_h_vals.index(max(my_h_vals))

        if my_h_vals[best_ind] == 35:
            c = discard_options[best_ind]
            Heuristic3.discard(self, c)
            return c

        if best_ind == 10:
            self.stuck += 1
        else:
            self.stuck = 0

        if self.stuck == 10:
            del my_h_vals[best_ind]
            del discard_options[best_ind]
            best_ind = my_h_vals.index(max(my_h_vals))
            self.stuck = 0

        if len(self.opponent_hand.contents) == 0:
            c = discard_options[best_ind]
            Heuristic3.discard(self, c)
            return c

        opponent_h_vals = []
        for i in range(len(discard_options)):
            opponent_h_vals.append(self.adversarial_h(discard_options[i]))

        orig_best_ind = best_ind
        orig_discard_options = discard_options[:]

        while discard_options != []:
            if my_h_vals[best_ind] == 35:
                c = discard_options[best_ind]
                Heuristic3.discard(self, c)
                return c

            if opponent_h_vals[best_ind] >= 10:
                del my_h_vals[best_ind]
                del discard_options[best_ind]
                del opponent_h_vals[best_ind]
                if len(my_h_vals) == 0:
                    best_ind = orig_best_ind
                    break
                best_ind = my_h_vals.index(max(my_h_vals))
            else:
                c = discard_options[best_ind]
                Heuristic3.discard(self,c)
                return c

        c = orig_discard_options[best_ind]
        Heuristic3.discard(self,c)
        return c
