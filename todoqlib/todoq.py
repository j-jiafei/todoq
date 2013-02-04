#!/usr/bin/env python

import sys
import argparse
import os
from file_access_helper import FileAccessHelper

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
    return

class SubCommandTopHandler(SubCommandHandler):
  """ The handler to deal with sub-command 'top' """
  def get_help_str(self):
    """ Returns the help str for sub-command 'top' """
    return 'show the top task'

  def execute(self, args):
    """ The function to be called when sub-command 'top' is executed """
    try:
      task_name, priority = helper.get_top_task()
      print '{0}\t\t{1}'.format(task_name, priority)
    except IndexError:
      self.print_no_task_error()
    return

class SubCommandFinishHandler(SubCommandHandler):
  """ The handler to deal with 'finish' """
  def get_help_str(self):
    """ Returns the help str for 'finish' """
    return 'mark the top task as finished and archive it'

  def execute(self, args):
    try:
      helper.mark_top_task_as_finished()
    except IndexError:
      self.print_no_task_error()
    return


class SubCommandPostponeHandler(SubCommandHandler):
  """ The handler to deal with 'postpone' """
  def get_help_str(self):
    """ Returns the help str for 'postpone' """
    return 'postpone the top task, and advance the second task'

  def execute(self, args):
    return

class SubCommandDropHandler(SubCommandHandler):
  """ The handler to deal with 'drop' """
  def get_help_str(self):
    """ Returns the help str for 'drop' """
    return 'mark the top task as dropped and archive it'

  def execute(self, args):
    try:
      helper.mark_top_task_as_dropped()
    except IndexError:
      self.print_no_task_error()
    return

class SubCommandListHandler(SubCommandHandler):
  """ The handler to deal with 'list' """
  def get_help_str(self):
    """ Returns the help str for 'list' """
    return 'list all the tasks in the current task queue'

class SubCommandShowqHandler(SubCommandHandler):
  """ The handler to deal with 'showq' """
  def get_help_str(self):
    """ Returns the help str for 'showq' """
    return 'list all the queues'

class SubCommandSelectqHandler(SubCommandHandler):
  """ The handler to deal with 'selectq' """
  def get_help_str(self):
    """ Returns the help str for 'selectq' """
    return 'select the queue as the current queue'

class SubCommandCreateqHandler(SubCommandHandler):
  """ The handler to deal with 'createq' """
  def get_help_str(self):
    """ Returns the help str for 'createq' """
    return 'create a new queue'

class SubCommandSyncHandler(SubCommandHandler):
  """ The handler to deal with 'sync' """
  def get_help_str(self):
    """ Returns the help str for 'sync' """
    return 'sync all the task queues with Dropbox'

def main():
  app = CommandLineApplication([
      ('add', SubCommandAddHandler),
      ('top', SubCommandTopHandler),
      ('postpone', SubCommandPostponeHandler),
      ('finish', SubCommandFinishHandler),
      ('drop', SubCommandDropHandler),
      ('list', SubCommandListHandler),
      ('showq', SubCommandShowqHandler),
      ('selectq', SubCommandSelectqHandler),
      ('createq', SubCommandCreateqHandler),
      ('sync', SubCommandSyncHandler),
    ], debug=True);
  app.run()

if __name__ == '__main__':
  main()
