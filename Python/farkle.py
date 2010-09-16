import random


class Dice(object):
    def __init__(self):
        self.score = 0
        self.set_aside = []
        self.remaining = [0, 0, 0, 0, 0, 0]

    def get_score(self):
        return self.score

    def get_set_aside(self, as_str=False):
        if as_str:
            return Dice.to_str(self.set_aside)
        else:
            return tuple(self.set_aside)

    def get_remaining(self, as_str=False):
        if as_str:
            return Dice.to_str(self.remaining)
        else:
            return tuple(self.remaining)

    @staticmethod
    def to_str(dice_values):
        return ' '.join([str(die) for die in dice_values])
        
    def roll(self):
        self.check_for_farkle(self.remaining) #<- eh? does not appear to do anything
        self.remaining = [random.randint(1,6) for die in self.remaining]

    #DOES NOT WORK for all cases
    def is_valid_set_aside(self, dice_values):
        for die_value in dice_values:
            found = False
            for die in self.remaining:
                if die == die_value:
                    found = True
            if not found:
                return False
        return True

    @staticmethod
    def find_n_of_a_kind(n, die_counts):
        matches = []
        for i in range(1,7):
            if die_counts[i] >= n:
                matches.append(i)
        return tuple(matches)

    #@staticmethod
    #def zero_out_counts(die_counts):   <- ??
        

    def dice_combination_value(self, dice_values):
        score = 0
        die_counts = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0}

        for die in dice_values:
            die_counts[die] += 1

        # four with a pair
        matches4, matches2 = Dice.find_n_of_a_kind(4, die_counts), Dice.find_n_of_a_kind(2, die_counts)
        if matches4 and matches2:
            score += 1500
            die_counts[matches4[0]] = die_counts[matches2[0]] = 0

        # two triplets
        matches = Dice.find_n_of_a_kind(3, die_counts)
        if len(matches) == 2
            score += 2500
            die_counts[matches[0]] = die_counts[matches[1]] = 0

        # three pairs
        matches = Dice.find_n_of_a_kind(2, die_counts)
        if len(matches) == 3:
            score += 1500
            die_counts[matches[0]] = die_counts[matches[1]] = die_counts[matches[2]] = 0

        # strait
        if len(set(range(1,7)) - set(dice_values)) == 0:
            score += 1500
            for i in range(1,7):
                die_counts[i] = 0

        # 6, 5, 4, and 3 of a kind
        matches = Dice.find_n_of_a_kind(6, die_counts)
        if matches:
            score += 3000
            die_counts[matches[0]] = 0

        matches = Dice.find_n_of_a_kind(5, die_counts)
        if matches:
            score += 2000
            die_counts[matches[0]] = 0

        matches = Dice.find_n_of_a_kind(4, die_counts)
        if matches:
            score += 1000
            die_counts[matches[0]] = 0

        matches = Dice.find_n_of_a_kind(3, die_counts)
        if matches[0] == 1:
            score += 300
        else:
            score += matches[0] * 100
        die_counts[matches[0]] = 0


        # single 1's and 5's
        if die_counts[1] > 0:
            score += die_counts[1] * 100
            die_counts[1] = 0
        if die_counts[5] > 0:
            score += die_counts[5] * 50
            die_counts[5] = 0

#        rules = [
#                {'die_counts':(4,2),'value':1500},
#                {'die_counts':(3,3),'value':2500},
#                {'die_counts':(2,2,2),'value':1500},
#                {'die_counts':(6,),'value':3000},
#                {'die_counts':(5,),'value':2000},
#                {'die_counts':(4,),'value':1000},
#                {'die_counts':(
#
#                {'die_counts':(3,),'value':},
#abstract out the setting of the die_counts to 0 ?


        if any(die_counts.values()):
            raise InvalidSetAsideException()

        return (score, die_counts)
        #return score and also remaining dice, do exception checking in two separate calling functions

    def check_for_farkle(self, dice_values):
        value, leftovers = self.dice_combination_value(dice_values)
        if value = 0:
            raise GotFarkleException()
    
    def evaluate_set_aside(self, dice_values):
        value, leftovers = self.dice_combination_value(dice_values)
        if value > 0 and not any(leftovers.values()):
            raise InvalidSetAsideException()
        else:
            return value

    def move_to_set_aside(self, dice_values):

        value = self.evaluate_set_aside(dice_values)
        self.score += value

        for die_value in dice_values:
            self.set_aside.append(die_value)
            self.remaining.remove(die_value)

        if len(self.set_aside) == 6:
            self.remaining = self.set_aside
            self.set_aside = []


class Rules(object):


class GotFarkleException(Exception):
    pass

class InvalidSetAsideException(Exception):
    pass

class CantRollException(Exception):
    pass


class HumanPlayer(object):
    def take_turn(self, dice, scores):
        while True:
            print "\n"*64
            print "\n\nScores:\n"
            for i, score in enumerate(scores):
                print "Player {0}: {1}".format(i, score)

            print "Turn score: ", dice.get_score()

            print "\nYou roll the dice:"
            try:
                dice.roll()
            except GotFarkleException as e:
                print "\nYou got a farkle!"
#HERE working on getting the interface to recognize a farkle, still print out the dice, then end the turn, also do not allow the dice to be rolled again once this happens
            print dice.get_remaining(as_str=True)

            print "\nSet Aside:"
            print dice.get_set_aside(as_str=True)

            while True:
                choices = raw_input("\nIndicate the dice you want to set aside by entering their numbers separated by spaces, or enter nothing to stop.\n")

                if choices == '':
                    return dice

                try:
                    dice.move_to_set_aside([int(choice) for choice in choices.split()])
                    break
                except ValueError as e:
                    print "The set aside must contain only integers from 1-6."
                except InvalidSetAsideException as e:
                    print "That set aside is not valid."




class AIPlayer(object):
    def take_turn(self, dice):
        pass


class Farkle(object):
    def __init__(self):
        self.players = []
        self.scores = []

    def add_player(self, player):
        self.players.append(player)
        self.scores.append(0)

#add a name, use the uuid for nonhuman players, could be a database key
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
    print "The winner is player " + str(winner) + "!"

if __name__ == "__main__":
    main()
