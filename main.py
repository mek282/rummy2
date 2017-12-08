"""
Main file: runs the game loop and updates the display
TODO:
- update text to be larger and display on multiple lines
- replace numbers with letters for ace and royals
- figure out why I need to call update so many times and fix it
- disallow drawing from discard and immediately discarding
- fix display when discard pile is empty
- display for a little before exiting upon win
"""

import sys, pygame
from objects import *
from control import *
from adversarial import *
from heuristic import *
from heuristic2 import *
from heuristic3 import *
from heuristic4 import *
from sa import *
from sa1 import *
from sa2 import *
from sa3 import *
from sa4 import *
from sa5 import *
from strategy import *
from sastrategy import *
from sastrategy1 import *
from human import *
from best_first import *

# constant values
WHITE = (255, 255, 255)
GREEN = (62, 145, 62)
BLACK = (0, 0, 0)

hand_locations = [[10, 280, 100, 150], [120, 280, 100, 150], [230, 280, 100, 150],
[340, 280, 100, 150], [450, 280, 100, 150], [10, 440, 100, 150],
[120, 440, 100, 150], [230, 440, 100, 150], [340, 440, 100, 150], [450, 440, 100, 150]]

deck_location = [230, 100, 100, 150]
discard_location = [340, 100, 100, 150]
temp_location = [560, 360, 100, 150]

def display_value(val):
    if val == 1:
        return "Ace"
    elif val == 11:
        return "Jack"
    elif val == 12:
        return "Queen"
    elif val == 13:
        return "King"
    else:
        return str(val)


def render_card(suit, value, suit_imgs, val_imgs, bg):
    start_ind = 0
    if suit is None:
        bg.blit(suit_imgs[4], (0,0))
        bg.blit(suit_imgs[4], (50,100))
        return
    elif suit == "Hearts":
        start_ind += 13
        bg.blit(suit_imgs[0], (0,0))
    elif suit == "Diamonds":
        start_ind += 13
        bg.blit(suit_imgs[1], (0,0))
    elif suit == "Spades":
        bg.blit(suit_imgs[2], (0,0))
    elif suit == "Clubs":
        bg.blit(suit_imgs[3], (0,0))
    bg.blit(val_imgs[start_ind + value - 1], (50, 100))


def render_p1_hand(hand, suit_imgs, val_imgs, cards):
    for r in range(10):
        render_card(hand.contents[r].suit, hand.contents[r].value,
                    suit_imgs, val_imgs, cards[r])


def update_display(screen, background, p1_cards, discard_card, suit_imgs,
                    val_imgs, game, font, msg, player1, tmp, tmp_card):
    # draw background
    screen.blit(background, (0,0))

    # draw card spaces
    for c in range(10):
        background.blit(p1_cards[c], (hand_locations[c][0], hand_locations[c][1]))
    pygame.draw.rect(screen, BLACK, deck_location, 0)
    background.blit(discard_card, (discard_location[0], discard_location[1]))

    # draw card images
    render_p1_hand(player1.hand, suit_imgs, val_imgs, p1_cards)
    if len(game.discard_pile.contents) > 0:
        top_of_discard = game.discard_pile.contents[len(game.discard_pile.contents) - 1]
        render_card(top_of_discard.suit, top_of_discard.value,
                    suit_imgs, val_imgs, discard_card)
    else:
        render_card(None, None,
                    suit_imgs, val_imgs, discard_card)

    #draw temp card
    background.blit(tmp, (temp_location[0], temp_location[1]))

    if tmp_card is not None:
        render_card(tmp_card.suit, tmp_card.value, suit_imgs, val_imgs, tmp)
    else:
        tmp.fill(WHITE)

    # write message
    text = font.render(msg, 1, (10, 10, 10))
    textpos = text.get_rect(centerx=background.get_width()/2, centery=50)
    background.fill(GREEN, (0, 0, 670, 100))
    background.blit(text, textpos)

    # update all
    pygame.display.flip()


