import random


class Dice(object):
    def __init__(self):
        self.score = 0
        self.set_aside = []
        self.remaining = [0, 0, 0, 0, 0, 0]

    def get_score(self):
        return self.score

    def get_set_aside(self):
        return [die for die in self.set_aside]

    def get_remaining(self):
        return [die for die in self.remaining]

    def roll(self):
        self.remaining = [random.randint(1,6) for die in self.remaining]

    def is_valid_set_aside(self, dice_values):
        for die_value in dice_values:
            found = False
            for die in self.remaining:
                if die == die_value:
                    found = True
            if found == False:
                return False
        return True

    def dice_combination_value(self, dice_values):
        return 100

    def move_to_set_aside(self, dice_values):
        if not self.is_valid_set_aside(dice_values):
            raise InvalidSetAsideException()

        value = self.dice_combination_value(dice_values)
        if value == 0:
            raise InvalidSetAsideException()

        for die_value in dice_values:
            self.set_aside.append(die_value)
            self.remaining.remove(die_value)


class InvalidSetAsideException(Exception):
    pass


class Player(object):
    def take_turn(self, dice):
        pass

class HumanPlayer(Player):
    def take_turn(self, dice):
        while True:
            dice.roll()
            choices = self.farkle_prompt(dice)
            if choices != '':
                try:
                    dice.move_to_set_aside([int(choice) for choice in choices.split()])
                    print "\n"*64
                except InvalidSetAsideException as e:
                    print "\n"*64
                    print "That set aside is not valid."
            else:
                return dice


    def clear_screen(self):
        print "\n"*64

    def farkle_prompt(self, dice):
        remaining = ' '.join([str(die) for die in dice.get_remaining()])
        set_aside = ' '.join([str(die) for die in dice.get_set_aside()])
        print "\n\nSet Aside:\n", set_aside
        print "Turn score: ", dice.get_score()
        print "\nYou roll the dice:\n", remaining
        return raw_input("\nIndicate the dice you want to set aside by entering their numbers separated by spaces, or enter nothing to stop.\n")


class AIPlayer(Player):
    def take_turn(self, dice):
        pass


class Farkle(object):
    def __init__(self):
        self.players = []
        self.scores = []

    def add_player(self, player):
        self.players.append(player)
        self.scores.append(0)

    def play(self):

        turn_index = 0
        while True:
            dice = self.players[turn_index].take_turn(Dice())
            self.scores[turn_index] = dice.get_score()

            if self.scores[turn_index] > 10000: break
            turn_index += 1
            if turn_index > len(self.players) - 1: turn_index = 0

        return turn_index


def main():
    farkle = Farkle()
    farkle.add_player(HumanPlayer())
    winner = farkle.play()
    print "The winner is player " + winner + "!"

if __name__ == "__main__":
    main()
