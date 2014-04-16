"""
  Copyright 2014 AlphaOmega Technology

  Licensed under the AlphaOmega Technology Open License Version 1.0
  You may not use this file except in compliance with this License.
  You may obtain a copy of the License at
 
      http://www.alphaomega-technology.com.au/license/AOT-OL/1.0

"""
__authors__   = "Glen Fletcher"
__copyright__ = "(c) 2014, AlphaOmega Technology"
__license__   = "AlphaOmega Technology Open License Version 1.0"
__contact__   = "Glen Fletcher <glen.fletcher@alphaomega-technology.com.au>"

try:
    import numpy as np
    has_numpy = True
except ImportError:
    import math
    has_numpy = False
import operator as op
from Equation.util import addOp, addFn, addConst, addUnaryOp

def equation_extend():
    addOp('+',"({0:s} + {1:s})","\\left({0:s} + {1:s}\\right)",False,1,op.add)
    addOp('-',"({0:s} - {1:s})","\\left({0:s} - {1:s}\\right)",False,1,op.sub)
    addOp('*',"({0:s} * {1:s})","\\left({0:s} \\times {1:s}\\right)",False,2,op.mul)
    addOp('/',"({0:s} / {1:s})","\\frac{{{0:s}}}{{{1:s}}}",False,2,op.div)
    addOp('%',"({0:s} % {1:s})","\\left({0:s} \\bmod {1:s}\\right)",False,2,op.mod)
    addOp('^',"({0:s} ^ {1:s})","{0:s}^{{{1:s}}}",False,3,op.pow)
    addOp('&',"({0:s} & {1:s})","\\left({0:s} \\land {1:s}\\right)",False,1,op.amd_)
    addOp('|',"({0:s} | {1:s})","\\left({0:s} \\lor {1:s}\\right)",False,1,op.or_)
    addUnaryOp('!',"(!{0:s})","\\not{{{0:s}}}",op.not_)
    addUnaryOp('-',"-{0:s}","-{0:s}",op.neg)
    addFn('abs',"abs({0:s})","\\left|{0:s}\\right|",1,op.abs)
    addFn('root',"root({0:s},{1:s})","\\sqrt[{1:s}]{{{0:s}}}",2,lambda a,b: a**(1/b))
    if has_numpy:
        addFn('sin',"sin({0:s})","\\sin\\left({0:s}\\right)",1,np.sin)
        addFn('cos',"cos({0:s})","\\cos\\left({0:s}\\right)",1,np.cos)
        addFn('tan',"tan({0:s})","\\tan\\left({0:s}\\right)",1,np.tan)
        addFn('re',"re({0:s})","Re\\left({0:s}\\right)",1,np.real)
        addFn('im',"re({0:s})","Im\\left({0:s}\\right)",1,np.imag)
        addFn('sqrt',"sqrt({0:s})","\\sqrt{{{0:s}}}",1,np.sqrt)
        addConst("pi",np.pi)
        addConst("e",np.e)
        addConst("Inf",np.Inf)
        addConst("NaN",np.NaN)
    else:
        addFn('sin',"sin({0:s})","\\sin\\left({0:s}\\right)",1,math.sin)
        addFn('cos',"cos({0:s})","\\cos\\left({0:s}\\right)",1,math.cos)
        addFn('tan',"tan({0:s})","\\tan\\left({0:s}\\right)",1,math.tan)
        addFn('re',"re({0:s})","Re\\left({0:s}\\right)",1,complex.real)
        addFn('im',"re({0:s})","Im\\left({0:s}\\right)",1,complex.imag)
        addFn('sqrt',"sqrt({0:s})","\\sqrt{{{0:s}}}",1,math.sqrt)
        addConst("pi",math.pi)
        addConst("e",math.e)
        addConst("Inf",float("Inf"))
        addConst("NaN",float("NaN"))