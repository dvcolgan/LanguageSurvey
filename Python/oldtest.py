import game
import unittest

class TestGame(unittest.TestCase):
    def setUp(self):

    def test_constructor(self):
        g = game.FarkleGame()
        self.assertEquals(g.get_roll(), (), "Roll is not empty!")
        self.assertEquals(g.get_set_aside(), (), "Set aside is not empty!")
        self.assertEquals(g.get_scores(), (0,0), "Scores not zero!")

    def test_roll_and_set_aside(self):
        g = game.FarkleGame()
        g.roll()
        roll = g.get_roll()
        self.assertEquals(len(roll), 6)
        g.set_aside((True, False, True, False, True, False))
        self.assertEquals(len(g.get_roll()), 3)
        self.assertEquals(len(g.get_set_aside()), 3)

    def test_calculate_combos_score(self):
        g = game.FarkleGame()
        self.assertEquals(g.calculate_combos_score([1]), 100)
        self.assertEquals(g.calculate_combos_score([5]), 50)
        self.assertEquals(g.calculate_combos_score([2]), 0)
        self.assertEquals(g.calculate_combos_score([3]), 0)
        self.assertEquals(g.calculate_combos_score([4]), 0)
        self.assertEquals(g.calculate_combos_score([6]), 0)

        self.assertEquals(g.calculate_combos_score([1,5]), 150)
        self.assertEquals(g.calculate_combos_score([1,1]), 200)
        self.assertEquals(g.calculate_combos_score([5,5]), 100)
        self.assertEquals(g.calculate_combos_score([2,3]), 0)
        self.assertEquals(g.calculate_combos_score([4,6]), 0)

        self.assertEquals(g.calculate_combos_score([1,1,1]), 300)
        self.assertEquals(g.calculate_combos_score([2,2,2]), 200)
        self.assertEquals(g.calculate_combos_score([3,3,3]), 300)
        self.assertEquals(g.calculate_combos_score([4,4,4]), 400)
        self.assertEquals(g.calculate_combos_score([5,5,5]), 500)
        self.assertEquals(g.calculate_combos_score([6,6,6]), 600)
        self.assertEquals(g.calculate_combos_score([2,3,4]), 0)
        self.assertEquals(g.calculate_combos_score([1,5,6]), 150)
        self.assertEquals(g.calculate_combos_score([3,5,6]), 50)

        self.assertEquals(g.calculate_combos_score([1,1,1,1]), 1000)
        self.assertEquals(g.calculate_combos_score([2,2,2,2]), 1000)
        self.assertEquals(g.calculate_combos_score([3,3,3,3]), 1000)
        self.assertEquals(g.calculate_combos_score([4,4,4,4]), 1000)
        self.assertEquals(g.calculate_combos_score([5,5,5,5]), 1000)
        self.assertEquals(g.calculate_combos_score([6,6,6,6]), 1000)
        self.assertEquals(g.calculate_combos_score([6,6,6,1]), 700)
        self.assertEquals(g.calculate_combos_score([4,4,4,5]), 450)
        self.assertEquals(g.calculate_combos_score([3,3,3,4]), 300)
        self.assertEquals(g.calculate_combos_score([1,2,3,4]), 100)
        self.assertEquals(g.calculate_combos_score([3,4,5,6]), 50)
        self.assertEquals(g.calculate_combos_score([2,3,4,6]), 0)

        self.assertEquals(g.calculate_combos_score([1,1,1,1,1]), 2000)
        self.assertEquals(g.calculate_combos_score([2,2,2,2,2]), 2000)
        self.assertEquals(g.calculate_combos_score([3,3,3,3,3]), 2000)
        self.assertEquals(g.calculate_combos_score([4,4,4,4,4]), 2000)
        self.assertEquals(g.calculate_combos_score([5,5,5,5,5]), 2000)
        self.assertEquals(g.calculate_combos_score([6,6,6,6,6]), 2000)

        self.assertEquals(g.calculate_combos_score([1,1,1,1,1,1]), 3000)
        self.assertEquals(g.calculate_combos_score([2,2,2,2,2,2]), 3000)
        self.assertEquals(g.calculate_combos_score([3,3,3,3,3,3]), 3000)
        self.assertEquals(g.calculate_combos_score([4,4,4,4,4,4]), 3000)
        self.assertEquals(g.calculate_combos_score([5,5,5,5,5,5]), 3000)
        self.assertEquals(g.calculate_combos_score([6,6,6,6,6,6]), 3000)

        self.assertEquals(g.calculate_combos_score([1,1,1,2,2,2]), 2500)
        self.assertEquals(g.calculate_combos_score([3,3,3,4,4,4]), 2500)
        self.assertEquals(g.calculate_combos_score([5,5,5,6,6,6]), 2500)

        self.assertEquals(g.calculate_combos_score([1,1,2,2,3,3]), 1500)
        self.assertEquals(g.calculate_combos_score([4,4,5,5,6,6]), 1500)

        self.assertEquals(g.calculate_combos_score([1,1,1,1,2,2]), 1500)
        self.assertEquals(g.calculate_combos_score([3,3,3,3,4,4]), 1500)
        self.assertEquals(g.calculate_combos_score([5,5,5,5,6,6]), 1500)

if __name__ == "__main__":
    unittest.main()
