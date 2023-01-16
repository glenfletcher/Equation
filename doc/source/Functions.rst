Functions, Operators & Constants
================================
The Following Functions, Operators and Constants are defined and useable in Expression Strings.

.. note:: All names are case-senitive

Constants
---------

Constants are basicaly unchanging global variabes, an used to define special values

========== ============= =========================================================================
Name       Version Added Value
========== ============= =========================================================================
**pi**     1.0           Pi (:math:`\pi`)
**e**      1.0           Euler's number (:math:`\mathrm{e}`)
**Inf**    1.0           Infinity (:math:`\infty`)
**NaN**    1.0           Not a Number
**h**      1.1           Plancks Constant (:math:`h`) [#scipy-const]_
**hbar**   1.1           Reduced Plancks Constant (:math:`\hbar`) [#scipy-const]_
**m_e**    1.1           Electron Mass (:math:`m_{\rm e}`) [#scipy-const]_
**m_p**    1.1           Proton Mass (:math:`m_{\rm p}`) [#scipy-const]_
**m_n**    1.1           Neturon Mass (:math:`m_{\rm n}`) [#scipy-const]_
**c**      1.1           Speed of Light (:math:`c`) [#scipy-const]_
**N_A**    1.1           Avogardo's Number (:math:`N_{\rm A}`) [#scipy-const]_
**mu_0**   1.1           Magnetic Constant (:math:`\mu_0`) [#scipy-const]_
**eps_0**  1.1           Electric Constant (:math:`\varepsilon_0`) [#scipy-const]_
**k**      1.1           Boltzmann Constant (:math:`k_\mathrm{b}`) [#scipy-const]_
**G**      1.1           Gravitational Constant (:math:`G`) [#scipy-const]_
**g**      1.1           Standard Accleration due to gravity (:math:`\mathrm{g}`) [#scipy-const]_
**q**      1.1           Elementary Charge (:math:`\mathit{e}`) [#scipy-const]_
**R**      1.1           Ideal Gas Constant (:math:`R`) [#scipy-const]_
**sigma**  1.1           Stefan-Boltzmann Constant (:math:`\sigma`) [#scipy-const]_
**Rb**     1.1           Rydberg Constant (:math:`R_\infty`) [#scipy-const]_
========== ============= =========================================================================


.. [#scipy-const] Requires scipy to use these constants

Operators
---------

Operators are special function maped to a symbol, that will appear between the operands
rather than as a name folloed by a comma seperated list of operands.

Operators have a Precedence this indicate the Priotiy with which they are applied
i.e. low Precedence valued operators will be evaluated before higher valued ones.

.. note:: Values of the same Precedence are evaluated left to right

======= ======================================== ============= ========== ===============================================
Symbol  Operation                                Syntax        Precedence Display
======= ======================================== ============= ========== ===============================================
\+      Added A to B                             ``A + B``     3          :math:`\left(A + B\right)`
\-      Subtract B from A                        ``A - B``     3          :math:`\left(A - B\right)`
\*      Mutlipy A by B                           ``A * B``     2          :math:`\left(A \times B\right)`
/       Divide A by B                            ``A / B``     2          :math:`\frac{A}{B}`
%       Reminder of A Divided by B               ``A % B``     2          :math:`\left(A \bmod B\right)`
^       Raise A to the B'th power                ``A ^ B``     1          :math:`A^{B}`
&       Logical AND of A and B                   ``A & B``     4          :math:`\left(A \land B\right)`
\|      Logical OR of A and B                    ``A | B``     4          :math:`\left(A \lor B\right)`
\<\\\>  Logical XOR of A and B                   ``A <\> B``   4          :math:`\left(A \oplus B\right)`
!       Logical NOT of A                         ``!A``        UNARY      :math:`\neg A`
\=\=    Test if A is equal to B                  ``A == B``    5          :math:`\left(A = B\right)`
\~      Test if A is similar to B                ``A ~ B``     5          :math:`\left(A \sim B\right)` [#similar]_
\!\=    Test if A isn't equal to B               ``A != B``    5          :math:`\left(A \neq B\right)`
\!\~    Test if A isn't similar to B             ``A !~ B``    5          :math:`\left(A \nsim B\right)` [#similar]_
\<      Test if A is less than to B              ``A < B``     5          :math:`\left(A < B\right)`
\>      Test if A is more than to B              ``A > B``     5          :math:`\left(A > B\right)`
\<\=    Test if A is less than or equal to B     ``A < B``     5          :math:`\left(A \leq B\right)`
\>\=    Test if A is more than or equal to B     ``A > B``     5          :math:`\left(A \geq B\right)`
\<\~    Test if A is less than or similar to B   ``A < B``     5          :math:`\left(A \lesssim B\right)` [#similar]_
\>\~    Test if A is more than or similar to B   ``A > B``     5          :math:`\left(A \gtrsim B\right)` [#similar]_
======= ======================================== ============= ========== ===============================================

.. [#similar] Check it values are very close rather then just equal, i.e. 1 is similar to 1.000001 but not equal (see :ref:`similar-module`)

Functions
---------

These as normal functions a name followed by a list of parameters

========== =========================== ============= ============================
Name       Operation                   Syntax        Display
========== =========================== ============= ============================
**abs**    Absolute value of A         ``abs(A)``    :math:`\left|A\right|`
**sin**    Sine value of A             ``sin(A)``    :math:`\sin\left(A\right)`
**cos**    Cosine value of A           ``cos(A)``    :math:`\cos\left(A\right)`
**tan**    Tangent value of A          ``tan(A)``    :math:`\tan\left(A\right)`
**arcsin** Inverse sine value of A     ``arcsin(A)`` :math:`\arcsin\left(A\right)`
**arccos** Inverse cosine value of A   ``arccos(A)`` :math:`\arccos\left(A\right)`
**arctan** Inverse tangent value of A  ``arctan(A)`` :math:`\arctan\left(A\right)`
**re**     Real Compoent of A          ``re(A)``     :math:`\Re\left(A\right)`
**im**     Imagery Compoent of A       ``im(A)``     :math:`\Im\left(A\right)`
**sqrt**   Square root of A            ``sqrt(A)``   :math:`\sqrt{A}`
**log**    Logarithm of A              ``log(A)``    :math:`\log{A}`
========== =========================== ============= ============================

Examples
--------

The Following are some example expressions demonstrating the Precedence order and display formating

.. code-block:: none

	sin(x*(y+z))
	sin((x * (y + z)))

.. math::

	\sin\left(\left(x \times \left(y + z\right)\right)\right)
	
.. code-block:: none

	(a+b)/(c+d)
	((a + b) / (c + d))

.. math::

	\frac{\left(a + b\right)}{\left(c + d\right)}
	
.. code-block:: none

	a+b/c+d*e^f
	((a + (b / c)) + (d * (e ^ f)))

.. math::

	\left(\left(a + \frac{b}{c}\right) + \left(d \times e^{f}\right)\right)
	
.. code-block:: none

	a^b/c^d
	((a ^ b) / (c ^ d))

.. math::

	\frac{a^{b}}{c^{d}}
	
.. code-block:: none

	a*b/c*d
	(((a * b) / c) * d)

.. math::
	
	\left(\frac{\left(a \times b\right)}{c} \times d\right)
	
.. code-block:: none

	a*b/(c*d)
	((a * b) / (c * d))

.. math::
	
	\frac{\left(a \times b\right)}{\left(c \times d\right)}
