## Case: CPU

You have two tasks, task1 and task2, which take several hours.
You want to run two tasks sequentially because sequential running is more computationally efficient than parallel running especially computational resource is limited.
The other advantage of sequential running is that you can develop task2 while task1 is running.

In this case, the task queue helps you.

### Procedure

1. Run task1 as background with the mgq.

1. Develope task2.

1. Add task2 to the the queue.

1. When the task1 is finished, the task2 will automatically start.

### mgq command

Queue name: CPU

task1: task1.sh

task2: task2.sh

```
% mgq CPU clear
% mgq CPU ad task1.sh
% mgq CPU start
```

<< develop task2 >>

```
% mgq CPU ad task2.sh
```

