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
import re
import glob
import os
import os.path
import sys
import traceback
import importlib

class ExpressionObject (object):
    def __init__(self,expression,*args,**kwargs):
        super(ExpressionObject,self).__init__(*args,**kwargs)
        self.expression = expression

    def tostr(self,it):
        return ""

    def torepr(self,it):
        return ""

    def __call__(self,it):
        pass
        

class ExpressionValue( ExpressionObject ):
    def __init__(self,value,*args,**kwargs):
        super(ExpressionValue,self).__init__(*args,**kwargs)
        self.value = value

    def tostr(self,args):
        return str(self.value)
    
    def torepr(self,args):
        return str(self.value)

    def __call__(self,args):
        return self.value
    
    def __repr__(self):
            return "<{0:s}.{1:s}({2:s}) object at {3:0=#10x}>".format(type(self).__module__,type(self).__name__,str(self.value),id(self))

class ExpressionFunction( ExpressionObject ):
    def __init__(self,function,nargs,display,id,isfunc,*args,**kwargs):
        super(ExpressionFunction,self).__init__(*args,**kwargs)
        self.function = function
        self.nargs = nargs
        self.display = display
        self.id = id
        self.isfunc = isfunc

    def tostr(self,args):
        params = []
        for i in xrange(self.nargs):
            params.append(args.pop())
        if self.isfunc:
            return str(self.display.format(','.join(params[::-1])))
        else:
            return str(self.display.format(*params[::-1]))
            
    def torepr(self,args):
        params = []
        for i in xrange(self.nargs):
            params.append(args.pop())
        if self.isfunc:
            return str(self.display.format(','.join(params[::-1])))
        else:
            return str(self.display.format(*params[::-1]))
            
    def __call__(self,args):
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

    def tostr(self,args):
        return str(self.name)

    def torepr(self,args):
        return str(self.name)

    def __call__(self,args):
        return self.expression.variables[self.name]
        
    def __repr__(self):
        return "<{0:s}.{1:s}({2:s}) object at {3:0=#10x}>".format(type(self).__module__,type(self).__name__,str(self.name),id(self))
            
def addFn(id,str,args,func):
    global fmatch
    sys.modules[__name__].functions[id] = {
        'str': str,
        'args': args,
        'prec': 1,
        'type': 'FUNC',
        'func': func}

def addOp(id,str,single,prec,left,func):
    global fmatch
    sys.modules[__name__].functions[id] = {
        'str': str,
        'args': 1 if single else 2,
        'prec': prec,
        'type': 'LEFT' if left else 'RIGHT',
        'func': func}

def addConst(name,value):
    sys.modules[__name__].constants[name] = value

