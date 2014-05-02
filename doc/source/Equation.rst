Modules
=======

.. automodule:: Equation

.. autoclass:: Equation.Expression
	:members:
   
	.. method:: fn(*args,**kwargs)
		
		Evaluates the Expression object using the variables passed, where preset arguments will act as the 
		defualt value for said arguments.
		
		:param \*args: Positional variables, order as defined by argorder, then position in equation
		:param \*\*kwargs: List of variables to be used by the equation for evaluation
		
		:returns: Result of Expression Evaluation
		
		:raises TypeError: For Invalid number of arguments, or arguments given multiple values, as with normal python functions
		
	.. method:: fn[var]
	
		Get the preset variable `var`, from the Expression Object

	.. method:: fn[var] = value
	
		Set the preset variable `var` to the value `value`

	.. method:: del fn[var]
	
		Removes the preset variable `var` from the Expression Object

	.. method:: var in fn
	
		:returns: True if `fn` has a variable `var`

	.. method:: var not in fn
	
		:returns: True if `fn` dosen't have a variable `var`

	.. method:: for var in fn
	
		Iterates over all variables `var` in `fn`

	.. method:: str(fn)
	
		Generates a Printable version of the Expression
		
		:returns: Latex String respresation of the Expression, suitable for rendering the equation

	.. method:: repr(fn)
	
		Generates a String that correctrly respresents the equation
		
		:returns: Convert the Expression to a String that passed to the constructor, will constuct an identical equation object (in terms of sequence of tokens, and token type/value)
		
		
.. automodule:: Equation.similar
	:members: