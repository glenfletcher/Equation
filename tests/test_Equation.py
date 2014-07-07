#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import unittest
from Equation import Expression
import numpy as np

if sys.version_info >= (3,):
    xrange = range

class TestEquation(unittest.TestCase):
    """Test example in README.md"""
    def setUp(self):
        self.fn = Expression("sin(x+y^2)", ["y","x"])

    def testRepr(self):
        self.assertEqual(Expression(repr(self.fn)),self.fn)

    def testCall(self):
        self.assertAlmostEqual(
            self.fn(3, 4),
            0.420167036826641
        )
        self.assertAlmostEqual(
            self.fn(y=3, x=4),
            0.420167036826641
        )

    def tearDown(self):
        pass


class TestEquation2(unittest.TestCase):
    def setUp(self):
        self.fn = Expression("sin(x+y^2)")

    def testRepr(self):
        self.assertEqual(Expression(repr(self.fn)),self.fn)

    def testCall(self):
        self.assertAlmostEqual(
            self.fn(3, 4),
            0.149877209662952
        )
        self.assertAlmostEqual(
            self.fn(x=3, y=4),
            0.149877209662952
        )

    def tearDown(self):
        pass


class TestEquation3(unittest.TestCase):
    def setUp(self):
        self.fn = Expression("x+y^2")

    def testRepr(self):
        self.assertEqual(Expression(repr(self.fn)),self.fn)

    def testCall(self):
        self.assertEqual(self.fn(3, 4), 19)
        self.assertEqual(self.fn(x=3, y=4), 19)

    def tearDown(self):
        pass

class TestEmpty(unittest.TestCase):
    def setUp(self):
        self.fn = Expression("")

    def testRepr(self):
        self.assertEqual(repr(self.fn),"")

    def testStr(self):
        self.assertEqual(str(self.fn),"")

    def tearDown(self):
        pass

class TestComplexEquation(unittest.TestCase):
    def setUp(self):
        pass

    def testCall(self):
        for expr,value in [ ("-8-2j",(-8-2j)),
                            ("-(8+2j)",(-8-2j)),
                            ("- 8+2j",(-8+2j)),
                            ("-8-2i",(-8-2j)),
                            ("-(8+2i)",(-8-2j)),
                            ("- 8+2i",(-8+2j)),
                            ("- 8 + -2j",(-8-2j)),
                            ("-(8 + - 2j)",(-8+2j)),
                            ("- 8 + +2j",(-8+2j)),
                            ]:
            result = Expression(expr)()
            self.assertEqual(result,value,"Expression(\"{0:s}\")() = {1!r:s} not {2!r:s}".format(expr,result,value))

    def tearDown(self):
        pass

class TestHexEquation(unittest.TestCase):
    def setUp(self):
        pass

    def testCall(self):
        for n in xrange(-784323,294924,6831):
            if n < 0:
                hexstr = hex(n)[3:]
                prefix = "-0x"
            else:
                hexstr = hex(n)[2:]
                prefix = "0x"
            self.assertEqual(Expression(prefix + hexstr)(),n)
            self.assertEqual(Expression(prefix + hexstr.upper())(),n)

    def tearDown(self):
        pass

class TestOctEquation(unittest.TestCase):
    def setUp(self):
        pass

    def testCall(self):
        if sys.version_info >= (3,):
            l = 2
        else:
            l = 1
        for n in xrange(-784323,294924,6831):
            if n < 0:
                octstr = oct(n)[l+1:]
                prefix = "-0o"
            else:
                octstr = oct(n)[l:]
                prefix = "0o"
            self.assertEqual(Expression(prefix + octstr)(),n)

    def tearDown(self):
        pass

class TestBinEquation(unittest.TestCase):
    def setUp(self):
        pass

    def testCall(self):
        for n in xrange(-784323,294924,6831):
            if n < 0:
                binstr = bin(n)[3:]
                prefix = "-0b"
            else:
                binstr = bin(n)[2:]
                prefix = "0b"
            self.assertEqual(Expression(prefix + binstr)(),n)

