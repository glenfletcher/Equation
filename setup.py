# -*- coding: utf-8 -*-
"""
Created on Fri Apr 11 00:30:51 2014

.. moduleauthor:: Glen Fletcher <glen.fletcher@alphaomega-technology.com.au>
"""
from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages
import os.path


import Equation as pkg


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name=pkg.__title__,
    version=pkg.__version__,
    author=pkg.__authors__[0][0],
    author_email=pkg.__authors__[0][1],
    license=pkg.__license__,
    packages=find_packages(),
    url='https://github.com/alphaomega-technology/' + pkg.__title__,
    long_description=read('README.md'),
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
