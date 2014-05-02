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

from __future__ import print_function

from . import __authors__,__copyright__,__license__,__contact__,__version__

import math

import sys
import re

if sys.version_info.major == 3:
    xrange = range
    basestring = str

class ExpressionObject (object):
    def __init__(self,*args,**kwargs):
        super(ExpressionObject,self).__init__(*args,**kwargs)

    def toStr(self,args,expression):
        return ""

    def toRepr(self,args,expression):
        return ""

    def __call__(self,args,expression):
        pass
        
class ExpressionValue( ExpressionObject ):
    def __init__(self,value,*args,**kwargs):
        super(ExpressionValue,self).__init__(*args,**kwargs)
        self.value = value

    def toStr(self,args,expression):
        if (isinstance(self.value,complex)):
            V = [self.value.real,self.value.imag]
            E = [0,0]
            B = [0,0]
            out = ["",""]
            for i in xrange(2):
                if V[i] == 0:
                    E[i] = 0
                    B[i] = 0
                else:
                    E[i] = int(math.floor(math.log10(abs(V[i]))))
                    B[i] = V[i]*10**-E[i]
                    if E[i] in [0,1,2,3] and str(V[i])[-2:] == ".0":
                        B[i] = int(V[i])
                        E[i] = 0
                    if E[i] in [-1,-2] and len(str(V[i])) <= 7:
                        B[i] = V[i]
                        E[i] = 0
                if i == 1:
                    fmt = "{{0:+{0:s}}}"
                else:
                    fmt = "{{0:-{0:s}}}"
                if type(B[i]) == int:
                    out[i] += fmt.format('d').format(B[i])
                else:
                    out[i] += fmt.format('.5f').format(B[i]).rstrip("0.")
                if i == 1:
                    out[i] += "\\imath"
                if E[i] != 0:
                    out[i] += "\\times10^{{{0:d}}}".format(E[i])
            return "\\left(" + ''.join(out) + "\\right)"
        elif (isinstance(self.value,float)):
            V = self.value
            E = 0
            B = 0
            out = ""
            if V == 0:
                E = 0
                B = 0
            else:
                E = int(math.floor(math.log10(abs(V))))
                B = V*10**-E
                if E in [0,1,2,3] and str(V)[-2:] == ".0":
                    B = int(V)
                    E = 0
                if E in [-1,-2] and len(str(V)) <= 7:
                    B = V
                    E = 0
            if type(B) == int:
                out += "{0:-d}".format(B)
            else:
                out += "{0:-.5f}".format(B).rstrip("0.")
            if E != 0:
                out += "\\times10^{{{0:d}}}".format(E)
                return "\\left(" + out + "\\right)"
            else:
                return out
        else:
            return str(self.value)
    
    def toRepr(self,args,expression):
        return str(self.value)

    def __call__(self,args,expression):
        return self.value
    
    def __repr__(self):
            return "<{0:s}.{1:s}({2:s}) object at {3:0=#10x}>".format(type(self).__module__,type(self).__name__,str(self.value),id(self))

class ExpressionFunction( ExpressionObject ):
    def __init__(self,function,nargs,form,display,id,isfunc,*args,**kwargs):
        super(ExpressionFunction,self).__init__(*args,**kwargs)
        self.function = function
        self.nargs = nargs
        self.form = form
        self.display = display
        self.id = id
        self.isfunc = isfunc

    def toStr(self,args,expression):
        params = []
        for i in xrange(self.nargs):
            params.append(args.pop())
        if self.isfunc:
            return str(self.display.format(','.join(params[::-1])))
        else:
            return str(self.display.format(*params[::-1]))
            
    def toRepr(self,args,expression):
        params = []
        for i in xrange(self.nargs):
            params.append(args.pop())
        if self.isfunc:
            return str(self.form.format(','.join(params[::-1])))
        else:
            return str(self.form.format(*params[::-1]))
            
    def __call__(self,args,expression):
        params = []
        for i in xrange(self.nargs):
            params.append(args.pop())
        return self.function(*params[::-1])
    
    def __repr__(self):
        return "<{0:s}.{1:s}({2:s},{3:d}) object at {4:0=#10x}>".format(type(self).__module__,type(self).__name__,str(self.id),self.nargs,id(self))

