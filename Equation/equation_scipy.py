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

try:
    import scipy.constants
    from Equation.util import addConst

    def equation_extend():
        addConst("h",scipy.constants.h)
        addConst("hbar",scipy.constants.hbar)
        addConst("eV",scipy.constants.electron_volt)
        addConst("me",scipy.constants.electron_mass)
        addConst("mp",scipy.constants.electron_mass)
        addConst("c",scipy.constants.speed_of_light)
        addConst("N_A",scipy.constants.N_A)
        addConst("mu_0",scipy.constants.mu_0)
        addConst("eps_0",scipy.constants.epsilon_0)
        addConst("kb",scipy.constants.Boltzmann)
except ImportError:
    def equation_extend():
        pass