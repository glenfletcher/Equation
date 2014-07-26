# -*- coding: utf-8 -*-
#==============================================================================
#   Copyright 2014 AlphaOmega Technology
#
#   Licensed under the AlphaOmega Technology Open License Version 1.0
#   You may not use this file except in compliance with this License.
#   You may obtain a copy of the License at
#
#       http://www.alphaomega-technology.com.au/license/AOT-OL/1.0
#==============================================================================

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
from Equation.similar import sim, nsim, gsim, lsim

def equation_extend():
    def product(*args):
        if len(args) == 1 and has_numpy:
            return np.prod(args[0])
        else:
            return reduce(op.mul,args,1)

    def sumargs(*args):
        if len(args) == 1:
            return sum(args[0])
        else:
            return sum(args)

    addOp('+',"({0:s} + {1:s})","\\left({0:s} + {1:s}\\right)",False,3,op.add)
    addOp('-',"({0:s} - {1:s})","\\left({0:s} - {1:s}\\right)",False,3,op.sub)
    addOp('*',"({0:s} * {1:s})","\\left({0:s} \\times {1:s}\\right)",False,2,op.mul)
    addOp('/',"({0:s} / {1:s})","\\frac{{{0:s}}}{{{1:s}}}",False,2,op.truediv)
    addOp('%',"({0:s} % {1:s})","\\left({0:s} \\bmod {1:s}\\right)",False,2,op.mod)
    addOp('^',"({0:s} ^ {1:s})","{0:s}^{{{1:s}}}",False,1,op.pow)
    addOp('**',"({0:s} ^ {1:s})","{0:s}^{{{1:s}}}",False,1,op.pow)
    addOp('&&',"({0:s} && {1:s})","\\left({0:s} \\land {1:s}\\right)",False,4,lambda a, b: bool(a) and bool(b))
    addOp('||',"({0:s} || {1:s})","\\left({0:s} \\lor {1:s}\\right)",False,4,lambda a, b: bool(a) or bool(b))
    addOp('&',"({0:s} & {1:s})","\\left({0:s} \\cap {1:s}\\right)",False,4,op.and_)
    addOp('|',"({0:s} | {1:s})","\\left({0:s} \\cup {1:s}\\right)",False,4,op.or_)
    addOp('</>',"({0:s} </> {1:s})","\\left({0:s} \\oplus {1:s}\\right)",False,4,op.xor)
    addOp('&|',"({0:s} </> {1:s})","\\left({0:s} \\oplus {1:s}\\right)",False,4,op.xor)
    addOp('|&',"({0:s} </> {1:s})","\\left({0:s} \\oplus {1:s}\\right)",False,4,op.xor)
    addOp('==',"({0:s} == {1:s})","\\left({0:s} = {1:s}\\right)",False,5,op.eq)
    addOp('=',"({0:s} == {1:s})","\\left({0:s} = {1:s}\\right)",False,5,op.eq)
    addOp('~',"({0:s} ~ {1:s})","\\left({0:s} \\approx {1:s}\\right)",False,5,sim)
    addOp('!~',"({0:s} !~ {1:s})","\\left({0:s} \\not\\approx {1:s}\\right)",False,5,nsim)
    addOp('!=',"({0:s} != {1:s})","\\left({0:s} \\neg {1:s}\\right)",False,5,op.ne)
    addOp('<>',"({0:s} != {1:s})","\\left({0:s} \\neg {1:s}\\right)",False,5,op.ne)
    addOp('><',"({0:s} != {1:s})","\\left({0:s} \\neg {1:s}\\right)",False,5,op.ne)
    addOp('<',"({0:s} < {1:s})","\\left({0:s} < {1:s}\\right)",False,5,op.lt)
    addOp('>',"({0:s} > {1:s})","\\left({0:s} > {1:s}\\right)",False,5,op.gt)
    addOp('<=',"({0:s} <= {1:s})","\\left({0:s} \\leq {1:s}\\right)",False,5,op.le)
    addOp('>=',"({0:s} >= {1:s})","\\left({0:s} \\geq {1:s}\\right)",False,5,op.ge)
    addOp('=<',"({0:s} <= {1:s})","\\left({0:s} \\leq {1:s}\\right)",False,5,op.le)
    addOp('=>',"({0:s} >= {1:s})","\\left({0:s} \\geq {1:s}\\right)",False,5,op.ge)
    addOp('<~',"({0:s} <~ {1:s})","\\left({0:s} \lessapprox {1:s}\\right)",False,5,lsim)
    addOp('>~',"({0:s} >~ {1:s})","\\left({0:s} \\gtrapprox {1:s}\\right)",False,5,gsim)
    addOp('~<',"({0:s} <~ {1:s})","\\left({0:s} \lessapprox {1:s}\\right)",False,5,lsim)
    addOp('~>',"({0:s} >~ {1:s})","\\left({0:s} \\gtrapprox {1:s}\\right)",False,5,gsim)
    addUnaryOp('!',"(!{0:s})","\\neg{0:s}",op.not_)
    addUnaryOp('-',"-{0:s}","-{0:s}",op.neg)
    addFn('abs',"abs({0:s})","\\left|{0:s}\\right|",1,op.abs)
    addFn('sum',"sum({0:s})","\\sum\\left({0:s}\\right)",'+',sumargs)
    addFn('prod',"prod({0:s})","\\prod\\left({0:s}\\right)",'+',product)
    if has_numpy:
        addFn('floor',"floor({0:s})","\\lfloor {0:s} \\rfloor",1,np.floor)
        addFn('ceil',"ceil({0:s})","\\lceil {0:s} \\rceil",1,np.ceil)
        addFn('round',"round({0:s})","\\lfloor {0:s} \\rceil",1,np.round)
        addFn('sin',"sin({0:s})","\\sin\\left({0:s}\\right)",1,np.sin)
        addFn('cos',"cos({0:s})","\\cos\\left({0:s}\\right)",1,np.cos)
        addFn('tan',"tan({0:s})","\\tan\\left({0:s}\\right)",1,np.tan)
        addFn('re',"re({0:s})","\\Re\\left({0:s}\\right)",1,np.real)
        addFn('im',"re({0:s})","\\Im\\left({0:s}\\right)",1,np.imag)
        addFn('sqrt',"sqrt({0:s})","\\sqrt{{{0:s}}}",1,np.sqrt)
        addConst("pi",np.pi)
        addConst("e",np.e)
        addConst("Inf",np.Inf)
        addConst("NaN",np.NaN)
    else:
        addFn('floor',"floor({0:s})","\\lfloor {0:s} \\rfloor",1,math.floor)
        addFn('ceil',"ceil({0:s})","\\lceil {0:s} \\rceil",1,math.ceil)
        addFn('round',"round({0:s})","\\lfloor {0:s} \\rceil",1,round)
        addFn('sin',"sin({0:s})","\\sin\\left({0:s}\\right)",1,math.sin)
        addFn('cos',"cos({0:s})","\\cos\\left({0:s}\\right)",1,math.cos)
        addFn('tan',"tan({0:s})","\\tan\\left({0:s}\\right)",1,math.tan)
        addFn('re',"re({0:s})","\\Re\\left({0:s}\\right)",1,complex.real)
        addFn('im',"re({0:s})","\\Im\\left({0:s}\\right)",1,complex.imag)
        addFn('sqrt',"sqrt({0:s})","\\sqrt{{{0:s}}}",1,math.sqrt)
        addConst("pi",math.pi)
        addConst("e",math.e)
        addConst("Inf",float("Inf"))
        addConst("NaN",float("NaN"))
