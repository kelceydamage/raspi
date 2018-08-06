#! /usr/bin/env python3

# License
#---------------------------------------------------------------------------------------------------- <-100
# Author: Kelcey Damage
# Python: 3.5+

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Imports
#---------------------------------------------------------------------------------------------------- <-100
from distutils.core import setup
from distutils.extension import Extension
import platform

# Constants
#---------------------------------------------------------------------------------------------------- <-100
USE_CYTHON = True
CYTHON_TRACE = False
LANGUAGE = 'c++'
CPP_VERSION = '11'

# Main
#---------------------------------------------------------------------------------------------------- <-100
ext = '.pyx' if USE_CYTHON else '.c'

extentions = [
    Extension(
        "motors/drive", 
        sources=["motors/drive{0}".format(ext)],
        extra_compile_args=['-std={0}{1}'.format(LANGUAGE, CPP_VERSION)],
        language=LANGUAGE,
        compiler_directives={'linetrace': CYTHON_TRACE}
        )
    ]

if USE_CYTHON:
    try:
        from Cython.Build import cythonize
        import Cython
    except ImportError as e:
        print('ERROR: Cython not found. Please install (pip install cython) and try again')
    else:
        Cython.Compiler.Options.annotate = True
        Cython.Compiler.Options.warning_errors = True
        Cython.Compiler.Options.convert_range = True
        Cython.Compiler.Options.cache_builtins = True
        Cython.Compiler.Options.gcc_branch_hints = True
        Cython.Compiler.Options.embed = "main"
        extentions = cythonize(extentions)

setup(
    ext_modules = extentions
)
