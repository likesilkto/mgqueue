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

### Example

You have several training python codes like deep learning. In this example, the account name is _likesilkto_.


#### 0. Initialize prefix

It run only once at first time.

```
% mgq tf0 clear
% mgq tf0 prefix "CUDA_VISIBLE_DEVICES=0 "
% mgq tf1 clear
% mgq tf1 prefix "CUDA_VISIBLE_DEVICES=1 "
```

#### 1. Clear the task queue of tf0.

```
% mgq tf0 rmall
% mgq tf1 rmall
```

#### 2. Register task train_mnist.py in ~/mnist to the tf0 queque.

```
% cd ~/mnist

% mgq tf0 as 'python train_mnist.py'
Added python train_mnist.py to tf0

% mgq tf0
prefix: CUDA_VISIBLE_DEVICES=0
 0 : python train_mnist.py > /dev/null 2> /dev/null
     /home/likesilkto/mnist/

% mgq tf1 as 'python train_fashon_mnist.py'
Added python train_fashon_mnist.py to tf1

% mgq tf1
prefix: CUDA_VISIBLE_DEVICES=1
 0 : python train_fashon_mnist.py > /dev/null 2> /dev/null
     /home/likesilkto/mnist/
```

#### 3. Register task train_cifar.py in ~/cifar to the tf0 queque.

```
% cd ~/cifar

% mgq tf0 ad 'python train_cifar10.py' -stdout train_cifar10.log
Added python train_cifar10.py to tf0

% mgq tf0
prefix: CUDA_VISIBLE_DEVICES=0
 0 : python train_mnist.py > /dev/null 2> /dev/null
     /home/likesilkto/mnist/
 1 : python train_cifar10.py > train_cifar10.log 2> /dev/null
     /home/mtanaka/tmp/cifar/

% mgq tf1 ad 'python train_cifar100.py' -stdout train_cifar100.log
Added python train_cifar100.py to tf1

% mgq tf1
prefix: CUDA_VISIBLE_DEVICES=1
 0 : python train_fashion_mnist.py > /dev/null 2> /dev/null
     /home/likesilkto/mnist/
 1 : python train_cifar100.py > train_cifar100.log 2> /dev/null
     /home/mtanaka/tmp/cifar/

% mgq
tf0 +  : 2
tf1 +  : 2
```

#### 4. Start tasks.

```
% mgq tf0 start
Daemon for tf0 is starting.

% mgq
tf0 +* : 2
tf1 +  : 2

% mgq tf1 start
Daemon for tf1 is starting.

% mgq
tf0 +* : 2
tf1 +* : 2
```

Or with gmail option.

```
% mgq tf0 start -gmail likesilkto
password for likesilkto@gmail.com:
Daemon for tf0 is starting.

% mgq tf1 start -gmail likesilkto
password for likesilkto@gmail.com:
Daemon for tf1 is starting.

% mgq
tf0 +* : 2
tf1 +* : 2
```
Please provide the password for gmail.
If you start with gmail option, you will receive the gmail when the task finish.

#### 5. Check status

```
% mgq tf0 log
YYYY-MM-DD hh:mm:ss,???:WARNING:Starting daemon.
YYYY-MM-DD hh:mm:ss,???:INFO:Daemon for tf0 is stared.
YYYY-MM-DD hh:mm:ss,???:INFO:Start python train_mnist.py > /dev/null 2> /dev/null on /home/likesilkto/mnist/

% mgq tf0
 * : python train_mnist.py > /dev/null 2> /dev/null
     /home/likesilkto/mnist/
 1 : python train_cifar10.py > train_cifar10.log 2> /dev/null
     /home/mtanaka/tmp/cifar/

% mgq tf1 log
YYYY-MM-DD hh:mm:ss,???:WARNING:Starting daemon.
YYYY-MM-DD hh:mm:ss,???:INFO:Daemon for tf1 is stared.
YYYY-MM-DD hh:mm:ss,???:INFO:Start python train_fashion_mnist.py > /dev/null 2> /dev/null on /home/likesilkto/mnist/

% mgq tf1
 * : python train_fashion_mnist.py > /dev/null 2> /dev/null
     /home/likesilkto/mnist/
 1 : python train_cifar100.py > train_cifar100.log 2> /dev/null
     /home/mtanaka/tmp/cifar/
```

#### 6. Add tasks

```
% cd ~/mnist
% mgq tf0 -l ad 'python train_fashion_mnist2.py'
 * : python train_mnist.py > /dev/null 2> /dev/null
     /home/likesilkto/mnist/
 1 : python train_cifar10.py > train_cifar10.log 2> /dev/null
     /home/mtanaka/tmp/cifar/
 2 : python train_fashion_mnist2.py > /dev/null 2> /dev/null
     /home/likesilkto/mnist/
```

#### 7. Stop tasks
If you want to stop the task,
```
% mgq tf0 stop
Daemon for tf0 is stopped.

% mgq
tf0 +  : 3
tf1 +* : 2

% mgq tf0 -l
 0 : python train_mnist.py > /dev/null 2> /dev/null
     /home/likesilkto/mnist/
 1 : python train_cifar10.py > train_cifar10.log 2> /dev/null
     /home/mtanaka/tmp/cifar/
 2 : python train_fashion_mnist2.py > /dev/null 2> /dev/null
     /home/likesilkto/mnist/
```


