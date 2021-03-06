import random

class GreedyAIPlayer(object):

    def __init__(self, stop_threshold):
        self.stop_threshold = stop_threshold

    def query_set_aside(self, remaining, set_aside, turn_score, total_scores):

        #print str(remaining.get_values()), str(set_aside.get_values()), str(turn_score), str(total_scores)
        #print "AI player rolled", remaining.get_values()

        dice_score = remaining.get_score()
        if remaining.count() == 6 and dice_score >= 1500 and dice_score != 2000:
            return remaining.get_values()

        result = []
        counts = remaining.get_counts()
        for die, count in counts.iteritems():
            if die == 1 or die == 5 or count >= 3:
                result.extend([die] * count)
        return result

    def query_stop(self, remaining, set_aside, turn_score, total_scores):
        if turn_score >= self.stop_threshold:
            return True
        else:
            return False

    def warn_invalid_set_aside(self):
        pass # the AI should never set aside invalidly

    def warn_farkle(self, roll):
        #print "AI player got a farkle!"
        #print "Dice: " + roll.get_values_as_string()
        pass

class HumanPlayer(object):

    def query_set_aside(self, remaining, set_aside, turn_score, total_scores):
        print "\n\nScores:\n"
        for i, score in enumerate(total_scores):
            print "Player {0}: {1}".format(i, score)

        print "Turn score: ", turn_score

        print "\nSet Aside:"
        print set_aside.get_values_as_string()

        print "\nYou roll the dice:"
        print remaining.get_values_as_string()

        choices = raw_input("\nIndicate the dice you want to set aside by entering their numbers separated by spaces.\n")

        try:
            return [int(choice) for choice in choices.split()]
        except ValueError:
            return ''

    def query_stop(self, remaining, set_aside, turn_score, total_scores):
        choice = raw_input("You have {0} points.  Hit enter to continue rolling, or type 'stop' to end your turn.\n".format(turn_score))
        if choice == '':
            return False
        else:
            return True

    def warn_invalid_set_aside(self):
        print "That set aside is invalid!"

    def warn_farkle(self, roll):
        print "You got a farkle!"
        print "Dice: " + roll.get_values_as_string()

class InvalidSetAsideException(Exception):
    pass

class GotFarkleException(Exception):
    pass

class BadDieException(Exception):
    pass

class DiceFactory(object):

    @staticmethod
    def rolled_dice(count):
        dice = Dice()
        dice.values = [random.randint(1, 6) for die in range(count)]
        return dice

    @staticmethod
    def set_as(values):
        for die in values:
            if not (1 <= die <= 6):
                raise BadDieException()
        dice = Dice()
        dice.values = list(values)
        return dice


