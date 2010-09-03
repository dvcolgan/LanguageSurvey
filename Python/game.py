HumanPlayer

c

class Turn
class Dice

something creates a new game and tells the game to start

game state is - player 1 needs to roll

game passes roll request to player 1
player 1 is an AI, AI selects what to do from its tree
player 1 is a human
    command line interface prints a prompt and waits for keyboard
    gui updates label state or something and waits for the user to enter data



game controller - decides what to do next

def pit_players(AI1, AI2):
    manager = TurnManager(Game(), AI1, AI2)
    g.play()



class TurnManager:
    def __init__(self, p1, p2, game):
        self.p1 = p1
        self.p2 = p2
        self.game = game
        self.game.new_game()

    def take_turn(self):
        self.p1.











import random

class HumanPlayer: pass
    def __init__(self):


class AIPlayer: pass

class CommandLineInterface: pass
    

class GUIInterface: pass


class IllegalSetAsideError(Exception): pass

class FarkleGame:
    def __init__(self):
        self.new_game()

    def new_game(self):
        self._roll = []
        self._set_aside = []
        self._p1_score = 0
        self._p2_score = 0

    def get_roll(self):
        return tuple(self._roll)

    def get_set_aside(self):
        return tuple(self._set_aside)

    def get_scores(self):
        return (self._p1_score, self._p2_score)

    def roll(self):
        self._roll = [random.randint(1,6) for x in range(6-len(self._set_aside))]

    def set_aside(self, ones_to_keep):
        keepers = []
        updated_roll = []

        for die, keep in zip(self._roll, ones_to_keep):
            if keep: keepers.append(die)
        if self.calculate_combos_score(keepers) > 0:
            for die, keep in zip(self._roll, ones_to_keep):
                if keep:
                    self._set_aside.append(die)
                else:
                    updated_roll.append(die)
                self._roll = updated_roll
        else:
            raise IllegalSetAsideError()

    def calculate_combos_score(self, dice):
        score = 0
        dice = self._sort_by_occurences(dice)

        if len(dice) == 6 and [dice[0]]*6 == dice:  #six of a kind
            score += 3000
            dice = ()

        if len(dice) == 6 and [dice[0]]*3 + [dice[3]]*3 == dice:  #two triplets
            score += 2500
            dice = ()

        if len(dice) == 6 and [dice[0]]*4 + [dice[4]]*2 == dice:  #four with a pair
            score += 1500
            dice = ()

        if len(dice) == 6 and sorted(dice) == [1,2,3,4,5,6]:  #straight
            score += 1500
            dice = ()

        if len(dice) == 6 and [dice[0]]*2 + [dice[2]]*2 + [dice[4]]*2 == dice: #three pairs
            score += 1500
            dice = ()

        if len(dice) >= 5 and [dice[0]]*5 == dice[:5]: #five of a kind
            score += 2000
            dice = dice[5:]

        if len(dice) >= 4 and [dice[0]]*4 == dice[:4]: #four of a kind
            score += 1000
            dice = dice[4:]

        #three of a kinds
        if len(dice) >= 3 and [dice[0]]*3 == dice[:3]:
            if dice[0] == 1:
                score += 300
            else:
                score += dice[0]*100
            dice = dice[3:]

        ones = 0
        fives = 0
        for die in dice:
            if die == 1: ones += 1
            if die == 5: fives += 1
        for one in range(ones):
            score += 100
            dice.remove(1)
        for five in range(fives):
            score += 50
            dice.remove(5)

        return score

    def _sort_by_occurences(self, dice):
        newdice = []
        occurences = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0}
        for die in dice:
            occurences[die] += 1

        while 1:
            largest_num = 0
            largest_cnt = 0
            for die, cnt in occurences.iteritems():
                if cnt > largest_cnt:
                    largest_num = die
                    largest_cnt = cnt
            if largest_cnt == 0: break
            newdice.extend([largest_num]*largest_cnt)
            del occurences[largest_num]

        return newdice


if __name__ == "__main__":
    g = FarkleGame()
    print g.calculate_combos_score((2,2,2))

#class FarkleState:
#    def __init__(self):
#        self.dice
#
#def canSetAsideAll(game):
#
#
#
#
#class MatingPool:
#    pass
#
#class Individual:
#    def mutate():
#        pass
#    def evaluate():
#        pass
#    def
#
#class 
