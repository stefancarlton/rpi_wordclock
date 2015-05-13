import tornado.websocket
import string

class time_default_handler(tornado.websocket.WebSocketHandler)::

    def initialize(self, plugin):
      self.plugin = plugin
    
    def open(self):
      print 'connection opened...'
      self.write_message("Time default plugin socket listening")
    
    def on_message(self, message):
      action = message.split(':')
      if action[0] == 'setColorIndex':
        self.plugin.setColorsFromIndex(action[1])
        self.write_message("Setting colours from index")
      elif action == 'setColors':
        self.plugin.setColors(action[1], action[2], action[3])
        self.write_message("Setting colours from actual")
