from newfarkle import Dice, DiceReporter
import unittest

class TestGame(unittest.TestCase):
    
    def test_dice(self):
        six_dice = Dice.roll(6)
        self.assertEquals(six_dice.count(), 6)

        set_dice = Dice.set_as((1, 2, 3, 4, 5, 6))
        counts = set_dice.get_counts()

        self.assertEquals(six_dice.count(), 6)
        self.assertEquals(counts, {1:1, 2:1, 3:1, 4:1, 5:1, 6:1})

        set_dice.add((1,2,3))
        self.assertEquals(set_dice.get_values(), (1,2,3,4,5,6,1,2,3))

        set_dice.remove((1,2,3,3))
        self.assertEquals(set_dice.get_values(), (4,5,6,1,2))

        self.assertRaises(ValueError, set_dice.remove, (1, 2, 3))
        self.assertEquals(set_dice.get_values(), (4,5,6,1,2))

        empty_case = Dice.set_as(())
        self.assertEquals(empty_case.get_values(), ())


    def test_reporter(self):
        self.assertEquals(DiceReporter(Dice.set_as((1, 2, 3, 4, 5, 6))).have_one_of_each(), True)
        self.assertEquals(DiceReporter(Dice.set_as((1, 1, 2, 2, 3, 3))).have_one_of_each(), False)

        self.assertEquals(DiceReporter(Dice.set_as((1, 1, 2, 2, 3, 3))).have_one_of_each(), False)

if __name__ == "__main__":
    unittest.main()
