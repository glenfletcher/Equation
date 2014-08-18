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

def addFn(id,str,latex,args,func,meta={}):
    core.functions[id] = {
        'str': str,
        'latex': latex,
        'args': args,
        'func': func,
        'meta': meta}

def addOp(id,str,latex,single,prec,func,meta={}):
    if single:
        raise RuntimeError("Single Ops Not Yet Supported")
    core.ops[id] = {
        'str': str,
        'latex': latex,
        'args': 2,
        'prec': prec,
        'func': func,
        'meta': meta}

def addUnaryOp(id,str,latex,func,meta={}):
    core.unary_ops[id] = {
        'str': str,
        'latex': latex,
        'args': 1,
        'prec': 0,
        'func': func,
        'meta': meta}

def addConst(name,value):
    core.constants[name] = value

def addScope(module,variable,default,setter=None,getter=None):
    core.scope[module + '.' + variable] = {
        'value': default,
        'get': getter,
        'set': setter}

def getScopeOr(module,variable,scope,default):
    name = module + '.' + variable
    if name in scope and scope[name] != None:
        return scope[name]
    else:
        return default