class TestFloorEquation(unittest.TestCase):
    def setUp(self):
        self.fn = Expression("floor(x)")
        self.fn2 = Expression("floor(2*(sin(x*2*pi)+1))")

    def testCall(self):
        self.assertEqual(self.fn(3.4),3)
        self.assertEqual(self.fn(2.9),2)
        self.assertEqual(self.fn(1.0),1)
        self.assertEqual(self.fn(-1.2),-2)
        self.assertEqual(self.fn2(np.linspace(0,1,5)).tolist(),[ 2.,  4.,  2.,  0.,  1.])

    def tearDown(self):
        pass

class TestCeilEquation(unittest.TestCase):
    def setUp(self):
        self.fn = Expression("ceil(x)")
        self.fn2 = Expression("ceil(2*(sin(x*2*pi)+1))")

    def testCall(self):
        self.assertEqual(self.fn(3.4),4)
        self.assertEqual(self.fn(2.9),3)
        self.assertEqual(self.fn(1.0),1)
        self.assertEqual(self.fn(-1.2),-1)
        self.assertEqual(self.fn2(np.linspace(0,1,5)).tolist(),[ 2.,  4.,  3.,  0.,  2.])

    def tearDown(self):
        pass

class TestRoundEquation(unittest.TestCase):
    def setUp(self):
        self.fn = Expression("round(x)")
        self.fn2 = Expression("round(2*(sin(x*2*pi)+1))")

    def testCall(self):
        self.assertEqual(self.fn(3.4),3)
        self.assertEqual(self.fn(2.9),3)
        self.assertEqual(self.fn(1.0),1)
        self.assertEqual(self.fn(-1.2),-1)
        self.assertEqual(self.fn(-1.5),-2)
        self.assertEqual(self.fn(1.5),2)
        self.assertEqual(self.fn2(np.linspace(0,1,5)).tolist(),[ 2.,  4.,  2.,  0.,  2.])

    def tearDown(self):
        pass

class TestAddEquation(unittest.TestCase):
    def setUp(self):
        self.fn = Expression("x + y")

    def testRepr(self):
        self.assertEqual(Expression(repr(self.fn)),self.fn)

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

class TestSubtractEquation(unittest.TestCase):
    def setUp(self):
        self.fn = Expression("x - y")

    def testRepr(self):
        self.assertEqual(Expression(repr(self.fn)),self.fn)

    def testCall(self):
        self.assertEqual(self.fn(1, 0), 1)
        self.assertEqual(self.fn(1, 1), 0)
        self.assertEqual(self.fn(2, 1), 1)
        self.assertEqual(self.fn(3, 1), 2)
        self.assertEqual(self.fn(15, 3), 12)

    def testType(self):
        self.assertEqual(type(self.fn(1, 2)), int)
        self.assertEqual(type(self.fn(1.0, 2.0)), float)
        self.assertEqual(type(self.fn(1, 2.0)), float)

    def tearDown(self):
        pass

class TestMultiplyEquation(unittest.TestCase):
    def setUp(self):
        self.fn = Expression("x * y")

    def testRepr(self):
        self.assertEqual(Expression(repr(self.fn)),self.fn)

    def testCall(self):
        self.assertEqual(self.fn(1, 0), 0)
        self.assertEqual(self.fn(1, 1), 1)
        self.assertEqual(self.fn(2, 1), 2)
        self.assertEqual(self.fn(3, 1), 3)
        self.assertEqual(self.fn(15, 3), 45)

    def testType(self):
        self.assertEqual(type(self.fn(1, 2)), int)
        self.assertEqual(type(self.fn(1.0, 2.0)), float)
        self.assertEqual(type(self.fn(1, 2.0)), float)

    def tearDown(self):
        pass

class TestPowerEquation(unittest.TestCase):
    def setUp(self):
        self.fn = Expression("x ^ y")

    def testRepr(self):
        self.assertEqual(Expression(repr(self.fn)),self.fn)

    def testCall(self):
        self.assertEqual(self.fn(1, 0), 1)
        self.assertEqual(self.fn(1, 1), 1)
        self.assertEqual(self.fn(2, 2), 4)
        self.assertEqual(self.fn(2, 0), 1)
        self.assertEqual(self.fn(3, 2), 9)
        self.assertEqual(self.fn(15, 3), 3375)

    def testType(self):
        self.assertEqual(type(self.fn(1, 2)), int)
        self.assertEqual(type(self.fn(1.0, 2.0)), float)
        self.assertEqual(type(self.fn(1, 2.0)), float)

    def tearDown(self):
        pass

