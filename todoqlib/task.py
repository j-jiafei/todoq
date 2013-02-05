""" The file contains the definition of class Task
"""

from xml.dom.minidom import Document

class Task:
  """ The class to describe a task """

  @classmethod
  def parse_task(cls, task_node):
    """ create a task from xml node """
    name = task_node.getElementsByTagName('Name')[0].childNodes[0].data
    priority = int(task_node.getElementsByTagName('Priority')[0]
        .childNodes[0].data)
    status = task_node.nodeName
    return cls(name, priority, status)

  def __init__(self, name, priority, status):
    self.name = name
    self.priority = priority
    self.status = status

  def to_xml_node(self, dom):
    """ create a task xml node from task """
    return

  def to_str(self):
    """ print tasks """
    return '"{0}" {1} {2}'.format(self.name, self.priority, self.status)
