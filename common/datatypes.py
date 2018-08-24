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
import sys


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
    def create_header(meta):
        return hashlib.md5(ujson.dumps(meta).encode()).hexdigest().encode()

    @staticmethod
    def create_id():
        return str(uuid.uuid4()).encode()

class Envelope(object):
    # [header, meta, udf, data]

    def __init__(self):
        self.contents = collections.deque(maxlen=4)
        self.lifespan = 0

    def pack(self, header, meta, udf, data):
        meta['lifespan'] = len(udf['pipeline'])
        meta['length'] = len(data)
        meta['size'] = sys.getsizeof(data)
        self.lifespan = meta['lifespan']
        self.length = meta['length']
        self.size = meta['size']
        [self.contents.append(Tools.serialize(x)) for x in (header, meta, udf, data)]
        del header
        del meta
        del udf
        del data
        
    def load(self, contents):
        [self.contents.append(x) for x in contents]
        meta = self.get_meta()
        self.lifespan = meta.lifespan
        self.length = meta.length
        self.size = meta.size
        del contents
        del meta

    def open(self):
        return [Tools.deserialize(x) for x in self.contents]

    def unpack(self):
        return self.get_raw_header(), self.get_meta(), self.get_udf(), self.get_data()

    def seal(self):
        return list(self.contents)

    def create_id(self):
        return str(uuid.uuid4()).encode()

    def get_header(self):
        return self.contents[0]

    def get_raw_header(self):
        return Tools.deserialize(self.contents[0])

    def get_meta(self):
        return Meta(Tools.deserialize(self.contents[1]))

    def get_udf(self):
        return Udf(Tools.deserialize(self.contents[2]))

    def get_data(self):
        return Tools.deserialize(self.contents[3])

    def update_data(self, data):
        self.contents.pop()
        self.contents.append(Tools.serialize(data))

    def update_meta(self, meta):
        self.contents.pop(1)
        self.contents.insert(Tools.serialize(meta.extract()), 1)

    def empty(self):
        self.contents.clear()

    def validate(self):
        if len(self.contents) != 4:
            raise Exception('[ENVELOPE] (validation): size missmatch')

class Udf(object):
    '''
    Attributes:     pipeline
                    data
                    completed
                    kwargs
    '''

    def __init__(self, udf=None):
        self.kwargs = {}
        self.pipeline = collections.deque()
        self.completed = collections.deque()
        if udf != None:
            self.load(udf)

    def extract(self):
        return {
            'pipeline': self.pipeline,
            'completed': self.completed,
            'kwargs': self.kwargs
        }

    def empty(self):
        self.data.clear()

    def load(self, udf):
        for k, v in udf.items():
            setattr(self, k, v)

    def consume(self):
        current = self.pipeline.pop(0)
        self.completed.append(current)
        return current

class Meta(object):
    '''
    Attributes:     size
                    length
                    lifespan
    '''
    
    def __init__(self, meta=None):
        self.size = 0
        self.length = 0
        self.lifespan = 0
        self.times = {}
        self.stage = Tools.create_id()
        if meta != None:
            self.load(meta)

    def extract(self):
        return {
            'size': self.size,
            'length': self.length,
            'lifespan': self.lifespan,
            'times': self.times,
            'stage': self.stage
        }

    def load(self, meta):
        for k, v in meta.items():
            setattr(self, k, v)

# Functions
# ------------------------------------------------------------------------ 79->

# Main
# ------------------------------------------------------------------------ 79->
