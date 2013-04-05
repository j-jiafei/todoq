import os
from xml.dom.minidom import parse, Document, getDOMImplementation
import time
import heapq
from task import Task
from queue import Queue
from queue import QueueNotFoundError
from sets import Set
import shutil


class FileAccessHelper:
  """ The helper class for data file saving, modifying and sync """
  def __init__(self, todoq_dir, debug = False):
    self.init_todoq_dir = todoq_dir
    try:
      if not os.path.exists(self.init_todoq_dir):
        os.mkdir(self.init_todoq_dir)
      path_info_file = open(os.path.join(todoq_dir, 'path.info'), 'r')
      self.todoq_dir = path_info_file.readlines()[0]
      path_info_file.close()
    except IOError:
      self.todoq_dir = todoq_dir
      path_info_file = open(os.path.join(todoq_dir, 'path.info'), 'w')
      path_info_file.write(todoq_dir)
      path_info_file.close()
    self.queue_info_path = os.path.join(self.todoq_dir, 'queue.info')
    self.queue_info_dom = None
    self.debug = debug
    self.queue_name = None
    self.queue_path = None
    self.queue_dom = None
    self.queue_node = None
    self.init_check(debug)

  def init_check(self, debug):
    """ Initialization check """
# existance of todoq_dir
    if not os.path.exists(self.todoq_dir):
      os.makedirs(self.todoq_dir)
# existance of queue_info_path
    queue_info_dom = self.get_queue_info_dom()
# default task check
    queue_name_set = Set()
    for node in queue_info_dom.documentElement.getElementsByTagName('Name'):
      queue_name_set.add(node.firstChild.data)
    if not 'default' in queue_name_set:
      self.create_queue('default')
    for file_name in os.listdir(self.todoq_dir):
      if not file_name.endswith('task'):
        continue
      queue_name = os.path.splitext(file_name)[0]
      if not queue_name == 'default' and not queue_name in queue_name_set:
        self.create_queue(queue_name)
