import random





class Dice(object):
#add the business rules to this class
    def __init__(self):
        self.score = 0
        self.set_aside = []
        self.remaining = [Die(), Die(), Die(), Die(), Die(), Die()]

    def get_score(self):
        return self.score

    def get_set_aside(self):
        return [die.get_value() for die in self.set_aside]

    def get_remaining(self):
        return [die.get_value() for die in self.remaining]

    def roll(self):
        for die in self.remaining:
            die.roll()

    def move_to_set_aside(self, dice_values):
        if !self.is_valid_set_aside(dice_values):
            raise InvalidSetAsideException()

        for i in reversed(sorted(dice_indices)):
            self.set_aside.append(self.remaining[i])
            del(self.remaining[i])


class InvalidSetAsideException(Exception):
    pass

class Die(object):
    def __init__(self):
        self.value = 0

    def roll(self):
        self.value = random.randint(1,6)

    def get_value(self):
        return self.value




class Player(object):
    def take_turn(self, dice):
        pass

class HumanPlayer(Player):
    def take_turn(self, dice):
        while True:
            dice.roll()
            remaining = ' '.join([str(die) for die in dice.get_remaining()])
            set_aside = ' '.join([str(die) for die in dice.get_set_aside()])

            print "\n\nSet Aside:\n", set_aside
            print "Turn score: ", dice.get_score()
            print "\nYou roll the dice:\n", remaining
            choices = raw_input("\nIndicate the dice you want to set aside by entering their nuumbers separated by spaces, or enter nothing to stop.\n")
            if choices != '':
                try:
                    dice.move_to_set_aside([int(choice) for choice in choices.split()])
                except InvalidSetAsideException as e:
                    print "That set aside is not valid."
            else:
                return dice


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
