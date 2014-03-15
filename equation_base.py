"""
  Copyright 2014 AlphaOmega Technology

  Licensed under the AlphaOmega Technology Open License Version 1.0
  You may not use this file except in compliance with this License.
  You may obtain a copy of the License at
 
      http://www.alphaomega-technology.com.au/license/AOT-OL/1.0

"""
__authors__   = "Glen Fletcher"
__copyright__ = "(c) 2014, AlphaOmega Technology"
__license__   = "AlphaOmega Technology Open License Version 1.0"
__contact__   = "Glen Fletcher <glen.fletcher@alphaomega-technology.com.au>"

import numpy as np

def equation_extend(addOp,addFn,addConst):
    addOp('+',"({0:s} + {1:s})","\left({0:s} + {1:s}\right)",False,1,True,np.add)
    addOp('-',"({0:s} - {1:s})","\left({0:s} - {1:s}\right)",False,1,True,np.subtract)
    addOp('*',"({0:s} * {1:s})","\left({0:s} \times {1:s}\right)",False,2,True,np.multiply)
    addOp('/',"({0:s} / {1:s})","\frac{{{0:s}}}{{{1:s}}}",False,2,True,np.divide)
    addOp('%',"({0:s} % {1:s})","\left({0:s} \bmod {1:s}\right)",False,2,True,np.mod)
    addOp('^',"({0:s} ^ {1:s})","{0:s}^{{{1:s}}}",False,3,True,np.power)
    addOp('&',"({0:s} & {1:s})","\left({0:s} \land {1:s}\right)",False,1,True,np.logical_and)
    addOp('|',"({0:s} | {1:s})","\left({0:s} \lor {1:s}\right)",False,1,True,np.logical_or)
    addOp('!',"(!{0:s})","\not{{{0:s}}}",True,0,False,np.logical_not)
    addFn('abs',"abs({0:s})","\left|{0:s}\right|",1,np.abs)
    addFn('sin',"sin({0:s})","\sin\left({0:s}\right)",1,np.sin)
    addFn('cos',"cos({0:s})","\cos\left({0:s}\right)",1,np.cos)
    addFn('tan',"tan({0:s})","\tan\left({0:s}\right)",1,np.tan)
    addFn('re',"re({0:s})","Re\left({0:s}\right)",1,np.real)
    addFn('im',"re({0:s})","Im\left({0:s}\right)",1,np.imag)
    addFn('im',"re({0:s})","Im\left({0:s}\right)",1,np.imag)
    addFn('root',"root({0:s},{1:s})","\sqrt[{1:s}]{{{0:s}}}",2,np.imag)
    addFn('sqrt',"sqrt({0:s})","\sqrt{{{0:s}}}",1,np.imag)
    addConst("pi",np.pi)
    addConst("e",np.e)
    addConst("Inf",np.Inf)
    addConst("NaN",np.NaN)