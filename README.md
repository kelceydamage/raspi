# Raspi 
Raspi is a library of light-weight services for programming Raspberry Pi's.

The goal of the `Raspi` platform is to create an extensable, scalable, hardware automation platform capable of realtime evaluation of it's state. The platform should be runnable on a single Raspberry Pi with exceptable performance, and scalable to a multiple Pi scenario sharing co-state and 'work-together' task orientation.

The initial hardware platform is Pi3 + MegaPi industrial IO.

Each component of `Raspi` should be self contained and plug-in replaceable/extensible. For lack or a better term, isolated/containerized.

### Contents
Currently contains:
```bash
task_engine:        Based on ZMQ, the primary orchestrator for handly both REQ => REP for
                    task automation, and PUB => SUB for sensor data retrieval.
```

In progress:
```bash
data_collector:     Micro daemon collective for streaming sensor data to task_engine 
                    subscribers.

data_store:         Light-weight storage system for state samples and subscriber for 
                    task_engine publishers.

hive_link:          Interlink service to share state and operations between task_engines.

task_operator:      Requestor for task execution, and interface for AI or remote-ops to
                    request task execution.

ai:                 High-level controller of sub_routines, such as pathfinding, and servo 
                    feedback control. Primary client for task_operator.

tasks:              Library of registered tasks, or system capabilities.
```

### Relationships
```bash                              
                               sub_routines 
                                    | ________ analysis
                                    |/   
                                    | ________ motor_drive
                                    |/
                                  tasks
                                    |
                                    | ________ data_store
                                    |/
ai _____> task_operator _____> task_engine [a] <_____ data_collector [Sensors]
                                   ||   
                                   ||
                                hive_link
                                   ||
                                   ||
                               task_engine [b, ...]
```
### More to follow....