class TestDivisionEquation(unittest.TestCase):
    def setUp(self):
        self.fn = Expression("x / y")

    def testRepr(self):
        self.assertEqual(Expression(repr(self.fn)),self.fn)

    def testCall(self):
        self.assertEqual(self.fn(0, 1), 0)
        self.assertEqual(self.fn(1, 1), 1)
        self.assertEqual(self.fn(2, 1), 2)
        self.assertEqual(self.fn(3, 1), 3)
        self.assertEqual(self.fn(15, 3), 5)
        self.assertRaises(ZeroDivisionError,self.fn,1,0)

    def testType(self):
        self.assertEqual(type(self.fn(1, 2)), float)
        self.assertEqual(type(self.fn(1.0, 2.0)), float)
        self.assertEqual(type(self.fn(1, 2.0)), float)

    def tearDown(self):
        pass

class TestAndEquation(unittest.TestCase):
    def setUp(self):
        self.fn = Expression("x & y")

    def testRepr(self):
        self.assertEqual(Expression(repr(self.fn)),self.fn)

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

    def testRepr(self):
        self.assertEqual(Expression(repr(self.fn)),self.fn)

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

    def testRepr(self):
        self.assertEqual(Expression(repr(self.fn)),self.fn)

    def testCall(self):
        self.assertFalse(self.fn(1))
        self.assertTrue(self.fn(0))
        self.assertFalse(self.fn(10))
        self.assertFalse(self.fn(True))
        self.assertTrue(self.fn(False))
        self.assertFalse(self.fn("string content"))
        self.assertTrue(self.fn(None))

    def testType(self):
        self.assertEqual(type(self.fn(True)), bool)
        self.assertEqual(type(self.fn(0)), bool)

    def tearDown(self):
        pass

class TestNegEquation(unittest.TestCase):
    def setUp(self):
        self.fn = Expression("-x")

    def testRepr(self):
        self.assertEqual(Expression(repr(self.fn)),self.fn)

    def testCall(self):
        self.assertEqual(self.fn(1),-1)
        self.assertEqual(self.fn(6+3j),(-6-3j))

    def tearDown(self):
        pass

class TestEqualsEquation(unittest.TestCase):
    def setUp(self):
        self.fn = Expression("x == y")

    def testRepr(self):
        self.assertEqual(Expression(repr(self.fn)),self.fn)

    def testCall(self):
        self.assertFalse(self.fn(1, 0))
        self.assertTrue(self.fn(0, 0))
        self.assertFalse(self.fn(10, 0))
        self.assertFalse(self.fn(1.0, 0))
        self.assertTrue(self.fn(1.0, 1.0))
        self.assertFalse(self.fn(True, False))
        self.assertTrue(self.fn(False, False))
        self.assertTrue(self.fn("string content", "string content"))
        self.assertFalse(self.fn("string content", "different string"))
        self.assertTrue(self.fn(None, None))

    def testType(self):
        self.assertEqual(type(self.fn(1, 1)), bool)
        self.assertTrue(self.fn(1, 1.0))

    def tearDown(self):
        pass


class TestSimilarEquation(unittest.TestCase):
    def setUp(self):
        self.fn = Expression("x ~ y")

    def testRepr(self):
        self.assertEqual(Expression(repr(self.fn)),self.fn)

    def testCall(self):
        # Only use values close to 1
        # floating point error may caluse failure for large expoents
        # i.e. for 10000 (1-(a(1-1e-5))/a)=1.0000000000065512e-05
        # This is floating due to folating point error
        for a in [0.001,1,1.5,4,100,1000]:
            ge = a*(1+1e-5)
            le = a*(1-1e-5)
            gt = a*(1+1.1e-5)
            lt = a*(1-1.1e-5)
            self.assertTrue(self.fn(a,ge),"{0:g} ~ {1:g}, is False".format(a,ge))
            self.assertTrue(self.fn(a,le),"{0:g} ~ {1:g}, is False".format(a,le))
            self.assertFalse(self.fn(a,gt),"{0:g} ~ {1:g}, is True".format(a,gt))
            self.assertFalse(self.fn(a,lt),"{0:g} ~ {1:g}, is True".format(a,lt))

    def testType(self):
        self.assertEqual(type(self.fn(1, 1)), bool)
        self.assertTrue(self.fn(1, 1.0))

    def tearDown(self):
        pass

