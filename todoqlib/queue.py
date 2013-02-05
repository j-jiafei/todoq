from xml.dom.minidom import Document

class QueueNotFoundError(Exception):
  pass

class Queue:
  """ The class to describe a queue """
  @classmethod
  def parse_queue(cls, queue_node):
    """ parse a queue from queue_node """
    name = queue_node.getElementsByTagName('Name')[0].firstChild.data
    status = queue_node.tagName
    return cls(name, status)

  def __init__(self, name, status):
    self.name = name
    self.status = status

  def to_xml_node(self, dom):
    """ create a task xml node from queue """
    queue_node = dom.createElement(self.status)
    queue_node.appendChild(dom.createElement('Name')).appendChild(
        dom.createTextNode(self.name))
    return queue_node

  def to_str(self):
    """ print queue """
    return '"{0}" {1}'.format(self.name, self.status)
