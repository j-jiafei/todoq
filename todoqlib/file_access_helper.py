import os
from xml.dom.minidom import parse, Document, getDOMImplementation
import time
import heapq

time_format_str = '%a, %d %b %Y %H:%M:%S'

class FileAccessHelper:
  """ The helper class for data file saving, modifying and sync """
  def __init__(self, todoq_dir, debug = False):
    self.todoq_dir = todoq_dir
    if not os.path.exists(todoq_dir):
      os.makedirs(todoq_dir)
    self.queue_info_file = os.path.join(todoq_dir, 'queue.info')
    self.debug = debug
    self.queue_name = None
    self.queue_path = None
    self.queue_dom = None
    self.queue_node = None
  
  def set_debug(self, debug):
    self.debug = debug
    return

  def get_queue_name(self):
    """ Get the current queue """
    self.queue_name = 'default'
    return self.queue_name

  def get_queue_path(self, queue_name = None):
    queue_name = queue_name or self.queue_name or self.get_queue_name()
    self.queue_path = self.queue_path or \
        os.path.join(self.todoq_dir, '{0}.task'.format(queue_name))
    return self.queue_path

  def get_queue_dom(self, queue_path = None):
    """ Get the current queue dom """
    queue_path = queue_path or self.get_queue_path()
    if self.queue_dom:
      return self.queue_dom
    try:
      self.queue_dom = parse(self.queue_path)
    except IOError:
      self.queue_dom = getDOMImplementation().createDocument(None, 'Queue', None)
    return self.queue_dom

  def get_queue_node(self, queue_dom = None):
    queue_dom = queue_dom or self.get_queue_dom()
    self.queue_node = self.queue_node or queue_dom.documentElement or \
        queue_dom.appendChild(queue_dom.createElement('Queue'))
    return self.queue_node

  def save_file(self, queue_dom = None):
    """ The xml dom is stored to a temporary first, and then overwrite the initial file """
    queue_dom = queue_dom or self.get_queue_dom()
    tmp_queue_path = self.get_queue_path() + '.swap'
    tmp_queue_file = open(tmp_queue_path, 'w')
    tmp_queue_file.write(queue_dom.toxml())
    tmp_queue_file.close()
    os.rename(tmp_queue_path, self.get_queue_path())
    return

  def add_task(self, task_name, priority):
    """ Add the new task to the curr queue """
    if self.debug:
      print 'add new task {0} with priority {1} to queue {2}'.format(\
          task_name, priority, self.get_queue_name())
    queue_dom = self.get_queue_dom()
    queue_node = self.get_queue_node()
    task_node = queue_node.appendChild(queue_dom.createElement('Unfinished'))
    name_node = task_node.appendChild(queue_dom.createElement('Name'))
    name_node.appendChild(queue_dom.createTextNode(task_name))
    priority_node = task_node.appendChild(queue_dom.createElement('Priority'))
    priority_node.appendChild(queue_dom.createTextNode(str(priority)))
    create_time_node = task_node.appendChild(queue_dom.createElement('CreateTime'))
    create_time_node.appendChild(queue_dom.createTextNode(time.strftime(time_format_str, time.localtime())))
    self.save_file()
    return

  def get_task_heap(self, tasks):
    heap = []
    for task_node in tasks:
      priority = int(task_node.getElementsByTagName('Priority')[0].childNodes[0].data)
      heapq.heappush(heap, (priority, task_node))
    return heap

  def get_node_data(self, node, tag):
    return node.getElementsByTagName(tag)[0].childNodes[0].data

  def get_top_node(self):
    queue_dom = self.get_queue_dom()
    unfinished_tasks = queue_dom.getElementsByTagName('Unfinished')
    heap = self.get_task_heap(unfinished_tasks)
    top_node = heap[-1][1]
    return top_node

  def get_top_task(self):
    """ Return the the top task """
    top_node = self.get_top_node()
    return (self.get_node_data(top_node, 'Name'), int(self.get_node_data(top_node, 'Priority')))
  
  def change_top_task_to_tag(self, tag):
    queue_dom = self.get_queue_dom()
    top_node = self.get_top_node()
    if self.debug:
      print 'Mark top task {0} as {1}'.format(self.get_node_data(top_node, 'Name'), tag)
    task_node = queue_dom.createElement(tag)
    for child in top_node.childNodes:
      task_node.appendChild(child.cloneNode(True))
    self.get_queue_node().replaceChild(task_node, top_node)
    return
    
  def mark_top_task_as_finished(self):
    self.change_top_task_to_tag('Finished')
    self.save_file()
    return
  
  def mark_top_task_as_dropped(self):
    self.change_top_task_to_tag('Dropped')
    self.save_file()
    return
