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
.. _similar-module:

Equation.similar Module
=======================

Provides support for similar type comparsion, and allows the tolerance to be changed

Comparsions work by detriming if the following is true

.. math::

    1-\frac{\min(A,B)}{\max(A,B)}\leq tolerance

If it is true the :math:`A` and :math:`B` are considered to be equal

This module only needs to be imported if you need to change the tolerance for similarlity
tests, otherwise you just need to use the similarlity operators in your expression

.. code-block:: python

    >>> from Equation import Expression
    >>> fn = Expression("x ~ y")
    >>> fn(1,1.1)
    False
    >>> fn(1,1.00001)
    True
    >>> fn(1,1.001)
    False
    >>> from Equation.similar import set_tol
    >>> set_tol(1e-2)
    >>> fn(1,1.1)
    False
    >>> fn(1,1.00001)
    True
    >>> fn(1,1.001)
    True

By default the tolerance is :math:`10^{-5}` Hence 1.001 isn't condisered similar to 1, but by
changing the tolerance to :math:`10^{-2}`, 1.001 is condisered similar to 1
"""

import numbers

from Equation.util import getScopeOr

_tol = 1e-5

def sim(a,b,scope={}):
    tol = getScopeOr('similar','tol',scope,_tol)
    if (a==b):
        return True
    elif a == 0 or b == 0:
        return False
    if (a<b):
        return (1-a/b)<=tol
    else:
        return (1-b/a)<=tol

def nsim(a,b,scope={}):
    tol = getScopeOr('similar','tol',scope,_tol)
    if (a==b):
        return False
    elif a == 0 or b == 0:
        return True
    if (a<b):
        return (1-a/b)>tol
    else:
        return (1-b/a)>tol

def gsim(a,b,scope={}):
    tol = getScopeOr('similar','tol',scope,_tol)
    if a >= b:
        return True
    return (1-a/b)<=tol

def lsim(a,b,scope={}):
    tol = getScopeOr('similar','tol',scope,_tol)
    if a <= b:
        return True
    return (1-b/a)<=tol

def tol_setter(value=1e-5):
    if isinstance(value,numbers.Real):
        return value
    else:
        raise TypeError(type(value))

def tol_getter(value):
    return value

def set_tol(value=1e-5):
    r"""Set Error Tolerance

    Set the tolerance for detriming if two numbers are simliar, i.e
    :math:`\left|\frac{a}{b}\right| = 1 \pm tolerance`

    Parameters
    ----------
    value: float
        The Value to set the tolerance to show be very small as it respresents the
        percentage of acceptable error in detriming if two values are the same.
    """
    global _tol
    if isinstance(value,numbers.Real):
        _tol = value
    else:
        raise TypeError(type(value))