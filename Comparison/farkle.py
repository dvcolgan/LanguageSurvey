import random


class VerboseGAPlayer(object):
    def __init__(self, gene):
        self.ga_player = GAPlayer(gene)

    def query_set_aside(self, remaining, set_aside, turn_score, total_scores):

        print 'GA player rolled the dice:'
        print remaining.get_values_as_string()
        proposed_set_aside = self.ga_player.query_set_aside(remaining,
                                                            set_aside,
                                                            turn_score,
                                                            total_scores)
        print 'GA player decided to set aside:',
        print DiceFactory.set_as(proposed_set_aside).get_values_as_string()
        return proposed_set_aside

    def query_stop(self, remaining, set_aside, turn_score, total_scores):
        choice = self.ga_player.query_stop(remaining,
                                           set_aside,
                                           turn_score,
                                           total_scores)
        if choice:
            print 'GA player decided to stop with', turn_score, 'points.\n'
        else:
            print 'GA player decided to keep rolling with {0} points'.format(turn_score)
        return choice

    def warn_invalid_set_aside(self):
        #the GA player should never get an error like this
        pass

    def warn_farkle(self, roll):
        print 'GA player got a farkle!'
        print "Dice:", roll.get_values_as_string(), '\n'


class GAPlayer(object):
    def __init__(self, gene=None):
