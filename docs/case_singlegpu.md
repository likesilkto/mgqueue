## Case: single GPU

GPU can accelerate deep-learning. 
You have two tasks, task1 and task2, which take several hours.
You want to run two tasks sequentially because sequential running is more computationally efficient than parallel running especially computational resource is limited.
The other advantage of sequential running is that you can develop task2 while task1 is running.

In this case, the task queue helps you.

### Procedure

1. Set prefix for running with GPU.

1. Run task1 as background with the mgq.

1. Develope task2.

1. Add task2 to the the queue.

1. When the task1 is finished, the task2 will automatically start.

### mgq command

Queue name: thGPU0

task1: task1.py (theano application)

task2: task2.py (theano application)

```
% mgq thGPU0 clear
% mgq thGPU0 prefix "THEANO_FLAGS=mode=FAST_RUN,device=gpu0,floatX=float32,"
% mgq thGPU0 ad "python task1.py"
% mgq thGPU0 start
% mgq thGPU0 ad "python task2.py"
```

