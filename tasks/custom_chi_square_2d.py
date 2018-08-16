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
import zlib

# Globals
# ------------------------------------------------------------------------ 79->
TC = TaskClient('task-chi-square-2d')
CHUNKSIZE = 1024

# Classes
# ------------------------------------------------------------------------ 79->

# Functions
# ------------------------------------------------------------------------ 79->
def distribute(data, func, kwargs):
    TC.setup_container('chi2')
    TC.insert(func, kwargs=kwargs)
    TC.send()

def task_custom_chi_square_2d(*args, **kwargs):
    '''
    with open('_pairs/metric_combos_1.list', 'rb') as f:
    r = f.read()
    z = zlib.decompress(r).decode()
    '''

    d = zlib.decompressobj(16+zlib.MAX_WBITS)
    _buffer = []
    file_name = kwargs['file']
    print('open file')
    try:
        with open(file_name, 'rb') as f:
            print('read-buffer')
            buffer = f.read(1024)
            c = 0
            #while line:
            while c < 3:
                outstr = d.decompress(buffer)
                print(outstr)
                buffer.read(CHUNKSIZE)
                c += 1
    except Exception as e:
        return str(e)

        outstr = d.flush()
        kwargs = {'pair': data, 'delimiter': ''}

    #print(args, kwargs)
    return outstr

# Main
# ------------------------------------------------------------------------ 79->
if __name__ == '__main__':
    pass



