""" The file contains the definition of class Task
"""
import time

TIME_FORMAT_STR = '%a, %d %b %Y %H:%M:%S'

class Task:
  """ The class to describe a task """

  @classmethod
  def parse_task(cls, task_node):
    """ create a task from xml node """
    name = task_node.getElementsByTagName('Name')[0].firstChild.data
    priority = int(task_node.getElementsByTagName('Priority')[0]
        .firstChild.data)
    status = task_node.nodeName
    return cls(name, priority, status)

  def __init__(self, name, priority, status):
    self.name = name
    self.priority = priority
    self.status = status

  def to_xml_node(self, dom):
    """ create a task xml node from task """
    task_node = dom.createElement(self.status)
    name_node = task_node.appendChild(dom.createElement('Name'))
    name_node.appendChild(dom.createTextNode(self.name))
    priority_node = task_node.appendChild(dom.createElement('Priority'))
    priority_node.appendChild(dom.createTextNode(str(self.priority)))
    create_time_node = task_node.appendChild(dom.createElement('CreateTime'))
    create_time_node.appendChild(dom.createTextNode(time.strftime(TIME_FORMAT_STR, time.localtime())))
    return task_node

  def to_str(self):
    """ print tasks """
    return '"{0}" {1} {2}'.format(self.name, self.priority, self.status)
