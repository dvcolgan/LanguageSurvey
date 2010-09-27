import random
import cPickle


#read:

#refactoring

#class should not pass its own instance variables
#large number of static methods means the class may need to be split

#the AI player does not need

#

#does this class need dice as state or only need to get passed it
class DiceEvaluator
    def __init__(self):
        self.score = 0
        self.got_farkle = False
        


#This class should only know about things related to dice, not scoring.
#No mutator methods are exposed.  Only the Turn class can access the dice values themselves.
class Dice(object):
    def __init__(self):
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
        

    def dice_in_set_aside(self, dice_values):

        proposed_dice = list(dice_values)
        actual_dice = list(self.remaining)

        for die in actual_dice:
            if die in proposed_dice:
                proposed_dice.remove(die)
                actual_dice.remove(die)
        if len(proposed_dice) > 0:
            return False
        else:
            return True


    def find_n_of_a_kind(self, n):
        self.count_dice()
        matches = []
        for i in range(1,7):
            if self.die_counts[i] >= n:
                matches.append(i)
        return tuple(matches)



    def count_dice():
        self.die_counts = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0}

        for die in self.dice_values:
            self.die_counts[die] += 1

        

#put in evaluation class
class Turn(object):

    def __init__(self, dice):
        self.dice = dice
        self.score = 0


    def roll(self):

        self.dice
        self.dice.remaining = [random.randint(1,6) for die in self.remaining]
        self.die_counts = None
        self.check_for_farkle()


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




#should be in the evaluation class
    def check_for_farkle(self):
        if self.dice_values == [0,0,0,0,0,0]: return
        value, leftovers = self.dice_combination_value()
        if value == 0:
            self.score = 0
            self.got_farkle = True   # set so that the dice can't be rolled again after getting a farkle
            raise GotFarkleException()
    
    def evaluate_set_aside(self):
        value, leftovers = self.dice_combination_value()
        if value > 0 and not any(leftovers.values()):
            return value
        else:
            raise InvalidSetAsideException()

    #should be in the dice class, because they relate to the current roll
#should not evaluate the score, should only set aside dice
    def move_to_set_aside(self):
        if not self.dice_in_set_aside():
            raise InvalidSetAsideException()

        value = self.evaluate_set_aside()
        self.score += value

        for die_value in dice_values:
            self.set_aside.append(die_value)
            self.remaining.remove(die_value)

        if len(self.set_aside) == 6:
            self.remaining = self.set_aside
            self.set_aside = []

class Dice:
    def get_set_aside(self, as_str=False):
    def get_remaining(self, as_str=False):
    def to_str(dice_values):
    def dice_in_set_aside(self, dice_values):
    def find_n_of_a_kind(self, n):
    def count_dice():

#the turn class is the only class that knows about the dice

class Turn:
    self.dice
    self.score
    
    def move_to_set_aside(self):
    def roll(self):
    def roll
    def set_aside
    def can_roll == check_for_farkle (call before rolling)
    def get_score(self):

    def dice_combination_value(self, dice):
    def check_for_farkle(self):
    def evaluate_set_aside(self):


    def

    def get_score

    def get_remaining

    def get_set_aside





class GotFarkleException(Exception):
    pass

class InvalidSetAsideException(Exception):
    pass

class CantRollException(Exception):
    pass



class TurnState(object):
    def get_set_aside
    def get_remaining
    def get_dice_counts
    def is_n_of_a_kind

class Dice:
    def roll
    def make_set_aside
    def 


class HumanPlayer(object):

#need to provide enough state but not too much
    def what_to_set_aside?(dice, other_players_scores):
        action = raw_input("What do you want to do+?")
        return action

    def stop_or_keep_rolling(dice, other_players_scores)


    def turn:

        while Not Farkle and Not Player Stops
            self.roll()
            player.what_to_set_aside()
            self.set_aside()
            player.stop_or_keep_rolling()


#enforce the rules and support the player
#adapter pattern

#for a workable compromise, the turn class has a roll method that scrambles the dice



