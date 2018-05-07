## Case: multiple GPUs

GPU can accelerate deep-learning. 
The mgq supports multiple queues. Each queue can be associated to GPU.

In this case, the task queue helps you.

### Procedure

1. Set prefix for running with GPUs.

1. Run task0 with the GPU0.

1. Run task1 with the GPU1.

### mgq command

Queue name: tf0

Queue name: tf1

task0: task0.py 

task1: task1.py 


Initialize the queue of tf0:
```
% mgq tf0 clear
% mgq tf0 prefix "CUDA_VISIBLE_DEVICES=0 "
% mgq tf1 clear
% mgq tf1 prefix "CUDA_VISIBLE_DEVICES=1 "
```

Add tasks to the queue of tf0:
```
% mgq tf0 ad "python task0.py paramA"
% mgq tf0 ad "python task0.py paramB"
% mgq tf1 ad "python task1.py paramA"
% mgq tf1 ad "python task1.py paramB"
```

Other option to the queue of tf0:
```
% cat mgqadd.sh
#!/usr/bin/env sh
mgq tf0 ad "python task0.py paramA"
mgq tf0 ad "python task0.py paramB"
mgq tf1 ad "python task1.py paramA"
mgq tf1 ad "python task1.py paramB"
% ./mgqadd.sh
```

Start the tasks in the queues of tf0 and tf1:
```
% mgq tf0 start
% mgq tf1 start
```

Then, task0.py with paramA and task1.py with paramA are started in parallel.
task0.py with paramB will be automatically started after task0.py with paramA will finish.
task1.py with paramB will be automatically started after task1.py with paramA will finish.

Once you initialized the queue, you just add and start the tasks.


