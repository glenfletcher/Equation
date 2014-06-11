# -*- coding: utf-8 -*-
#==============================================================================
#   Copyright 2014 AlphaOmega Technology
#
#   Licensed under the AlphaOmega Technology Open License Version 1.0
#   You may not use this file except in compliance with this License.
#   You may obtain a copy of the License at
#
#       http: //www.alphaomega-technology.com.au/license/AOT-OL/1.0
#==============================================================================

from . import __authors__, __copyright__, __license__, __contact__, __version__

from core import Expression


def parseUnits(expression, argorder=[], units=None):
    eq = Expression(expression, argorder)
    units = Units(eq._Expression__expression, units)
    return eq*units

_units = {
    'prefix': {
        'y': -24,
        'z': -21,
        'a': -18,
        'f': -15,
        'p': -12,
        'n': -9,
        'u': -6,
        'm': -3,
        'k': +3,
        'M': +6,
        'G': +9,
        'T': +12,
        'P': +15,
        'E': +18,
        'Z': +21,
        'Y': +24
    },
    'base': [
        'length',
        'mass',
        'time',
        'current',
        'temperature',
        'amount',
        'intensity'
    ],
    'units': {
        'base': {
            'm': {
                'unit': 'length',
                'mulitpler': (1, 0)
                },
            'g': {
                'unit': 'mass',
                'multipler': (1, -3)
                },
            's': {
                'unit': 'time',
                'mulitpler': (1, 0)
                },
            'A': {
                'unit': 'current',
                'mulitpler': (1, 0)
                },
            'K': {
                'unit': 'temperature',
                'mulitpler': (1, 0)
                },
            'mol': {
                'unit': 'amount',
                'mulitpler': (1, 0)
                },
            'cd': {
                'unit': 'intensity',
                'mulitpler': (1, 0)
                },
            'rad': {
                'unit': None,
                'mulitpler': (1, 0)
                },
            'sr': {
                'unit': None,
                'mulitpler': (1, 0)
                },
            },
        'derived': {
            'Hz': {
                'unit': {'s': -1},
                'mulitpler': (1, 0)
                },
            'N': {
                'unit': {'kg': 1, 'm': 1, 's': -2},
                'mulitpler': (1, 0)
                },
            'Pa': {
                'unit': {'kg': 1, 'm': -1, 's': -2},
                'mulitpler': (1, 0)
                },
            'J': {
                'unit': {'kg': 1, 'm': 2, 's': -2},
                'mulitpler': (1, 0)
                },
            'W': {
                'unit': {'kg': 1, 'm': 2, 's': -3},
                'mulitpler': (1, 0)
                },
            'C': {
                'unit': {'s': 1, 'A': 1},
                'mulitpler': (1, 0)
                },
            'V': {
                'unit': {'kg': 1, 'm': 2, 's': -3, 'A': -1},
                'mulitpler': (1, 0)
                },
            'F': {
                'unit': {'kg': -1, 'm': -2, 's': 4, 'A': 2},
                'mulitpler': (1, 0)
                },
            'ohm': {
                'unit': {'kg': 1, 'm': 2, 's': -3, 'A': -2},
                'mulitpler': (1, 0)
                },
            'S': {
                'unit': {'kg': -1, 'm': -2, 's': 3, 'A': 2},
                'mulitpler': (1, 0)
                },
            'Wb': {
                'unit': {'kg': 1, 'm': 2, 's': -2, 'A': 1},
                'mulitpler': (1, 0)
                },
            'T': {
                'unit': {'kg': 1, 's': -2, 'A': -1},
                'mulitpler': (1, 0)
                },
            'H': {
                'unit': {'kg': 1, 'm': 2, 's': -2, 'A': -2},
                'mulitpler': (1, 0)
                },
            '°C': {
                'unit': {'K': 1},
                'mulitpler': (1, 0),
                'warn': '°C relative to 273.15K, unit conversion may cause unexpected errors.'
                },
            'lm': {
                'unit': {'cd': 1, 'sr': 1},
                'mulitpler': (1, 0)
                },
            'lx': {
                'unit': {'cd': 1, 'm': -2, 'sr': 1},
                'mulitpler': (1, 0)
                },
            'Bq': {
                'unit': {'s': -1},
                'mulitpler': (1, 0)
                },
            'Gy': {
                'unit': {'m': 2, 's': -2},
                'mulitpler': (1, 0)
                },
            'Sv': {
                'unit': {'m': 2, 's': -2},
                'mulitpler': (1, 0)
                },
            'kat': {
                'unit': {'s': -1, 'mol': 1},
                'mulitpler': (1, 0)
                },
            }
        }
    }


class Units(object):
    def __init__(self, unitexpr='', units=None, *args, **kwargs):
        super(Units, self)(*args, **kwargs)
        if isinstance(unitexpr, type(self)):
            pass
        else:
            if unitexpr[:6] == '$attr.' and hasattr(self, unitexpr[6:]):
                __expression = getattr(self, unitexpr[6:])
            else:
                __expression = unitexpr


class UnitsExpression(Expression, Units):
    def __init__(self, expression, argorder=[], units=None, *args, **kwargs):
        if isinstance(expression, type(self)):
            super(UnitsExpression, self)(
                expression=expression,
                argorder=[],
                unitexpr=expression,
                units=None,
                *args, **kwargs)
        else:
            super(UnitsExpression, self)(
                expression=expression,
                argorder=argorder,
                unitexpr='$attr._Expression__expression',
                units=units,
                *args, **kwargs)
