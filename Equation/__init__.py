# ==============================================================================
#   Copyright 2014 AlphaOmega Technology
#
#   Licensed under the AlphaOmega Technology Open License Version 1.0
#   You may not use this file except in compliance with this License.
#   You may obtain a copy of the License at
#
#       http://www.alphaomega-technology.com.au/license/AOT-OL/1.0
# ==============================================================================
"""
Equation Module
===============

This is the only module you should need to import

It maps the Expression Class from `Equation.core.Expression`

Its recomended you use the code::

    from Equation import Expression
    ...

to import the Expression Class, as this is the only Class/Function you
should use.

.. moduleauthor:: Glen Fletcher <glen.fletcher@alphaomega-technology.com.au>
"""

from ._info import (__authors__, __copyright__, __license__,
                    __contact__, __version__, __title__, __desc__)
from .core import Expression

all = ['util']


def _load():
    import os
    import os.path
    import sys
    import traceback
    import importlib
    from .core import recalculateFMatch

    plugins_loaded = {}
    if __name__ == "__main__":
        dirname = os.path.abspath(os.getcwd())
        prefix = ""
    else:
        dirname = os.path.dirname(os.path.abspath(__file__))
        if __package__ is not None:
            prefix = __package__ + "."
        else:
            prefix = ""
    for file in os.listdir(dirname):
        plugin_file, extension = os.path.splitext(os.path.basename(file))
        if not plugin_file.lower().startswith("equation_", 0, 9) or extension.lower() not in ['.py', '.pyc']:  # noqa: E501
            continue
        if plugin_file not in plugins_loaded:
            plugins_loaded[plugin_file] = 1
            try:
                plugin_script = importlib.import_module(prefix + plugin_file)
            except:  # noqa: E722
                errtype, errinfo, errtrace = sys.exc_info()
                fulltrace = ''.join(traceback.format_exception(errtype, errinfo, errtrace)[1:])
                sys.stderr.write(
                    f"Was unable to load {plugin_file}: {errinfo}\nTraceback:"
                    f"\n{fulltrace}\n")
                continue
            if not hasattr(plugin_script, 'equation_extend'):
                sys.stderr.write(
                    f"The plugin '{plugin_file}' from file "
                    f"'{dirname.rstrip('/') + '/' + plugin_file + extension}'"
                    " is invalid because its missing the attribute 'equation_extend'\n")
                continue
            plugin_script.equation_extend()
    recalculateFMatch()


_load()
