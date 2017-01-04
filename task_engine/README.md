# Task Engine
Task Engine is a light-weight secure task-queuing system for Raspberry Pi robots.

*Maximum IO = 4000 @ 30ms response-time & 50 chunk-size, on the Pi3 b+*

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

## Features
Task Engine includes the following features

|Feature|Default|Explanation|
|-------|-------|-----------|
|HOST|127.0.0.1|The interface ip that ZMQ runs on.|
|TASK_WORKERS|2|The numbers of REQ-REP task workers to spawn.|
|DATA_WORKERS|1|The number of PUB-SUB data workers to spawn.|
|RESPONSE_TIME|0.005 (5ms)|A measure of how often the task queue is flushed to the task engine. This is configurable in the task engine configuration. Increasing the response time will increase IO throughput at the cost of task sluggishness. useful for complex action chains.|
|CHUNKING|True|A routing and load-balancing option for determining the maximum tasks to be sent to a worker before switching workers.|
|CHUNKING_SIZE|10|Increasing chunk size can increase throughput at the cost of balancing. It is possible to choke a worker is response time is too high and chunk size too large. When operating servos or other complex tasks a lesser throughput with quicker response is desired.|
|ENABLE_STDOUT|True|Writes interactions to the terminal.|

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
This shows the `REQUESTOR` making 63 requests to the `ROUTER`. The `CHUNKER` picks up the oversized package and splits it up into 8 chunks, evenly balancing the chunks over the `WORKERS`. As each chunk is processed and returned to the `DEALER`, the `ASSEMBLER` begins reassembly of the original package. Once assembly is complete, the package is returned to the `REQUESTOR` with a response entry for each of the 63 requested tasks. These are identified by their task serial(pack) in case the `REQUESTOR` requires the response. If no response is required, the data package is discarded. This occurs completely asynchronously thanks to `ZMQ`.

