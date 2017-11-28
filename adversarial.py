"""
    The "Adversarial" AI will try to minimize its opponent's potential to achieve
    Rummy, without thinking about trying to win itself.

    It will track which cards are in the discard pile, which cards it knows
    to be in the opponent's hand, and which cards it knows the opponent has
    discarded (recently).

    It will discard cards that are unlikely to be similar to its opponent's hand,
    and it will always draw from the deck (rather than picking up the last
    card discarded by the opponent), to maximize the potential that it will
    draw a card its opponent needed.
"""

from objects import *

class Adversarial(Player):
    def __init__(self, game, name):
        Player.__init__(self, game, name)
        self.opponent_hand = Deck(0)
        self.opponent_dislikes = Deck(0)

    """ Returns a score for card, indicating how valuable it may be to the
        opponent. A card with a high similarity to the opponent's 'disliked'
        cards as well as a low similarity to the cards known to be in the
        opponent's hand will have a low score. Similarly, a card that is
        dissimilar to the opponent's disliked cards and similar to the
        opponent's hand will have a high score. """
    def h(self, card):
        h = 0
        # add 10 points for every new run it would give the opponent
        current_matches = self.opponent_hand.find_runs()
        current_matches.extend(self.opponent_hand.find_x_of_a_kind())
        new_hand = Deck(0)
        new_hand.contents = self.opponent_hand.contents[:]
        new_hand.add(card)
        new_matches = new_hand.find_runs()
        new_matches.extend(new_hand.find_x_of_a_kind())
        h += (len(new_matches) - len(current_matches))

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

    def play_draw(self):
        self.process_opponent_move()
        return self.draw_deck()

    def play_discard(self):
        h_vals = []
        for i in range(11):
            h_vals.append(self.h(self.hand.contents[i]))
        ind = h_vals.index(min(h_vals))
        c = self.hand.contents[ind]
        self.discard(c)
        return c
