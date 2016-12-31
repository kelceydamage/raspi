# Raspi 
Raspi is a library of light-weight services for programming Raspberry Pi's.

### Contents
Currently contains:
```bash
task_engine
```

In progress:
```bash
data_collector
data_store
hive_link
task_operator
ai
tasks
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