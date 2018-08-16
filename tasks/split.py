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
            os.path.abspath(__file__)
            )
        )
    )
from task_engine.client.client import TaskClient
from common.print_helpers import print_nested, print_package, printc, Colours

# Globals
# ------------------------------------------------------------------------ 79->
TC = TaskClient('task-split')

# Classes
# ------------------------------------------------------------------------ 79->

# Functions
# ------------------------------------------------------------------------ 79->
def distribute(data, func, kwargs):
	TC.setup_container(func)
	TC.insert(func, kwargs=kwargs)
	TC.send()

def task_split(*args, **kwargs):
	return kwargs

# Main
# ------------------------------------------------------------------------ 79->
if __name__ == '__main__':
	pass