class ExpressionVariable( ExpressionObject ):
    def __init__(self,name,*args,**kwargs):
        super(ExpressionVariable,self).__init__(*args,**kwargs)
        self.name = name

    def toStr(self,args,expression):
        return str(self.name)

    def toRepr(self,args,expression):
        return str(self.name)

    def __call__(self,args,expression):
        if self.name in expression.variables:
            return expression.variables[self.name]
        else:
            return 0 # Default variables to return 0
        
    def __repr__(self):
        return "<{0:s}.{1:s}({2:s}) object at {3:0=#10x}>".format(type(self).__module__,type(self).__name__,str(self.name),id(self))

class Expression( object ):
    """Expression or Equation Object
    
    This is a object that respresents an equation string in a manner
    that allows for it to be evaluated
    
    Arithmetic Operators:
        Expression objects support combining with the standard arithmetic operators
        to create new Expression objects, they may also be combined with numerical
        constant, and strings containg a valid Expression.
        
            >>> from Equation import Expression
            >>> fn = Expression("x")
            >>> fn += 2
            >>> fn
            (x + 2)
            >>> fn **=3
            >>> fn
            ((x + 2) ^ 3)
            >>> fn -= "z"
            >>> fn
            (((x + 2) ^ 3) - z)
            >>> fn(1,2)
            25
    
    Parameters
    ----------
    expression: str
        String resprenstation of an equation
    argorder: list of str
        List of variable names, indicating the position of variable
        for mapping from positional arguments    
    """
    def __init__(self,expression,argorder=[],*args,**kwargs):
        super(Expression,self).__init__(*args,**kwargs)
        if isinstance(expression,type(self)): # clone the object
            self.__args = list(expression.__args)
            self.__vars = dict(expression.__vars) # intenral array of preset variables
            self.__argsused = set(expression.__argsused)
            self.__expr = list(expression.__expr)
            self.variables = {} # call variables
        else:
            self.__expression = expression
            self.__args = argorder;
            self.__vars = {} # intenral array of preset variables
            self.__argsused = set()
            self.__expr = [] # compiled equation tokens
            self.variables = {} # call variables
            self.__compile()
            del self.__expression
    
    def __getitem__(self, name):
        """fn[var]
        
        Fetch the preset variable `var`,from the Expression Object
        """
        if name in self.__argsused:
            if name in self.__vars:
                return self.__vars[name]
            else:
                return None
        else:
            raise KeyError(name)
    
    def __setitem__(self,name,value):
        """fn[var] = value
        
        Set the preset variable `var` to the value `value`
        """
        if name in self.__argsused:
            self.__vars[name] = value
        else:
            raise KeyError(name)
    
    def __delitem__(self,name):
        """del fn[var]
        
        Removes the preset variable `var` from the Expression Object
        """
        if name in self.__argsused:
            if name in self.__vars:
                del self.__vars[name]
        else:
            raise KeyError(name)
            
    def __contains__(self, name):
        """var in fn
        
        Returns True if `fn` has a preset variable `var`
        """
        return name in self.__argsused
        
    def __call__(self,*args,**kwargs):
        """fn(\*args,\*\*kwargs)
        
        Arguments
        ---------
        \*args:
            Positional variables, order as defined by argorder, then position in equation
        \*\*kwargs:
            List of variables to be used by the equation for evaluation
            
        Returns
        -------
        varies
            Result of evaluating the Expression, type will depende appon the expression and the variables used to evaluate the expression.
        """
        self.variables = {}
        self.variables.update(constants) # i.e. pi, e, i, etc.
        self.variables.update(self.__vars)
        if len(args) > len(self.__args):
            raise TypeError("<{0:s}.{1:s}({2:s}) object at {3:0=#10x}>() takes at most {4:d} arguments ({5:d} given)".format(
                    type(self).__module__,type(self).__name__,repr(self),id(self),len(self.__args),len(args)))
        for i in xrange(len(args)):
            if i < len(self.__args):
                if self.__args[i] in kwargs:
                    raise TypeError("<{0:s}.{1:s}({2:s}) object at {3:0=#10x}>() got multiple values for keyword argument '{4:s}'".format(
                        type(self).__module__,type(self).__name__,repr(self),id(self),self.__args[i]))
                self.variables[self.__args[i]] = args[i]
        self.variables.update(kwargs)
        for arg in self.__argsused:
            if arg not in self.variables:
                min_args = len(self.__argsused - (set(self.__vars.keys()) | set(constants.keys())))
                raise TypeError("<{0:s}.{1:s}({2:s}) object at {3:0=#10x}>() takes at least {4:d} arguments ({5:d} given) '{6:s}' not defined".format(
                    type(self).__module__,type(self).__name__,repr(self),id(self),min_args,len(args)+len(kwargs),arg))
        expr = self.__expr[::-1]
        args = [];
        while len(expr) > 0:
            t = expr.pop()
            r = t(args,self)
            args.append(r)
        if len(args) > 1:
            return args
        else:
            return args[0]
        
    def __next(self,__expect_op):
        if __expect_op:
            m = gematch.match(self.__expression)    
            if m != None:
                self.__expression = self.__expression[m.end():]
                g = m.groups()
                return g[0],'CLOSE'
            m = smatch.match(self.__expression)
            if m != None:
                self.__expression = self.__expression[m.end():]
                return ",",'SEP'
            m = omatch.match(self.__expression)    
            if m != None:
                self.__expression = self.__expression[m.end():]
                g = m.groups()
                return g[0],'OP'
        else:
            m = gsmatch.match(self.__expression)    
            if m != None:
                self.__expression = self.__expression[m.end():]
                g = m.groups()
                return g[0],'OPEN'
            m = vmatch.match(self.__expression)
            if m != None:
                self.__expression = self.__expression[m.end():]
                g = m.groupdict(0)
                if g["ivalue"]:
                    return complex(int(g["rsign"]+"1")*float(g["rvalue"])*10**int(g["rexpoent"]),int(g["isign"]+"1")*float(g["ivalue"])*10**int(g["iexpoent"])),'VALUE'
                elif g["rexpoent"] or g["rvalue"].find('.')>=0:
                    return int(g["rsign"]+"1")*float(g["rvalue"])*10**int(g["rexpoent"]),'VALUE'
                else:
                    return int(g["rsign"]+"1")*int(g["rvalue"]),'VALUE'
            m = nmatch.match(self.__expression)
            if m != None:
                self.__expression = self.__expression[m.end():]
                g = m.groups()
                return g[0],'NAME'
            m = fmatch.match(self.__expression)
            if m != None:
                self.__expression = self.__expression[m.end():]
                g = m.groups()
                return g[0],'FUNC'
            m = umatch.match(self.__expression)
            if m != None:
                self.__expression = self.__expression[m.end():]
                g = m.groups()
                return g[0],'UNARY'
            return None

    def show(self):
        """Show RPN tokens
        
        This will print out the internal token list (RPN) of the expression
        one token perline.
        """
        for expr in self.__expr:
            print(expr)
            
    def __str__(self):
        """str(fn)
        
        Generates a Printable version of the Expression
        
        Returns
        -------
        str
            Latex String respresation of the Expression, suitable for rendering the equation
        """
        expr = self.__expr[::-1]
        args = [];
        while len(expr) > 0:
            t = expr.pop()
            r = t.toStr(args,self)
            args.append(r)
        if len(args) > 1:
            return args
        else:
            return args[0]

    def __repr__(self):
        """repr(fn)
        
        Generates a String that correctrly respresents the equation
        
        Returns
        -------
        str
            Convert the Expression to a String that passed to the constructor, will constuct
            an identical equation object (in terms of sequence of tokens, and token type/value)
        """
        expr = self.__expr[::-1]
        args = [];
        while len(expr) > 0:
            t = expr.pop()
            r = t.toRepr(args,self)
            args.append(r)
        if len(args) > 1:
            return args
        else:
            return args[0]
    
    def __iter__(self):
        return iter(self.__argsused)
            
    def __lt__(self, other):
        if isinstance(other, Expression):
            return repr(self) < repr(other)
        else:
            raise TypeError("{0:s} is not an {1:s} Object, and can't be compared to an Expression Object".format(repr(other), type(other)))

    def __eq__(self, other):
        if isinstance(other, Expression):
            return repr(self) == repr(other)
        else:
            raise TypeError("{0:s} is not an {1:s} Object, and can't be compared to an Expression Object".format(repr(other), type(other)))
    
    def __combine(self,other,op):  
        if op not in ops or not isinstance(other,(int,float,complex,type(self),basestring)):
            return NotImplemented
        else:
            obj = type(self)(self)
            if isinstance(other,(int,float,complex)):
                obj.__expr.append(ExpressionValue(other))
            else:
                if isinstance(other,basestring):
                    try:
                        other = type(self)(other)
                    except:
                        raise SyntaxError("Can't Convert string, \"{0:s}\" to an Expression Object".format(other))
                obj.__expr += other.__expr
                obj.__argsused |= other.__argsused
                for v in other.__args:
                    if v not in obj.__args:
                        obj.__args.append(v)
                for k,v in other.__vars.items():
                    if k not in obj.__vars:
                        obj.__vars[k] = v
                    elif v != obj.__vars[k]:
                        raise RuntimeError("Predifined Variable Conflict in '{0:s}' two differing values defined".format(k))
            fn = ops[op]
            obj.__expr.append(ExpressionFunction(fn['func'],fn['args'],fn['str'],fn['latex'],op,False))
        return obj

    def __rcombine(self,other,op):
        if op not in ops or not isinstance(other,(int,float,complex,type(self),basestring)):
            return NotImplemented
        else:
            obj = type(self)(self)
            if isinstance(other,(int,float,complex)):
                obj.__expr.insert(0,ExpressionValue(other))
            else:
                if isinstance(other,basestring):
                    try:
                        other = type(self)(other)
                    except:
                        raise SyntaxError("Can't Convert string, \"{0:s}\" to an Expression Object".format(other))
                obj.__expr = other.__expr + self.__expr
                obj.__argsused = other.__argsused | self.__expr
                __args = other.__args
                for v in obj.__args:
                    if v not in __args:
                        __args.append(v)
                obj.__args = __args
                for k,v in other.__vars.items():
                    if k not in obj.__vars:
                        obj.__vars[k] = v
                    elif v != obj.__vars[k]:
                        raise RuntimeError("Predifined Variable Conflict in '{0:s}' two differing values defined".format(k))
            fn = ops[op]
            obj.__expr.append(ExpressionFunction(fn['func'],fn['args'],fn['str'],fn['latex'],op,False))
        return obj
        
    def __icombine(self,other,op):  
        if op not in ops or not isinstance(other,(int,float,complex,type(self),basestring)):
            return NotImplemented
        else:
            obj = self
            if isinstance(other,(int,float,complex)):
                obj.__expr.append(ExpressionValue(other))
            else:
                if isinstance(other,basestring):
                    try:
                        other = type(self)(other)
                    except:
                        raise SyntaxError("Can't Convert string, \"{0:s}\" to an Expression Object".format(other))
                obj.__expr += other.__expr
                obj.__argsused |= other.__argsused
                for v in other.__args:
                    if v not in obj.__args:
                        obj.__args.append(v)
                for k,v in other.__vars.items():
                    if k not in obj.__vars:
                        obj.__vars[k] = v
                    elif v != obj.__vars[k]:
                        raise RuntimeError("Predifined Variable Conflict in '{0:s}' two differing values defined".format(k))
            fn = ops[op]
            obj.__expr.append(ExpressionFunction(fn['func'],fn['args'],fn['str'],fn['latex'],op,False))
        return obj

    def __apply(self,op):
        fn = unary_ops[op]
        obj = type(self)(self)
        obj.__expr.append(ExpressionFunction(fn['func'],1,fn['str'],fn['latex'],op,False))
        return obj
    
    def __applycall(self,op):
        fn = functions[op]
        if 1 not in fn['args'] or '*' not in fn['args']:
            raise RuntimeError("Can't Apply {0:s} function, dosen't accept only 1 argument".format(op))
        obj = type(self)(self)
        obj.__expr.append(ExpressionFunction(fn['func'],1,fn['str'],fn['latex'],op,False))
        return obj

    def __add__(self,other):
        return self.__combine(other,'+')
    
    def __sub__(self,other):
        return self.__combine(other,'-')
    
    def __mul__(self,other):
        return self.__combine(other,'*')
    
    def __div__(self,other):
        return self.__combine(other,'/')
    
    def __truediv__(self,other):
        return self.__combine(other,'/')
    
    def __pow__(self,other):
        return self.__combine(other,'^')  
    
    def __mod__(self,other):
        return self.__combine(other,'%')
    
    def __and__(self,other):
        return self.__combine(other,'&')
        
    def __or__(self,other):
        return self.__combine(other,'|')
    
    def __xor__(self,other):
        return self.__combine(other,'</>')
    
    def __radd__(self,other):
        return self.__rcombine(other,'+')
    
    def __rsub__(self,other):
        return self.__rcombine(other,'-')
    
    def __rmul__(self,other):
        return self.__rcombine(other,'*')
    
    def __rdiv__(self,other):
        return self.__rcombine(other,'/')
    
    def __rtruediv__(self,other):
        return self.__rcombine(other,'/')
    
    def __rpow__(self,other):
        return self.__rcombine(other,'^')  
    
    def __rmod__(self,other):
        return self.__rcombine(other,'%')
    
    def __rand__(self,other):
        return self.__rcombine(other,'&')
        
    def __ror__(self,other):
        return self.__rcombine(other,'|')
    
    def __rxor__(self,other):
        return self.__rcombine(other,'</>')
        
    def __iadd__(self,other):
        return self.__icombine(other,'+')
    
    def __isub__(self,other):
        return self.__icombine(other,'-')
    
    def __imul__(self,other):
        return self.__icombine(other,'*')
    
    def __idiv__(self,other):
        return self.__icombine(other,'/')
    
    def __itruediv__(self,other):
        return self.__icombine(other,'/')
    
    def __ipow__(self,other):
        return self.__icombine(other,'^')  
    
    def __imod__(self,other):
        return self.__icombine(other,'%')
    
    def __iand__(self,other):
        return self.__icombine(other,'&')
        
    def __ior__(self,other):
        return self.__icombine(other,'|')
    
    def __ixor__(self,other):
        return self.__icombine(other,'</>')
    
    def __neg__(self):
        return self.__apply('-')
    
    def __invert__(self):
        return self.__apply('!')
    
    def __abs__(self):
        return self.__applycall('abs')
    
    def __getfunction(self,op):
        if op[1] == 'FUNC':
            fn = functions[op[0]]
            fn['type'] = 'FUNC'            
        elif op[1] == 'UNARY':
            fn = unary_ops[op[0]]
            fn['type'] = 'UNARY'
            fn['args'] = 1
        elif op[1] == 'OP':
            fn = ops[op[0]]
            fn['type'] = 'OP'
        return fn            

    def __compile(self):
        self.__expr = []
        stack = []
        argc = []
        __expect_op = False
        v = self.__next(__expect_op)
        while v != None:
            if not __expect_op and v[1] == "OPEN":
                stack.append(v)
                __expect_op = False       
            elif __expect_op and v[1] == "CLOSE":
                op = stack.pop()
                while op[1] != "OPEN":
                    fs = self.__getfunction(op)
                    self.__expr.append(ExpressionFunction(fs['func'],fs['args'],fs['str'],fs['latex'],op[0],False))
                    op = stack.pop()
                if len(stack) > 0 and stack[-1][0] in functions:
                    op = stack.pop()
                    fs = functions[op[0]]
                    args = argc.pop()
                    if fs['args'] != '+' and (args != fs['args'] and args not in fs['args']):
                        raise SyntaxError("Invalid number of arguments for {0:s} function".format(op[0]))
                    self.__expr.append(ExpressionFunction(fs['func'],args,fs['str'],fs['latex'],op[0],True))
                __expect_op = True
            elif __expect_op and v[0] == ",":
                argc[-1] += 1
                op = stack.pop()
                while op[1] != "OPEN":
                    fs = self.__getfunction(op)
                    self.__expr.append(ExpressionFunction(fs['func'],fs['args'],fs['str'],fs['latex'],op[0],False))
                    op = stack.pop()
                stack.append(op)
                __expect_op = False
            elif __expect_op and v[0] in ops:
                fn = ops[v[0]]
                if len(stack) == 0:
                    stack.append(v)
                    __expect_op = False
                    v = self.__next(__expect_op)
                    continue
                op = stack.pop()
                if op[0] == "(":
                    stack.append(op)
                    stack.append(v)
                    __expect_op = False
                    v = self.__next(__expect_op)
                    continue
                fs = self.__getfunction(op)
                while True:
                    if (fn['prec'] >= fs['prec']):
                        self.__expr.append(ExpressionFunction(fs['func'],fs['args'],fs['str'],fs['latex'],op[0],False))
                        if len(stack) == 0:
                            stack.append(v)
                            break
                        op = stack.pop()
                        if op[0] == "(":
                            stack.append(op)
                            stack.append(v)
                            break                            
                        fs = self.__getfunction(op)
                    else:
                        stack.append(op)
                        stack.append(v)
                        break
                __expect_op = False
            elif not __expect_op and v[0] in unary_ops:
                fn = unary_ops[v[0]]
                stack.append(v)
                __expect_op = False
            elif not __expect_op and v[0] in functions:
                stack.append(v)
                argc.append(1)
                __expect_op = False
            elif not __expect_op and v[1] == 'NAME':
                self.__argsused.add(v[0])
                if v not in self.__args:
                    self.__args.append(v[0])
                self.__expr.append(ExpressionVariable(v[0]))
                __expect_op = True
            elif not __expect_op and v[1] == 'VALUE':
                self.__expr.append(ExpressionValue(v[0]))
                __expect_op = True
            else:
                raise SyntaxError("Invalid Token \"{0:s}\" in Expression, Expected {1:s}".format(v,"Op" if __expect_op else "Value"))
            v = self.__next(__expect_op)
        if len(stack) > 0:
            op = stack.pop()
            while op != "(":
                fs = self.__getfunction(op)
                self.__expr.append(ExpressionFunction(fs['func'],fs['args'],fs['str'],fs['latex'],op[0],False))
                if len(stack) > 0:
                    op = stack.pop()
                else:
                    break

