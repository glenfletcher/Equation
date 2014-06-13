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
import re

from collections import defaultdict
from operator import itemgetter


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
                'warn': '°C relative to 273.15K,'
                    ' unit conversion may cause unexpected errors.'
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


_matchunit = re.compile(r'\s*(?P<prefix>{prefix:s})?(?P<unit>{unit:s})'.format(
                prefix='|'.join(map(re.escape, _units['prefix'].keys())),
                unit='|'.join(map(re.escape, sorted(
                    _units['units']['base'].keys() +
                        _units['units']['derived'].keys(),
                    key=len,
                    reverse=True)))))

_matchop = re.compile(r'\s*(?P<op>/|\^)')

_matchopen = re.compile(r'\s*(?P<open>\()')

_matchclose = re.compile(r'\s*(?P<open>\))')

_matchindex = re.compile(r'\s*(?P<sign>\+|\-)?\s*(?P<value>\d+)')


class Units(object):
    def __init__(self, unitexpr='', units=None, *args, **kwargs):
        super(Units, self).__init__(*args, **kwargs)
        if isinstance(unitexpr, type(self)):
            pass
        else:
            if unitexpr[:6] == '$attr.' and hasattr(self, unitexpr[6:]):
                self.__expression = getattr(self, unitexpr[6:])
            else:
                self.__expression = unitexpr
            self.__baseunits = defaultdict(int)  # this is the unit type
            # multipler for base units i.e. g -> 0.001 as kg is SI,
            # k will appear in multiplyer not base multipler,
            # as base just respresents type, i.e.
            #     we can convert between units with matching base type
            self.__basemultiplyer = [1, 0]
            self.__multiplyer = [1, 0]  # multipler to apply to base units
            self.__units = defaultdict(int)  # actuall units
            self.__parse()

    def __str__(self):
        s = ''
        for k, v in sorted(self.__baseunits.items(), key=itemgetter(1), reverse=True):
            s += r" \textup{" + k + "}" + (("^{" + str(v) + "}") if v != 0 else "")
        return s

    def __parse(self):
        invert = False
        nextinvert = False
        grouped = False
        index = 0
        while True:
            m = _matchunit.match(self.__expression)
            if m is not None:
                self.__expression = self.__expression[m.end():]
                print self.__expression
            else:
                break
            g = m.groupdict()
            if g['unit'] is None:
                raise SyntaxError("Missing Unit")
            if g['prefix'] is not None:
                self.__multiplyer[1] += _units['prefix'][g['prefix']]
            m = _matchop.match(self.__expression)
            index = 1
            if m is not None:
                self.__expression = self.__expression[m.end():]
                print self.__expression
                opg = m.groupdict()
                if opg['op'] == '^': # index
                    m = _matchindex.match(self.__expression)
                    print m
                    if m is not None:
                        self.__expression = self.__expression[m.end():]
                        print self.__expression
                        ig = m.groupdict()
                        print ig
                        index = int(
                            (ig['sign'] if ig['sign'] is not None else '') +
                            ig['value'])
                        print (
                            (ig['sign'] if ig['sign'] is not None else '') +
                            ig['value'])
                        print index
                elif opg['op'] == '/': # invert
                    nextinvert = True
            if invert:
                index *= -1
            print index
            if g['unit'] in _units['units']['base']: # is base unit
                unit = _units['units']['base'][g['unit']]
                self.__units[g['unit']] += index
                self.__baseunits[g['unit']] += index
                self.__basemultiplyer[0] *= unit['mulitpler'][0]
                self.__basemultiplyer[1] += unit['mulitpler'][1]*index
            elif g['unit'] in _units['units']['derived']: # is derived unit
                unit = _units['units']['derived'][g['unit']]
                self.__units[g['unit']] += index
                for k,v in unit['unit'].items():
                    bunit = _units['units']['base'][k]
                    self.__baseunits[g['unit']] += index*v
                    self.__basemultiplyer[0] *= unit['mulitpler'][0]
                    self.__basemultiplyer[1] += unit['mulitpler'][1]*index*v
                self.__multiplyer[0] *= unit['mulitpler'][0]
                self.__multiplyer[1] += unit['mulitpler'][1]*index
            if grouped:
                m = _matchclose.match(self.__expression)
                if m is not None:
                    self.__expression = self.__expression[m.end():]
                    grouped = False
            if not grouped and invert:
                invert = False
            if nextinvert:
                invert = True
                m = _matchopen.match(self.__expression)
                if m is not None:
                    self.__expression = self.__expression[m.end():]
                    grouped = True


#class UnitsExpression(Expression, Units):
#    def __init__(self, expression, argorder=[], units=None, *args, **kwargs):
#        if isinstance(expression, type(self)):
#            super(UnitsExpression, self)(
#                expression=expression,
#                argorder=[],
#                unitexpr=expression,
#                units=None,
#                *args, **kwargs)
#        else:
#            super(UnitsExpression, self)(
#                expression=expression,
#                argorder=argorder,
#                unitexpr='$attr._Expression__expression',
#                units=units,
#                *args, **kwargs)
