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

### Example

You have several training python codes like deep learning. In this example, the account name is _likesilkto_.

#### 1. Clear the task queue of CPU.

```
% mgq CPU rmall
```

#### 2. Register task train_mnist.py in ~/mnist to the CPU queque.

```
% cd ~/mnist

% mgq CPU as 'python train_mnist.py'
Added python train_mnist.py to CPU

% mgq CPU
 0 : python train_mnist.py > /dev/null 2> /dev/null
     /home/likesilkto/mnist/
```

#### 3. Register task train_cifar.py in ~/cifar to the CPU queque.

```
% cd ~/cifar

% mgq CPU ad 'python train_cifar.py' -stdout train_cifar.log
Added python train_cifar.py to CPU

% mgq CPU
 0 : python train_mnist.py > /dev/null 2> /dev/null
     /home/likesilkto/mnist/
 1 : python train_cifar.py > train_cifar.log 2> /dev/null
     /home/mtanaka/tmp/cifar/
```

#### 4. Start tasks.

```
% mgq CPU start
Daemon for CPU is starting.
```

Or with gmail option.

```
% mgq CPU start -gmail likesilkto
password for likesilkto@gmail.com:
Daemon for CPU is starting.
```
Please provide the password for gmail.
If you start with gmail option, you will receive the gmail when the task is finished.

#### 5. Check status

```
% mgq CPU log
YYYY-MM-DD hh:mm:ss,???:WARNING:Starting daemon.
YYYY-MM-DD hh:mm:ss,???:INFO:Daemon for CPU is stared.
YYYY-MM-DD hh:mm:ss,???:INFO:Start python train_mnist.py > /dev/null 2> /dev/null on /home/likesilkto/mnist/

% mgq CPU
 * : python train_mnist.py > /dev/null 2> /dev/null
     /home/likesilkto/mnist/
 1 : python train_cifar.py > train_cifar.log 2> /dev/null
     /home/mtanaka/tmp/cifar/
```

#### 6. Add tasks

```
% cd ~/mnist
% mgq CPU -l ad 'python train_fashion_mnist.py'
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
% mgq CPU stop
Daemon for CPU is stopped.

% mgq CPU -l
 0 : python train_mnist.py > /dev/null 2> /dev/null
     /home/likesilkto/mnist/
 1 : python train_cifar.py > train_cifar.log 2> /dev/null
     /home/mtanaka/tmp/cifar/
 2 : python train_fashion_mnist.py > /dev/null 2> /dev/null
     /home/likesilkto/mnist/
```

