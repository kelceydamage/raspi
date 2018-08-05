#! /usr/bin/env python3

from distutils.core import setup
from distutils.extension import Extension
import platform

USE_CYTHON = True

ext = '.pyx' if USE_CYTHON else '.c'

extentions = [
    Extension(
        "motors/drive", 
        sources=["motors/drive{0}".format(ext)],
        extra_compile_args=['-std=c++11'],
        language="c++"
        )
    ]

if USE_CYTHON:
    from Cython.Build import cythonize
    import Cython
    Cython.Compiler.Options.annotate = True
    Cython.Compiler.Options.warning_errors = True
    Cython.Compiler.Options.convert_range = True
    Cython.Compiler.Options.cache_builtins = True
    Cython.Compiler.Options.gcc_branch_hints = True
    Cython.Compiler.Options.embed = False
    extentions = cythonize(extentions)

setup(
    ext_modules = extentions
)
