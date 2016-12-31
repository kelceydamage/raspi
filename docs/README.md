# Raspi 
Raspi is a library of light-weight services for programming Raspberry Pi's.

The goal of the `Raspi` platform is to create an extensable, scalable, hardware automation platform capable of realtime evaluation of it's state. The platform should be runnable on a single Raspberry Pi with exceptable performance, and scalable to a multiple Pi scenario sharing co-state and 'work-together' task orientation.

### Some early design considerations
* The initial hardware platform is Pi3 + MegaPi industrial IO.
* ARMv7 Processor rev 4 (v7l)
* Each component of `Raspi` should be self contained and plug-in replaceable/extensible. For lack or a better term, isolated/containerized.
* intercommunication message serialization to start off as JSON, but will move to msgpack if necessary.
* Optimization should be on memory footprint
* Performance goal is 1.5x operational speed requirements, 1 second allowance for task response-time
* Python based for easy IO interaction with hardware components

## Contents
###Currently contains:

```bash
task_engine:        Based on ZMQ, the primary orchestrator for handling both REQ => REP for
                    task automation, and PUB => SUB for sensor data retrieval.
```

###In progress:

```bash
data_collector:     Micro daemon collective for streaming sensor data to task_engine 
                    subscribers.

data_store:         Light-weight storage system for state samples and subscriber for 
                    task_engine publishers.

hive_link:          Interlink service to share state and operations between task_engines.

task_operator:      Requestor for task execution, and interface for AI or remote-ops to
                    request task execution. Most likely based on Flask.

ai:                 High-level controller of sub_routines, such as pathfinding, and servo 
                    feedback control. Primary client for task_operator.

tasks:              Library of registered tasks, or system capabilities.

touch_ui:           Interface for 7-inch touch-screen. Most likely based on TK.

monitoring:         Data-visualization page for observing application.
```

## Relationships
```bash                              
                                               sub_routines 
                                                    | ________ analysis
                                                    |/   
                                                    | ________ motor_drive
                                                    |/
                                               tasks (code_modules)
                                                    |
                                                    | ________ data_store
                                                    |/
                ai _____> task_operator _____> task_engine [a] <_____ data_collector [Sensors]
                               /|                  ||   
                              / |                  ||
                             /  |              hive_link
                            /   |                  ||
                           /    |                  ||
                          /     |              task_engine [b, ...]
touch_screen ______> touch_ui   |
                                |
                                |
                                |                 
                                |
                                | 
            browser ______> monitoring
```

## Non-Core Libraries 
```bash
pyzmq
```

## Interaction Specification v0.1

| Service | Port | Notes |
|---------|------|-------|
|task_engine: workers|10000 - #####| task_engine will assign a sequencial port to all worker types requested in the configuration file. |

### More to follow....
