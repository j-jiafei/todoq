#!/usr/bin/env python

import sys
import argparse
import os
from file_access_helper import FileAccessHelper
from task import Task
from queue import QueueNotFoundError

helper = FileAccessHelper(os.path.join(os.path.expanduser('~'), '.todoq'))

class CommandLineApplication:
  """ The command line application class to deal with sub-command dispatching """
  def __init__(self, sub_command_list, debug = False):
    """ sub_command_list is the list from sub-command to handler class """
    self.sub_command_list = sub_command_list
    helper.set_debug(debug)

  def run(self):
    """ The function to be called to run the whole program """
    parser = argparse.ArgumentParser(prog='todoq')
    subparsers = parser.add_subparsers(help='sub-command help')
    for element in self.sub_command_list:
      handler = element[1]()
      parser_add = subparsers.add_parser(element[0], help=handler.get_help_str())
      handler.add_arguments(parser_add)
      parser_add.set_defaults(func=handler.execute)
    args = parser.parse_args()
    args.func(args)
    return


class SubCommandHandler:
  """ The base class for all the sub-command handlers """
  def get_help_str(self):
    """ Returns default help str """
    return 'sub-command'

  def add_arguments(self, subparser):
    """ Add no arguments for default """
    return

  def execute(self, args):
    """ The default function to be called when sub-command is executed """
    return

  def print_no_task_error(self):
    print 'There is no task in the queue.'
    return

  def print_no_queue_error(self):
    print 'There is no queue now.'
    return

  def confirm(self, prompt=None, resp=False):
    if prompt is None:
      prompt = 'Confirm'
    if resp:
      prompt = '{0} [{1}]|{2}: '.format(prompt, 'y', 'n')
    else:
      prompt = '{0} [{1}]|{2}: '.format(prompt, 'n', 'y')
    while True:
      ans = raw_input(prompt)
      if not ans:
        return resp
      if ans not in ['y', 'Y', 'n', 'N']:
        print 'please enter y or n.'
        continue
      if ans == 'y' or ans == 'Y':
        return True
      if ans == 'n' or ans == 'N':
        return False


class SubCommandAddHandler(SubCommandHandler):
  """ The handler to deal with sub-command 'add' """
  def get_help_str(self):
    """ Returns the help str for sub-command 'add' """
    return 'add a new task'

  def add_arguments(self, subparser):
    """ Add optional and positional arguments to subparser """
    subparser.add_argument('task_name', nargs=1)
    subparser.add_argument('priority', type=int, nargs='?', default=17)
    return

  def execute(self, args):
    """ The function to be called when sub-command 'add' is executed """
    helper.add_task(args.task_name[0], args.priority)
    print "[todoq] Add a new task to '{0}'".format(helper.get_queue_name())
    print ""
    print "\t{0} <- {1}".format(args.task_name[0], args.priority)
    print ""
    return


class SubCommandTopHandler(SubCommandHandler):
  """ The handler to deal with sub-command 'top' """
  def get_help_str(self):
    """ Returns the help str for sub-command 'top' """
    return 'show the top task'

  def execute(self, args):
    """ The function to be called when sub-command 'top' is executed """
    try:
      task = helper.get_top_task()
      print "[todoq] The top task in '{0}'".format(helper.get_queue_name())
      print ""
      print "\t{0} <- {1}".format(task.get_name(), task.get_priority())
      print ""
    except IndexError:
      self.print_no_task_error()
    return


class SubCommandFinishHandler(SubCommandHandler):
  """ The handler to deal with 'finish' """
  def get_help_str(self):
    """ Returns the help str for 'finish' """
    return 'finish and archive the top task'

  def execute(self, args):
    try:
      top_task = helper.get_top_task()
      top_task_name = top_task.get_name()
      top_task_priority = top_task.get_priority()
      helper.mark_top_task_as_finished()
      print "[todoq] Finish the top task in '{0}'!".format(
          helper.get_queue_name())
      print ""
# \u2714 is the heavy check mark in unicode
      print u"\t{0} <- {1} \u2714".format(top_task_name, top_task_priority)
      print ""
    except IndexError:
      self.print_no_task_error()
    return


class SubCommandPostponeHandler(SubCommandHandler):
  """ The handler to deal with 'postpone' """
  def get_help_str(self):
    """ Returns the help str for 'postpone' """
    return 'postpone the top task, and advance the second task'

  def add_arguments(self, subparser):
    """ Add the priority argument for 'postpone """
    subparser.add_argument('priority', type=int, nargs='?')
    return

  def execute(self, args):
    """ Change the priority value of the top task """
    try:
      helper.postpone_top_task(args.priority)
      print "[todoq] Postpone the top task in '{0}'".format(
          helper.get_queue_name())
      print "[todoq] The current top task in '{0}'".format(
          helper.get_queue_name())
      print ""
      top_task = helper.get_top_task()
      print "\t{0} <- {1}".format(top_task.name, top_task.priority)
      print ""
    except IndexError:
      self.print_no_task_error()
    return