class Expression( object ):
    
    def __init__(self,expression,*args,**kwargs):
        super(Expression,self).__init__(*args,**kwargs)
        self.__expression = expression
        self.__compile()

    def __call__(self,**variables):
        self.variables = sys.modules[__name__].constants # i.e. pi, e, i, etc.
        self.variables.update(variables)
        expr = self.__expr[::-1]
        args = [];
        while len(expr) > 0:
            t = expr.pop()
            r = t(args)
            args.append(r)
        if len(args) > 1:
            return args
        else:
            return args[0]
        
    def __next(self):
        m = sys.modules[__name__].fmatch.match(self.__expression)
        if m != None:
            self.__expression = self.__expression[m.end():]
            g = m.groups()
            return g[0]
        m = sys.modules[__name__].nmatch.match(self.__expression)
        if m != None:
            self.__expression = self.__expression[m.end():]
            g = m.groups()
            return g[0]
        m = sys.modules[__name__].vmatch.match(self.__expression)
        if m != None:
            self.__expression = self.__expression[m.end():]
            g = m.groupdict(0)
            return np.complex(float(g["rvalue"])*10**float(g["rexpoent"]),float(g["ivalue"])*10**float(g["iexpoent"]))
        m = sys.modules[__name__].smatch.match(self.__expression)
        if m != None:
            self.__expression = self.__expression[m.end():]
            return ","
        return None

    def show(self): 
        for expr in self.__expr:
            print expr
            
    def __str__(self):
        expr = self.__expr[::-1]
        args = [];
        while len(expr) > 0:
            t = expr.pop()
            r = t.tostr(args)
            args.append(r)
        if len(args) > 1:
            return args
        else:
            return args[0]

    def __repr__(self):
        expr = self.__expr[::-1]
        args = [];
        while len(expr) > 0:
            t = expr.pop()
            r = t.torepr(args)
            args.append(r)
        if len(args) > 1:
            return args
        else:
            return args[0]

    def __compile(self):
        self.__expr = []
        stack = []
        argc = []
        v = self.__next()
        while v != None:
            if v == "(":
                stack.append(v)
            elif v == ")":
                op = stack.pop()
                while op != "(":
                    fs = sys.modules[__name__].functions[op]
                    self.__expr.append(ExpressionFunction(fs['func'],fs['args'],fs['str'],op,False,self))
                    op = stack.pop()
                if len(stack) > 0 and stack[-1] in sys.modules[__name__].functions and sys.modules[__name__].functions[stack[-1]]['type'] == 'FUNC':
                    op = stack.pop()
                    fs = sys.modules[__name__].functions[op]
                    args = argc.pop()
                    if fs['args'] != '+' or (args != fs['args'] and args not in fs['args']):
                        self.__expr.append(ExpressionFunction(fs['func'],args,fs['str'],op,True,self))
            elif v == ",":
                argc[-1] += 1
                op = stack.pop()
                while op != "(":
                    fs = sys.modules[__name__].functions[op]
                    self.__expr.append(ExpressionFunction(fs['func'],fs['args'],fs['str'],op,False,self))
                    op = stack.pop()
                stack.append(op)
            elif v in sys.modules[__name__].functions:
                fn = sys.modules[__name__].functions[v]
                if fn['type'] == 'FUNC':
                    stack.append(v)
                    argc.append(1)
                else:
                    if len(stack) == 0:
                        stack.append(v)
                        v = self.__next()
                        continue
                    op = stack.pop()
                    if op == "(":
                        stack.append(op)
                        stack.append(v)
                        v = self.__next()
                        continue
                    fs = sys.modules[__name__].functions[op]
                    while True:
                        if (fn['type'] == 'LEFT' and fn['prec'] == fs['prec']) or (fn['prec'] < fs['prec']):
                            self.__expr.append(ExpressionFunction(fs['func'],fs['args'],fs['str'],op,False,self))
                            if len(stack) == 0:
                                stack.append(v)
                                break
                            if op == "(":
                                stack.append(op)
                                stack.append(v)
                                break
                            op = stack.pop()
                            fs = sys.modules[__name__].functions[op]
                        else:
                            stack.append(op)
                            stack.append(v)
                            break
            elif isinstance(v,basestring):
                self.__expr.append(ExpressionVariable(v,self))
            else:
                self.__expr.append(ExpressionValue(v,self))
            v = self.__next()
        if len(stack) > 0:
            op = stack.pop()
            while op != "(":
                fs = sys.modules[__name__].functions[op]
                self.__expr.append(ExpressionFunction(fs['func'],fs['args'],fs['str'],op,False,self))
                if len(stack) > 0:
                    op = stack.pop()
                else:
                    break

def Load():
    if not hasattr(Load, "loaded"):
        Load.loaded = False
    if not Load.loaded:
        Load.loaded = True
        sys.modules[__name__].constants = {}
        sys.modules[__name__].functions = {}
        sys.modules[__name__].smatch = re.compile("\s*,")
        sys.modules[__name__].vmatch = re.compile("\s*(?P<rvalue>[+-]?(?:\d+\.\d+|\d+\.|\.\d+|\d+))(?:[Ee](?P<rexpoent>[+-]\d+))?(?:\s*(?P<sep>\+)?\s*(?P<ivalue>(?(rvalue)(?(sep)[+-]?|[+-])|[+-]?)?(?:\d+\.\d+|\d+\.|\.\d+|\d+))(?:[Ee](?P<iexpoent>[+-]\d+))?[ij])?")
        sys.modules[__name__].nmatch = re.compile("\s*([a-zA-Z_][a-zA-Z0-9_]*)")
        Plugins = {}
        PluginsLoaded = {}
        if __name__ == "__main__":
            dir = os.getcwd()
        else:
            dir = os.path.dirname(__PATH__)
        sys.path.append(dir)
        for file in glob.glob(dir + "/equation_*.py"):
            Pluginfile,extension = os.path.splitext(os.path.basename(file))
            if (Pluginfile == "__init__"):
                continue
            if (((extension == '.py') or (extension == '.pyc')) and (not PluginsLoaded.has_key(Pluginfile))):
                PluginsLoaded[Pluginfile] = 1
                try:
                        PluginScript = importlib.import_module(Pluginfile)
                except:
                        errtype, errinfo, errtrace = sys.exc_info()
                        fulltrace = ''.join(traceback.format_exception(errtype, errinfo, errtrace)[1:])
                        print "Was unable to load {0:s}: {1:s}\nTraceback:\n{2:s}".format(Pluginfile, errinfo, fulltrace)
                        continue
                if not hasattr(PluginScript,'equation_extend'):
                    print "The plugin '{0:s}' from file '{1:s}' is invalid because its missing the attribute 'equation_extend'".format(Pluginfile,(dir.rstrip('/') + '/' + Pluginfile + '.' + extension))
                    continue
                PluginScript.equation_extend(addOp,addFn,addConst)
                print "{0:s} Loaded".format(Pluginfile)
        sys.modules[__name__].fmatch = re.compile('\s*(\(|\)|' + '|'.join(map(re.escape,sys.modules[__name__].functions.keys())) + ')')
Load()