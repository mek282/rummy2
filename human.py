"""

"""

import sys
import pygame
from objects import *
#import init_gui as ig

hand_locations = [[10, 280, 100, 150], [120, 280, 100, 150], [230, 280, 100, 150],
[340, 280, 100, 150], [450, 280, 100, 150], [10, 440, 100, 150],
[120, 440, 100, 150], [230, 440, 100, 150], [340, 440, 100, 150], [450, 440, 100, 150]]

deck_location = [230, 100, 100, 150]
discard_location = [340, 100, 100, 150]
temp_location = [560, 360, 100, 150]


class Human(Player):
    def __init__(self, game, name):
        Player.__init__(self, game, name)
        self.whichDeck = 0

    """ Returns the card the player chose to draw. """
    def play_draw(self):
        discard_card = pygame.Rect(discard_location[0], discard_location[1],
                                   discard_location[2], discard_location[3])
        deck_card = pygame.Rect(deck_location[0], deck_location[1],
                                deck_location[2], deck_location[3])
        while(True):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if discard_card.collidepoint(x, y):
                        if len(self.game_state.discard_pile.contents) == 0:
                            pass
                        else:
                            self.whichDeck = 0
                            return self.draw_discard()
                    elif deck_card.collidepoint(x, y):
                        self.whichDeck = 1
                        return self.draw_deck()
        return None


    def play_discard(self):
        cards = [pygame.Rect(c[0], c[1], c[2], c[3]) for c in hand_locations]
        cards.append(pygame.Rect(temp_location[0], temp_location[1],
                                 temp_location[2], temp_location[3]))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    for i in range(10 + self.whichDeck):
                        if cards[i].collidepoint(x, y):
                            c = self.hand.contents[i]
                            self.discard(c)
                            return c
        return None
