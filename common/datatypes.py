#!/usr/bin/env python
# ------------------------------------------------------------------------ 79->
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
# ------------------------------------------------------------------------ 79->
"""
SUMMARY: 
"""

# Imports
# ------------------------------------------------------------------------ 79->
import hashlib
import base64
import ujson
import collections
import uuid


# Globals
# ------------------------------------------------------------------------ 79->

# Classes
# ------------------------------------------------------------------------ 79->
class Tools(object):

    @staticmethod
    def serialize(obj):
        return base64.b64encode((ujson.dumps(obj)).encode())

    @staticmethod
    def deserialize(obj):
        return ujson.loads(base64.b64decode(obj).decode())

    @staticmethod
    def create_header(self, meta):
        return hashlib.md5(ujson.dumps(meta).encode()).hexdigest().encode()

class Envelope(object):

    def __init__(self):
        self.contents = collections.deque(maxlen=4)
        self.lifespan = 0

    def pack(self, header, meta, udf):
        meta['lifespan'] = len(udf['pipeline'])
        self.lifespan = meta['lifespan']
        [self.contents.append(Tools.serialize(x)) for x in (header, '', meta, udf)]
        
    def load(self, contents):
        [self.contents.append(x) for x in contents if Tools.deserialize(x) != '']
        self.contents.insert(1, contents[1])
        self.lifespan = self.get_meta().lifespan
        del contents

    def open(self):
        return [Tools.deserialize(x) for x in self.contents]

    def seal(self):
        return list(self.contents)

    def create_header(self, meta):
        return str(uuid.uuid4()).encode()

    def get_header(self):
        return self.contents[0]

    def get_raw_header(self):
        return Tools.deserialize(self.contents[0])

    def get_meta(self):
        return Meta(Tools.deserialize(self.contents[2]))

    def get_udf(self):
        return Udf(Tools.deserialize(self.contents[3]))

    def update_udf(self, udf):
        self.contents.pop()
        self.contents.append(Tools.serialize(udf.extract()))

    def update_contents(self, meta, udf):
        self.contents.pop()
        self.contents.pop()
        self.contents.append(Tools.serialize(meta.extract()))
        self.contents.append(Tools.serialize(udf.extract()))

    def empty(self):
        self.contents.clear()

    def validate(self):
        if len(self.contents) != 4:
            raise Exception('[ENVELOPE] (validation): size missmatch')
        if self.contents[1] != Tools.serialize(''): #b'IiI=':
            raise Exception('[ENVELOPE] (validation): order missmatch')

class Udf(object):
    '''
    Attributes:     pipeline
                    data
                    completed
                    kwargs
    '''

    def __init__(self, udf=None):
        self.pipeline = collections.deque()
        self.data = collections.deque()
        self.completed = collections.deque()
        if udf != None:
            print('udf-load')
            self.load(udf)

    def extract(self):
        return {
            'pipeline': self.pipeline,
            'data': self.data,
            'completed': self.completed,
            'kwargs': self.kwargs
        }

    def extract_less(self):
        return {
            'pipeline': self.pipeline,
            'data': [],
            'completed': self.completed,
            'kwargs': self.kwargs
        }

    def load(self, udf):
        for k, v in udf.items():
            setattr(self, k, v)

    def consume(self):
        current = self.pipeline.pop(0)
        self.completed.append(current)
        return current

    def set_data(self, data):
        if isinstance(data, list):
            for item in data:
                self.data.append(item)
        elif isinstance(data, tuple):
            self.data.append(data)

class Meta(object):
    '''
    Attributes:     size
                    length
                    lifespan
    '''
    
    def __init__(self, meta=None):
        if meta != None:
            self.load(meta)

    def extract(self):
        return {
            'size': self.size,
            'length': self.length,
            'lifespan': self.lifespan,
            'times': {}
        }

    def load(self, meta):
        for k, v in meta.items():
            setattr(self, k, v)

# Functions
# ------------------------------------------------------------------------ 79->

# Main
# ------------------------------------------------------------------------ 79->
