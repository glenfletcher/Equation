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
r"""
Provides support for similar type comparsion, and allows the tolerance to be changed
"""

_tol = 1e-5

def sim(a,b):
    if (a<b):
        return (1-a/b)<=_tol
    else:
        return (1-b/a)<=_tol

def nsim(a,b):
    if (a<b):
        return (1-a/b)>_tol
    else:
        return (1-b/a)>_tol
    
def gsim(a,b):
    if a >= b:
        return True
    return (1-a/b)<=_tol

def lsim(a,b):
    if a <= b:
        return True
    return (1-b/a)<=_tol
    
def set_tol(value=None):
    r"""Set Error Tolerance
    
    Set the tolerance for detriming if two numbers are simliar, i.e
    :math:`\frac{a}{b} = 1 \pm tol`
    
    Paramters
    =========
    value: float
        The Value to set the tolerance to show be very small i.e. > 1e^-3
    """
    global _tol
    if isinstance(value,float):
        _tol = value
    else:
        raise TypeError(type(value))