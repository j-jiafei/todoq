===============
 TODOQ
===============

---------------------------------------
 The Simplest Command-line TODO List
---------------------------------------


To be released soon, and comments are welcome. Twitter: Jeff Jia @JeffreyFJ

Introduction
===============

TODOQ is a single-task-display, priority-based, command-line TODO list (I don't know whether someone has come up with such a concept as 
single-task display).

"Single-task-display" means that usually it only displays the top task, and you can "finish", "drop" or "postpone" it.

"Priority-based" means the order of tasks is totally based on priority, which is an unsigned int (whichever python int type supports).

"Command-line" means it is run by linux / unix (mac included) terminal.

TODOQ also supports multiple queues, in case you want to work in multiple threads at the same time in a period.

We also support the sync of tasks, and dropbox account is required if you want to use the feature.

The story behind the design of TODOQ
===============

We hope to design the world's simplest command-line TODO list, and we have two basic goals for it:
1. The TODO list should help users focus on work.
2. The task management overhead should be minimized.

Personally I am a TODO list enthusiast. Starting from paper and pencil when I was in high school, I have been trying to use
TODO list to help me schedule my life. I explored and used different methods and tools to help me track the status of
daily tasks. Some of the tools are pretty cool, and I actually used them for quite while. But from my experience, I found that I
never kept using a single tool for more than two weeks. At first, I might be attracted to a tool and make up my mind for a resolution
to make my life well-planed. But soon I found that the tool does not actually help me much on focus and getting things done, but the
overhead to manage the TODO list itself is pretty high.

Now as a research assistant, a side-project developer and a student at the same time. I use command-line tools quite a lot every day.
Sometimes I use web-based TODO list to help me track problems to solve, features to implement, or bugs to fix. But switching between
command line and browser can be a pain sometimes, and looks less professional. Such a switching could also be distracting sometimes.

Then my friends and I decide to write a TODO list tool for developers like us, basically command-line everything guys =). We hope it 
could be really light-wight, "prevent" over-managing task list, and help focus on work. So we come up with the idea of single-task
display TODO list. Instead of displaying all the tasks, we simply show the top one, the one with the highest priority. Operations,
like "finish", "drop", "postpone", are only limited to the top one to minimize the TODO list management overhead. Tasks can still be
listed with the command "peek", which is highly not recommended. We hope users could just focus on the top task at the moment, and thinking
about other tasks only when absolutely necessary.

You may find such a design may be inconvenient sometimes. You may want to arrange the order of tasks, set a deadline for it, or simply drop
some of them. These operations are almost unsupported in TODOQ. Instead, for the order, we use priority (basically any unsigned int number between
0 and whatever python int type supports). The tasks are ordered based on priority completely. We don't use deadline for tasks. We believe that
human mind should be able to transform urgency to priority easily, and for work, a good way to meet a deadline is to do it as early as possible.
You may want to drop some of tasks since you have finished them, or they are not necessary any more, but why not do it later, cause managing TODO
list itself could also be "viewed" as a task with not-the-highest priority.

We hope you could enjoy using TODOQ, and make it help you improve your valuable productivity.

 
Install
===============

This part will be added later.

Usage
===============

taskq add task\_name priority
---------------

Add a task into the current queue. If the last including-no-space string is a number, it will be used as priority.
Priority can be any unsigned int, so you can set any large or crazy number as you want. A priority is forced to given,
and should be different from that of any other task.

e.g. 
taskq add "finish the front page UI design" 999
task name - finish the front page UI design
priority - 999

e.g. 
taskq add "check email" 10
task name - check email
priority - 10


taskq top
---------------
Display the top task. Yes, you are right, just the top one task.

taskq finish
---------------
Mark the top task as "finished".

taskq postpone priority
---------------
Postpone the top task.

taskq drop
---------------
Mark the top task as "dropped".

taskq list
---------------
List all the tasks in the current queue. HIGHLY NOT RECOMMENDED.

Options
~~~~~~~~~~~~~~~
* \-u: list all the unfinished tasks
* \-a: list all the tasks
* \-f: list all the finished tasks
* \-d: list all the dropped tasks
* \-n [count]: specifiy the number of tasks to be displayed

taskq showq
---------------
List all the queues. Single queue is recommended. Multiple queues are designed for those
who like multiple-thread processing.

taskq selectq queue\_id
---------------
Select the queue as the current queue.

taskq createq queue\_name
---------------
Create a new queue.

taskq --help, taskq -h, taskq help
---------------
Show help. Any weird commands will also lead to help.

taskq sync
---------------
Sync to dropbox. (Dropbox account required.)


License
===============
Apache license is applied if you want to use the source code.
[ http://www.apache.org/licenses/LICENSE-2.0](
http://www.apache.org/licenses/LICENSE-2.0)
