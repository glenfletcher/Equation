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
    url='https://github.com/alphaomega-technology/Equation',
    long_description=read('README.md'),
    install_requires = ["numpy"],
)