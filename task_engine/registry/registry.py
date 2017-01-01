#!/usr/bin/env python
#-------------------------------------------------------------------------------- <-80
# Author: Kelcey Damage
# Python: 2.7

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Doc
#-------------------------------------------------------------------------------- <-80
"""
SUMMARY:        Registry of trusted functions for execution
"""

# Imports
#-------------------------------------------------------------------------------- <-80
import os
os.sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
                )
            )
        )
    )
from inspect import getmembers
from inspect import isfunction
import pkgutil
import sys

# Globals
#-------------------------------------------------------------------------------- <-80

# Classes
#-------------------------------------------------------------------------------- <-80

# Functions
#-------------------------------------------------------------------------------- <-80
def load_tasks(dirname):
    """
NAME:           load_tasks
DESCRIPTION:    Auto loader and parser for task modules. This function is written for
                efficiency, so I appologize for lack of readability.
    """
    functions = {}
    member_list = []
    for importer, package_name, _ in pkgutil.iter_modules([dirname]):
        full_package_name = '%s.%s' % (dirname, package_name)
        if full_package_name not in sys.modules:
            module = importer.find_module(package_name).load_module(full_package_name)
            for member in [x for x in dir(module) if 'TASK_' in x]:
                functions[member] = member

    return functions

# Main
#-------------------------------------------------------------------------------- <-80
functions = load_tasks('../../tasks')
