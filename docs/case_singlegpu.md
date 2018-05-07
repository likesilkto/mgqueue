## Case: single GPU with tensorflow

GPU can accelerate deep-learning. 
You have two tasks, task1 and task2, which take several hours.
You want to run two tasks sequentially because sequential running is more computationally efficient than parallel running especially computational resource is limited.
The other advantage of sequential running is that you can develop task2 while task1 is running.

In this case, the task queue helps you.

### Procedure

1. Set prefix for running with the specific GPU.

1. Add task1 and task2 to the queue.

1. Start the queue. 

### mgq command

Queue name: tf0

GPU: GPU0

task1: task1.py

task2: task2.py


Initialize the queue of tf0:
```
% mgq tf0 clear
% mgq tf0 prefix "CUDA_VISIBLE_DEVICES=0 "
```

Add tasks to the queue of tf0:
```
% mgq tf0 ad "python task1.py"
% mgq tf0 ad "python task2.py"
```

Other option to the queue of tf0:
```
% cat mgqadd.sh
#!/usr/bin/env sh
mgq tf0 ad "python task1.py"
mgq tf0 ad "python task2.py"
% ./mgqadd.sh
```

Start the tasks in the queue of tf0:
```
% mgq tf0 start
```
Then, task1.py is started and task2.py will be automatically started after task2.py will finish.

Once you initialized the queue, you just add and start the tasks.
