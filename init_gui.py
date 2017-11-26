"""
Main file: runs the game loop and updates the display
TODO:
- display player 1's hand, the discard pile, the top of the deck, possibly
player 2's (face down) hand, and a text window
- update the text window to prompt the human player during their turn
- update the discard pile and deck
- animations???
"""

import sys, pygame
from objects import *
from control import *
from gametree import *
from heuristic import *
from strategy import *
from human import *

# constant values
WHITE = (255, 255, 255)
GREEN = (62, 145, 62)
BLACK = (0, 0, 0)

hand_locations = [[10, 280, 100, 150], [120, 280, 100, 150], [230, 280, 100, 150],
[340, 280, 100, 150], [450, 280, 100, 150], [10, 440, 100, 150],
[120, 440, 100, 150], [230, 440, 100, 150], [340, 440, 100, 150], [450, 440, 100, 150]]

deck_location = [175, 100, 100, 150]
discard_location = [285, 100, 100, 150]
temp_location = [395, 100, 100, 150]

def render_card(suit, value, suit_imgs, val_imgs, bg):
    start_ind = 0
    if suit == "Hearts":
        start_ind += 13
        bg.blit(suit_imgs[0], (0,0))
    if suit == "Diamonds":
        start_ind += 13
        bg.blit(suit_imgs[1], (0,0))
    if suit == "Spades":
        bg.blit(suit_imgs[2], (0,0))
    if suit == "Clubs":
        bg.blit(suit_imgs[3], (0,0))
    bg.blit(val_imgs[start_ind + value - 1], (50, 100))


def render_p1_hand(hand, suit_imgs, val_imgs, cards):
    for r in range(10):
        render_card(hand.contents[r].suit, hand.contents[r].value,
                    suit_imgs, val_imgs, cards[r])


def update_display(screen, background, p1_cards, discard_card, suit_imgs,
                    val_imgs, game, font, msg, player1):
    screen.blit(background, (0,0))

    for c in range(10):
        background.blit(p1_cards[c], (hand_locations[c][0], hand_locations[c][1]))
    pygame.draw.rect(screen, BLACK, deck_location, 0)
    background.blit(discard_card, (discard_location[0], discard_location[1]))

    render_p1_hand(player1.hand, suit_imgs, val_imgs, p1_cards)
    if len(game.discard_pile.contents) > 0:
        top_of_discard = game.discard_pile.contents[len(game.discard_pile.contents) - 1]
        render_card(top_of_discard.suit, top_of_discard.value,
                    suit_imgs, val_imgs, discard_card)
    else:
        discard_card.fill((150, 150, 150))
    text = font.render(msg, 1, (10, 10, 10))
    textpos = text.get_rect(centerx=background.get_width()/2, centery=50)
    background.blit(text, textpos)
    pygame.display.flip()