#create a dsl and do code generation? for later
        self.gene_mutator = [
self.randint01, #0, rolled 3, two 1's: 0=take one, 1=take two
self.randint01, #1, rolled 3, two 5's: 0=take one, 1=take two
self.randint01, #2, rolled 3, one 1 and one 5: 0=take 1, 1=take both

self.randint01, #3, rolled 4, two 1's: 0=take one, 1=take two
self.randint01, #4, rolled 4, two 5's: 0=take one, 1=take two
self.randint01, #5, rolled 4, one 1 and one 5: 0=take 1, 1=take both

self.randint02, #6, rolled 5, three 1's and a 5: 0=take one, 1=take three, 2=take four
self.randint02, #7, rolled 5, three 2's and a 1 or 5: 0=take one, 1=take three, 2=take four
self.randint02, #8, rolled 5, three 3's and a 1 or 5: 0=take one, 1=take three, 2=take four
self.randint02, #9, rolled 5, three 4's and a 1 or 5: 0=take one, 1=take three, 2=take four
self.randint02, #10, rolled 5, three 5's and a 1: 0=take one, 1=take three, 2=take four
self.randint02, #11, rolled 5, three 6's and a 1 or 5: 0=take one, 1=take three, 2=take four

self.randint01, #12, rolled 5, two 1's: 0=take one, 1=take two
self.randint01, #13, rolled 5, two 5's: 0=take one, 1=take two
self.randint01, #14, rolled 5, one 1 and one 5: 0=take 1, 1=take both

self.randint02, #15, rolled 6, three 1's and two 5's: 0=take one, 1=take three, 2=take five
self.randint02, #16, rolled 6, three 2's and two others: 0=take one, 1=take three, 2=take five
self.randint02, #17, rolled 6, three 3's and two others: 0=take one, 1=take three, 2=take five
self.randint02, #18, rolled 6, three 4's and two others: 0=take one, 1=take three, 2=take five
self.randint02, #19, rolled 6, three 5's and two 1's: 0=take one, 1=take three, 2=take five
self.randint02, #20, rolled 6, three 6's and two others: 0=take one, 1=take three, 2=take five

self.randint02, #21, rolled 6, three 1's and a 5: 0=take one, 1=take three, 2=take four
self.randint02, #22, rolled 6, three 2's and a 1 or 5: 0=take one, 1=take three, 2=take four
self.randint02, #23, rolled 6, three 3's and a 1 or 5: 0=take one, 1=take three, 2=take four
self.randint02, #24, rolled 6, three 4's and a 1 or 5: 0=take one, 1=take three, 2=take four
self.randint02, #25, rolled 6, three 5's and a 1: 0=take one, 1=take three, 2=take four
self.randint02, #26, rolled 6, three 6's and a 1 or 5: 0=take one, 1=take three, 2=take four

self.randint01, #27, rolled 6, two 1's: 0=take one, 1=take two
self.randint01, #28, rolled 6, two 5's: 0=take one, 1=take two
self.randint01, #29, rolled 6, one 1 and one 5: 0=take 1, 1=take both

self.randrange50_3500, #30, if have 1 dice left, threshold to stop at
self.randrange50_3500, #31, if have 2 dice left, threshold to stop at
self.randrange50_3500, #32, if have 3 dice left, threshold to stop at
self.randrange50_3500, #33, if have 4 dice left, threshold to stop at
self.randrange50_3500, #34, if have 5 dice left, threshold to stop at
self.randrange50_3500, #35, if have 6 dice left, threshold to stop at
        ]

        if gene is not None:
            self.gene = gene
        else:
            self.gene = [self.gene_mutator[i]() for i in range(len(self.gene_mutator))]

    def randint01(self):
        return random.randint(0,1)

    def randint02(self):
        return random.randint(0,2)

    def randrange50_3500(self):
        return random.choice(range(0, 3501, 50))

    def query_set_aside(self, remaining, set_aside, turn_score, total_scores):
        if (remaining.contains_one_scoring_die() or
            remaining.contains_only_three_of_a_kind() or
            remaining.get_score() >= 1000 or
            remaining.all_dice_score()):
            return remaining.get_most_valuable_set_aside()

        if remaining.count() == 2:
            return remaining.get_most_valuable_set_aside()

        if remaining.count() == 3:
            if remaining.get_counts()[1] == 2:
                if self.gene[0] == 0: return (1,)
                if self.gene[0] == 1: return (1,1)
            elif remaining.get_counts()[5] == 2:
                if self.gene[1] == 0: return (5,)
                if self.gene[1] == 1: return (5,5)
            elif remaining.get_counts()[1] == 1 and remaining.get_counts()[5] == 1:
                if self.gene[2] == 0: return (1,)
                if self.gene[2] == 1: return (1,5)

        if remaining.count() == 4:
            if remaining.get_counts()[1] == 2:
                if self.gene[3] == 0: return (1,)
                if self.gene[3] == 1: return (1,1)
            elif remaining.get_counts()[5] == 2:
                if self.gene[4] == 0: return (5,)
                if self.gene[4] == 1: return (5,5)
            elif remaining.get_counts()[1] == 1 and remaining.get_counts()[5] == 1:
                if self.gene[5] == 0: return (1,)
                if self.gene[5] == 1: return (1,5)
            
        if remaining.count() == 5:
            if remaining.contains_three_of_a_kind_and_one_other(1):
                if self.gene[6] == 0:
                    return remaining.get_most_valuable_single_die()
                if self.gene[6] == 1:
                    return (1,1,1)
                if self.gene[6] == 2:
                    return remaining.get_most_valuable_set_aside()
            elif remaining.contains_three_of_a_kind_and_one_other(2):
                if self.gene[7] == 0:
                    return remaining.get_most_valuable_single_die()
                if self.gene[7] == 1:
                    return (2,2,2)
                if self.gene[7] == 2:
                    return remaining.get_most_valuable_set_aside()
            elif remaining.contains_three_of_a_kind_and_one_other(3):
                if self.gene[8] == 0:
                    return remaining.get_most_valuable_single_die()
                if self.gene[8] == 1:
                    return (3,3,3)
                if self.gene[8] == 2:
                    return remaining.get_most_valuable_set_aside()
            elif remaining.contains_three_of_a_kind_and_one_other(4):
                if self.gene[9] == 0:
                    return remaining.get_most_valuable_single_die()
                if self.gene[9] == 1:
                    return (4,4,4)
                if self.gene[9] == 2:
                    return remaining.get_most_valuable_set_aside()
            elif remaining.contains_three_of_a_kind_and_one_other(5):
                if self.gene[10] == 0:
                    return remaining.get_most_valuable_single_die()
                if self.gene[10] == 1:
                    return (5,5,5)
                if self.gene[10] == 2:
                    return remaining.get_most_valuable_set_aside()
            elif remaining.contains_three_of_a_kind_and_one_other(6):
                if self.gene[11] == 0:
                    return remaining.get_most_valuable_single_die()
                if self.gene[11] == 1:
                    return (6,6,6)
                if self.gene[11] == 2:
                    return remaining.get_most_valuable_set_aside()

            elif remaining.get_counts()[1] == 2:
                if self.gene[12] == 0: return (1,)
                if self.gene[12] == 1: return (1,1)
            elif remaining.get_counts()[5] == 2:
                if self.gene[13] == 0: return (5,)
                if self.gene[13] == 1: return (5,5)
            elif remaining.get_counts()[1] == 1 and remaining.get_counts()[5] == 1:
                if self.gene[14] == 0: return (1,)
                if self.gene[14] == 1: return (1,5)


        if remaining.count() == 6:
            if remaining.contains_three_of_a_kind_and_two_others(1):
                if self.gene[15] == 0:
                    return remaining.get_most_valuable_single_die()
                if self.gene[15] == 1:
                    return (1,1,1)
                if self.gene[15] == 2:
                    return remaining.get_most_valuable_set_aside()
            elif remaining.contains_three_of_a_kind_and_two_others(2):
                if self.gene[16] == 0:
                    return remaining.get_most_valuable_single_die()
                if self.gene[16] == 1:
                    return (2,2,2)
                if self.gene[16] == 2:
                    return remaining.get_most_valuable_set_aside()
            elif remaining.contains_three_of_a_kind_and_two_others(3):
                if self.gene[17] == 0:
                    return remaining.get_most_valuable_single_die()
                if self.gene[17] == 1:
                    return (3,3,3)
                if self.gene[17] == 2:
                    return remaining.get_most_valuable_set_aside()
            elif remaining.contains_three_of_a_kind_and_two_others(4):
                if self.gene[18] == 0:
                    return remaining.get_most_valuable_single_die()
                if self.gene[18] == 1:
                    return (4,4,4)
                if self.gene[18] == 2:
                    return remaining.get_most_valuable_set_aside()
            elif remaining.contains_three_of_a_kind_and_two_others(5):
                if self.gene[19] == 0:
                    return remaining.get_most_valuable_single_die()
                if self.gene[19] == 1:
                    return (5,5,5)
                if self.gene[19] == 2:
                    return remaining.get_most_valuable_set_aside()
            elif remaining.contains_three_of_a_kind_and_two_others(6):
                if self.gene[20] == 0:
                    return remaining.get_most_valuable_single_die()
                if self.gene[20] == 1:
                    return (6,6,6)
                if self.gene[20] == 2:
                    return remaining.get_most_valuable_set_aside()

            if remaining.contains_three_of_a_kind_and_one_other(1):
                if self.gene[21] == 0:
                    return remaining.get_most_valuable_single_die()
                if self.gene[21] == 1:
                    return (1,1,1)
                if self.gene[21] == 2:
                    return remaining.get_most_valuable_set_aside()
            elif remaining.contains_three_of_a_kind_and_one_other(2):
                if self.gene[22] == 0:
                    return remaining.get_most_valuable_single_die()
                if self.gene[22] == 1:
                    return (2,2,2)
                if self.gene[22] == 2:
                    return remaining.get_most_valuable_set_aside()
            elif remaining.contains_three_of_a_kind_and_one_other(3):
                if self.gene[23] == 0:
                    return remaining.get_most_valuable_single_die()
                if self.gene[23] == 1:
                    return (3,3,3)
                if self.gene[23] == 2:
                    return remaining.get_most_valuable_set_aside()
            elif remaining.contains_three_of_a_kind_and_one_other(4):
                if self.gene[24] == 0:
                    return remaining.get_most_valuable_single_die()
                if self.gene[24] == 1:
                    return (4,4,4)
                if self.gene[24] == 2:
                    return remaining.get_most_valuable_set_aside()
            elif remaining.contains_three_of_a_kind_and_one_other(5):
                if self.gene[25] == 0:
                    return remaining.get_most_valuable_single_die()
                if self.gene[25] == 1:
                    return (5,5,5)
                if self.gene[25] == 2:
                    return remaining.get_most_valuable_set_aside()
            elif remaining.contains_three_of_a_kind_and_one_other(6):
                if self.gene[26] == 0:
                    return remaining.get_most_valuable_single_die()
                if self.gene[26] == 1:
                    return (6,6,6)
                if self.gene[26] == 2:
                    return remaining.get_most_valuable_set_aside()

            elif remaining.get_counts()[1] == 2:
                if self.gene[27] == 0: return (1,)
                if self.gene[27] == 1: return (1,1)
            elif remaining.get_counts()[5] == 2:
                if self.gene[28] == 0: return (5,)
                if self.gene[28] == 1: return (5,5)
            elif remaining.get_counts()[1] == 1 and remaining.get_counts()[5] == 1:
                if self.gene[29] == 0: return (1,)
                if self.gene[29] == 1: return (1,5)
            

        


    def query_stop(self, remaining, set_aside, turn_score, total_scores):
        if remaining.count() == 1:
            return turn_score >= self.gene[30]
        if remaining.count() == 2:
            return turn_score >= self.gene[31]
        if remaining.count() == 3:
            return turn_score >= self.gene[32]
        if remaining.count() == 4:
            return turn_score >= self.gene[33]
        if remaining.count() == 5:
            return turn_score >= self.gene[34]
        if remaining.count() == 6:
            return turn_score >= self.gene[35]
        return True

    def warn_invalid_set_aside(self):
        raise InvalidSetAsideException()

    def warn_farkle(self, roll):
        pass


