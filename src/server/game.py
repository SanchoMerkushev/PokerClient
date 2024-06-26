"""Main game mechanics module."""
from time import sleep
from random import sample, choices
import json
import gettext
import os

from .constants import COMBINATIONS, CARDS_ON_TABLE, CARDS_ON_HAND, ALL_CARDS, START_BALANCE, RANKS, BIG_BLIND_SIZE
from .combinations import count_combination
from .misc import recv_end, END
from .client import UI


translation = gettext.translation("msg", "po", fallback=True)
_ = translation.gettext


def send_inf_to_player(player, key, inf, answer=False):
    """Send data to player."""
    if not isinstance(player, HumanPlayer):
        return
    sleep(0.01)
    state = {key: inf}
    if answer:
        state["answer"] = True
    data = json.dumps(state)+END
    player.conn.sendall(data.encode())


def send_state_to_players(round_state, cur_player):
    """Send full game state."""
    if not isinstance(cur_player, HumanPlayer):
        return
    state = {
        "sync": True,
        "visible_cards": round_state.visible_cards,
        "sum_bids": round_state.sum_bids,
    }
    players = {}
    for player in round_state.players:
        cards = [("F", "F"), ("F", "F")] if player.fold else [("X", "X"), ("X", "X")]
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


def send_self_states(round_state, cur_player):
    """Send full game state."""
    if not isinstance(cur_player, SelfPlayer):
        return
    state = {
        "sync": True,
        "visible_cards": round_state.visible_cards,
        "sum_bids": round_state.sum_bids,
    }
    players = {}
    for player in round_state.players:
        cards = [("F", "F"), ("F", "F")] if player.fold else [("X", "X"), ("X", "X")]
        players[player.name] = {
            "name": player.name,
            "fold": player.fold,
            "bid": player.bid,
            "cards": cards,
            "balance": player.balance,
            "turn": player.name == cur_player.name
        }
    state["players"] = players
    ui_obj = UI()
    ui_obj.print_state(state, cur_player.name, cur_player.cards)


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
        for rank in self.my_combination_tuple[1]:
            combination_str += " " + RANKS[rank]
        if self.my_combination_tuple[2] is not None:
            combination_str += _(" with another cards")
            for rank in self.my_combination_tuple[2]:
                combination_str += " " + RANKS[rank]
        self.my_combination_str = combination_str

    def turn_fold(self):
        """Do basic fold."""
        self.fold = True
        self.raise_bid = False

    def turn_call(self, opponent_bid):
        """Do basic call."""
        self.balance -= opponent_bid - self.bid
        self.bid = opponent_bid
        self.raise_bid = False

    def turn_raise(self, opponent_bid, amount):
        """Do basic raise."""
        self.balance -= opponent_bid - self.bid + amount
        self.bid = opponent_bid + amount
        self.raise_bid = True


class HumanPlayer(Player):
    """Implementation of Player class for Human input."""

    def __init__(self, name, conn, addr):
        super().__init__(name)
        self.conn = conn
        self.addr = addr

    def close(self):
        """Disconnect player."""
        self.conn.close()

    def turn(self, opponent_bid, max_raise):
        """Fold or call or raise."""
        inf = _("{} your bid {} opponent bid is {}\n").format(self.name, self.bid, opponent_bid)
        if self.bid < opponent_bid:
            inf += _("CALL costs {} or RAISE smth over opponent bid or FOLD\n").format(opponent_bid - self.bid)
        else:
            inf += _("CALL (it is free) or RAISE\n")
        inf += _("Write FOLD or CALL or RAISE [N]")
        while True:
            command = recv_end(self.conn, END)
            command = list(map(str.upper, command.split()))
            if command[0] == "FOLD":
                self.turn_fold()
                break
            elif command[0] == "CALL":
                self.turn_call(opponent_bid)
                break
            elif command[0] == "RAISE" and len(command) > 1:
                amount = int(command[1])
                if opponent_bid - self.bid + amount <= self.balance:
                    self.turn_raise(opponent_bid, amount)
                    break
                else:
                    inf = _("Not enough money, your maximum raise is {}").format(self.balance - opponent_bid + self.bid)
            else:
                inf = _("Wrong command try FOLD or CALL or RAISE [N]")
        print()


class ComputerPlayer(Player):
    """Implementation of Player class for Bot player."""

    def turn(self, opponent_bid, max_raise):
        """Bot logic."""
        type_turn = choices((0, 1, 2), weights=[40, 100, 30])[0]
        if type_turn == 0:
            self.turn_fold()
        elif type_turn == 1:
            self.turn_call(opponent_bid)
        elif type_turn == 2:
            self.turn_raise(20, opponent_bid)


