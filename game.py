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
        return count_combination(self.cards + table_cards)


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

    def dealing_cards(self):
        amount_cards = CARDS_ON_TABLE + len(self.players) * CARDS_ON_HAND
        cards = sample(ALL_CARDS, amount_cards)
        self.table_cards = cards[:CARDS_ON_TABLE]
        for i in range(len(self.players)):
            self.players[i].cards = [cards[CARDS_ON_TABLE + i * CARDS_ON_HAND], cards[CARDS_ON_TABLE + i * CARDS_ON_HAND + 1]]

    def finish_round(self):
        win_player = self.players[0]
        for i in range(1, len(self.players)):
            if self.players[i].my_combination(self.table_cards) > win_player.my_combination(self.table_cards):
                win_player =  self.players[i]
        print()
        print("WIN")
        print(win_player.cards)
        print(win_player.my_combination(game.table_cards))



cur_players = []
for name in ["Bob", "Mike", "Tom", "Jhon", "Ivan"]:
    cur_players.append(HumanPlayer(name))
game = Round(cur_players)

print(game.table_cards)
print()
for player in cur_players:
    print(player.cards)
    print(player.my_combination(game.table_cards))
    print()
game.finish_round()


    

    
