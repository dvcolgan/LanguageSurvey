from farkle import Dice, DiceFactory
from ga import SequenceProblem
import unittest

class TestGame(unittest.TestCase):
    def setUp(self):
        pass


    def test_contains_three_of_a_kind_and_two_others(self):
        self.assertEquals(
                DiceFactory.set_as((1,2,2,5,4,2)
                                  ).contains_three_of_a_kind_and_two_others(2),
                          True)
        self.assertEquals(
                DiceFactory.set_as((4,4,2,2,2,2)
                                  ).contains_three_of_a_kind_and_two_others(2),
                          False)
        self.assertEquals(
                DiceFactory.set_as((1,1,1,1,2,2)
                                  ).contains_three_of_a_kind_and_two_others(1),
                          False)
        self.assertEquals(
                DiceFactory.set_as((5,5,1,5,1,2)
                                  ).contains_three_of_a_kind_and_two_others(5),
                          True)
        self.assertEquals(
                DiceFactory.set_as((6,6,1,6,1,2)
                                  ).contains_three_of_a_kind_and_two_others(6),
                          True)
        self.assertEquals(
                DiceFactory.set_as((3,6,1,6,2,2)
                                  ).contains_three_of_a_kind_and_two_others(6),
                          False)


    def test_contains_three_of_a_kind_and_one_other(self):
        self.assertEquals(
                DiceFactory.set_as((1,2,2,3,4,2)
                                  ).contains_three_of_a_kind_and_one_other(2),
                          True)
        self.assertEquals(
                DiceFactory.set_as((4,4,2,2,2,2)
                                  ).contains_three_of_a_kind_and_one_other(2),
                          False)
        self.assertEquals(
                DiceFactory.set_as((1,1,1,1,2,2)
                                  ).contains_three_of_a_kind_and_one_other(1),
                          False)
        self.assertEquals(
                DiceFactory.set_as((5,5,1,5,2,2)
                                  ).contains_three_of_a_kind_and_one_other(5),
                          True)
        self.assertEquals(
                DiceFactory.set_as((6,6,1,6,2,2)
                                  ).contains_three_of_a_kind_and_one_other(6),
                          True)
        self.assertEquals(
                DiceFactory.set_as((3,6,1,6,2,2)
                                  ).contains_three_of_a_kind_and_one_other(6),
                          False)

    def test_all_dice_score(self):
        self.assertEquals(
                DiceFactory.set_as((1,2,2,3,4,2)
                                  ).all_dice_score(),
                          False)
        self.assertEquals(
                DiceFactory.set_as((4,4,2,2,2,2)
                                  ).all_dice_score(),
                          True)
        self.assertEquals(
                DiceFactory.set_as((1,1,5,2,2,2)
                                  ).all_dice_score(),
                          True)
        

    def test_contains_only_three_of_a_kind(self):
        self.assertEquals(
                DiceFactory.set_as((1,2,2,3,4,2)
                                  ).contains_only_three_of_a_kind(),
                          False)
        self.assertEquals(
                DiceFactory.set_as((6,2,2,3,4,2)
                                  ).contains_only_three_of_a_kind(),
                          True)
        self.assertEquals(
                DiceFactory.set_as((6,6,2,3,4,2)
                                  ).contains_only_three_of_a_kind(),
                          False)


    def test_contains_n_or_more_of_a_kind(self):
        self.assertEquals(
                DiceFactory.set_as((1,2,2,3,4,2)
                                  ).contains_n_or_more_of_a_kind(3),
                          True)
        self.assertEquals(
                DiceFactory.set_as((1,4,2,3,4,2)
                                  ).contains_n_or_more_of_a_kind(3),
                          False)

    def test_contains_one_scoring_die(self):
        self.assertEquals(
                DiceFactory.set_as((1,2,6,3,4,2)).contains_one_scoring_die(),
                True)
        self.assertEquals(
                DiceFactory.set_as((1,5,2,3,4,2)).contains_one_scoring_die(),
                False)
        self.assertEquals(
                DiceFactory.set_as((3,4,2,3,4,2)).contains_one_scoring_die(),
                False)

    def test_sequence_problem(self):
        m = SequenceProblem()
        self.assertEquals(m.run_tournament(range(10), [9,7,5,4,2,1,6,7,4,8]), range(10))
        self.assertEquals(m.run_tournament([0,0,0,0,0,0,0,0,0,0], [0,1,0,0,0,0,0,0,0,0]), [0,1,0,0,0,0,0,0,0,0])


    def test_scoring(self):
        self.assertEquals(DiceFactory.set_as((1,)).get_score(), 100)
        self.assertEquals(DiceFactory.set_as((5,)).get_score(), 50)
        self.assertEquals(DiceFactory.set_as((2,)).get_score(), 0)
        self.assertEquals(DiceFactory.set_as((3,)).get_score(), 0)
        self.assertEquals(DiceFactory.set_as((4,)).get_score(), 0)
        self.assertEquals(DiceFactory.set_as((6,)).get_score(), 0)
        self.assertEquals(DiceFactory.set_as((1,5)).get_score(), 150)
        self.assertEquals(DiceFactory.set_as((1,1)).get_score(), 200)
        self.assertEquals(DiceFactory.set_as((5,5)).get_score(), 100)
        self.assertEquals(DiceFactory.set_as((2,3)).get_score(), 0)
        self.assertEquals(DiceFactory.set_as((4,6)).get_score(), 0)
        self.assertEquals(DiceFactory.set_as((1,1,1)).get_score(), 300)
        self.assertEquals(DiceFactory.set_as((2,2,2)).get_score(), 200)
        self.assertEquals(DiceFactory.set_as((3,3,3)).get_score(), 300)
        self.assertEquals(DiceFactory.set_as((4,4,4)).get_score(), 400)
        self.assertEquals(DiceFactory.set_as((5,5,5)).get_score(), 500)
        self.assertEquals(DiceFactory.set_as((6,6,6)).get_score(), 600)
        self.assertEquals(DiceFactory.set_as((2,3,4)).get_score(), 0)
        self.assertEquals(DiceFactory.set_as((1,5,6)).get_score(), 150)
        self.assertEquals(DiceFactory.set_as((3,5,6)).get_score(), 50)
        self.assertEquals(DiceFactory.set_as((1,1,1,1)).get_score(), 1000)
        self.assertEquals(DiceFactory.set_as((2,2,2,2)).get_score(), 1000)
        self.assertEquals(DiceFactory.set_as((3,3,3,3)).get_score(), 1000)
        self.assertEquals(DiceFactory.set_as((4,4,4,4)).get_score(), 1000)
        self.assertEquals(DiceFactory.set_as((5,5,5,5)).get_score(), 1000)
        self.assertEquals(DiceFactory.set_as((6,6,6,6)).get_score(), 1000)
        self.assertEquals(DiceFactory.set_as((6,6,6,1)).get_score(), 700)
        self.assertEquals(DiceFactory.set_as((4,4,4,5)).get_score(), 450)
        self.assertEquals(DiceFactory.set_as((3,3,3,4)).get_score(), 300)
        self.assertEquals(DiceFactory.set_as((1,2,3,4)).get_score(), 100)
        self.assertEquals(DiceFactory.set_as((3,4,5,6)).get_score(), 50)
        self.assertEquals(DiceFactory.set_as((2,3,4,6)).get_score(), 0)
        self.assertEquals(DiceFactory.set_as((1,1,1,1,1)).get_score(), 2000)
        self.assertEquals(DiceFactory.set_as((2,2,2,2,2)).get_score(), 2000)
        self.assertEquals(DiceFactory.set_as((3,3,3,3,3)).get_score(), 2000)
        self.assertEquals(DiceFactory.set_as((4,4,4,4,4)).get_score(), 2000)
        self.assertEquals(DiceFactory.set_as((5,5,5,5,5)).get_score(), 2000)
        self.assertEquals(DiceFactory.set_as((6,6,6,6,6)).get_score(), 2000)
        self.assertEquals(DiceFactory.set_as((1,1,1,1,1,1)).get_score(), 3000)
        self.assertEquals(DiceFactory.set_as((2,2,2,2,2,2)).get_score(), 3000)
        self.assertEquals(DiceFactory.set_as((3,3,3,3,3,3)).get_score(), 3000)
        self.assertEquals(DiceFactory.set_as((4,4,4,4,4,4)).get_score(), 3000)
        self.assertEquals(DiceFactory.set_as((5,5,5,5,5,5)).get_score(), 3000)
        self.assertEquals(DiceFactory.set_as((6,6,6,6,6,6)).get_score(), 3000)
        self.assertEquals(DiceFactory.set_as((1,1,1,2,2,2)).get_score(), 2500)
        self.assertEquals(DiceFactory.set_as((3,3,3,4,4,4)).get_score(), 2500)
        self.assertEquals(DiceFactory.set_as((5,5,5,6,6,6)).get_score(), 2500)
        self.assertEquals(DiceFactory.set_as((1,1,2,2,3,3)).get_score(), 1500)
        self.assertEquals(DiceFactory.set_as((4,4,5,5,6,6)).get_score(), 1500)
        self.assertEquals(DiceFactory.set_as((1,1,1,1,2,2)).get_score(), 1500)
        self.assertEquals(DiceFactory.set_as((3,3,3,3,4,4)).get_score(), 1500)
        self.assertEquals(DiceFactory.set_as((5,5,5,5,6,6)).get_score(), 1500)
        self.assertEquals(DiceFactory.set_as((5,5,4,5,6,6)).get_score(zero_for_extra=True), 0)
        self.assertEquals(DiceFactory.set_as((4,6)).get_score(zero_for_extra=True), 0)
        self.assertEquals(DiceFactory.set_as((1,5,4,6)).get_score(zero_for_extra=True), 0)
        self.assertEquals(DiceFactory.set_as((3,3,3,4)).get_score(zero_for_extra=True), 0)
        self.assertEquals(DiceFactory.set_as((1,2,3,4)).get_score(zero_for_extra=True), 0)
        self.assertEquals(DiceFactory.set_as((3,4,5,6)).get_score(zero_for_extra=True), 0)
        self.assertEquals(DiceFactory.set_as((2,3,4,6)).get_score(zero_for_extra=True), 0)
        self.assertEquals(DiceFactory.set_as((6, 2, 5, 2, 6, 4)).get_score(zero_for_extra=False), 50)

    def test_set_aside(self):
        remaining = DiceFactory.set_as((2,2,2,2,3,4))
        proposed_set_aside = DiceFactory.set_as((2,2,2,2))
        self.assertEquals(proposed_set_aside.is_valid_set_aside(remaining), True)

        remaining = DiceFactory.set_as((1,3,2,2,3,4))
        proposed_set_aside = DiceFactory.set_as((1,))
        self.assertEquals(proposed_set_aside.is_valid_set_aside(remaining), True)

if __name__ == "__main__":
    unittest.main()
