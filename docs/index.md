## Overview

The mgq (Minimal Gram Queue) manages background tasks.
When the current task is finished, the next task will be automatically started.


## Functionalities

+ Multi-queues

+ Adding task

+ Remove task

+ Swith task


## Install

```
% pip install git+https://github.com/likesilkto/mgqueue
```

If you use anyenv, restart shell.

## Getting start

```
% mgq test ad 'echo test' -stdout test.log
% mgq test -l
% mgq test start
% mgq test log
% cat test.log
```

