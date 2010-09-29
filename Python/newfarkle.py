import random


class HumanPlayer(object):
    def __init__(self):
        pass

    def query_set_aside(self, remaining_reporter, set_aside_reporter, turn_score, total_scores):
        print "\n\nScores:\n"
        for i, score in enumerate(total_scores):
            print "Player {0}: {1}".format(i, score)

        print "Turn score: ", turn_score

        print "\nSet Aside:"
        print set_aside_reporter.get_values_as_string()

        print "\nYou roll the dice:"
        print remaining_reporter.get_values_as_string()

        choices = raw_input("\nIndicate the dice you want to set aside by entering their numbers separated by spaces, or enter nothing to stop.\n")

        return [int(choice) for choice in choices.split()]


    def query_stop(self, remaining_reporter, set_aside_reporter, turn_score, total_scores):
        choice = raw_input("You have {0} points.  Hit enter to continue rolling, or type 'stop' to end your turn.\n".format(turn_score))
        if choice == '':
            return False
        else:
            return True



class Turn(object):
    
    def take(self, player, total_scores):

        set_aside = Dice.set_as(())
        set_aside_reporter = DiceReporter(set_aside)
        remaining = Dice.roll(6)
        remaining_reporter = DiceReporter(remaining)
        turn_score = 0

        while True:
            
            remaining = Dice.roll(remaining.count())

            while True:
                proposed_set_aside = player.query_set_aside(remaining_reporter, set_aside_reporter, turn_score, total_scores)

                if remaining_reporter.is_valid_set_aside(proposed_set_aside):
                    remaining.remove(proposed_set_aside)
                    set_aside.add(proposed_set_aside)
                    break
                else:
                    self.player.warn_invalid_set_aside()

            print remaining.values
            if player.query_stop(remaining_reporter, set_aside_reporter, turn_score, total_scores):
                return score
            

            

            

class InvalidSetAsideException(Exception):
    pass

class GotFarkleException(Exception):
    pass


class Dice(object):

    @staticmethod
    def roll(count):
        dice = Dice()
        dice.values = [random.randint(1,6) for die in range(count)]        
        return dice

    #fix so that it throws an exception if you enter a number not 1-6
    @staticmethod
    def set_as(values):
        dice = Dice()
        dice.values = list(values)
        return dice

    def count(self):
        return len(self.values)

    def get_counts(self):
        die_counts = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0}

        for die in self.values:
            die_counts[die] += 1

        return die_counts

    def get_values(self):
        return tuple(self.values)

    def add(self, new_dice):
        self.values.extend(new_dice)

    def remove(self, dice_values):
        for die_value in dice_values:
            self.values.remove(die_value)



class DiceReporter(object):
    def __init__(self, dice):
        self.dice = dice

    def have_one_of_each(self):
        counts = self.dice.get_counts()
        return all([counts[die] > 0 for die in range(1,7)])

    def have_n_of_a_kind(self, n):
         pass

    def get_values_as_string(self):
        return ' '.join([str(die) for die in self.dice.get_values()])

    def is_valid_set_aside(self, dice_values):
        if not self.contains_values(dice_values): return False
        if not self.is_scoring_combination(dice_values): return False
        return True

    def contains_values(self, dice_values):
        proposed_dice = list(dice_values)

        for die in self.dice.get_values():
            if die in proposed_dice:
                proposed_dice.remove(die)

        return len(proposed_dice) == 0

    def is_scoring_combination(dice_values):





    def dice_combination_value(self, dice):
        score = 0
        self.count_dice()

        # four with a pair
        matches4, matches2 = dice.find_n_of_a_kind(4, die_counts), dice.find_n_of_a_kind(2, die_counts)
        if matches4 and matches2:
            score += 1500
            die_counts[matches4[0]] = die_counts[matches2[0]] = 0

        # two triplets
        matches = Dice.find_n_of_a_kind(3, die_counts)
        if len(matches) == 2:
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
        if matches:
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

        return (score, die_counts)




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
            turn = Turn()
            score = turn.take(self.players[turn_index], tuple(self.scores))

            self.scores[turn_index] += score

            if self.scores[turn_index] > 10000: break
            turn_index += 1
            if turn_index > len(self.players) - 1: turn_index = 0

        return turn_index


def main():
    farkle = Farkle()
    farkle.add_player(HumanPlayer())
    winner = farkle.play()
    print "The winner is player {0}!".format(winner)

if __name__ == "__main__":
    main()
