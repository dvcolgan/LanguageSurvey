import random


class HumanPlayer(object):
    def __init__(self):
        pass

    def query_set_aside(self, remaining, set_aside, turn_score, total_scores):
        print "\n\nScores:\n"
        for i, score in enumerate(total_scores):
            print "Player {0}: {1}".format(i, score)

        print "Turn score: ", turn_score

        print "\nSet Aside:"
        print set_aside.get_values_as_string()

        print "\nYou roll the dice:"
        print remaining.get_values_as_string()

        choices = raw_input("\nIndicate the dice you want to set aside by entering their numbers separated by spaces, or enter nothing to stop.\n")

        return [int(choice) for choice in choices.split()]


    def query_stop(self, remaining, set_aside, turn_score, total_scores):
        choice = raw_input("You have {0} points.  Hit enter to continue rolling, or type 'stop' to end your turn.\n".format(turn_score))
        if choice == '':
            return False
        else:
            return True

    def warn_invalid_set_aside(self):
        print "That set aside is invalid!"


    
            

            

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
        dice.values = [random.randint(1,6) for die in range(count)]        
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


    def count(self):
        return len(self.values)

    def get_counts(self):
        die_counts = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0}
        for die in self.values:
            die_counts[die] += 1
        return die_counts

    def get_values(self):
        return tuple(self.values)

    def have_one_of_each(self):
        counts = self.get_counts()
        return all([counts[die] > 0 for die in range(1,7)])

    def get_values_as_string(self):
        return ' '.join([str(die) for die in self.get_values()])

    def is_valid_set_aside(self, dice_values):
        if not self.contains_values(dice_values): return False
        if self.get_score(zero_for_extra=True) == 0: return False
        return True

    def contains_values(self, dice_values):
        proposed_dice = list(dice_values)
        for die in self.get_values():
            if die in proposed_dice:
                proposed_dice.remove(die)
        return len(proposed_dice) == 0

    def is_farkle(self, dice_values):
        return self.get_score() == 0


    def find_n_of_a_kind(self, n, die_counts):
        matches = []
        for i in range(1,7):
            if die_counts[i] >= n:
                matches.append(i)
        return tuple(matches)
        
    def add(self, new_dice):
        self.values.extend(new_dice)

    def remove(self, dice_values):
        for die_value in dice_values:
            self.values.remove(die_value)


    def get_score(self, zero_for_extra=False):
        score = 0
        die_counts = self.get_counts()

        # four with a pair
        matches4, matches2 = self.find_n_of_a_kind(4, die_counts), self.find_n_of_a_kind(2, die_counts)
        if matches4 and matches2:
            score += 1500
            die_counts[matches4[0]] = die_counts[matches2[0]] = 0

        # two triplets
        matches = self.find_n_of_a_kind(3, die_counts)
        if len(matches) == 2:
            score += 2500
            die_counts[matches[0]] = die_counts[matches[1]] = 0

        # three pairs
        matches = self.find_n_of_a_kind(2, die_counts)
        if len(matches) == 3:
            score += 1500
            die_counts[matches[0]] = die_counts[matches[1]] = die_counts[matches[2]] = 0

        # strait
        if self.have_one_of_each():
            score += 1500
            for i in range(1,7):
                die_counts[i] = 0

        # 6, 5, 4, and 3 of a kind
        matches = self.find_n_of_a_kind(6, die_counts)
        if matches:
            score += 3000
            die_counts[matches[0]] = 0

        matches = self.find_n_of_a_kind(5, die_counts)
        if matches:
            score += 2000
            die_counts[matches[0]] = 0

        matches = self.find_n_of_a_kind(4, die_counts)
        if matches:
            score += 1000
            die_counts[matches[0]] = 0

        matches = self.find_n_of_a_kind(3, die_counts)
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

        if zero_for_extra and not all(die_counts.values()):
            return 0
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

        return turn_index

    def take_turn(self):
        player = self.players[self.turn_index]
        turn_score = 0
        set_aside = DiceFactory.set_as(())
        remaining = DiceFactory.set_as((1,1,1,1,1,1)) #junk value to initialize the number of dice

        while True:
            remaining = DiceFactory.rolled_dice(remaining.count())

            while True:
                proposed_set_aside = player.query_set_aside(remaining,
                                                            set_aside,
                                                            turn_score,
                                                            tuple(self.scores))

                if remaining.is_valid_set_aside(proposed_set_aside):
                    remaining.remove(proposed_set_aside)
                    set_aside.add(proposed_set_aside)
                    break
                else:
                    player.warn_invalid_set_aside()

            if player.query_stop(remaining, set_aside, turn_score, tuple(self.scores)):
                return score
            



def main():
    farkle = Farkle()
    farkle.add_player(HumanPlayer())
    winner = farkle.play()
    print "The winner is player {0}!".format(winner)

if __name__ == "__main__":
    main()
