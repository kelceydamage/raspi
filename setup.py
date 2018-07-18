#! /usr/bin/env python3

from distutils.core import setup
from distutils.extension import Extension
import platform

USE_CYTHON = True

ext = '.pyx' if USE_CYTHON else '.c'

extentions = [
    Extension(
        "motors.drive", 
        sources=["motors/drive{0}".format(ext)],
        extra_compile_args=['-Wno-strict-prototypes'],
        language="c++"
        )
    ]

if USE_CYTHON:
    from Cython.Build import cythonize
    extentions = cythonize(extentions)

setup(
    ext_modules = extentions
)