class TestNotEqualsEquation(unittest.TestCase):
    def setUp(self):
        self.fn = Expression("x != y")

    def testRepr(self):
        self.assertEqual(Expression(repr(self.fn)),self.fn)

    def testCall(self):
        self.assertTrue(self.fn(1, 0))
        self.assertFalse(self.fn(0, 0))
        self.assertTrue(self.fn(10, 0))
        self.assertTrue(self.fn(1.0, 0))
        self.assertFalse(self.fn(1.0, 1.0))
        self.assertTrue(self.fn(True, False))
        self.assertFalse(self.fn(False, False))
        self.assertFalse(self.fn("string content", "string content"))
        self.assertTrue(self.fn("string content", "different string"))
        self.assertFalse(self.fn(None, None))

    def testType(self):
        self.assertEqual(type(self.fn(1, 1)), bool)
        self.assertFalse(self.fn(1, 1.0))

    def tearDown(self):
        pass

class TestNotSimilarEquation(unittest.TestCase):
    def setUp(self):
        self.fn = Expression("x !~ y")

    def testRepr(self):
        self.assertEqual(Expression(repr(self.fn)),self.fn)

    def testCall(self):
        # Only use values close to 1
        # floating point error may caluse failure for large expoents
        # i.e. for 10000 (1-(a(1-1e-5))/a)=1.0000000000065512e-05
        # This is floating due to folating point error
        for a in [0.001,1,1.5,4,100,1000]:
            ge = a*(1+1e-5)
            le = a*(1-1e-5)
            gt = a*(1+1.1e-5)
            lt = a*(1-1.1e-5)
            self.assertFalse(self.fn(a,ge),"{0:g} !~ {1:g}, is True".format(a,ge))
            self.assertFalse(self.fn(a,le),"{0:g} !~ {1:g}, is True".format(a,le))
            self.assertTrue(self.fn(a,gt),"{0:g} !~ {1:g}, is False".format(a,gt))
            self.assertTrue(self.fn(a,lt),"{0:g} !~ {1:g}, is False".format(a,lt))

    def testType(self):
        self.assertEqual(type(self.fn(1, 1)), bool)
        self.assertFalse(self.fn(1, 1.0))

    def tearDown(self):
        pass


class TestGreaterThanEquation(unittest.TestCase):
    def setUp(self):
        self.fn = Expression("x > y")

    def testRepr(self):
        self.assertEqual(Expression(repr(self.fn)),self.fn)

    def testCall(self):
        self.assertTrue(self.fn(1, 0))
        self.assertFalse(self.fn(0, 0))
        self.assertFalse(self.fn(0, 1))
        self.assertFalse(self.fn(-2, -1))
        self.assertTrue(self.fn(10, 0))
        self.assertTrue(self.fn(True, False))
        self.assertFalse(self.fn(False, True))
        self.assertFalse(self.fn(False, False))
        self.assertFalse(self.fn("string content", "string content"))
        self.assertTrue(self.fn("string content", "string alphabetically earlier"))

    def testType(self):
        self.assertEqual(type(self.fn(1, 1)), bool)
        self.assertFalse(self.fn(1, 1.0))

    def tearDown(self):
        pass

class TestGreaterThanOrEqualToEquation(unittest.TestCase):
    def setUp(self):
        self.fn = Expression("x >= y")

    def testRepr(self):
        self.assertEqual(Expression(repr(self.fn)),self.fn)

    def testCall(self):
        self.assertTrue(self.fn(1, 0))
        self.assertTrue(self.fn(0, 0))
        self.assertFalse(self.fn(0, 1))
        self.assertFalse(self.fn(-2, -1))
        self.assertTrue(self.fn(10, 0))
        self.assertTrue(self.fn(True, False))
        self.assertFalse(self.fn(False, True))
        self.assertTrue(self.fn(False, False))
        self.assertTrue(self.fn("string content", "string content"))
        self.assertTrue(self.fn("string content", "string alphabetically earlier"))

    def testType(self):
        self.assertEqual(type(self.fn(1, 1)), bool)
        self.assertTrue(self.fn(1, 1.0))


