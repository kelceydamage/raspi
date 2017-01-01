# Tasks

Simply drop your task module into this folder and start the Task Engine. In order for your task to be registered in the task registry, prepend the entry function with TASK_. This flag will signal the registry to store the task and make it available to workers. This way you can write complex modules with classes and easily expose your API with the TASK_ flag.

All functions with the TASK_ flag should expect *args, **kwargs.

### More to follow....