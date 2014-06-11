# -*- coding: utf-8 -*-
###############################################################################
#   Copyright 2014 AlphaOmega Technology
#
#   Licensed under the AlphaOmega Technology Open License Version 1.0
#   You may not use this file except in compliance with this License.
#   You may obtain a copy of the License at
#
#       http://www.alphaomega-technology.com.au/license/AOT-OL/1.0
###############################################################################
r"""
.. _similar-module:

Equation.similar Module
=======================

Provides support for similar type comparison, and allows the tolerance to be changed

Comparison work by determining if the following is true

.. math::

    1-\frac{\min(A,B)}{\max(A,B)}\leq tolerance

If it is true the :math:`A` and :math:`B` are considered to be equal

This module only needs to be imported if you need to change the tolerance for similarity
tests, otherwise you just need to use the similarity operators in your expression

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

By default the tolerance is :math:`10^{-5}` Hence 1.001 isn't considered similar to 1, but by
changing the tolerance to :math:`10^{-2}`, 1.001 is considered similar to 1
"""

_tol = 1e-5


def sim(a, b):
    if a == b:
        return True
    elif a == 0 or b == 0:
        return False
    if a < b:
        return (1 - a / b) <= _tol
    else:
        return (1 - b / a) <= _tol


def nsim(a, b):
    if a == b:
        return False
    elif a == 0 or b == 0:
        return True
    if a < b:
        return (1 - a / b) > _tol
    else:
        return (1 - b / a) > _tol


def gsim(a, b):
    if a >= b:
        return True
    return (1 - a / b) <= _tol


def lsim(a, b):
    if a <= b:
        return True
    return (1 - b / a) <= _tol


def set_tol(value=1e-5):
    r"""Set Error Tolerance

    Set the tolerance for determining if two numbers are similar, i.e
    :math:`\left|\frac{a}{b}\right| = 1 \pm tolerance`

    Parameters
    ----------
    value: float
        The Value to set the tolerance to show be very small as it represents the
        percentage of acceptable error in determining if two values are the same.
    """
    global _tol
    if isinstance(value, float):
        _tol = value
    else:
        raise TypeError(type(value))