#### client
*_Edited for readability._*
```bash
[CLIENT] recv: [
	'{"length": 1, "version": 0.1, "role": "assembler", "part": 8, "serial": "a0e366bb6cac9043957f11506778ab44", 
		"size": 8, "type": "ACK", "id": "TASK-20430", "pack": 1483507553.307392}', 
	'{"size": 1, "data": [
		"job-70684b074b6565633d54d3750c973a01: 2.5"], 
		"pack": 1483507553.307392}', 
	'{"size": 10, "data": [
		"job-d69bf43328e7fd2a75667a8d25ae599a: 2.5", "job-f2d9e5557e518aa2e229711b5712ef74: 2.5", 
		"job-5dd65644a84501281cb84dcceec42bb7: 2.5", "job-1297313e85b37f470de1e72deee6450a: 2.5", 
		"job-1a9f9a8875d7a988241cea5a87232b88: 2.5", "job-f9b8ca8db86f3508701fb58e3ef11b9a: 2.5", 
		"job-184e5d9f4c39441634b625a96eb72b42: 2.5", "job-0e72ef8c31b3c90cde6749aa9c336320: 2.5", 
		"job-b73b656c054afd1ee7f88b6275111c72: 2.5", "job-035675946381be36c1b097e1fd6c7da4: 2.5"], 
		"pack": 1483507553.307392}', 
	'{"size": 10, "data": [
		"job-f18ea23e16d9531c3173eb82c7fa9ccb: 2.5", "job-fceaa808c2320159344df9dc56cda385: 2.5", 
		"job-92cef1e06bc5f454ab061b5cc95cc37b: 2.5", "job-8568b5a24b080a6b7d66d2b32b49c571: 2.5", 
		"job-90d58b7b881bc3ac059a8b1e1ffdcf91: 2.5", "job-39e11942745e412c2106cab0f4daab61: 2.5", 
		"job-383445436f41da1973ad8959475511ed: 2.5", "job-c5a7d2156d6067615c2e061f03b5e515: 2.5", 
		"job-514da57a43927763df92aeaf8720682e: 2.5", "job-3b81a66f679236650e073a5f55ab529a: 2.5"], 
		"pack": 1483507553.307392}', 
	'{"size": 10, "data": [
		"job-f7c18e681349fbcdc0af3ea583e00a22: 2.5", "job-a611bb0fda4ff032dbb40f01c478a166: 2.5", 
		"job-9879eca354f8f0bc75f531c77838d233: 2.5", "job-b8de71da2f3be536b949c6dc74482a82: 2.5", 
		"job-916d85e4722a82f6dd1dbf25d85e09ed: 2.5", "job-531c19bc21e766c8eee7414102bd259c: 2.5", 
		"job-842ec05c06da735b5896f453f28e8bb8: 2.5", "job-5519daf94549a9c91c2586eb01d66287: 2.5", 
		"job-4e14719f513b4ef0dc1b55b8f1bbb1db: 2.5", "job-851f6c6781b650cee046332f6445b823: 2.5"], 
		"pack": 1483507553.307392}', 
	'{"size": 10, "data": [
		"job-290c6986e32b810b07b48089f68eb8ad: 2.5", "job-ed61deb1b967f89a7beea9467d745a1b: 2.5", 
		"job-9bec9fda0d6adafcb2eeded15fbc117c: 2.5", "job-5d2ad7e66399a3087b6a6e834f493d35: 2.5", 
		"job-7e41dc99685a894eb27f0ea68bc8dbd3: 2.5", "job-47e6e699a509e08c927dc73951053f5a: 2.5", 
		"job-90742a495c751707a0e9bb3c2a7926f3: 2.5", "job-64a67af2f81e30f50af582416116344a: 2.5", 
		"job-0e76febca42ec23a74545330941f09c7: 2.5", "job-2826db55faeca757aff28bdbaeee97f6: 2.5"], 
		"pack": 1483507553.307392}', 
	'{"size": 10, "data": [
		"job-920f35031bcf92680776aad662eab7d8: 2.5", "job-8541a265f3d1ca673352b6ec69f0d6b5: 2.5", 
		"job-31ceff23d26562d9b52a65958aeb2352: 2.5", "job-d4de91040fd7d5941af6a11fbc8d5511: 2.5", 
		"job-e0815c59da85be261ec9bfab01a70c79: 2.5", "job-3e8d8963b0a36011e3642ee0fda45db6: 2.5", 
		"job-447df1c0ccf7b4254dd1fccbc1cb7359: 2.5", "job-c085928279cecc135a6e95a40253b6a0: 2.5", 
		"job-1e9354adee8f7c0dc2525c5600785601: 2.5", "job-39107adf24cee2e5416dd511784fbe3b: 2.5"], 
		"pack": 1483507553.307392}', 
	'{"size": 10, "data": [
		"job-9d2db18add414a6f36aa1e5f5fb46cc4: 2.5", "job-064c4a253cdf281cedcb18c611f736f0: 2.5", 
		"job-1fc0686d057aee635a3da36d17799d0a: 2.5", "job-74686001ff6c314bb550268558d845b0: 2.5", 
		"job-52465c56aada725002076ff4d00a6a33: 2.5", "job-ec8fef53b5528cff6dde550037eef4a7: 2.5", 
		"job-5f484344006dce9bd9a872f816bbecef: 2.5", "job-6420a522930bfad71c8232ab38b09307: 2.5", 
		"job-5ceb93f1a48e2bcd41ec6a7e3d40185c: 2.5", "job-b4fc4161f201bb796461fb7bf5d02ce7: 2.5"], 
		"pack": 1483507553.307392}', 
	'{"size": 2, "data": [
		"job-7b5660a80a8cf59314d94196ea47fc58: 2.5", "job-0579c387c613c0db95e0b3c8c27f9f01: 2.5"], 
		"pack": 1483507553.307392}
']
running 70 samples, took: 0.0247650146484
```

