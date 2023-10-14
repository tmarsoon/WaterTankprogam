import random

# Define global constants
MIN_FILL_VALUE = 75
MAX_FILL_VALUE = 80

# Define global variables to represent player tanks
human_tank = 0
computer_tank = 0

# Define global variables to represent player hands
human_cards = []
computer_cards = []

# Define global variables to represent card piles
water_cards_pile = []
power_cards_pile = []


def get_user_input(question):
    while True:
        user_input = input(question).strip()
        if len(user_input) == 0:
            continue
        elif user_input.isdigit():
            return int(user_input)
        elif user_input.upper() in ["SOH", "DOT", "DMT"]:
            return user_input.upper()
        else:
            return user_input.lower()


def setup_water_cards():
    water_cards = [1] * 30 + [5] * 15 + [10] * 8
    random.shuffle(water_cards)
    return water_cards


def setup_power_cards():
    power_cards = ["SOH"] * 10 + ["DOT"] * 2 + ["DMT"] * 3
    random.shuffle(power_cards)
    return power_cards


def setup_cards():
    water_cards_pile = setup_water_cards()
    power_cards_pile = setup_power_cards()
    return water_cards_pile, power_cards_pile


def get_card_from_pile(pile, index):
    card = pile.pop(index)
    return card


def arrange_cards(cards_list):
    water_cards = [card for card in cards_list if isinstance(card, int)]
    power_cards = [card for card in cards_list if isinstance(card, str)]
    water_cards.sort()
    power_cards.sort()
    cards_list[:] = water_cards + power_cards


def deal_cards(water_cards_pile, power_cards_pile):
    player_1_cards = []
    player_2_cards = []

    for _ in range(3):
        player_1_cards.append(get_card_from_pile(water_cards_pile, 0))
        player_2_cards.append(get_card_from_pile(water_cards_pile, 0))
    for _ in range(2):
        player_1_cards.append(get_card_from_pile(power_cards_pile, 0))
        player_2_cards.append(get_card_from_pile(power_cards_pile, 0))

    arrange_cards(player_1_cards)
    arrange_cards(player_2_cards)

    return player_1_cards, player_2_cards


def apply_overflow(tank_level):
    if tank_level > MAX_FILL_VALUE:
        overflow = tank_level - MAX_FILL_VALUE
        tank_level = MAX_FILL_VALUE - overflow
    return tank_level


def use_card(player_tank, card_to_use, player_cards, opponent_tank):
    if isinstance(card_to_use, int):
        player_tank += card_to_use
    elif card_to_use == "SOH":
        amount_stolen = opponent_tank // 2
        opponent_tank -= amount_stolen
        player_tank += amount_stolen
    elif card_to_use == "DOT":
        opponent_tank = 0
    elif card_to_use == "DMT":
        player_tank *= 2

    player_tank = apply_overflow(player_tank)
    player_cards.remove(card_to_use)
    return player_tank, opponent_tank


def discard_card(card_to_discard, player_cards, water_cards_pile, power_cards_pile):
    player_cards.remove(card_to_discard)
    if isinstance(card_to_discard, int):
        water_cards_pile.append(card_to_discard)
    elif isinstance(card_to_discard, str):
        power_cards_pile.append(card_to_discard)


def filled_tank(tank):
    return MIN_FILL_VALUE <= tank <= MAX_FILL_VALUE


def check_pile(pile, pile_type):
    if len(pile) == 0:
        if pile_type == "water":
            pile.extend(setup_water_cards())
        elif pile_type == "power":
            pile.extend(setup_power_cards())


def human_play(human_tank, human_cards, water_cards_pile, power_cards_pile, computer_tank):
    print("Human's Turn")
    print(f"Human Tank: {human_tank}")
    print(f"Computer Tank: {computer_tank}")
    print(f"Your Hand: {human_cards}")
    while True:
        action = get_user_input("Do you want to use or discard a card? ").lower()
        if action == "use":
            card_to_use = get_user_input("Enter the card you want to use: ")
            if card_to_use in human_cards:
                human_tank, computer_tank = use_card(human_tank, card_to_use, human_cards, computer_tank)
                print(f"Used {card_to_use}")
                break
            else:
                print("Invalid card. Try again.")
        elif action == "discard":
            card_to_discard = get_user_input("Enter the card you want to discard: ")
            if card_to_discard in human_cards:
                discard_card(card_to_discard, human_cards, water_cards_pile, power_cards_pile)
                print(f"Discarded {card_to_discard}")
                break
            else:
                print("Invalid card. Try again.")
        else:
            print("Invalid action. Enter 'use' or 'discard'.")

    # Draw a new card of the same type
    if isinstance(card_to_use, int):
        human_cards.append(get_card_from_pile(water_cards_pile, 0))
    elif isinstance(card_to_use, str):
        human_cards.append(get_card_from_pile(power_cards_pile, 0))
    arrange_cards(human_cards)

    return human_tank, computer_tank


def computer_play(computer_tank, computer_cards, water_cards_pile, power_cards_pile, human_tank):
    print("Computer's Turn")
    print(f"Computer Tank: {computer_tank}")
    print(f"Your Tank: {human_tank}")

    # Implement the computer's strategy here

    # Draw a new card of the same type
    card_to_use_or_discard = random.choice(computer_cards)
    if isinstance(card_to_use_or_discard, int):
        computer_cards.append(get_card_from_pile(water_cards_pile, 0))
    elif isinstance(card_to_use_or_discard, str):
        computer_cards.append(get_card_from_pile(power_cards_pile, 0))
    arrange_cards(computer_cards)

    return computer_tank, human_tank


def main():
    print("Welcome to the Water Tank card game!")

    # Set up card piles
    water_cards_pile, power_cards_pile = setup_cards()

    # Randomly choose the starting player
    starting_player = random.choice(["human", "computer"])
    if starting_player == "human":
        print("You are the starting player!")
    else:
        print("Computer is the starting player!")

    # Deal cards to players
    human_cards, computer_cards = deal_cards(water_cards_pile, power_cards_pile)

    while True:
        if starting_player == "human":
            human_tank, computer_tank = human_play(human_tank, human_cards, water_cards_pile, power_cards_pile,
                                                   computer_tank)
            if filled_tank(human_tank):
                print("Congratulations! You filled your tank and won the game!")
                break
            computer_tank, human_tank = computer_play(computer_tank, computer_cards, water_cards_pile, power_cards_pile,
                                                      human_tank)
            if filled_tank(computer_tank):
                print("Computer filled its tank and won the game. Better luck next time!")
                break
        else:
            computer_tank, human_tank = computer_play(computer_tank, computer_cards, water_cards_pile, power_cards_pile,human_tank)
            if filled_tank(computer_tank):
                print("Computer filled its tank and won the game. Better luck next time!")
                break
            human_tank, computer_tank = human_play(human_tank, human_cards, water_cards_pile, power_cards_pile,
                                                   computer_tank)
            if filled_tank(human_tank):
                print("Congratulations! You filled your tank and won the game!")
                break


if __name__ == '__main__':
    main()