constants = {}
unary_ops = {}
ops = {}
functions = {}
smatch = re.compile("\s*,")
vmatch = re.compile("\s*(?P<rsign>[+-]?)\s*(?P<rvalue>(?:\d+\.\d+|\d+\.|\.\d+|\d+))(?:[Ee](?P<rexpoent>[+-]?\d+))?(?:\s*(?P<sep>(?(rvalue)\+|))?\s*(?P<isign>(?(rvalue)(?(sep)[+-]?|[+-])|[+-]?)?)\s*(?P<ivalue>(?:\d+\.\d+|\d+\.|\.\d+|\d+))(?:[Ee](?P<iexpoent>[+-]?\d+))?[ij])?")
nmatch = re.compile("\s*([a-zA-Z_][a-zA-Z0-9_]*)")
gsmatch = re.compile('\s*(\()')
gematch = re.compile('\s*(\))')

def recalculateFMatch():
    global fmatch, omatch, umatch
    fks = sorted(functions.keys(), key=len, reverse=True)
    oks = sorted(ops.keys(), key=len, reverse=True)
    uks = sorted(unary_ops.keys(), key=len, reverse=True)
    fmatch = re.compile('\s*(' + '|'.join(map(re.escape,fks)) + ')')
    omatch = re.compile('\s*(' + '|'.join(map(re.escape,oks)) + ')')
    umatch = re.compile('\s*(' + '|'.join(map(re.escape,uks)) + ')')
