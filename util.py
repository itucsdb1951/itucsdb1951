
'''
Code retrieved from : https://exploreflask.com/en/latest/views.html#custom-converters
'''

from werkzeug.routing import BaseConverter

class ListConverter(BaseConverter):
  def to_python(self, value):
    return value.split(',')

  def to_url(self, values):
    return ','.join(BaseConverter.to_url(self, value) for value in values)