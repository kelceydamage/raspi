#!/usr/bin/env python3
#-------------------------------------------------------------------------- 80->
# Author: ${name=Kelcey Damage}
# Python: 3.5+
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Doc
#-------------------------------------------------------------------------- 80->
# To run this use:
# [cmdline]$ python3 setup.py $FILNAME_AS_ARG_$0 build_ext --inplace --force 

# Imports
#-------------------------------------------------------------------------- 80->
from distutils.core import setup
from distutils.extension import Extension
import platform
import sys

# Globals
#-------------------------------------------------------------------------- 80->
USE_CYTHON = True
CYTHON_TRACE = False
LANGUAGE = 'c++'
CPP_VERSION = '11'
FILES = sys.argv[1:-3]

# Classes
#-------------------------------------------------------------------------- 80->

# Functions
#-------------------------------------------------------------------------- 80->

# Main
#-------------------------------------------------------------------------- 80->
if __name__ == '__main__':
    ext = '.pyx' if USE_CYTHON else '.c'
    extentions = []
    print('COMPILING: {0}\n'.format(FILES))

    '''
    for file in FILES:
        sys.argv.pop(sys.argv.index(file))
        x = Extension(
            "{0}".format(file.replace('/', '.')), 
            sources=["{0}{1}".format(file, ext)],
            extra_compile_args=['-std={0}{1}'.format(LANGUAGE, CPP_VERSION)],
            language=LANGUAGE,
            include_dirs=['.']
            )
        extentions.append(x)
    '''

    extentions = [
    Extension(
        "common.marshalling", 
        sources=["common/marshalling{0}".format(ext)],
        extra_compile_args=['-Wno-strict-prototypes', '-std=c++11'],
        language="c++"
        ),
    Extension(
        "common.datatypes", 
        sources=["common/datatypes{0}".format(ext)],
        extra_compile_args=['-Wno-strict-prototypes', '-std=c++11'],
        language="c++"
        ),
    Extension(
        "task_engine.client.client", 
        sources=["task_engine/client/client{0}".format(ext)],
        extra_compile_args=['-Wno-strict-prototypes', '-std=c++11'],
        language="c++"
        ),
    Extension(
        "task_engine.engine.routers", 
        sources=["task_engine/engine/routers{0}".format(ext)],
        extra_compile_args=['-Wno-strict-prototypes', '-std=c++11'],
        language="c++"
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
            extentions = cythonize(
                extentions, 
                compiler_directives={'linetrace': CYTHON_TRACE}
                )
    setup(
        ext_modules = extentions,
        include_dirs=["."]
    )
