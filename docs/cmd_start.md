## Start

```
mgq queue start [-gmail GMAIL ] 
```

Start to run of the tasks in the queue.

### Example
```
% mgq queue start
```

### Example mail
```
% mgq queue start -gmail GMAIL
```

Plese give the password for the GMAIL@gmail.com.
Then, when the task finish, the mail will be sent from GMAIL@gmail.com to GMAIL+mgq@gmail.com.

you'll need to configure "less" secure method to use this functionality.

[Reference to send the gmail with python.](https://stackabuse.com/how-to-send-emails-with-gmail-using-python/)
