import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template

class MainHandler(tornado.web.RequestHandler):
  def get(self):
    loader = tornado.template.Loader(".")
    self.write(loader.load("index.html").generate())

class WSHandler(tornado.websocket.WebSocketHandler):
  def open(self):
    print 'connection opened...'
    self.write_message("The server says: 'Hello'. Connection was accepted.")

  def on_message(self, message):
    self.message = message
    self.message_received = true
    self.time_default.setColorsFromIndex(message)
#    self.write_message("The server says: " + message + " back at you")
#    print 'received:', message

  def on_close(self):
    print 'connection closed...'
    
  def set_time_default(self, time_default):
    self.time_default = time_default
