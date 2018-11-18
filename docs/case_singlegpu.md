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
Then, task1.py is started and task2.py will be automatically started after task2.py will be finished.

Once you initialized the queue, you just add and start the tasks.

### Example

You have several training python codes like deep learning. In this example, the account name is _likesilkto_.

#### 1. Clear the task queue of tf0.

```
% mgq tf0 rmall
```

#### 2. Register task train_mnist.py in ~/mnist to the tf0 queque.

```
% cd ~/mnist

% mgq tf0 as 'python train_mnist.py'
Added python train_mnist.py to tf0

% mgq tf0
 0 : python train_mnist.py > /dev/null 2> /dev/null
     /home/likesilkto/mnist/
```

#### 3. Register task train_cifar.py in ~/cifar to the tf0 queque.

```
% cd ~/cifar

% mgq tf0 ad 'python train_cifar.py' -stdout train_cifar.log
Added python train_cifar.py to tf0

% mgq tf0
 0 : python train_mnist.py > /dev/null 2> /dev/null
     /home/likesilkto/mnist/
 1 : python train_cifar.py > train_cifar.log 2> /dev/null
     /home/mtanaka/tmp/cifar/
```

#### 4. Start tasks.

```
% mgq tf0 start
Daemon for tf0 is starting.
```

Or with gmail option.

```
% mgq tf0 start -gmail likesilkto
password for likesilkto@gmail.com:
Daemon for tf0 is starting.
```
Please provide the password for gmail.
If you start with gmail option, you will receive the gmail when the task is finished.

#### 5. Check status

```
% mgq tf0 log
YYYY-MM-DD hh:mm:ss,???:WARNING:Starting daemon.
YYYY-MM-DD hh:mm:ss,???:INFO:Daemon for CPU is stared.
YYYY-MM-DD hh:mm:ss,???:INFO:Start python train_mnist.py > /dev/null 2> /dev/null on /home/likesilkto/mnist/

% mgq tf0
 * : python train_mnist.py > /dev/null 2> /dev/null
     /home/likesilkto/mnist/
 1 : python train_cifar.py > train_cifar.log 2> /dev/null
     /home/mtanaka/tmp/cifar/
```

#### 6. Add tasks

```
% cd ~/mnist
% mgq tf0 -l ad 'python train_fashion_mnist.py'
 * : python train_mnist.py > /dev/null 2> /dev/null
     /home/likesilkto/mnist/
 1 : python train_cifar.py > train_cifar.log 2> /dev/null
     /home/mtanaka/tmp/cifar/
 2 : python train_fashion_mnist.py > /dev/null 2> /dev/null
     /home/likesilkto/mnist/
```

#### 7. Stop tasks
If you want to stop the task,
```
% mgq tf0 stop
Daemon for tf0 is stopped.

% mgq tf0 -l
 0 : python train_mnist.py > /dev/null 2> /dev/null
     /home/likesilkto/mnist/
 1 : python train_cifar.py > train_cifar.log 2> /dev/null
     /home/mtanaka/tmp/cifar/
 2 : python train_fashion_mnist.py > /dev/null 2> /dev/null
     /home/likesilkto/mnist/
```

