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
SUMMARY: Classes to represent various cusstom math functions
"""

# Imports
#-------------------------------------------------------------------------------- <-80

# Globals
#-------------------------------------------------------------------------------- <-80

# Classes
#-------------------------------------------------------------------------------- <-80
class CustomMath(object):
    """
NAME:
DESCRIPTION:
    """
    def __init__(self):
        super(CustomMath, self).__init__()

    def exponential_moving_average(self, data, window):
        pass

    def simple_moving_average(self, data, window):
        x = sum(data[-window:])
        return float(x) / window
