# Task Engine
Task Engine is a light-weight secure task-queuing system for Raspberry Pi robots.

### Testing Task Engine
To test Task Engine simply run the `start_engine.py` utility.

when running the `start_engine.py` script you should see an output similar to below if using the default configuration.
```bash
[REGISTERED-TASKS]:
[-] task_count
------------------
### Type [ctrl-c] to exit and shutdown workers ###
Starting process [20709]: <function start_worker at 0x76725e30>
Starting [ROUTER] on socket: 127.0.0.1:9000
Starting process [20711]: <function start_worker at 0x76725e30>
Starting process [20710]: <function start_worker at 0x76725e30>
Starting worker[TASK] on socket: 127.0.0.1:10001
[ROUTER-9000(FRONTEND)] Listener online
[ROUTER-9001(BACKEND)] Listener online
Starting process [20712]: <function start_worker at 0x76725e30>
[ROUTER-MASTER] Routing started
loop
Starting worker[TASK] on socket: 127.0.0.1:10000
Starting worker[DATA] on socket: 127.0.0.1:10002
[WORKER-20711(TASK)] Listener online
[WORKER-20712(DATA)] Listener online
[WORKER-20710(TASK)] Listener online
```

Hitting `ctrl-c` or sending SIGTERM should generate an output similar to below.
```bash
Closing application and stopping services...
Sucessfully terminated process [7758]: <function start_worker at 0x76685a70>
Sucessfully terminated process [7759]: <function start_worker at 0x76685a70>
Sucessfully terminated process [7760]: <function start_worker at 0x76685a70>
```

## Interaction v0.1
Task Engine starts a ROUTER and [n] number of DATA and TASK workers. Requestors send requests to the ROUTER as the frontend of the task engine.

## Mesage Specification v0.1
Below are the initial specifications for structuring messages. These are subject to revision. More information exists in ../common/datatypes.py

All messages contain at least a META frame. Expected combinations are as follows:

|Message Parts|Explanation|
|-------------|-----------|
|[META]|Used for ack type messages|
|[META, TASK]|Used for action requests|
|[META, DATA]|Used for data interaction requests|

### Sample communication
#### client
```bash
[CLIENT] Sending: ['{"type": "REQ", "version": 0.1, "role": "requestor", "id": "CLIENT", "pack": 1483311405.215693}', '{"task": "TASK_count", "pack": 1483311405.215693, "args": [2, 3], "kwargs": {}}']
[CLIENT] Received: ['{"type": "ACK", "version": 0.1, "role": "responder", "id": "TASK-31928", "pack": 1483311405.217414}']
running 10000 samples, took: 0.00262403488159
```

#### task_engine
```bash
[ROUTER-9000(FRONTEND)] Forwarding: ['\x00k\x8bEw', '', '{"type": "REQ", "version": 0.1, "role": "requestor", "id": "CLIENT", "pack": 1483311405.215693}', '{"task": "TASK_count", "pack": 1483311405.215693, "args": [2, 3], "kwargs": {}}']
loop
[WORKER-31928(TASK)] Received task: ['{"type": "REQ", "version": 0.1, "role": "requestor", "id": "CLIENT", "pack": 1483311405.215693}', '{"task": "TASK_count", "pack": 1483311405.215693, "args": [2, 3], "kwargs": {}}']
[WORKER-31928(TASK)] Task complete: {"type": "ACK", "version": 0.1, "role": "responder", "id": "TASK-31928", "pack": 1483311405.217414}
[ROUTER-9001(BACKEND)] Forwarding: ['\x00k\x8bEw', '', '{"type": "ACK", "version": 0.1, "role": "responder", "id": "TASK-31928", "pack": 1483311405.217414}']
loop
```

### META Message format [JSON]
```bash
self.message = {
	'id': <string>,
	'role': <string>
	'version': <string>,
	'type': <string>,
	'pack': <float>
}
```

### TASK Message format [JSON]
```bash
self.message = {
	'task': <string>,
	'args': <list>,
	'kwargs': <dict>,
	'pack': <float>
}	
```

### DATA Message format [JSON]
```bash
self.message = {
	'data': <any-format>,
	'pack': <float>
}	
```

### Message formatting
here is a template for formatting messages. Below we are creating a TASK request. It is important to note that metadata should precede other frames.
```python
from common.datatypes import TaskFrame
from common.datatypes import MetaFrame
from common.datatypes import DataFrame
from common.datatypes import prepare
import time

pack = time.time()
kwargs = {
'id': 'CLIENT',
'role': 'requestor',
'version': 0.1,
'type': 'REQ',
'pack': pack
}
meta = prepare(MetaFrame(pack), kwargs)
kwargs = {
'task': 'task_count',
'args': [2, 3],
'kwargs': {},
'pack': pack
}
task = prepare(TaskFrame(pack), kwargs)

message = [meta, task]
```

### More to follow....