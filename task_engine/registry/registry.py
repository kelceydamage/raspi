#!/usr/bin/env python3
# ------------------------------------------------------------------------ 79->
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
# ------------------------------------------------------------------------ 79->

# Imports
# ------------------------------------------------------------------------ 79->
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
import importlib

# Globals
# ------------------------------------------------------------------------ 79->

# Classes
# ------------------------------------------------------------------------ 79->

# Functions
# ------------------------------------------------------------------------ 79->
def load_tasks(dirname):
    """
NAME:           load_tasks
DESCRIPTION:    Auto loader and parser for task modules. This function is written for
                efficiency, so I appologize for lack of readability.
    """
    functions = {}
    member_list = []
    for importer, package_name, _ in pkgutil.iter_modules([dirname]):
        full_package_name = 'tasks.%s' % (package_name)
        if package_name not in sys.modules:
            try:
                module = importer.find_module(package_name).load_module()
                for member in [x for x in dir(module) if 'task_' in x]:
                    functions[member] = '{0}.{1}'.format(package_name, member)
            except Exception as e:
                print(e)

    return functions

# Main
# ------------------------------------------------------------------------ 79->