class GreedyAIPlayer(object):

    def __init__(self, stop_threshold):
        self.stop_threshold = stop_threshold

    def query_set_aside(self, remaining, set_aside, turn_score, total_scores):

        print "AI player rolled", remaining.get_values()

        if remaining.count() == 6 and remaining.get_score() > 1000:
            return remaining.get_values()

        result = []
        counts = remaining.get_counts()
        for die, count in counts.iteritems():
            if die == 1 or die == 5 or count >= 3:
                result.extend([die] * count)
        return result

    def query_stop(self, remaining, set_aside, turn_score, total_scores):
        if turn_score < self.stop_threshold:
            return False
        else:
            return True

    def warn_invalid_set_aside(self):
        pass # the AI should never set aside invalidly

    def warn_farkle(self, roll):
        print "AI player got a farkle!"
        print "Dice: " + roll.get_values_as_string()


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


class FarkleProblem(object):
    def create_random_individual(self):
        return GAPlayer()

    def run_tournament(self, p1, p2):
        game = Farkle()
        game.add_player(p1)
        game.add_player(p2)

        p1_wins, p2_wins = 0, 0
        for i in range(10):
            winner = game.play()
            if winner == 0: p1_wins += 1
            if winner == 1: p2_wins += 1
        if p1_wins >= p2_wins: return p1
        if p1_wins <  p2_wins: return p2


    def mate_individuals(self, i1, i2):
        pivot = random.randint(0,len(i1.gene_mutator)-1)
        child1 = i1.gene[:pivot] + i2.gene[pivot:]
        child2 = i2.gene[:pivot] + i1.gene[pivot:]
        return GAPlayer(child1), GAPlayer(child2)

    def mutate_individual(self, ind, mutation_rate):
        pivot = random.randint(0,len(ind.gene_mutator)-1)
        ind.gene[pivot] = ind.gene_mutator[pivot]()
        return ind


