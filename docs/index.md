## Overview

The mgq (Minimal Gram tasnk Queue) manages background tasks.
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
% mgq test ad "echo test" -stdout test.log
% mgq test -l
% mgq test start
% mgq test log
% cat test.log
```

## Requirement

+ Python 3.6.0 or later

+ mgq makes directory: $HOME/.mgq

## Git repository

[mgqueue](https://github.com/likesilkto/mgqueue)

## Author

[likesilkto](https://github.com/likesilkto)

## License

[MIT](https://github.com/likesilkto/tool/blob/master/LICENSE)


