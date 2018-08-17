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
from task_engine.client.client import distribute
from common.print_helpers import Colours
from common.print_helpers import printc
import zlib

# Globals
# ------------------------------------------------------------------------ 79->
CHUNKSIZE = 4
COLOURS = Colours()

# Classes
# ------------------------------------------------------------------------ 79->

# Functions
# ------------------------------------------------------------------------ 79->
def shuffle(file_buffer, kwargs):
    if kwargs['file_method'] == 'line':
        print('shuffle: LINE >>>')
        for line in file_buffer:
            kwargs['data'] = line
            distribute(kwargs['pipeline'].pop(0), kwargs=kwargs)
    elif kwargs['file_method'] == 'file':
        print('shuffle: FILE >>>')
        kwargs['data'] = file_buffer
        distribute(kwargs['pipeline'].pop(0), kwargs=kwargs)
    else:
        print('shuffle: ERROR >>>')
        return file_buffer

def task_open_file(*args, **kwargs):
    printc('Starting Task: Open File', COLOURS.LIGHTBLUE)
    p_serial = kwargs['p_serial']
    file_name = kwargs['file']
    file_path = kwargs['path']
    kwargs['data'] = 'fsffsefsf, fesfe , f sefsefsee'
    kwargs['delimiter'] = ','
    return distribute(
        func=kwargs['pipeline'].pop(0), 
        name='open_file', 
        kwargs=kwargs, 
        serial=p_serial
        )
    '''
    try:
        with open('{0}/{1}'.format(file_path, file_name), 'rb') as f:
            r = f.read()
            z = zlib.decompress(r).decode()
            if len(kwargs['pipeline']) > 0:
                return shuffle(z, kwargs)
            else:
                return z
    except Exception as e:
        print('---')
        printc(str(e), COLOURS.RED)
        return str(e)
    '''

# Main
# ------------------------------------------------------------------------ 79->