class SelfPlayer(Player):
    """Implementation of Player class for Self player."""

    def turn(self, opponent_bid, max_raise):
        """Turn logic."""
        inf = _("{} your bid {} opponent bid is {}\n").format(self.name, self.bid, opponent_bid)
        if self.bid < opponent_bid:
            inf += _("CALL costs {} or RAISE smth over opponent bid or FOLD\n").format(opponent_bid - self.bid)
        else:
            inf += _("CALL (it is free) or RAISE\n")
        inf += _("Write FOLD or CALL or RAISE [AMOUNT]")
        print(inf)
        while True:
            command = input()
            command = list(map(str.upper, command.split()))
            if command[0] == "FOLD":
                self.turn_fold()
                break
            elif command[0] == "CALL":
                self.turn_call(opponent_bid)
                break
            elif command[0] == "RAISE" and len(command) > 1:
                amount = int(command[1])
                if amount > max_raise:
                    inf = _("Maximum raise of Round is {}").format(max_raise)
                    print(inf)
                elif opponent_bid - self.bid + amount <= self.balance:
                    self.turn_raise(opponent_bid, amount)
                    break
                else:
                    inf = _("Not enough money, your maximum raise is {}").format(self.balance - opponent_bid + self.bid)
                    print(inf)
            else:
                inf = _("Wrong command try FOLD or CALL or RAISE [AMOUNT]")
                print(inf)


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
            send_inf_to_player(self.players[i], "cards_on_hand", self.players[i].cards)

    def finish_round(self):
        """Check wining conditions at last round."""
        win_players = []
        win_combination = -1, None, None
        for player in self.players:
            if player.fold:
                player.fold = False
                continue
            if player.my_combination(self.table_cards) > win_combination:
                win_players = [player]
            elif player.my_combination(self.table_cards) == win_combination:
                win_players.append(player)
            win_combination = max(win_combination, player.my_combination(self.table_cards))
        win_size = self.sum_bids // len(win_players)
        for player in win_players:
            player.balance += win_size
        os.system("clear")
        inf = _("Winner - {} win {} with {}").format(player.name, win_size, player.my_combination_str)
        print(inf)
        for player in self.players:
            send_inf_to_player(player, "finish_round", inf)

    def set_bids(self):
        """Round logic."""
        amount_not_fold = 0
        for player in self.players:
            if not player.fold:
                amount_not_fold += 1
        if amount_not_fold <= 1:
            return
        opponent_bid = self.players[-1].bid
        end_round = True
        while end_round:
            end_round = False
            max_raise = self.players[0].balance - self.players[0].bid
            for player in self.players:
                max_raise = min(max_raise, player.balance - player.bid)
            for player in self.players:
                send_state_to_players(self, player)
                send_self_states(self, player)
                if not player.fold and not (player.bid == opponent_bid and not player.first_bid_of_round):
                    player.turn(opponent_bid, max_raise)
                    opponent_bid = max(opponent_bid, player.bid)
                    end_round = end_round or player.raise_bid
                    if player.fold:
                        amount_not_fold -= 1
                    if amount_not_fold <= 1:
                        return
                player.first_bid_of_round = False
        for player in self.players:
            player.first_bid_of_round = True
            player.raise_bid = False
            self.sum_bids += player.bid
            player.bid = 0

    def open_cards(self, amount_visible_cards):
        """Open common cards."""
        for i in range(amount_visible_cards):
            self.visible_cards[i] = self.table_cards[i]

    def big_blind(self):
        """Pay big blind."""
        self.players[-1].turn_raise(0, BIG_BLIND_SIZE)

    def play(self):
        """Game loop."""
        self.big_blind()
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

    def rotate_players(self):
        """Remove players with zero balance and rotate."""
        new_players = []
        for player in self.players:
            if player.balance > 0:
                new_players.append(player)
            else:
                if isinstance(player, SelfPlayer):
                    print(_("{} your lost all!\nGAME OVER!!!").format(player.name))
                    exit()
                print(_("{} exit the game").format(player.name))
        if len(new_players) == 1:
            print(_("{} YOUR WIN ALL!!!!").format(player.name))
            exit()
        self.players = new_players[1:] + new_players[:1]

    def start(self):
        """Start a game."""
        print()
        print(_("Start Game with {} players").format(len(self.players)))
        for player in self.players:
            print(player.name, player.balance)
        print()
        for amount in range(self.max_rounds):
            game = Round(self.players)
            for player in self.players:
                player.my_combination(game.table_cards)
            game.play()
            sleep(1)
            self.rotate_players()
            for player in self.players:
                print(player.name, player.balance)
            print()
        self.disconnect_all()

    def disconnect_all(self):
        """Disconnect all players at the end of the game."""
        for player in self.players:
            if isinstance(player, HumanPlayer):
                send_inf_to_player(player, "game_over", True)
