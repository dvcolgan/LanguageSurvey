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
        score = 0
        die_counts = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0}

        for die in dice_values:
            die_counts[die] += 1

        # 3, 4, 5, and 6 of a kind
        for i in range(1,7):
            if die_counts[i] == 6:
                score += 3000
                die_counts[i] = 0
            if die_counts[i] == 5:
                score += 2000
                die_counts[i] = 0
            if die_counts[i] == 4:
                score += 1000
                die_counts[i] = 0
            if die_counts[i] == 3:
                if i == 1:
                    score += 300
                else:
                    score += i*100
                die_counts[i] = 0

        # four with a pair
        i_2, i_4 = None, None
        for i in range(1,7):
            if die_counts[i] == 2: i_2 = i
            if die_counts[i] == 4: i_4 = i
        if i_2 and i_4:
            score += 1500
            die_counts[i_2] = 0
            die_counts[i_4] = 0

        # two triplets
        i_3a, i_3b = None, None
        for i in range(1,7):
            if die_counts[i] == 3:
                if not i_3a:
                    i_3a = i
                else:
                    i_3b = i
        if i_3a and i_3b:
            score += 2500
            die_counts[i_3a] = 0
            die_counts[i_3b] = 0

        # three pairs
        i_2a, i_2b, i_2c = None, None, None
        for i in range(1,7):
            if die_counts[i] == 2:
                if not i_2a:
                    i_2a = i
                elif not i_2b:
                    i_2b = i
                else:
                    i_2c = i
        if i_2a and i_2b and i_2c:
            score += 1500
            die_counts[i_2a] = 0
            die_counts[i_2b] = 0
            die_counts[i_2c] = 0

        # strait
        seen = {1:False, 2:False, 3:False, 4:False, 5:False, 6:False}
        for i in range(1,7):
            if die_counts[i] > 0: seen[i] = True
        if all(seen.values()):
            score += 1500
            for i in range(1,7):
                die_counts[i] = 0

        # single 1's and 5's
        if die_counts[1] > 0:
            score += die_counts[1] * 100
            die_counts[1] = 0
        if die_counts[5] > 0:
            score += die_counts[5] * 50
            die_counts[5] = 0

        if any(die_counts.values()):
            raise InvalidSetAsideException()

        return score

    def move_to_set_aside(self, dice_values):
        if not self.is_valid_set_aside(dice_values):
            raise InvalidSetAsideException()

        value = self.dice_combination_value(dice_values)
        if value == 0:
            raise InvalidSetAsideException()

        for die_value in dice_values:
            self.set_aside.append(die_value)
            self.remaining.remove(die_value)

        self.score += value

        if len(self.set_aside) == 6:
            self.remaining = self.set_aside
            self.set_aside = []


class InvalidSetAsideException(Exception):
    pass


class Player(object):
    def take_turn(self, dice):
        pass

class HumanPlayer(Player):
    def take_turn(self, dice, scores):
        while True:
            dice.roll()
            print "Scores:\n"
            for i, score in enumerate(scores):
                print "Player {0}: {1}".format(i, score)

            remaining = ' '.join([str(die) for die in dice.get_remaining()])
            set_aside = ' '.join([str(die) for die in dice.get_set_aside()])
            print "\n\nSet Aside:\n", set_aside
            print "Turn score: ", dice.get_score()
            print "\nYou roll the dice:\n", remaining
            choices = raw_input("\nIndicate the dice you want to set aside by entering their numbers separated by spaces, or enter nothing to stop.\n")
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
            dice = self.players[turn_index].take_turn(Dice(), tuple(self.scores))
            self.scores[turn_index] += dice.get_score()

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
