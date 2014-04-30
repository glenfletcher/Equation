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

from . import __authors__,__copyright__,__license__,__contact__,__version__
try:
    from Equation import core
except ImportError:
    import core

def addFn(id,str,latex,args,func):
    core.functions[id] = {
        'str': str,
        'latex': latex,
        'args': args,
        'func': func}

def addOp(id,str,latex,single,prec,func):
    if single:
        raise RuntimeError("Single Ops Not Yet Supported")
    core.ops[id] = {
        'str': str,
        'latex': latex,
        'args': 2,
        'prec': prec,
        'func': func}

def addUnaryOp(id,str,latex,func):
    core.unary_ops[id] = {
        'str': str,
        'latex': latex,
        'args': 1,
        'prec': 0,
        'func': func}

def addConst(name,value):
    core.constants[name] = value