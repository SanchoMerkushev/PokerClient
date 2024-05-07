"""Main game mechanics module."""
from time import sleep
from random import sample
import socket
import json

from src.constants import COMBINATIONS, CARDS_ON_TABLE, CARDS_ON_HAND, ALL_CARDS, START_BALANCE
from src.combinations import count_combination
from src.misc import recv_end, END


def send_inf_to_player(player, key, inf, answer=False):
    """Send data to player."""
    sleep(0.1)
    state = {key: inf}
    if answer:
        state["answer"] = True
    data = json.dumps(state)+END
    player.conn.sendall(data.encode())


def send_state_to_players(round_state, cur_player):
    """Send full game state."""
    state = {
        "sync": True,
        "visible_cards": round_state.visible_cards,
        "sum_bids": round_state.sum_bids,
    }
    players = {}
    for player in round_state.players:
        cards = player.cards if player.fold else [("X", "X"), ("X", "X")]
        players[player.name] = {
            "name": player.name,
            "fold": player.fold,
            "bid": player.bid,
            "cards": cards,
            "balance": player.balance,
            "turn": player.name == cur_player.name
        }
    state["players"] = players
    for player in round_state.players:
        data = json.dumps(state) + END
        player.conn.sendall(data.encode())


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

    def __init__(self, name, conn, addr):
        super().__init__(name)
        self.conn = conn
        self.addr = addr

    def close(self):
        """Disconnect player."""
        self.conn.close()

    def turn(self, opponent_bid):
        """Fold or call or raise."""
        inf = "{} your bid {} opponent bid is {}\n".format(self.name, self.bid, opponent_bid)
        if self.bid < opponent_bid:
            inf += "CALL costs {} or RAISE smth over opponent bid or FOLD\n".format(opponent_bid - self.bid)
        else:
            inf += "CALL (it is free) or RAISE\n"
        inf += "Write FOLD or CALL or RAISE [N]"
        send_inf_to_player(self, "output_inf", inf, answer=True)
        while True:
            command = recv_end(self.conn, END)
            command = list(map(str.upper, command.split()))
            if command[0] == "FOLD":
                self.fold = True
                self.raise_bid = False
                break
            elif command[0] == "CALL":
                self.balance -= opponent_bid - self.bid
                self.bid = opponent_bid
                self.raise_bid = False
                break
            elif command[0] == "RAISE" and len(command) > 1:
                amount = int(command[1])
                if opponent_bid - self.bid + amount <= self.balance:
                    self.balance -= opponent_bid - self.bid + amount
                    self.bid = opponent_bid + amount
                    self.raise_bid = True
                    break
                else:
                    inf = "Not enough money, your maximum raise is {}".format(self.balance - opponent_bid + self.bid)
                    send_inf_to_player(self, "output_inf", inf, answer=True)
            else:
                inf = "Wrong command try FOLD or CALL or RAISE [N]"
                send_inf_to_player(self, "output_inf", inf, answer=True)


class ComputerPlayer(Player):
    """Implementation of Player class for Bot player."""

    def turn(self, opponent_bid):
        """Bot logic."""
        pass


class Round:
    """One Round of game."""

    def __init__(self, players):
        self.players = players
        self.table_cards = None
        self.dealing_cards()
        self.sum_bids = 0
        self.visible_cards = ["XX"] * 5

    def dealing_cards(self):
        """Shaffle and deal cards to players and table."""
        amount_cards = CARDS_ON_TABLE + len(self.players) * CARDS_ON_HAND
        cards = sample(ALL_CARDS, amount_cards)
        self.table_cards = cards[:CARDS_ON_TABLE]
        for i in range(len(self.players)):
            self.players[i].cards = [cards[CARDS_ON_TABLE + i * CARDS_ON_HAND],
                                     cards[CARDS_ON_TABLE + i * CARDS_ON_HAND + 1]]
            send_inf_to_player(players[i], "cards_on_hand", self.players[i].cards)

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
            player.balance += self.sum_bids / len(win_players)
        inf = "Winner - {} win {} with {}".format(player.name, self.sum_bids / len(win_players), player.my_combination_str)
        for player in self.players:
            send_inf_to_player(player, "finish_round", inf)
        sleep(4)
            
    def set_bids(self):
        """Round logic."""
        opponent_bid = 0
        end_round = True
        while end_round:
            end_round = False
            for player in self.players:
                send_state_to_players(self, player)
                if not player.fold and not (player.bid == opponent_bid and not player.first_bid_of_round):
                    player.turn(opponent_bid)
                    opponent_bid = max(opponent_bid, player.bid)
                    end_round = end_round or player.raise_bid
                player.first_bid_of_round = False
        for player in self.players:
            player.first_bid_of_round = True
            self.sum_bids += player.bid
            player.bid = 0

    def open_cards(self, amount_visible_cards):
        """Open common cards."""
        for i in range(amount_visible_cards):
            self.visible_cards[i] = self.table_cards[i]

    def play(self):
        """Game loop."""
        self.open_cards(0)
        self.set_bids()
        self.open_cards(3)
        self.set_bids()
        self.open_cards(4)
        self.set_bids()
        self.open_cards(5)
        self.set_bids()
        self.finish_round()


class Game:
    """Main game class."""

    def __init__(self, players, max_rounds):
        self.players = players
        self.max_rounds = max_rounds

    def start(self):
        """Start a game."""
        cur_players = self.players
        for _ in range(self.max_rounds):
            game = Round(cur_players)
            for player in cur_players:
                player.my_combination(game.table_cards)
            game.play()
            for player in cur_players:
                print(player.name, player.balance)
            print()
        self.disconnect_all()

    def disconnect_all(self):
        """Disconnect all players at the end of the game."""
        for player in self.players:
            if isinstance(player, HumanPlayer):
                send_inf_to_player(player, "game_over", True)


if __name__ == "__main__":
    players = []
    s = socket.create_server(("", 5000))
    s.listen(4)
    for name in range(2):
        conn, addr = s.accept()
        name = recv_end(conn, END)
        players.append(HumanPlayer(name, conn, addr))
    s.close()

    Game(players, 2).start()
