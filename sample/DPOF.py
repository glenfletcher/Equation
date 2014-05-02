#!/usr/bin/env python
#############################################
# Dynamic Plotting of Function Sample
#############################################
from Equation import Expression
from Equation.core import constants
import matplotlib.pyplot as plt
import numpy as np
import h5py

db = h5py.File("dataset.hdf5", "r") # External Data base of consts and values

while True:
    expr = raw_input("Enter Equation to Plot in terms of (x): ") # Fetch Equation From User Input

    try:
        fn = Expression(expr,['x'])
    except SyntaxError as err:
        print err.message
        continue

    if 'x' not in fn: # check 'x' is used in expr
        print "Error: Equation must have a variable named x"
        continue

    for v in fn: # load all data values from db
        if v == 'x':
            continue
        if v in db:
            fn[v] = db[v]
            continue
        if v in db.attrs:
            fn[v] = db.attrs[v]
            continue
        if v in constants:
            continue
        print "Error: Variable '{0:s}' is not defined in database".format(v)
        break # Break the For Loop
    else:
        break # Break the While Loop

# One We get Here fn is a valid Expression object requiring a single argument 'x'

x = np.linspace(0,1,1000)

plt.plot(x,fn(x))
plt.title("Plot of ${0:s}$".format(fn))
plt.show()
