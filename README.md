# TODOQ - To Be Released Soon

The simplest command-line TODO list for work, which leads extremely focus.

I like TODO list, and I have used quite a lot of them, but sadly none of them fits me well.
First, when I look at the long list of tasks to do, I am scared and bored, and I turn to
procrastinate.

Second, I am a VIM lover, and I use command-line tools for almost all of my programming stuff,
from my work to my part-time projects. I don't want to open a browser, or some apps to distract me.

Third, I find I wast my time on tasks priority management. When I look at my TODO, I arrange them occasionally
to make sure the order is according to priority. This is time overhead for TODO list, and I hope I could save
the time.

These are the reasons why I come up with the idea of TODOQ. It is very simple, but fully functional. You can add
tasks, check the top task, postpone or delete it. The tasks are ordered by priority, and you can create several queues
for multiple-task processing.

There is another story about single-task display. There is a theory about programmers that if you want him to make a website
in two weeks, he intends to procrastinate until there are just two days left, and then finish it in a messy way. If you just
tell him that to fix a bug this afternoon, he may do it pretty well. The theory may not apply to you, and I believe for most
ones, single task is enough to keep them focused and working efficiently.

## Install


## Use
### add [task name] [priority]

Add a task into the current queue. If the last including-no-space string is a number, it will be used as priority.
Priority can be any unsigned int, so you can set any large or crazy number as you want. If no priority is specified, 17
is set as the default priority.

e.g. add finish the front page UI design 999
task name - finish the front page UI design
priority - 999

e.g. add check email
task name - check email
priority - 17


### top
Display the top task. Yes, you are right, just the top one task.

### postpone
Postpone the top task, and you need to select one from the tasks to advance it to top.

### delete
Delete the top task. Yes, you can only delete the top one. This is designed on purpose, because we hope to make the
TODO list management overhead as small as possible.

### peek
HIGHLY NOT RECOMMENDED
List all the tasks in the current queue.

### showq
List all the queues. Single queue is recommended. Multiple queues are designed for those
who like multiple-thread processing.

### select [queue name]
Select the queue as the current queue.

### create [queue name]
Create a new queue.

### help | ?
Show help. Any weird command will also lead to help.

## License
Apache license is applied if you want to use the source code.
[ http://www.apache.org/licenses/LICENSE-2.0](
http://www.apache.org/licenses/LICENSE-2.0)
