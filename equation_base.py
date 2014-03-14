###################################################################################
#
#  Copyright 2014 AlphaOmega Technology
#
#  Licensed under the AlphaOmega Technology Open License Version 1.0
#  You may not use this file except in compliance with this License.
#  You may obtain a copy of the License at
# 
#      http://www.alphaomega-technology.com.au/license/AOT-OL/1.0
#
###################################################################################

import numpy as np

def equation_extend(addOp,addFn,addConst):
    addOp('+',"({0:s} + {1:s})",False,1,True,np.add)
    addOp('-',"({0:s} - {1:s})",False,1,True,np.subtract)
    addOp('*',"({0:s} * {1:s})",False,2,True,np.multiply)
    addOp('/',"({0:s} / {1:s})",False,2,True,np.divide)
    addOp('%',"({0:s} % {1:s})",False,2,True,np.mod)
    addOp('^',"({0:s} ^ {1:s})",False,3,True,np.power)
    addOp('&',"({0:s} & {1:s})",False,1,True,np.logical_and)
    addOp('|',"({0:s} | {1:s})",False,1,True,np.logical_or)
    addOp('!',"(!{0:s})",True,0,False,np.logical_not)
    addFn('abs',"abs({0:s})",1,np.abs)
    addFn('sin',"sin({0:s})",1,np.sin)
    addFn('cos',"cos({0:s})",1,np.cos)
    addFn('tan',"tan({0:s})",1,np.tan)
    addFn('re',"re({0:s})",1,np.real)
    addFn('im',"im({0:s})",1,np.imag)
    addConst("pi",np.pi)
    addConst("e",np.e)
    addConst("Inf",np.Inf)
    addConst("NaN",np.NaN)