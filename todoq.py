#! /usr/bin/env python

import optparse

def main():
  """ Runs program and handles command line options"""
  p = optparse.OptionParser(usage = 'Usage: %prog command [params]',
                            description = 'Simplest command-line todo list',
                            version = '%prog 1.0')

  (args, opts) = p.parse_args()
  

#  p.add_option('--add', '-a',
#               action='store_true',
#               default=False,
#               help='add a new task')
#  p.add_option('--top', '-t',
#               action='store_true',
#               default=False,
#               help='show the top task')
#  p.add_option('--finish', '-f',
#               action='store_true',
#               default=False,
#               help='mark the top task as finished and archive it')
#  p.add_option('--postpone', '-p',
#               action='store_true',
#               default=False,
#               help='postpone the top task, and advance the second task')
#  p.add_option('--drop', '-d',
#               action='store_true',
#               default=False,
#               help='mark the top task as dropped and archive it')
#  p.add_option('--list', '',
#               action='store_true',
#               default=False,
#               help='list all the tasks in the current task queue')
#  p.add_option('--showq', '',
#               action='store_true',
#               default=False,
#               help='list all the queues')
#  p.add_option('--selectq', '',
#               action='store_true',
#               default=False,
#               help='select the queue with the ID as the current queue')
#  p.add_option('--createq', '',
#               action='store_true',
#               default=False,
#               help='create a new queue')
#  p.add_option('--sync', '',
#               action='store_true',
#               default=False,
#               help='sync all the queue with Dropbox')


  
  


if __name__ == '__main__':
  main()