class TestGreaterThanOrSimilarToEquation(unittest.TestCase):
    def setUp(self):
        self.fn = Expression("x >~ y")

    def testRepr(self):
        self.assertEqual(Expression(repr(self.fn)),self.fn)

    def testCall(self):
        # Only use values close to 1
        # floating point error may caluse failure for large expoents
        # i.e. for 10000 (1-(a(1-1e-5))/a)=1.0000000000065512e-05
        # This is floating due to folating point error
        for a in [0.001,1,1.5,4,100,1000]:
            ge = a*(1+1e-5)
            le = a*(1-1e-5)
            gt = a*(1+1.1e-5)
            lt = a*(1-1.1e-5)
            self.assertTrue(self.fn(a,ge),"{0:g} >~ {1:g}, is False".format(a,ge))
            self.assertTrue(self.fn(a,le),"{0:g} >~ {1:g}, is False".format(a,le))
            self.assertFalse(self.fn(a,gt),"{0:g} >~ {1:g}, is True".format(a,gt))
            self.assertTrue(self.fn(a,lt),"{0:g} >~ {1:g}, is False".format(a,lt))

    def testType(self):
        self.assertEqual(type(self.fn(1, 1)), bool)
        self.assertTrue(self.fn(1, 1.0))

    def tearDown(self):
        pass

class TestLessThanEquation(unittest.TestCase):
    def setUp(self):
        self.fn = Expression("x < y")

    def testRepr(self):
        self.assertEqual(Expression(repr(self.fn)),self.fn)

    def testCall(self):
        self.assertFalse(self.fn(1, 0))
        self.assertFalse(self.fn(0, 0))
        self.assertTrue(self.fn(0, 1))
        self.assertTrue(self.fn(-2, -1))
        self.assertFalse(self.fn(10, 0))
        self.assertFalse(self.fn(True, False))
        self.assertTrue(self.fn(False, True))
        self.assertFalse(self.fn(False, False))
        self.assertFalse(self.fn("string content", "string content"))
        self.assertFalse(self.fn("string content", "string alphabetically earlier"))

    def testType(self):
        self.assertEqual(type(self.fn(1, 1)), bool)
        self.assertFalse(self.fn(1, 1.0))

class TestLessThanOrEqualToEquation(unittest.TestCase):
    def setUp(self):
        self.fn = Expression("x <= y")

    def testRepr(self):
        self.assertEqual(Expression(repr(self.fn)),self.fn)

    def testCall(self):
        self.assertFalse(self.fn(1, 0))
        self.assertTrue(self.fn(0, 0))
        self.assertTrue(self.fn(0, 1))
        self.assertTrue(self.fn(-2, -1))
        self.assertFalse(self.fn(10, 0))
        self.assertFalse(self.fn(True, False))
        self.assertTrue(self.fn(False, True))
        self.assertTrue(self.fn(False, False))
        self.assertTrue(self.fn("string content", "string content"))
        self.assertFalse(self.fn("string content", "string alphabetically earlier"))

    def testType(self):
        self.assertEqual(type(self.fn(1, 1)), bool)
        self.assertTrue(self.fn(1, 1.0))

    def tearDown(self):
        pass


class TestLessThanOrSimilarToEquation(unittest.TestCase):
    def setUp(self):
        self.fn = Expression("x <~ y")

    def testRepr(self):
        self.assertEqual(Expression(repr(self.fn)),self.fn)

    def testCall(self):
        # Only use values close to 1
        # floating point error may caluse failure for large expoents
        # i.e. for 10000 (1-(a(1-1e-5))/a)=1.0000000000065512e-05
        # This is floating due to folating point error
        for a in [0.001,1,1.5,4,100,1000]:
            ge = a*(1+1e-5)
            le = a*(1-1e-5)
            gt = a*(1+1.1e-5)
            lt = a*(1-1.1e-5)
            self.assertTrue(self.fn(a,ge),"{0:g} <~ {1:g}, is False".format(a,ge))
            self.assertTrue(self.fn(a,le),"{0:g} <~ {1:g}, is False".format(a,le))
            self.assertTrue(self.fn(a,gt),"{0:g} <~ {1:g}, is False".format(a,gt))
            self.assertFalse(self.fn(a,lt),"{0:g} <~ {1:g}, is True".format(a,lt))

    def testType(self):
        self.assertEqual(type(self.fn(1, 1)), bool)
        self.assertTrue(self.fn(1, 1.0))

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
