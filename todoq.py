#! /usr/bin/env python

import sys
import argparse

class CommandLineApplication:
  """ The command line application class to deal with sub-command dispatching """
  def __init__(self, sub_command_list):
    """ sub_command_list is the list from sub-command to handler class """
    self.sub_command_list = sub_command_list

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

class SubCommandAddHandler(SubCommandHandler):
  """ The handler to deal with sub-command 'add' """
  def get_help_str(self):
    """ Returns the help str for sub-command 'add' """
    return 'add a new task'

  def add_arguments(self, subparser):
    """ Add optional and positional arguments to subparser """
    subparser.add_argument('task_name', nargs=1)
    subparser.add_argument('priority', type=int, nargs='?')
    return

  def execute(self, args):
    """ The function to be called when sub-command 'add' is executed """
    print 'add is executed'
    return

class SubCommandTopHandler(SubCommandHandler):
  """ The handler to deal with sub-command 'top' """
  def get_help_str(self):
    """ Returns the help str for sub-command 'top' """
    return 'show the top task'

  def execute(self, args):
    """ The function to be called when sub-command 'top' is executed """
    print 'top is executed'
    return

class SubCommandFinishHandler(SubCommandHandler):
  """ The handler to deal with 'finish' """
  def get_help_str(self):
    """ Returns the help str for 'finish' """
    return 'mark the top task as finished and archive it'

class SubCommandPostponeHandler(SubCommandHandler):
  """ The handler to deal with 'postpone' """
  def get_help_str(self):
    """ Returns the help str for 'postpone' """
    return 'postpone the top task, and advance the second task'

class SubCommandDropHandler(SubCommandHandler):
  """ The handler to deal with 'drop' """
  def get_help_str(self):
    """ Returns the help str for 'drop' """
    return 'mark the top task as dropped and archive it'

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

if __name__ == '__main__':
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
    ]);
  app.run()
