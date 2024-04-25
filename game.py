from random import sample
from constants import *
from combinations import *


'''
Class Player is abstrasc class for subclasses HumanPlayer and ComputerPlayer
'''
class Player:

    def __init__(self, name):
        self.balance = START_BALANCE
        self.name = name
        self.bid = 0
        self.cards = None
        self.cur_game = None

    def exit_from_game(self):
        '''Exit game and free place for another players'''
        pass

    def turn(self):
        '''Fold or call or raise'''
        pass

    def my_combination(self, table_cards):
        self.my_combination_tuple = count_combination(self.cards + table_cards)
        self.create_my_combination_str();
        return self.my_combination_tuple

    def create_my_combination_str(self):
        combination_str = COMBINATIONS[self.my_combination_tuple[0]]
        combination_str += " " + str(self.my_combination_tuple[1])
        if self.my_combination_tuple[2] is not None:
            combination_str += " with another cards" + str(self.my_combination_tuple[2])
        self.my_combination_str = combination_str
        


class HumanPlayer(Player):

    def turn(self):
        pass

class ComputerPlayer(Player):

    def turn(self):
        pass

'''
One Round of game
'''
class Round:

    def __init__(self, players):
        self.players = players
        self.dealing_cards()
        self.sum_bid = 0

    def dealing_cards(self):
        amount_cards = CARDS_ON_TABLE + len(self.players) * CARDS_ON_HAND
        cards = sample(ALL_CARDS, amount_cards)
        self.table_cards = cards[:CARDS_ON_TABLE]
        for i in range(len(self.players)):
            self.players[i].cards = [cards[CARDS_ON_TABLE + i * CARDS_ON_HAND], cards[CARDS_ON_TABLE + i * CARDS_ON_HAND + 1]]

    def finish_round(self):
        win_players = []
        win_combination = -1, None, None
        for player in self.players:
            if player.my_combination(self.table_cards) > win_combination:
                win_players = [player]
            elif player.my_combination(self.table_cards) == win_combination:
                win_players.append(player)
            win_combination = max(win_combination, player.my_combination(self.table_cards))
        for player in win_players:
            player.balance += self.sum_bid / len(win_players)
        



cur_players = []
for name in ["Bob", "Mike", "Tom", "Jhon"]:
    cur_players.append(HumanPlayer(name))
for _ in range(5):
    game = Round(cur_players)
    print("TABLE ", game.table_cards)
    for player in cur_players:
        print(player.name, player.cards)
        player.my_combination(game.table_cards)
        print(player.my_combination_str)
        print()
        player.balance -= 100
        game.sum_bid += 100
    game.finish_round()
    for player in cur_players:
        print(player.name, player.balance)


    

    
