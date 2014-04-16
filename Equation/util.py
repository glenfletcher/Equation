# -*- coding: utf-8 -*-
"""
Created on Fri Apr 11 00:51:34 2014

  Copyright 2014 AlphaOmega Technology

  Licensed under the AlphaOmega Technology Open License Version 1.0
  You may not use this file except in compliance with this License.
  You may obtain a copy of the License at
 
      http://www.alphaomega-technology.com.au/license/AOT-OL/1.0
      
.. moduleauthor:: Glen Fletcher <glen.fletcher@alphaomega-technology.com.au>
"""

from . import __authors__,__copyright__,__license__,__contact__,__version__
import core

def addFn(id,str,latex,args,func):
    core.functions[id] = {
        'str': str,
        'latex': latex,
        'args': args,
        'prec': 1,
        'type': 'FUNC',
        'func': func}

def addOp(id,str,latex,single,prec,func):
    core.functions[id] = {
        'str': str,
        'latex': latex,
        'args': 1 if single else 2,
        'prec': prec,
        'type': 'LEFT',
        'func': func}

def addUnaryOp(id,str,latex,prec,func):
    core.functions['_unary'] = {
        'str': str,
        'latex': latex,
        'args': 1,
        'prec': prec,
        'type': 'RIGHT',
        'func': func}

def addConst(name,value):
    core.constants[name] = value