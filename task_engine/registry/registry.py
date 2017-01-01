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
SUMMARY:		Registry of trusted functions for execution
"""

# Imports
#-------------------------------------------------------------------------------- <-80
import os
os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tasks.tasks import count

# Globals
#-------------------------------------------------------------------------------- <-80
functions = {
	'count': count
}

# Classes
#-------------------------------------------------------------------------------- <-80

# Functions
#-------------------------------------------------------------------------------- <-80

# Main
#-------------------------------------------------------------------------------- <-80