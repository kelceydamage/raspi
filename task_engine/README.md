# Task Engine
Task Engine is a light-weight secure task-queuing system for Raspberry Pi robots.

### Testing Task Engine
To test Task Engine simply run the `start_engine.py` utility.

when running the `start_engine.py` script you should see an output similar to below if using the default configuration.
```bash
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
Task Engine starts workers on port 10000 and above sequentially, starting with TASK workers and then DATA workers. This will be configurable but is recommended as specification. 

**Once the ROUT worker is completed, it will handle brokering.

## Mesage Specification v0.1
Below are the initial specifications for structuring messages. These are subject to revision.

### REPL Message format [JSON]
```bash
{
	"meta": {
		"source": <hostname>,
		"cname": <system-identifier>,
		"version": <source-version>
	}
}
```

### TASK Message format [JSON]
```bash
{
	"name": <string>,
	"args": <list>,
	"kwargs": <dict>,
	"meta": {
		"source": <hostname>,
		"cname": <system-identifier>,
		"version": <source-version>
	}
}
```

### DATA Message format [JSON]
```bash
{
	"data": <dict>,
	"service": <sensor-provider-name>,
	"meta": {
		"source": <hostname>,	
		"cname": <system-identifier>,
		"version": <source-version>
	}
}
```

### More to follow....