"""Main game mechanics module."""
from random import sample
from constants import COMBINATIONS, CARDS_ON_TABLE, CARDS_ON_HAND, ALL_CARDS, START_BALANCE
from combinations import count_combination


class Player:
    """Class Player is abstract class for subclasses HumanPlayer and ComputerPlayer."""

    def __init__(self, name):
        self.name = name
        self.balance = START_BALANCE
        self.bid = 0
        self.cards = None
        self.fold = False
        self.raise_bid = False
        self.first_bid_of_round = True

    def exit_from_game(self):
        """Exit game and free place for another players."""
        pass

    def turn(self, opponent_bid):
        """Player input."""
        pass

    def my_combination(self, table_cards):
        """Return combinations."""
        self.my_combination_tuple = count_combination(self.cards + table_cards)
        self.create_my_combination_str()
        return self.my_combination_tuple

    def create_my_combination_str(self):
        """Make a pretty string with combinations."""
        combination_str = COMBINATIONS[self.my_combination_tuple[0]]
        combination_str += " " + str(self.my_combination_tuple[1])
        if self.my_combination_tuple[2] is not None:
            combination_str += " with another cards" + str(self.my_combination_tuple[2])
        self.my_combination_str = combination_str


class HumanPlayer(Player):
    """Implementation of Player class for Human input."""

    def turn(self, opponent_bid):
        """Fold or call or raise."""
        print(f"{self.name} your bid {self.bid} opponent bid is {opponent_bid}")
        if self.bid < opponent_bid:
            print(f"CALL costs {opponent_bid - self.bid} or RAISE smth over opponent bid or FOLD")
        else:
            print("CALL (it is free) or RAISE")
        print("write FOLD or CALL or RAISE [x]")
        while True:
            command = input().split()
            if command[0] == "FOLD":
                self.fold = True
                self.raise_bid = False
                break
            elif command[0] == "CALL":
                self.balance -= opponent_bid - self.bid
                self.bid = opponent_bid
                self.raise_bid = False
                break
            elif command[0] == "RAISE":
                amount = int(command[1])
                self.balance -= opponent_bid - self.bid + amount
                self.bid = opponent_bid + amount
                self.raise_bid = True
                break
            else:
                print("wrong command try FOLD or CALL or RAISE")


class ComputerPlayer(Player):
    """Implementation of Player class for Bot player."""

    def turn(self, opponent_bid):
        """Bot logic."""
        pass


class Round:
    """One Round of game."""

    def __init__(self, players):
        self.players = players
        self.dealing_cards()
        self.max_bid = 0
        self.sum_bid = 0
        self.table_cards = None
        self.viseble_cards = ["XX"] * 5
        self.dealing_cards()

    def dealing_cards(self):
        """Shaffle and deal cards to players and table."""
        amount_cards = CARDS_ON_TABLE + len(self.players) * CARDS_ON_HAND
        cards = sample(ALL_CARDS, amount_cards)
        self.table_cards = cards[:CARDS_ON_TABLE]
        for i in range(len(self.players)):
            self.players[i].cards = [cards[CARDS_ON_TABLE + i * CARDS_ON_HAND],
                                     cards[CARDS_ON_TABLE + i * CARDS_ON_HAND + 1]]

    def finish_round(self):
        """Check wining conditions at last round."""
        win_players = []
        win_combination = -1, None, None
        for player in self.players:
            if player.fold:
                continue
            if player.my_combination(self.table_cards) > win_combination:
                win_players = [player]
            elif player.my_combination(self.table_cards) == win_combination:
                win_players.append(player)
            win_combination = max(win_combination, player.my_combination(self.table_cards))
        for player in win_players:
            print(f"{player.name} win {self.sum_bid / len(win_players)} with {player.my_combination_str}")
            player.balance += self.sum_bid / len(win_players)

    def turn(self):
        """Round logic."""
        opponent_bid = 0
        end_round = True
        while end_round:
            end_round = False
            for player in self.players:
                if not player.fold and not (player.bid == opponent_bid and not player.first_bid_of_round):
                    player.turn(opponent_bid)
                    opponent_bid = max(opponent_bid, player.bid)
                    end_round = end_round or player.raise_bid
                player.first_bid_of_round = False
        for player in self.players:
            player.first_bid_of_round = True
            self.sum_bid += player.bid
            player.bid = 0

    def play(self):
        """Game loop."""
        print(self.viseble_cards, "Total bids", self.sum_bid)
        self.turn()
        self.viseble_cards[0], self.viseble_cards[1], self.viseble_cards[2] = \
            self.table_cards[0], self.table_cards[1], self.table_cards[2]
        print(self.viseble_cards, "Total bids", self.sum_bid)
        self.turn()
        self.viseble_cards[3] = self.table_cards[3]
        print(self.viseble_cards, "Total bids", self.sum_bid)
        self.turn()
        self.viseble_cards[4] = self.table_cards[4]
        print(self.viseble_cards, "Total bids", self.sum_bid)
        self.turn()
        self.finish_round()


cur_players = []
for name in ["Bob", "Mike", "Ann"]:
    cur_players.append(HumanPlayer(name))
for _ in range(2):
    game = Round(cur_players)
    for player in cur_players:
        print(player.name, player.cards)
        player.my_combination(game.table_cards)
    print()
    game.play()
    for player in cur_players:
        print(player.name, player.balance)
    print()