#### task_engine
*_Edited for readability._*
```bash
[ROUTER-20429(FRONTEND)] Chunking: 63/10: {"length": 63, "version": 0.1, "role": "requestor", "part": 0, 
	"serial": "a0e366bb6cac9043957f11506778ab44", "type": "REQ", "id": "CLIENT", "pack": 1483507553.307392}
[WORKER-20431(TASK)] Received task: Package a0e366bb6cac9043957f11506778ab44, Chunk 1
[WORKER-20431(TASK)] Received task: Package a0e366bb6cac9043957f11506778ab44, Chunk 3
[ROUTER-20429(BACKEND)] Forwarding: {"length": 1, "version": 0.1, "role": "responder", "part": 1, 
	"serial": "a0e366bb6cac9043957f11506778ab44", "type": "ACK", "id": "TASK-20431", "pack": 1483507553.307392}
[ROUTER-20429(BACKEND)] Forwarding: Assembling: a0e366bb6cac9043957f11506778ab44, Part: 7.0
[WORKER-20430(TASK)] Received task: Package a0e366bb6cac9043957f11506778ab44, Chunk 2
[WORKER-20431(TASK)] Received task: Package a0e366bb6cac9043957f11506778ab44, Chunk 5
[WORKER-20430(TASK)] Received task: Package a0e366bb6cac9043957f11506778ab44, Chunk 4
[ROUTER-20429(BACKEND)] Forwarding: {"length": 1, "version": 0.1, "role": "responder", "part": 2, 
	"serial": "a0e366bb6cac9043957f11506778ab44", "type": "ACK", "id": "TASK-20430", "pack": 1483507553.307392}
[ROUTER-20429(BACKEND)] Forwarding: Assembling: a0e366bb6cac9043957f11506778ab44, Part: 6.0
[ROUTER-20429(BACKEND)] Forwarding: {"length": 1, "version": 0.1, "role": "responder", "part": 3, 
	"serial": "a0e366bb6cac9043957f11506778ab44", "type": "ACK", "id": "TASK-20431", "pack": 1483507553.307392}
[ROUTER-20429(BACKEND)] Forwarding: Assembling: a0e366bb6cac9043957f11506778ab44, Part: 5.0
[WORKER-20431(TASK)] Received task: Package a0e366bb6cac9043957f11506778ab44, Chunk 7
[WORKER-20430(TASK)] Received task: Package a0e366bb6cac9043957f11506778ab44, Chunk 6
[ROUTER-20429(BACKEND)] Forwarding: {"length": 1, "version": 0.1, "role": "responder", "part": 5, 
	"serial": "a0e366bb6cac9043957f11506778ab44", "type": "ACK", "id": "TASK-20431", "pack": 1483507553.307392}
[ROUTER-20429(BACKEND)] Forwarding: Assembling: a0e366bb6cac9043957f11506778ab44, Part: 4.0
[ROUTER-20429(BACKEND)] Forwarding: {"length": 1, "version": 0.1, "role": "responder", "part": 4, 
	"serial": "a0e366bb6cac9043957f11506778ab44", "type": "ACK", "id": "TASK-20430", "pack": 1483507553.307392}
[ROUTER-20429(BACKEND)] Forwarding: Assembling: a0e366bb6cac9043957f11506778ab44, Part: 3.0
[ROUTER-20429(BACKEND)] Forwarding: {"length": 1, "version": 0.1, "role": "responder", "part": 7, 
	"serial": "a0e366bb6cac9043957f11506778ab44", "type": "ACK", "id": "TASK-20431", "pack": 1483507553.307392}
[ROUTER-20429(BACKEND)] Forwarding: Assembling: a0e366bb6cac9043957f11506778ab44, Part: 2.0
[ROUTER-20429(BACKEND)] Forwarding: {"length": 1, "version": 0.1, "role": "responder", "part": 6, 
	"serial": "a0e366bb6cac9043957f11506778ab44", "type": "ACK", "id": "TASK-20430", "pack": 1483507553.307392}
[ROUTER-20429(BACKEND)] Forwarding: Assembling: a0e366bb6cac9043957f11506778ab44, Part: 1.0
[WORKER-20430(TASK)] Received task: Package a0e366bb6cac9043957f11506778ab44, Chunk 8
[ROUTER-20429(BACKEND)] Forwarding: {"length": 1, "version": 0.1, "role": "responder", "part": 8, 
	"serial": "a0e366bb6cac9043957f11506778ab44", "type": "ACK", "id": "TASK-20430", "pack": 1483507553.307392}
[ROUTER-20429(BACKEND)] Forwarding: Assembling: a0e366bb6cac9043957f11506778ab44, Part: 0.0
[ROUTER-20429(BACKEND)] Forwarding: Shipped: a0e366bb6cac9043957f11506778ab44
```

### META Message format [JSON]
```bash
self.message = {
	'id': <string>,
	'role': <string>
	'version': <string>,
	'type': <string>,
	'pack': <float>,
	'length': <int>,
	'serial': <md5-hash>,
	'part': <int>,
	'size': <int>
}
```

### TASK Message format [JSON]
```bash
self.message = {
	'task': <string>,
	'args': <list>,
	'kwargs': <dict>,
	'pack': <md5-hash>
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