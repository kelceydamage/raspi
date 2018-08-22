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
from common.print_helpers import Colours
from common.print_helpers import printc
import zlib

# Globals
# ------------------------------------------------------------------------ 79->
COLOURS = Colours()

# Classes
# ------------------------------------------------------------------------ 79->

# Functions
# ------------------------------------------------------------------------ 79->
def task_open_file(kwargs):
    printc('Starting Task: Open File', COLOURS.LIGHTBLUE)
    file_name = kwargs['kwargs']['file']
    file_path = kwargs['kwargs']['path']
    with open('{0}/{1}'.format(file_path, file_name), 'rb') as f:
        r = f.read()
        z = zlib.decompress(r).decode()
    parts = z.split(kwargs['kwargs']['delimiter'])
    results = []
    for i in range(len(parts)):
        results.append((kwargs['completed'][-1], parts.pop().strip('\n')))
    del parts
    return results

# Main
# ------------------------------------------------------------------------ 79->
