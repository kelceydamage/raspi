# Task Engine
Task Engine is a light-weight secure task-queuing system for Raspberry Pi robots.

### Testing Task Engine
To test Task Engine simply run the `start_engine.py` utility.

Run the sim_client to have Task Engine complete 10,000 sums.

## Mesage Specification v0.1
Below are the initial specifications for structuring messages. These are subject to revision.

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