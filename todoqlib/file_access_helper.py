import os
from xml.dom.minidom import parse, Document, getDOMImplementation
import time

time_format_str = '%a, %d %b %Y %H:%M:%S'

class FileAccessHelper:
  """ The helper class for data file saving, modifying and sync """
  def __init__(self, todoq_dir):
    self.todoq_dir = todoq_dir
    if not os.path.exists(todoq_dir):
      os.makedirs(todoq_dir)
    self.queue_info_file = os.path.join(todoq_dir, 'queue.info')
    self.queue_name = None
    self.queue_file_path = None
  
  def get_queue_name(self):
    """ Get the current queue """
    self.queue_name = 'default'
    self.queue_file_path = \
        os.path.join(self.todoq_dir, '{0}.task'.format(self.queue_name))
    return self.queue_name

  def get_queue_dom(self):
    """ Get the current queue dom """
    try:
      queue_dom = parse(self.queue_file_path)
    except IOError:
      queue_dom = getDOMImplementation().createDocument(None, 'Queue', None)
    return queue_dom

  def get_queue_node(self, queue_dom):
    queue_node = queue_dom.documentElement
    if not queue_node:
      queue_node = queue_dom.appendChild(queue_dom.createElement('Queue'))
    return queue_node

  def save_file(self, queue_dom):
    """ The xml dom is stored to a temporary first, and then overwrite the initial file """
    tmp_queue_file_path = self.queue_file_path + '.swap'
    tmp_queue_file = open(tmp_queue_file_path, 'w')
    tmp_queue_file.write(queue_dom.toxml())
    tmp_queue_file.close()
    os.rename(tmp_queue_file_path, self.queue_file_path)
    return

  def add_task(self, task_name, priority):
    """ Add the new task to the curr queue """
    self.get_queue_name()
    print 'add new task {0} with priority {1} to queue {2}'.format(\
        task_name, priority, self.queue_name)
    queue_dom = self.get_queue_dom()
    queue_node = self.get_queue_node(queue_dom)
    task_node = queue_node.appendChild(queue_dom.createElement('Unfinished'))
    name_node = task_node.appendChild(queue_dom.createElement('Name'))
    name_node.appendChild(queue_dom.createTextNode(task_name))
    priority_node = task_node.appendChild(queue_dom.createElement('Priority'))
    priority_node.appendChild(queue_dom.createTextNode(str(priority)))
    create_time_node = task_node.appendChild(queue_dom.createElement('create_time'))
    create_time_node.appendChild(queue_dom.createTextNode(time.strftime(time_format_str, time.localtime())))
    self.save_file(queue_dom)
    return

  def top_task(self):
    """ Return the the top task """
