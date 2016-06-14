import unittest
from multiobjective_fitness import MultiobjectiveFitness

class TestMultiObjectiveFitness(unittest.TestCase):

    def test_ops(self):
        a = MultiobjectiveFitness((1,2))
        b = MultiobjectiveFitness((1,3))
        c = MultiobjectiveFitness((0,4))
        d = MultiobjectiveFitness((2,8))

        self.assertTrue(b>a)
        self.assertFalse(c<a)
        self.assertTrue(b<d)