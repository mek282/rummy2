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
