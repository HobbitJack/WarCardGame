import random


def generate_deck(numbers: range, cards_per_value) -> list[int]:
    deck: list[int] = []
    for card_value in numbers:
        for _ in range(cards_per_value):
            deck.append(card_value)

    return deck


def shuffle_deck(deck: list[int]) -> list[int]:
    shuffled_deck: list[int] = []
    for _ in range(len(deck)):
        shuffled_deck.append(deck[random.randrange(0, len(deck))])

    return shuffled_deck


def concat_decks(first_deck: list[int], second_deck: list[int]) -> list[int]:
    new_deck = first_deck.copy()

    for _ in range(len(second_deck)):
        new_deck.append(second_deck.pop())

    return new_deck


def draw(
    deck_1: list[int], deck_2: list[int], draw_pool: list[int]
) -> tuple[int, list[int]]:
    print("Draw!")
    draw_pool.append(deck_1.pop(0))
    draw_pool.append(deck_2.pop(0))

    if len(deck_1) == 0:
        return (1, draw_pool)
    if len(deck_2) == 0:
        return (0, draw_pool)

    for _ in range(3 if len(deck_1) >= 4 else len(deck_1) - 1):
        draw_pool.append(deck_1.pop(0))
    for _ in range(3 if len(deck_2) >= 4 else len(deck_2) - 1):
        draw_pool.append(deck_2.pop(0))

    print(f"Player 1's Card: {deck_1[0]}    Player 2's Card: {deck_2[0]}")

    if deck_1[0] > deck_2[0]:
        draw_pool.append(deck_2.pop(0))
        print(f"Player 1 wins {len(draw_pool)} cards!")
        draw_pool.append(deck_1.pop(0))
        return (0, draw_pool)
    elif deck_1[0] < deck_2[0]:
        draw_pool.append(deck_1.pop(0))
        print(f"Player 2 wins {len(draw_pool)} cards!")
        draw_pool.append(deck_2.pop(0))
        return (1, draw_pool)
    else:
        return draw(deck_1, deck_2, draw_pool)


def game_loop(deck_1: list[int], deck_2: list[int]):
    player1_winnings: list[int] = []
    player2_winnings: list[int] = []

    while len(deck_1) > 0 and len(deck_2) > 0:
        print(f"Player 1's Card: {deck_1[0]}    Player 2's Card:{deck_2[0]}")

        if deck_1[0] > deck_2[0]:
            print("To Player 1!")
            player1_winnings.append(deck_2.pop(0))
            player1_winnings.append(deck_1.pop(0))
        elif deck_1[0] < deck_2[0]:
            print("To Player 2!")
            player2_winnings.append(deck_1.pop(0))
            player2_winnings.append(deck_2.pop(0))
        else:
            if (draw_results := draw(deck_1, deck_2, []))[0] == 0:
                player1_winnings = concat_decks(player1_winnings, draw_results[1])
            else:
                player2_winnings = concat_decks(player2_winnings, draw_results[1])

        deck_1 = concat_decks(deck_1, player1_winnings)
        deck_2 = concat_decks(deck_2, player2_winnings)

    if len(deck_1) == 0:
        print("Player 2 wins the game!")
        return 1

    if len(deck_2) == 0:
        print("Player 1 wins the game!")
        return 2

    return 0


if __name__ == "__main__":
    game_deck = generate_deck(range(2, 15), 4)
    game_deck = shuffle_deck(game_deck)
    if len(game_deck) % 2 == 0:
        player1_deck = game_deck[0 : len(game_deck) // 2 - 1]
        player2_deck = game_deck[len(game_deck) // 2 : -1]
    else:
        player1_deck = game_deck[0 : len(game_deck) // 2 - 1]
        player2_deck = game_deck[len(game_deck) // 2 : -1]

    won_yet = 0
    while won_yet == 0:
        won_yet = game_loop(player1_deck, player2_deck)