def main():
    """ main game loop - initializes screen and updates"""
    # game initialization
    deck = Deck()
    game = Game(deck)

    player1 = SAStrategy(game, "test")
    game.player1 = player1
    game.turn = player1
    player2 = Adversarial(game, "test2")
    game.player2 = player2

    # GUI initialization
    pygame.init()
    size = width, height = 670, 600
    screen = pygame.display.set_mode(size)

    background = pygame.Surface(screen.get_size()).convert()
    background.fill(GREEN)

    clock = pygame.time.Clock()

    discard_card = pygame.Surface((100,150)).convert()
    discard_card.fill(WHITE)
    tmp = pygame.Surface((100,150)).convert()
    tmp.fill(WHITE)

    msg = "Your turn! Select a card to draw."
    font = pygame.font.Font(None, 22)

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

    for c in range(10):
        p1_cards[c].fill(WHITE)
        #background.blit(p1_cards[c], (hand_locations[c][0], hand_locations[c][1]))

    suit_imgs = [pygame.image.load("img/heart.png").convert(),
    pygame.image.load("img/diamond.png").convert(),
    pygame.image.load("img/spade.png").convert(),
    pygame.image.load("img/club.png").convert(),
    pygame.image.load("img/blank.png").convert()]

    for i in range(5):
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
    val_imgs, game, font, msg, player1, tmp, None)
    update_display(screen, background, p1_cards, discard_card, suit_imgs,
    val_imgs, game, font, msg, player1, tmp, None) # why does this fix things??? is there a better way??

    playing = True
    turns = 0
    # *********************** MAIN GAME LOOP **********************************
    while playing:
        clock.tick(60)
        turns += 1
        #print([(c.value, c.suit) for c in player1.hand.contents])

        update_display(screen, background, p1_cards, discard_card, suit_imgs,
        val_imgs, game, font, msg, player1, tmp, None)
        update_display(screen, background, p1_cards, discard_card, suit_imgs,
        val_imgs, game, font, msg, player1, tmp, None)

        # execute player 1's turn
        if game.turn == game.player1:
            print("Time to draw")
            c = game.player1.play_draw()
            print("Player 1 drew:")
            print(c.suit)
            print(c.value)
            if c is None:
                pygame.quit()
            msg = "Select a card to discard."
            update_display(screen, background, p1_cards, discard_card, suit_imgs,
                            val_imgs, game, font, msg, player1, tmp, c)
            update_display(screen, background, p1_cards, discard_card, suit_imgs,
                            val_imgs, game, font, msg, player1, tmp, c)
            update_display(screen, background, p1_cards, discard_card, suit_imgs,
                            val_imgs, game, font, msg, player1, tmp, c)
            print("Time to discard")
            c = game.player1.play_discard()
            print("Player 1 discarded:")
            print(c.suit)
            print(c.value)
            if c is None:
                pygame.quit()
            update_display(screen, background, p1_cards, discard_card, suit_imgs,
                            val_imgs, game, font, msg, player1, tmp, None)
            update_display(screen, background, p1_cards, discard_card, suit_imgs,
                            val_imgs, game, font, msg, player1, tmp, None)

            #At the end of a play, each player has the opportunity to say rummy.
            #If they say rummy, and they don't have one, the other player gets to
            #see their hand. If they do have a rummy, they win and the game ends.
            #We need to implement a function to check if a player has a rummy.
            matches = game.check_goal_state(player1)
            if(matches is not None):
                msg = "You win!"
                playing = False
                print("YOU WIN!")
                print(turns)
                print([(c.value, c.suit) for c in player1.hand.contents])
                print([(c.value, c.suit) for c in matches])
                update_display(screen, background, p1_cards, discard_card, suit_imgs,
                                val_imgs, game, font, msg, player1, tmp, None)
                return ("player1", turns)
            else:
                game.turn = game.player2
        # execute player 2's turn
        elif game.turn == game.player2:
            print("AI's turn. AI Hand:")
            print([(c.value, c.suit) for c in player2.hand.contents])
            d = game.recent_discard()
            c_draw = game.player2.play_draw()
            print("AI drew:")
            print(c_draw.suit)
            print(c_draw.value)
            c_disc = game.player2.play_discard()
            print("AI discarded:")
            print(c_disc.suit)
            print(c_disc.value)
            if d == c_draw:
                msg = ("P2 drew " + display_value(c_draw.value) + " of " + c_draw.suit
                + " from the discard pile, and discarded " + display_value(c_disc.value) +
                " of " + c_disc.suit + ".")
            else:
                msg = ("P2 drew from the deck, and discarded "
                + display_value(c_disc.value) + " of " + c_disc.suit + ".")
            update_display(screen, background, p1_cards, discard_card, suit_imgs,
                            val_imgs, game, font, msg, player1, tmp, None)
            print([(c.value, c.suit) for c in player2.hand.contents])
            matches = game.check_goal_state(player2)
            if(matches is not None):
                msg = "You lose! Player 2 has Rummy!"
                playing = False
                print("YOU LOSE!")
                print(turns)
                print([(c.value, c.suit) for c in player2.hand.contents])
                print([(c.value, c.suit) for c in matches])
                update_display(screen, background, p1_cards, discard_card, suit_imgs,
                                val_imgs, game, font, msg, player1, tmp, None)
                return ("player2", turns)
            else:
                game.turn = game.player1

        # TODO: make the quit screen loop once someone wins
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                playing = False


#main()
    #pygame.quit()
