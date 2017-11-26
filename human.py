"""

"""

import sys
import pygame
from objects import *
#import init_gui as ig

hand_locations = [[10, 280, 100, 150], [120, 280, 100, 150], [230, 280, 100, 150],
[340, 280, 100, 150], [450, 280, 100, 150], [10, 440, 100, 150],
[120, 440, 100, 150], [230, 440, 100, 150], [340, 440, 100, 150], [450, 440, 100, 150]]

deck_location = [175, 100, 100, 150]
discard_location = [285, 100, 100, 150]
temp_location = [395, 100, 100, 150]


class Human(Player):
    def __init__(self, game, name):
        Player.__init__(self, game, name)

    """ Returns the card the player chose to draw. """
    def play_draw(self):
        discard_card = pygame.Rect(discard_location[0], discard_location[1],
                                   discard_location[2], discard_location[3])
        deck_card = pygame.Rect(deck_location[0], deck_location[1],
                                deck_location[2], deck_location[3])
        while(True):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    playing = False
                    return
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    playing = False
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if discard_card.collidepoint(x, y):
                        if len(self.game_state.discard_pile.contents) == 0:
                            pass
                        else:
                            return self.draw_discard()
                    elif deck_card.collidepoint(x, y):
                        return self.draw_deck()
        return


    def play_discard(self):
        cards = [pygame.Rect(c[0], c[1], c[2], c[3]) for c in hand_locations]
        cards.append(pygame.Rect(temp_location[0], temp_location[1],
                                 temp_location[2], temp_location[3]))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    playing = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    playing = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    for i in range(11):
                        if cards[i].collidepoint(x, y):
                            c = self.hand.contents[i]
                            self.discard(c)
                            return c
        return None
