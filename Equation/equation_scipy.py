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
__authors__   = "Glen Fletcher"
__copyright__ = "(c) 2014, AlphaOmega Technology"
__license__   = "AlphaOmega Technology Open License Version 1.0"
__contact__   = "Glen Fletcher <glen.fletcher@alphaomega-technology.com.au>"

try:
    import scipy.constants
    from Equation.util import addConst

    def equation_extend():
        addConst("h",scipy.constants.h)
        addConst("hbar",scipy.constants.hbar)
        addConst("me",scipy.constants.m_e)
        addConst("mp",scipy.constants.m_p)
        addConst("mn",scipy.constants.m_n)
        addConst("c",scipy.constants.c)
        addConst("N_A",scipy.constants.N_A)
        addConst("mu_0",scipy.constants.mu_0)
        addConst("eps_0",scipy.constants.epsilon_0)
        addConst("k",scipy.constants.k)
        addConst("G",scipy.constants.G)
        addConst("g",scipy.constants.g)
        addConst("ee",scipy.constants.e)
        addConst("R",scipy.constants.R)
        addConst("sigma",scipy.constants.e)
        addConst("Rb",scipy.constants.Rydberg)
except ImportError:
    def equation_extend():
        pass