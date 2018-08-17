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
from common.datatypes import MetaFrame
from common.datatypes import DataFrame
from common.print_helpers import Colours
from common.print_helpers import printc

# Globals
# ------------------------------------------------------------------------ 79->
COLOURS = Colours()

# Classes
# ------------------------------------------------------------------------ 79->

# Functions
# ------------------------------------------------------------------------ 79->
def task_end(*args, **kwargs):
    printc('PIPELINE COMPLETE: Termination Task', COLOURS.PURPLE)
    p_serial = kwargs['p_serial']
    meta = MetaFrame(0)
    meta.set_serial(p_serial)
    data = DataFrame(0)
    if isinstance(kwargs['data'], list):
        data.set_data(kwargs['data'])
    else:
        data.set_data([kwargs['data']])
    return [meta.serialize(), data.serialize()]

# Main
# ------------------------------------------------------------------------ 79->



