import random

class Dice(object):
#add the business rules to this class
    def __init__(self):
        self.score = 0
        self.set_aside = []
        self.remaining = []

    def get_points(self):
        return self.score

    def roll(self):
        for die in self.remaining:
            die.roll()


class Die(object):
    def __init__(self):
        self.value = 0

    def roll(self):
        self.value = random.randint(1,6)

    def get_value(self):
        return self.value


class Farkle(object):
    def __init__(self):
        self.players = []
        self.scores = []

    def add_player(self, player):
        self.players.append(player)

    def play(self):

        turn_index = 0
        while True:
            score = self.players[turn_index].take_turn()

            if score > 10000: break
            turn_index += 1
            if turn_index > len(player): turn_index = 0

        return turn_index



class Player(object):
    def take_turn(self):
        pass

class HumanPlayer(Player):
    pass

class AIPlayer(Player):
    pass
