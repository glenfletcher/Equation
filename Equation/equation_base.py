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
from Equation.util import addOp, addFn, addConst, addUnaryOp, addScope
from Equation.similar import sim, nsim, gsim, lsim, _tol as similar_tol, tol_setter, tol_getter

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

    addScope('similar','tol',None,tol_setter,tol_getter)
    addOp('+',"({0:s} + {1:s})","\\left({0:s} + {1:s}\\right)",False,3,op.add)
    addOp('-',"({0:s} - {1:s})","\\left({0:s} - {1:s}\\right)",False,3,op.sub)
    addOp('*',"({0:s} * {1:s})","\\left({0:s} \\times {1:s}\\right)",False,2,op.mul)
    addOp('/',"({0:s} / {1:s})","\\frac{{{0:s}}}{{{1:s}}}",False,2,op.truediv)
    addOp('%',"({0:s} % {1:s})","\\left({0:s} \\bmod {1:s}\\right)",False,2,op.mod)
    addOp('^',"({0:s} ^ {1:s})","{0:s}^{{{1:s}}}",False,1,op.pow)
    addOp('**',"({0:s} ^ {1:s})","{0:s}^{{{1:s}}}",False,1,op.pow)
    addOp('&',"({0:s} & {1:s})","\\left({0:s} \\land {1:s}\\right)",False,4,op.and_)
    addOp('|',"({0:s} | {1:s})","\\left({0:s} \\lor {1:s}\\right)",False,4,op.or_)
    addOp('</>',"({0:s} </> {1:s})","\\left({0:s} \\oplus {1:s}\\right)",False,4,op.xor)
    addOp('&|',"({0:s} </> {1:s})","\\left({0:s} \\oplus {1:s}\\right)",False,4,op.xor)
    addOp('|&',"({0:s} </> {1:s})","\\left({0:s} \\oplus {1:s}\\right)",False,4,op.xor)
    addOp('==',"({0:s} == {1:s})","\\left({0:s} = {1:s}\\right)",False,5,op.eq)
    addOp('=',"({0:s} == {1:s})","\\left({0:s} = {1:s}\\right)",False,5,op.eq)
    addOp('~',"({0:s} ~ {1:s})","\\left({0:s} \\sim {1:s}\\right)",False,5,sim,{'has_scope':True})
    addOp('!~',"({0:s} !~ {1:s})","\\left({0:s} \\nsim {1:s}\\right)",False,5,nsim,{'has_scope':True})
    addOp('!=',"({0:s} != {1:s})","\\left({0:s} \\neg {1:s}\\right)",False,5,op.ne)
    addOp('<>',"({0:s} != {1:s})","\\left({0:s} \\neg {1:s}\\right)",False,5,op.ne)
    addOp('><',"({0:s} != {1:s})","\\left({0:s} \\neg {1:s}\\right)",False,5,op.ne)
    addOp('<',"({0:s} < {1:s})","\\left({0:s} < {1:s}\\right)",False,5,op.lt)
    addOp('>',"({0:s} > {1:s})","\\left({0:s} > {1:s}\\right)",False,5,op.gt)
    addOp('<=',"({0:s} <= {1:s})","\\left({0:s} \\leq {1:s}\\right)",False,5,op.le)
    addOp('>=',"({0:s} >= {1:s})","\\left({0:s} \\geq {1:s}\\right)",False,5,op.ge)
    addOp('=<',"({0:s} <= {1:s})","\\left({0:s} \\leq {1:s}\\right)",False,5,op.le)
    addOp('=>',"({0:s} >= {1:s})","\\left({0:s} \\geq {1:s}\\right)",False,5,op.ge)
    addOp('<~',"({0:s} <~ {1:s})","\\left({0:s} \\lesssim {1:s}\\right)",False,5,lsim,{'has_scope':True})
    addOp('>~',"({0:s} >~ {1:s})","\\left({0:s} \\gtrsim {1:s}\\right)",False,5,gsim,{'has_scope':True})
    addOp('~<',"({0:s} <~ {1:s})","\\left({0:s} \\lesssim {1:s}\\right)",False,5,lsim,{'has_scope':True})
    addOp('~>',"({0:s} >~ {1:s})","\\left({0:s} \\gtrsim {1:s}\\right)",False,5,gsim,{'has_scope':True})
    addUnaryOp('!',"(!{0:s})","\\neg{0:s}",op.not_)
    addUnaryOp('-',"-{0:s}","-{0:s}",op.neg)
    addFn('abs',"abs({0:s})","\\left|{0:s}\\right|",1,op.abs)
    addFn('sum',"sum({0:s})","\\sum\\left({0:s}\\right)",'+',sumargs)
    addFn('prod',"prod({0:s})","\\prod\\left({0:s}\\right)",'+',product)
    if has_numpy:
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
