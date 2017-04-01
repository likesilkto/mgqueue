## Case: multiple GPUs

GPU can accelerate deep-learning. 
The mgq supports multiple queues. Each queue can be associated to GPU.

In this case, the task queue helps you.

### Procedure

1. Set prefix for running with GPUs.

1. Run task0 as background with the GPU0.

1. Run task1 as background with the GPU1.

### mgq command

Queue name: thGPU0

Queue name: thGPU1

task0: task0.py (theano application)

task1: task1.py (theano application)

```
% mgq thGPU0 clear
% mgq thGPU0 prefix "THEANO_FLAGS=mode=FAST_RUN,device=gpu0,floatX=float32,"
% mgq thGPU0 ad "python task0.py"
% mgq thGPU0 start
```

```
% mgq thGPU1 clear
% mgq thGPU1 prefix "THEANO_FLAGS=mode=FAST_RUN,device=gpu1,floatX=float32,"
% mgq thGPU1 ad "python task1.py"
% mgq thGPU1 start
```