class Turn:

    def take(self, dice, scores):
        while True:
            print "\n\nScores:\n"
            for i, score in enumerate(scores):
                print "Player {0}: {1}".format(i, score)

            print "Turn score: ", dice.get_score()

            print "\nSet Aside:"
            print dice.get_set_aside(as_str=True)

            print "\nYou roll the dice:"
            try:
                dice.roll()
            except GotFarkleException as e:
                print dice.get_remaining(as_str=True)
                print "\nYou got a farkle!"
                raw_input('Hit enter to end your turn.')
                return dice

            print dice.get_remaining(as_str=True)


            while True:
                choices = raw_input("\nIndicate the dice you want to set aside by entering their numbers separated by spaces, or enter nothing to stop.\n")

                try:
                    dice.move_to_set_aside([int(choice) for choice in choices.split()])
                    break
                except ValueError as e:
                    print "The set aside must contain only integers from 1-6."
                except InvalidSetAsideException as e:
                    print "That set aside is not valid."
            
            while True:
                choice = raw_input("You have {0} points.  Hit enter to continue rolling, or type 'stop' to end your turn.\n".format(dice.get_score()))
                if choice == '':
                    break
                if choice.lower() == 'stop':
                    return dice
                

roll()

class AIDecisionMaker(object):
    def __init__(self):

#take this and copy it x number of times for each score level
        self.strategy = {
            'three_dice':roll{
                'two_5s':stop
                'two_1s':
                'one_1_and_one_5':
            },
            'four_dice':{
                'two_5s':
                'two_1s':
                'one_1_and_one_5':
            },
            'five_dice':{
                'two_5s':
                'two_1s':
                'one_1_and_one_5':
                'three_1s_or_three_3s_and_one_1_or_5':
                'three_2s_and_one_1_or_5':
                'three_4s_and_one_1_or_5':
                'three_5s_and_one_1_or_5':
                'lessthan100 and three_6s_and_one_1_or_5':
                'lessthan200 and three_6s_and_one_1_or_5':
                'lessthan300 and three_6s_and_one_1_or_5':
                'lessthan400 and three_6s_and_one_1_or_5':
                'lessthan500 and three_6s_and_one_1_or_5':
                'lessthan600 and three_6s_and_one_1_or_5':

            },
            'six_dice':{
                'two_5s':
                'two_1s':
                'one_1_and_one_5':
                'three_1s_or_three_3s_and_one_1_or_5':
                'three_2s_and_one_1_or_5':
                'three_4s_and_one_1_or_5':
                'three_5s_and_one_1_or_5':
                'three_6s_and_one_1_or_5':
                'three_1s_or_three_3s_and_two_1_or_5':
                'three_2s_and_two_1_or_5':
                'three_4s_and_two_1s_or_5s':
                'three_5s_and_two_1_or_5':
                'three_6s_and_two_1_or_5':
            },

            'roll_or_stop_thresholds':{1:0, 2:0, 3:0, 4:0, 5:0, 6:0}
        }

        def set_strategy(self, strategy):
            self.strategy = strategy
        
        def save_to_file(self, filename):
            f = open(filename, 'w')
            cPickle.dump(self.strategy, f)
            f.close()

        def load_from_file(self, filename):
            f = open(filename)
            self.strategy = cPickle.load(f)
            f.close()


class AIPlayer(object):
    def __init__(decision_tree):
        self.decisions_tree = AIDecisionMaker()
        self.
        self.name = str(uuid.uuid4())




    def take_turn(self, dice, scores):
        self.dice = dice

        self.get_move()

        
    def get_move(self):
        if len(self.dice == 6):



    def can_set_aside_all(self):
        if self.dice.find_n_of_a_kind(6, 



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


class GA
mutation_rate = 0.01
crossover_rate = 0.7
population = [Individual]
mating_pool = [Individual]

run()
do_crossover()
conduct_tournament()
fill_mating_pool()
evaluate_population()

class FarkleTournament
farkle_game

add_players()
run()

class Individual(object):
    def __init__(self):
        self.gene
Evaluate()






def main():
    farkle = Farkle()
    farkle.add_player(HumanPlayer())
    winner = farkle.play()
    print "The winner is player {0}!".format(winner)

if __name__ == "__main__":
    main()
