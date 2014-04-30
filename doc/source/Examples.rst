Examples
========
The following code demonstrates more advanced uses of the Equation Package

Dynamic Ploting of functions
----------------------------

Requires numpy, matplotlib and h5py

.. code-block:: python

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
	
The Following is the result of running the script, given "dataset.hdf5" contains the attribute ``A = 3``
	
.. code-block:: none

	Enter Equation to Plot in terms of (x): A*sin(x*re(sqrt(x-(0.5+0j))))

.. image:: _static/DPOF01.png

.. code-block:: none

	Enter Equation to Plot in terms of (x): A*sin(x*im(sqrt(x-(0.5+0j))))

.. image:: _static/DPOF02.png

This sample asks the user for some function of ``x`` and then loads required data from a hdf5 file by search the file for 
variables in the function the user entered. Once the data has been retrived the function is plotted in the range :math:`[0,1]`
and the plot is titled using the display form of the function the user entered.

.. note:: It is important to search the hdf5 file for variables as hdf5 files may contain thousands of variables and take several Gigabytes of space.