#manually set the python random methods to do the same thing for tests

#make this into a test?
#run this problem every time we change the GA code

class SequenceIndividual(object):
    def __init__(self):
        self.gene = [random.randint(0,9) for i in range(10)]

class SequenceProblem(object):
    def create_random_individual(self):
        return SequenceIndividual()

    def run_tournament(self, p1, p2):
        p1_fitness, p2_fitness = 0, 0
        for i in range(10):
            if p1.gene[i] == i: p1_fitness += 1
            if p2.gene[i] == i: p2_fitness += 1

        if p1_fitness >= p2_fitness: return p1
        if p1_fitness <  p2_fitness: return p2

    def mate_individuals(self, seq1, seq2):
        pivot = random.randint(0,9)
        child1, child2 = SequenceIndividual, SequenceIndividual
        child1.gene = seq1.gene[:pivot] + seq2.gene[pivot:]
        child2.gene = seq2.gene[:pivot] + seq1.gene[pivot:]
        return child1, child2

    def mutate_individual(self, seq, mutation_rate):
        if random.random() < mutation_rate:
            pivot = random.randint(0,9)
            seq.gene[pivot] = random.randint(0,9)
        return seq





class GA(object):
    def __init__(self, problem_manager, population_size=128, max_generations=100, mutation_rate=0.01, crossover_rate=0.8):
        self.population = []
        self.problem_manager = problem_manager
        self.population_size = population_size
        self.max_generations = max_generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.mating_pool = []

    def generate_random_population(self):
        self.population = [self.problem_manager.create_random_individual()
                for i in range(self.population_size)]

    def hold_binary_tournament(self):
        self.mating_pool = []
        for i in range(self.population_size):
            contestant1 = random.choice(self.population)
            contestant2 = random.choice(self.population)
            winner = self.problem_manager.run_tournament(contestant1,
                                                         contestant2)
            self.mating_pool.append(winner)

    def do_crossover(self):
        self.population = []
        for i in range(0, self.population_size, 2):
            individual1, individual2 = self.mating_pool[i], self.mating_pool[i+1]
            if random.random() < self.crossover_rate:
                self.population.extend(self.problem_manager.mate_individuals(individual1,individual2))
            else:
                self.population.extend((individual1, individual2))

    def do_mutation(self):
        for individual in self.population:
            if random.random() < self.mutation_rate:
                self.problem_manager.mutate_individual(individual, self.mutation_rate)

    def find_converging_individual(self):
        #thanks to http://stackoverflow.com/questions/3957856/determine-if-a-python-list-is-95-the-same
        # first use the Boyer-Moore Majority Vote Algorithm to determine the
        # most common element, then count that element to determine if it makes
        # up 95% of the elements

        candidate_cnt = 0
        current_candidate = self.population[0]
        for ind in self.population:
            if lists_are_same(ind.gene, current_candidate.gene):
                candidate_cnt += 1
            else:
                candidate_cnt -= 1

            if candidate_cnt == 0:
                current_candidate = ind
                candidate_cnt = 1

        times_appearing = 0
        for ind in self.population:
            if lists_are_same(ind.gene, current_candidate.gene):
                times_appearing += 1

        convergence = (1.0 * times_appearing) / len(self.population)
        return convergence, current_candidate


    def find_strongest_individual(self):
        pool = list(self.population)
        winners = []
        while len(pool) > 1:
            for i in range(0, len(pool), 2):
                individual1, individual2 = pool[i], pool[i+1]
                winner = self.problem_manager.run_tournament(individual1,
                                                             individual2)
                winners.append(winner)
            pool = winners
            winners = []
        return pool[0]


    def print_report(self):
        for individual in self.population:
            print individual.gene

    def run(self):
        try:
            self.generate_random_population()
            for i in range(self.max_generations):
                print 'generation',  i
                self.hold_binary_tournament()
                self.do_crossover()
                self.do_mutation()
                convergence, most_common_ind = self.find_converging_individual()
                print convergence
                if convergence > 0.95:
                    print most_common_ind.gene
                    break
            else:
                print self.find_strongest_individual().gene
        except KeyboardInterrupt:
            print self.find_strongest_individual().gene


if __name__ == "__main__":
    print 'starting'
    ga = GA(FarkleProblem())
    ga.run()
    print 'done'

def main():
    farkle = Farkle()
    #farkle.add_player(GreedyAIPlayer(500))
    farkle.add_player(VerboseGAPlayer([0, 0, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 0, 0, 0, 2, 2, 1, 1, 1, 0, 1, 1, 1, 2, 2, 1, 0, 1, 2400, 50, 0, 2900, 450, 1600]))
    winner = farkle.play()
    print "The winner is player {0}!".format(winner)

if __name__ == "__main__":
    main()