class SubCommandDropHandler(SubCommandHandler):
  """ The handler to deal with 'drop' """
  def get_help_str(self):
    """ Returns the help str for 'drop' """
    return "'drop' the top task and archive it"

  def execute(self, args):
    try:
      top_task = helper.get_top_task()
      top_task_name = top_task.get_name()
      top_task_priority = top_task.get_priority()
      helper.mark_top_task_as_dropped()
      print "[todoq] Drop the top task in '{0}'...".format(
          helper.get_queue_name())
      print ""
# \u2714 is the heavy check mark in unicode
      print u"\t{0} <- {1} \u2718".format(top_task_name, top_task_priority)
      print ""
    except IndexError:
      self.print_no_task_error()
    return


class SubCommandListHandler(SubCommandHandler):
  """ The handler to deal with 'list' """

  def get_help_str(self):
    """ Returns the help str for 'list' """
    return 'list all the tasks in the current task queue'

  def add_arguments(self, subparser):
    """ Add the priority argument for 'postpone """
    subparser.add_argument('-u', '--unfinished',
                           help='display all the unfinished tasks',
                           action='store_true')
    subparser.add_argument('-a', '--all',
                           help='display all the tasks',
                           action='store_true')
    subparser.add_argument('-f', '--finished',
                           help='display all the finished tasks',
                           action='store_true')
    subparser.add_argument('-d', '--dropped',
                           help='display all the dropped tasks',
                           action='store_true')
    subparser.add_argument('-n', '--count',
                           help='specify the number of tasks to be displayed',
                           type=int)
    return

  def execute(self, args):
    tasks = helper.get_tasks((args.all, args.unfinished, args.finished,
                              args.dropped), args.count)
    if not tasks:
      self.print_no_task_error()
    for task in tasks:
      print task.to_str()
    return


class SubCommandShowqHandler(SubCommandHandler):
  """ The handler to deal with 'showq' """
  def get_help_str(self):
    """ Returns the help str for 'showq' """
    return 'list all the queues'

  def add_arguments(self, subparser):
    subparser.add_argument('-a', '--active',
                           help='display the current active queue',
                           action='store_true')
    subparser.add_argument('-i', '--inactive',
                           help='display all the inactive queues',
                           action='store_true')
    return

  def execute(self, args):
    queues = helper.get_queues((args.active, args.inactive))
    if not queues:
      self.print_no_queue_error()
    for queue in queues:
      print queue.to_str()
    return


class SubCommandSelectqHandler(SubCommandHandler):
  """ The handler to deal with 'selectq' """
  def get_help_str(self):
    """ Returns the help str for 'selectq' """
    return 'select the queue as the current queue'

  def add_arguments(self, subparser):
    subparser.add_argument('queue_name', nargs = 1,
                           help='the name of queue to be selected')
    return

  def execute(self, args):
    try:
      helper.select_queue(args.queue_name[0])
      print 'Select "{0}" as the current active queue'.format(args.queue_name[0])
    except QueueNotFoundError as detail:
      print detail
    return


class SubCommandCreateqHandler(SubCommandHandler):
  """ The handler to deal with 'createq' """
  def get_help_str(self):
    """ Returns the help str for 'createq' """
    return 'create a new queue'

  def add_arguments(self, subparser):
    subparser.add_argument('queue_name', nargs = 1,
                           help='the name of queue to be selected')
    return

  def execute(self, args):
    helper.create_queue(args.queue_name[0])
    print 'Create a new queue "{0}"'.format(args.queue_name[0])
    return


class SubCommandDeleteqHandler(SubCommandHandler):
  """ The handler to deal with 'createq' """
  def get_help_str(self):
    """ Returns the help str for 'createq' """
    return 'delete an existing queue'

  def add_arguments(self, subparser):
    subparser.add_argument('queue_name', nargs = 1,
                           help='the name of queue to be selected')
    return

  def execute(self, args):
    if not self.confirm():
      return
    try:
      helper.delete_queue(args.queue_name[0])
      print 'Delete an existing queue "{0}"'.format(args.queue_name[0])
    except QueueNotFoundError as detail:
      print detail
    return


def main():
  app = CommandLineApplication([
      ('add', SubCommandAddHandler),
      ('top', SubCommandTopHandler),
      ('postpone', SubCommandPostponeHandler),
      ('finish', SubCommandFinishHandler),
      ('drop', SubCommandDropHandler),
      ('ls', SubCommandListHandler),
      ('showq', SubCommandShowqHandler),
      ('selectq', SubCommandSelectqHandler),
      ('createq', SubCommandCreateqHandler),
      ('deleteq', SubCommandDeleteqHandler),
    ], debug=True);
  app.run()


if __name__ == '__main__':
  main()
