#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from Equation import Expression


class TestEquation(unittest.TestCase):
    """Test example in README.md"""
    def setUp(self):
        self.fn = Expression("sin(x+y^2)", ["y","x"])

    def testCall(self):
        self.assertAlmostEqual(
            self.fn(3, 4),
            0.149877209662952
        )

    def tearDown(self):
        pass


class TestAddEquation(unittest.TestCase):
    def setUp(self):
        self.fn = Expression("x + y")

    def testCall(self):
        self.assertEqual(self.fn(1, 0), 1)
        self.assertEqual(self.fn(1, 1), 2)
        self.assertEqual(self.fn(2, 1), 3)
        self.assertEqual(self.fn(3, 1), 4)
        self.assertEqual(self.fn(15, 3), 18)

    def testType(self):
        self.assertEqual(type(self.fn(1, 2)), int)
        self.assertEqual(type(self.fn(1.0, 2.0)), float)
        self.assertEqual(type(self.fn(1, 2.0)), float)

    def tearDown(self):
        pass


class TestAndEquation(unittest.TestCase):
    def setUp(self):
        self.fn = Expression("x & y")

    def testCall(self):
        self.assertEqual(self.fn(1, 0), 0)
        self.assertEqual(self.fn(1, 1), 1)
        self.assertEqual(self.fn(2, 1), 0)
        self.assertEqual(self.fn(3, 1), 1)
        self.assertEqual(self.fn(15, 3), 3)

    def testType(self):
        self.assertEqual(type(self.fn(1, 2)), int)
        self.assertRaises(TypeError, self.fn, 1.0, 2)

    def tearDown(self):
        pass


class TestOrEquation(unittest.TestCase):
    def setUp(self):
        self.fn = Expression("x | y")

    def testCall(self):
        self.assertEqual(self.fn(1, 0), 1)
        self.assertEqual(self.fn(1, 1), 1)
        self.assertEqual(self.fn(2, 1), 3)
        self.assertEqual(self.fn(3, 1), 3)
        self.assertEqual(self.fn(15, 3), 15)

    def testType(self):
        self.assertEqual(type(self.fn(1, 2)), int)
        self.assertRaises(TypeError, self.fn, 1.0, 2)

    def tearDown(self):
        pass



class TestNotEquation(unittest.TestCase):
    def setUp(self):
        self.fn = Expression("!x")

    def testCall(self):
        self.assertFalse(self.fn(1))
        self.assertTrue(self.fn(0))
        self.assertFalse(self.fn(10))
        self.assertFalse(self.fn(True))
        self.assertTrue(self.fn(False))
        self.assertFalse(self.fn("string content"))
        self.assertTrue(self.fn(None))
        self.assertEqual(type(self.fn(True)), bool)
        self.assertEqual(type(self.fn(0)), bool)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
