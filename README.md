[![Build Status](https://travis-ci.org/alphaomega-technology/Equation.png)](https://travis-ci.org/alphaomega-technology/Equation)

Equation Interpeter
===================
The Equation Package provide an extentable Equation Parser and Evaluation System.

It will take a string such as `"sin(x+y^2)"` and convert it to a python object that can be called
this allow the safe evaluation of equations stored in configuration files or enterned from the 
keyboard. This Package never calls a python evaluation command hence their is no risk of executing
any unexpected python code.

The Generated Expression Object is desgined to behave like a python function, and can be used any where
a python funcion is expected, it may be called with either positional or keyword arguments to set the
Equations Variables, by default the order of the variables is as they appear in the equation, however
an explicit order may be set when the Expression object is created.

Example
-------

	>>> from Equation import Expression
	>>> fn = Expression("sin(x+y^2)",["y","x"])
	>>> fn
	sin((x + (y ^ (2+0j))))
	>>> print fn
	\sin\left(\left(x + y^{(2+0j)}\right)\right)
	>>> fn(3,4)
	(0.42016703682664092+0j)

Numpy Arrays Supported
----------------------

The default function maping used by this package map the operators and functions to Numpy Functions, hence the generated object may be called with
numpy arrays.

Latex Support
-------------

The display string format i.e. str() is set to use Latex syntax allowing high quality equations to be rendered in output this syntax is supported by the grqaphing package matplotlib

Note: repr() method will return a string suitable for passing to Expression, however it is recalucated from the tokenized expression, and has all brackets.

Future Versions
---------------
Goals for future versions are:

- Reduce repr() type respresentation to use only required brackets
- Allow the use of function variable, rather than just predefined functions