class Dice(object):

    def __init__(self):
        self.counts = None

    def count(self):
        return len(self.values)

    def get_most_valuable_single_die(self):
        counts = self.get_counts()
        if counts[1] > 0:
            return (1,)
        elif counts[5] > 0:
            return (5,)
        else:
            return None
            
    def get_most_valuable_set_aside(self):
        counts = self.get_counts()

        # 4 of a kind with a pair and 3 pairs are the only scoring combinations with a pair of dice
        if counts.values().count(4) and counts.values().count(2):
            return self.get_values()
        if counts.values().count(2) == 3:
            return self.get_values()
        
        result = []
        for die, count in counts.iteritems():
            if count >= 3 or die == 1 or die == 5:
                result.extend([die]*count)
        return tuple(result)


    def all_dice_score(self):
        counts = self.get_counts()
        if (((counts[2] >= 3 or counts[2] ==0) and
             (counts[3] >= 3 or counts[3] ==0) and
             (counts[4] >= 3 or counts[4] ==0) and
             (counts[6] >= 3 or counts[6] ==0))
            or
            (counts.values().count(4) and
             counts.values().count(2))):
            return True
        else:
            return False

    def contains_three_of_a_kind_and_two_others(self, i):
        counts = self.get_counts()

        if i == 1 and counts[1] == 3 and counts[5] == 2: return True
        if i == 5 and counts[5] == 3 and counts[1] == 2: return True

        if ((i == 2 and counts[2] == 3 and counts[3] < 3 and counts[4] < 3 and counts[6] < 3) or
            (i == 3 and counts[2] < 3 and counts[3] == 3 and counts[4] < 3 and counts[6] < 3) or
            (i == 4 and counts[2] < 3 and counts[3] < 3 and counts[4] == 3 and counts[6] < 3) or
            (i == 6 and counts[2] < 3 and counts[3] < 3 and counts[4] < 3 and counts[6] == 3)):

            if (counts[1] == 2 and counts[5] == 0) or (counts[5] == 2 and counts[1] == 0) or (counts[1] == 1 and counts[5] == 1):
                return True
            else:
                return False
        else:
            return False

    def contains_three_of_a_kind_and_one_other(self, i):
        counts = self.get_counts()

        if i == 1 and counts[1] == 3 and counts[5] == 1: return True
        if i == 5 and counts[5] == 3 and counts[1] == 1: return True

        if ((i == 2 and counts[2] == 3 and counts[3] < 3 and counts[4] < 3 and counts[6] < 3) or
            (i == 3 and counts[2] < 3 and counts[3] == 3 and counts[4] < 3 and counts[6] < 3) or
            (i == 4 and counts[2] < 3 and counts[3] < 3 and counts[4] == 3 and counts[6] < 3) or
            (i == 6 and counts[2] < 3 and counts[3] < 3 and counts[4] < 3 and counts[6] == 3)):

            if (counts[1] == 1 and counts[5] == 0) or (counts[5] == 1 and counts[1] == 0):
                return True
            else:
                return False
        else:
            return False

    def contains_n_or_more_of_a_kind(self, n):
        return any(map(lambda (die,count): count >= n,
                   self.get_counts().iteritems()))

    def contains_only_three_of_a_kind(self):
        die_counts = self.get_counts()
        if ((die_counts[1] == 0 or die_counts[1] == 3) and
            (die_counts[5] == 0 or die_counts[5] == 3) and 
            (any(map(lambda (die,count): count==3, die_counts.iteritems())))):
            return True
        else:
            return False

    def contains_one_scoring_die(self):
        if self.contains_n_or_more_of_a_kind(3):
            return False

        die_counts = self.get_counts()
        if die_counts[1] == 1 and die_counts[5] == 0 or die_counts[1] == 0 and die_counts[5] == 1:
            return True
        else:
            return False

    def get_counts(self):
        if self.counts == None:
            die_counts = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0}
            for die in self.values:
                die_counts[die] += 1
            self.counts = die_counts
        return self.counts


    def get_values(self):
        return tuple(self.values)

    def have_one_of_each(self):
        counts = self.get_counts()
        return all([counts[die] > 0 for die in range(1, 7)])

    def get_values_as_string(self):
        return ' '.join([str(die) for die in self.get_values()])

    def is_valid_set_aside(self, remaining):
        if not remaining.contains_values(self):
            return False
        if self.get_score(zero_for_extra=True) == 0:
            return False
        return True

    def contains_values(self, dice):
        proposed_dice = list(dice.get_values())
        for die in self.get_values():
            if die in proposed_dice:
                proposed_dice.remove(die)
        return len(proposed_dice) == 0

    def is_farkle(self):
        return self.get_score() == 0

    def find_n_of_a_kind(self, n):
        matches = []
        die_counts = self.get_counts()
        for i in range(1,7):
            if die_counts[i] >= n:
                matches.append(i)
        return tuple(matches)

    def add(self, new_dice):
        self.values.extend(new_dice.get_values())

    def remove(self, dice):
        for die_value in dice.get_values():
            self.values.remove(die_value)

    def get_score(self, zero_for_extra=False, return_extra=False):
        score = 0
        die_counts = self.get_counts()

        # four with a pair, two triplets, three pairs, strait,
        # and 6 of a kind can all just return their point value
        # because they use all the dice
        if die_counts.values().count(4) and die_counts.values().count(2):
            return 1500
        if die_counts.values().count(3) == 2:
            return 2500
        if die_counts.values().count(2) == 3:
            return 1500
        if self.have_one_of_each():
            return 1500
        if die_counts.values().count(6):
            return 3000

        #3, 4, and 5 of a kind
        if die_counts.values().count(5):
            score += 2000
            if die_counts[1] == 1: score += 100
            if die_counts[5] == 1: score += 50
            if zero_for_extra and (die_counts[2] == 1 or
                                   die_counts[3] == 1 or
                                   die_counts[4] == 1 or
                                   die_counts[6] == 1):
                score = 0
            return score

        if die_counts.values().count(4):
            score += 1000
            if die_counts[1] <= 2: score += 100 * die_counts[1]
            if die_counts[5] <= 2: score += 50 * die_counts[5]
            if zero_for_extra and (1 <= die_counts[2] <= 2 or
                                   1 <= die_counts[3] <= 2 or
                                   1 <= die_counts[4] <= 2 or
                                   1 <= die_counts[6] <= 2):
                score = 0
            return score

        for die in range(1,7):
            if die_counts[die] == 3:
                if die == 1:
                    score += 300
                else:
                    score += die * 100
        if 1 <= die_counts[1] <= 2: score += 100 * die_counts[1]
        if 1 <= die_counts[5] <= 2: score += 50 * die_counts[5]
        if zero_for_extra and (1 <= die_counts[2] <= 2 or
                               1 <= die_counts[3] <= 2 or
                               1 <= die_counts[4] <= 2 or
                               1 <= die_counts[6] <= 2):
            score = 0
        return score

class NotEnoughPlayersException(Exception):
    pass

class Farkle(object):

    def __init__(self):
        self.players = []
        self.scores = []
        self.turn_index = 0

    def add_player(self, player):
        self.players.append(player)
        self.scores.append(0)

#add a name, use the uuid for nonhuman players, could be a database key
    def play(self):
        if len(self.players) == 0: raise NotEnoughPlayersException()

        while True:
            score = self.take_turn()
            self.scores[self.turn_index] += score

            if self.scores[self.turn_index] > 10000: break
            self.turn_index += 1
            if self.turn_index > len(self.players) - 1: self.turn_index = 0

        return self.turn_index

    def take_turn(self):
        player = self.players[self.turn_index]
        turn_score = 0
        set_aside = DiceFactory.set_as(())
        #junk value to initialize the number of dice
        remaining = DiceFactory.set_as((1,1,1,1,1,1))

        while True:
            remaining = DiceFactory.rolled_dice(remaining.count())
            if remaining.is_farkle():
                player.warn_farkle(remaining)
                return 0

            while True:
                proposed_set_aside = DiceFactory.set_as(player.query_set_aside(remaining,
                                                                               set_aside,
                                                                               turn_score,
                                                                               tuple(self.scores)))

                if proposed_set_aside.is_valid_set_aside(remaining):
                    remaining.remove(proposed_set_aside)
                    set_aside.add(proposed_set_aside)
                    break
                else:
                    player.warn_invalid_set_aside()

            turn_score += proposed_set_aside.get_score()
            if player.query_stop(remaining, set_aside, turn_score, tuple(self.scores)):
                return turn_score
            if remaining.count() == 0:
                remaining = DiceFactory.set_as((1,1,1,1,1,1))
                set_aside = DiceFactory.set_as(())

def lists_are_same(lst1, lst2):
    for e1, e2 in zip(lst1, lst2):
        if e1 != e2:
            return False
    return True

def main():
    wins = [0, 0, 0, 0]
    for i in range(10000):
        if i % 100 == 0:
            print "Game", i
        farkle = Farkle()
        #farkle.add_player(HumanPlayer())
        farkle.add_player(GreedyAIPlayer(300))
        farkle.add_player(GreedyAIPlayer(500))
        farkle.add_player(GreedyAIPlayer(800))
        farkle.add_player(GreedyAIPlayer(1000))
        winner = farkle.play()
        wins[winner] += 1
        #print "The winner is player {0}!".format(winner)
    for i, win in enumerate(wins):
        print "Player", i, "had", win, "wins."

if __name__ == "__main__":
    main()
