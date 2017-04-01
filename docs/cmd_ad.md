## Add "command"

```
mgq queue [-ls] ad "command" [-stdout stdout_file] [-stderr stderr_file]
```

It adds "command" to the queue.
Files for stdout and/or stderr can be specified.
Default stdout and stderr are /dev/null.

### Example
```
% mgq queue ad "python a.py"
```

```
% mgq queue -ls ad "python a.py" -stdout a.stdout
```

