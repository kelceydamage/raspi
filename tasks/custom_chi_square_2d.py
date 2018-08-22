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
CHUNKSIZE = 1024
COLOURS = Colours()

# Classes
# ------------------------------------------------------------------------ 79->

# Functions
# ------------------------------------------------------------------------ 79->
def task_custom_chi_square_2d(*args, **kwargs):
    print('starting task')
    d = zlib.decompressobj(zlib.MAX_WBITS|32)
    _buffer = []
    file_name = kwargs['file']
    file_path = kwargs['path']
    outstr = b''
    print('open file')
    try:
        with open('{0}/{1}'.format(file_path, file_name), 'rb') as f:
            print('read-buffer')
            buffer = f.read(1024)
            #c = 0
            #while line:
            print('decompress')
            while buffer:
                #zlib.compress(str_buff)
                outstr += d.decompress(buffer)
                buffer = f.read(CHUNKSIZE)
                #c += 1
    except Exception as e:
        printc(str(e), COLOURS.RED)
        return str(e)

    outstr += d.decompress(buffer)
    out = d.flush()
    outstr = outstr.decode()
    outstr = outstr.split('\n')
    kwargs = {'pair': '', 'delimiter': ''}

    #print(args, kwargs)
    return len(outstr)

# Main
# ------------------------------------------------------------------------ 79->
if __name__ == '__main__':
    pass



