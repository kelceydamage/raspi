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

"""

# Imports
#-------------------------------------------------------------------------------- <-80
import os
os.sys.path.append(
    os.path.dirname(
        os.path.dirname(

            os.path.abspath(__file__)
            )
        )
    )
from common.datatypes import TaskFrame
from common.datatypes import MetaFrame
from common.datatypes import DataFrame
from common.datatypes import prepare
import time

# Globals
#-------------------------------------------------------------------------------- <-80

# Classes
#-------------------------------------------------------------------------------- <-80

# Functions
#-------------------------------------------------------------------------------- <-80

# Main
#-------------------------------------------------------------------------------- <-80
if __name__ == '__main__':
    start = time.time()
    # Pack is simply a time epoch which can be used to identify all frames in an envelope
    pack = time.time()
    T = TaskFrame(pack)
    M = MetaFrame(pack)
    M.digest()
    #meta = prepare(M, kwargs)
    M.message['pack'] = M.hash
    M.message['id'] = 'CLIENT'
    M.message['version'] = 0.1
    M.message['type'] = 'REQ'
    M.message['role'] = 'requestor'
    print M.serialize()
    print time.time() - start

    print 100 / 10