# active task check
    if not queue_info_dom.documentElement.getElementsByTagName('Active'):
      self.select_queue('default')
    return
  
  def set_debug(self, debug):
    self.debug = debug
    return

  def get_queue_name(self):
    """ Get the current queue """
    if self.queue_name:
      return self.queue_name
    dom = self.get_queue_info_dom()
    active_task_node = dom.getElementsByTagName('Active')
    self.queue_name = active_task_node[0].getElementsByTagName(
        'Name')[0].firstChild.data
    return self.queue_name

  def get_queue_path(self, queue_name = None):
    queue_name = queue_name or self.queue_name or self.get_queue_name()
    self.queue_path = self.queue_path or \
        os.path.join(self.todoq_dir, '{0}.task'.format(queue_name))
    return self.queue_path

  def get_queue_info_dom(self, queue_info_path = None):
    queue_info_path = queue_info_path or self.queue_info_path
    if self.queue_info_dom:
      return self.queue_info_dom
    try:
      self.queue_info_dom = parse(queue_info_path)
    except IOError:
      self.queue_info_dom = getDOMImplementation().createDocument(None, 'Info',
          None)
    return self.queue_info_dom

  def get_queue_dom(self, queue_path = None):
    """ Get the current queue dom """
    queue_path = queue_path or self.get_queue_path()
    if self.queue_dom:
      return self.queue_dom
    try:
      self.queue_dom = parse(queue_path)
    except IOError:
      self.queue_dom = getDOMImplementation().createDocument(None, 'Queue', None)
    return self.queue_dom

  def get_queue_node(self, queue_dom = None):
    queue_dom = queue_dom or self.get_queue_dom()
    self.queue_node = self.queue_node or queue_dom.documentElement or \
        queue_dom.appendChild(queue_dom.createElement('Queue'))
    return self.queue_node

  def save_file(self, path, dom):
    dom = dom or self.get_dom()
    tmp_path = path + '.swap'
    tmp_file = open(tmp_path, 'w')
    tmp_file.write(dom.toxml())
    tmp_file.close()
    os.rename(tmp_path, path)

  def save_queue_info_file(self, queue_info_dom = None):
    queue_info_dom = queue_info_dom or self.get_queue_info_dom()
    self.save_file(self.queue_info_path, self.queue_info_dom)
    return

  def save_queue_file(self, queue_dom = None):
    """ The xml dom is stored to a temporary first, and then overwrite the initial file """
    queue_dom = queue_dom or self.get_queue_dom()
    self.save_file(self.get_queue_path(), queue_dom)
    return

  def add_task(self, task_name, priority):
    """ Add the new task to the curr queue """
    if self.debug:
      print 'add new task {0} with priority {1} to queue {2}'.format(\
          task_name, priority, self.get_queue_name())
    queue_dom = self.get_queue_dom()
    queue_node = self.get_queue_node()
    task = Task(task_name, priority, 'Unfinished')
    queue_node.appendChild(task.to_xml_node(queue_dom))
    self.save_queue_file()
    return

  def get_task_heap(self, task_nodes):
    """ The key is the negation of priority """
    heap = []
    for task_node in task_nodes:
      key = -int(task_node.getElementsByTagName('Priority')[0].firstChild.data)
      heapq.heappush(heap, (key, task_node))
    return heap

  def get_node_data(self, node, tag):
    return node.getElementsByTagName(tag)[0].childNodes[0].data

  def get_top_node(self):
    queue_dom = self.get_queue_dom()
    unfinished_tasks = queue_dom.getElementsByTagName('Unfinished')
    heap = self.get_task_heap(unfinished_tasks)
    top_node = heap[0][1]
    return top_node

  def get_top_task(self):
    """ Return the the top task """
    top_node = self.get_top_node()
    return Task.parse_task(top_node)
  
  def change_top_task_to_tag(self, tag):
    queue_dom = self.get_queue_dom()
    top_node = self.get_top_node()
    if self.debug:
      print 'Mark top task "{0}" as {1}'.format(self.get_node_data(top_node, 'Name'), tag)
    top_node.tagName = tag
    return
    
  def mark_top_task_as_finished(self):
    self.change_top_task_to_tag('Finished')
    self.save_queue_file()
    return
  
  def mark_top_task_as_dropped(self):
    self.change_top_task_to_tag('Dropped')
    self.save_queue_file()
    return

  def postpone_top_task(self, priority):
    dom = self.get_queue_dom()
    top_node = self.get_top_node()
    if self.debug:
      print 'Reset top task with the priority of {0}'.format(priority)
    top_node.getElementsByTagName('Priority')[0].firstChild.data = str(priority)
    self.save_queue_file()
    return

  def get_tasks(self, filter_tuple, count):
    """ filter_tuple = (all, unfinished, finished, dropped) """
    queue_node = self.get_queue_node()
    task_nodes = []
    if filter_tuple[0] or filter_tuple[1] \
      or not filter_tuple[2] and not filter_tuple[3]:
      task_nodes = task_nodes + queue_node.getElementsByTagName('Unfinished')
    if filter_tuple[0] or filter_tuple[2]:
      task_nodes = task_nodes + queue_node.getElementsByTagName('Finished')
    if filter_tuple[0] or filter_tuple[3]:
      task_nodes = task_nodes + queue_node.getElementsByTagName('Dropped')
    heap = self.get_task_heap(task_nodes)
    tasks = []
    for element in reversed(heap):
      task_node = element[1]
      tasks.append(Task.parse_task(task_node))
    return tasks

  def select_queue(self, queue_name):
    """ Mark the queue with the name as the active queue """
    dom = self.get_queue_info_dom()
    try:
      dom.getElementsByTagName('Active')[0].tagName = 'Inactive'
    except IndexError:
      pass
    dest_queue_node = None
    for node in dom.getElementsByTagName('Name'):
      if node.firstChild.data == queue_name:
        dest_queue_node = node.parentNode
    if dest_queue_node is None:
      raise QueueNotFoundError('Cannot find the queue with the name "{0}"'
          .format(queue_name))
    dest_queue_node.tagName = 'Active'
    self.save_queue_info_file()
    return

  def create_queue(self, queue_name):
    dom = self.get_queue_info_dom()
    queue = Queue(queue_name, 'Inactive')
    dom.documentElement.appendChild(queue.to_xml_node(dom))
    self.save_queue_info_file()
    return

  def get_queues(self, filter_tuple):
    dom = self.get_queue_info_dom()
    queue_nodes = []
    if filter_tuple[0]:
      queue_nodes = dom.documentElement.getElementsByTagName('Active')
    elif filter_tuple[1]:
      queue_nodes = dom.documentElement.getElementsByTagName('Inactive')
    else:
      queue_nodes = dom.documentElement.childNodes
    return map(lambda queue_node: Queue.parse_queue(queue_node), queue_nodes)

  def delete_queue(self, queue_name):
    if queue_name == 'default':
      raise QueueNotFoundError('Default queue cannot be deleted')
    dom = self.get_queue_info_dom()
    dest_queue_node = None
    for node in dom.getElementsByTagName('Name'):
      if node.firstChild.data == queue_name:
        dest_queue_node = node.parentNode
    if dest_queue_node is None:
      raise QueueNotFoundError('Cannot find the queue with the name \
          "{0}"'.format(queue_name))
    dest_queue_node.parentNode.removeChild(dest_queue_node)
    self.save_queue_info_file()
    try:
      os.remove(self.get_queue_path(queue_name))
    except OSError:
      pass
    return

  def set_path(self, path):
    new_path = os.path.abspath(path)
    if not os.path.exists(new_path):
      os.makedirs(new_path)
    path_info_file_path = os.path.join(self.init_todoq_dir, 'path.info')
    try:
      path_info_file = open(path_info_file_path, 'r')
      prev_path = path_info_file.readlines()[0]
    except IOError:
      prev_path = init_todoq_dir
      pass
    if prev_path == new_path:
      return False
    path_info_file = open(path_info_file_path, 'w')
    path_info_file.write(new_path)
    path_info_file.close()
    for file_name in os.listdir(prev_path):
      if file_name == 'path.info':
        continue
      shutil.copy(os.path.join(prev_path, file_name), 
                  os.path.join(new_path, file_name))
      os.remove(os.path.join(prev_path, file_name))
    return True