def main():
    """ main game loop - initializes screen and updates"""
    # game initialization
    deck = Deck()
    game = Game(deck)

    player1 = Human(game, "test")
    game.player1 = player1
    game.turn = player1
    player2 = Player(game, "test2")
    game.player2 = player2

    # GUI initialization
    pygame.init()
    size = width, height = 560, 600
    screen = pygame.display.set_mode(size)

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(GREEN)

    clock = pygame.time.Clock()

    msg = "Let's play Rummy!"
    font = pygame.font.Font(None, 36)

    c1 = pygame.Surface((100,150)).convert()
    c2 = pygame.Surface((100,150)).convert()
    c3 = pygame.Surface((100,150)).convert()
    c4 = pygame.Surface((100,150)).convert()
    c5 = pygame.Surface((100,150)).convert()
    c6 = pygame.Surface((100,150)).convert()
    c7 = pygame.Surface((100,150)).convert()
    c8 = pygame.Surface((100,150)).convert()
    c9 = pygame.Surface((100,150)).convert()
    c10 = pygame.Surface((100,150)).convert()
    p1_cards = [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10]

    discard_card = pygame.Surface((100,150)).convert()
    discard_card.fill(WHITE)
    tmp = pygame.Surface((100,150)).convert()
    tmp.fill(WHITE)
    pygame.draw.rect(screen, BLACK, deck_location, 0)

    for c in range(10):
        p1_cards[c].fill(WHITE)
        background.blit(p1_cards[c], (hand_locations[c][0], hand_locations[c][1]))

    suit_imgs = [pygame.image.load("img/heart.png").convert(),
    pygame.image.load("img/diamond.png").convert(),
    pygame.image.load("img/spade.png").convert(),
    pygame.image.load("img/club.png").convert()]

    for i in range(4):
        suit_imgs[i] = pygame.transform.scale(suit_imgs[i], (50, 50))

    val_imgs = [pygame.image.load("img/ba.png").convert(),
    pygame.image.load("img/b2.png").convert(),
    pygame.image.load("img/b3.png").convert(),
    pygame.image.load("img/b4.png").convert(),
    pygame.image.load("img/b5.png").convert(),
    pygame.image.load("img/b6.png").convert(),
    pygame.image.load("img/b7.png").convert(),
    pygame.image.load("img/b8.png").convert(),
    pygame.image.load("img/b9.png").convert(),
    pygame.image.load("img/b10.png").convert(),
    pygame.image.load("img/bj.png").convert(),
    pygame.image.load("img/bq.png").convert(),
    pygame.image.load("img/bk.png").convert(),
    pygame.image.load("img/ra.png").convert(),
    pygame.image.load("img/r2.png").convert(),
    pygame.image.load("img/r3.png").convert(),
    pygame.image.load("img/r4.png").convert(),
    pygame.image.load("img/r5.png").convert(),
    pygame.image.load("img/r6.png").convert(),
    pygame.image.load("img/r7.png").convert(),
    pygame.image.load("img/r8.png").convert(),
    pygame.image.load("img/r9.png").convert(),
    pygame.image.load("img/r10.png").convert(),
    pygame.image.load("img/rj.png").convert(),
    pygame.image.load("img/rq.png").convert(),
    pygame.image.load("img/rk.png").convert()]

    for i in range(26):
        val_imgs[i] = pygame.transform.scale(val_imgs[i], (50, 50))

    update_display(screen, background, p1_cards, discard_card, suit_imgs,
    val_imgs, game, font, msg, player1)
    playing = True

    # *********************** MAIN GAME LOOP **********************************
    while playing:

        update_display(screen, background, p1_cards, discard_card, suit_imgs,
        val_imgs, game, font, msg, player1)
        clock.tick(60)

        # execute player 1's turn
        if game.turn == game.player1:
            c = game.player1.play_draw()
            tmp.fill(WHITE)
            background.blit(tmp, (temp_location[0], temp_location[1]))
            render_card(c.suit, c.value, suit_imgs, val_imgs, tmp)
            update_display(screen, background, p1_cards, discard_card, suit_imgs,
                            val_imgs, game, font, msg, player1)
            clock.tick(1)

            game.player1.play_discard()
            tmp.fill(GREEN)
            update_display(screen, background, p1_cards, discard_card, suit_imgs,
                            val_imgs, game, font, msg, player1)
            clock.tick(1)
            #At the end of a play, each player has the opportunity to say rummy.
            #If they say rummy, and they don't have one, the other player gets to
            #see their hand. If they do have a rummy, they win and the game ends.
            #We need to implement a function to check if a player has a rummy.
            if(game.check_goal_state(player1) is not None):
                msg = "You win!"
                playing = False
            else:
                game.turn = game.player2
        # execute player 2's turn
        elif game.turn == game.player2:
            #game.player2.play_draw()
            #game.player2.play_discard()TODO - uncomment once implemented
            if(game.check_goal_state(player2) is not None):
                msg = "You lose! Player 2 has Rummy!"
                playing = False
            else:
                game.turn = game.player1

        # process new events - only on human's turn???
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                playing = False

        # update display!
        #update_display(screen, background, p1_cards, discard_card, suit_imgs,
        #            val_imgs, game, font, msg, player1)

    pygame.quit()
