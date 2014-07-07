# -*- coding: utf-8 -*-
"""
Created on Fri Apr 11 00:30:51 2014

.. moduleauthor:: Glen Fletcher <glen.fletcher@alphaomega-technology.com.au>
"""
from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages
import os.path
import re

pkg_name = 'Equation'
pkg = {}
with open(os.path.join(pkg_name,'_info.py')) as f: exec(f.read(),pkg,pkg)

reimg = re.compile("^!\[(?P<label>[^\]]*)\]\((?P<src>[^\)]*)\)$")
relink = re.compile("\[(?P<label>[^\]]*)\]\((?P<href>[^\)]*)\)")
reimglink = re.compile(
"^\[!\[(?P<label>[^\]]*)\]\((?P<src>[^\)]*)\)\]\((?P<href>[^\)]*)\)$")

def read(fname):
    """Read Markdown File And Convert to reST"""
    imgindex = 0
    lines = ""
    for line in open(os.path.join(os.path.dirname(__file__), fname),'rt'):
        m = reimg.match(line)
        if m is not None:
            g = m.groupdict()
            if g['label'] is None:
                g['label'] = 'image' + imgindex
                imgindex += 1
            lines = "|{label:s}|\n\n.. |{label:s}| image:: {src:s}\n".format(
                        **g)
            continue
        m = reimglink.match(line)
        if m is not None:
            g = m.groupdict()
            if g['label'] is None:
                g['label'] = 'image' + imgindex
                imgindex += 1
            lines += "|{label:s}|\n\n.. |{label:s}| image:: {src:s}\n"\
                "   :target: {href:s}".format(**g)
            continue
        if line[0:5] == "Note:":
            line = ".. Note::" + line[5:]
        line = relink.sub('`\g<label> <\g<href>>`_',line)
        lines += line
    return lines

def readlist(fname):
    return open(os.path.join(
        os.path.dirname(__file__),
        fname),'rt').read().split('\n')

if '__appname__' in pkg:
    console_scripts = [pkg['__appname__'] + '=' + pkg_name + ".console:run"]
else:
    console_scripts = None

entry_points = {}
if console_scripts is not None:
    entry_points['console_script'] = console_scripts

setup(
    name=pkg['__title__'],
    version=pkg['__version__'],
    author=pkg['__authors__'][0][0],
    author_email=pkg['__authors__'][0][1],
    license=pkg['__license__'],
    description=pkg['__desc__'],
    packages=find_packages(),
    url='https://github.com/alphaomega-technology/' + pkg['__title__'],
    long_description=read('README.md'),
    entry_points=entry_points,
    install_requires = [],
    extras_require = {
        'VectorMaths': ['numpy'],
        'SciConst': ['scipy>=0.12.0']
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Mathematics",
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
    ],
    zip_safe=False,
    test_suite='tests',
)
