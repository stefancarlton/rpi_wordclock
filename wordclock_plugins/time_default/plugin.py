import datetime
import os
import time
import time_english
import wordclock_tools.wordclock_colors as wcc


class plugin(tornado.websocket.WebSocketHandler):
    '''
    A class to display the current time (default mode).
    This default mode needs to be adapted to the hardware
    layout of the wordclock (the choosen stancil) and is
    the most essential time display mode of the wordclock.
    '''

    def __init__(self, config):
      '''
      Initializations for the startup of the current wordclock plugin
      '''
      # Get plugin name (according to the folder, it is contained in)
      self.name = os.path.dirname(__file__).split('/')[-1]

      # Choose language
      self.taw = time_english.time_english()

      # Other color modes...
      self.color_modes = \
             [[wcc.BLACK, wcc.WWHITE, wcc.WWHITE],
              [wcc.BLACK, wcc.WHITE, wcc.WHITE],
              [wcc.BLACK, wcc.PINK, wcc.GREEN],
              [wcc.BLACK, wcc.RED, wcc.YELLOW],
              [wcc.BLACK, wcc.BLUE, wcc.RED],
              [wcc.BLACK, wcc.RED, wcc.BLUE],
              [wcc.YELLOW, wcc.RED, wcc.BLUE],
              [wcc.RED, wcc.BLUE, wcc.BLUE],
              [wcc.RED, wcc.WHITE, wcc.WHITE],
              [wcc.GREEN, wcc.YELLOW, wcc.PINK],
              [wcc.WWHITE, wcc.BLACK, wcc.BLACK],
              [wcc.BLACK, wcc.Color(30,30,30), wcc.Color(30,30,30)]]
        
      self.setColorsFromIndex(0)
      self.setIncTimePrefix(True)
        
      self.rb_pos = 0 # index position for "rainbow"-mode

    def getIndicies(self, time):
      '''
      Returns indices, which represent the current time, when illuminated
      '''
      return self.taw.get_time(time, self.inc_time_prefix)

  
    def setIncTimePrefix(self, inc_time_prefix):
      '''
      Sets the inclusion of the time prefix (IT IS)
      '''
      self.inc_time_prefix = inc_time_prefix
      self.setTime(self.wcd)
      
    def setColorsFromIndex(self, color_index):
      '''
      Set the colours to be used from the index
      '''
      self.setColors(self.color_modes[self.color_mode_pos][0], self.color_modes[self.color_mode_pos][1], self.color_modes[self.color_mode_pos][2])
        
    def setColors(self, bg_color, word_color, minute_color):
      '''
      set the colours by 
      '''
      self.bg_color     = bg_color
      self.word_color   = word_color
      self.minute_color = minute_color
      self.setDisplay(self.wcd)

    
    def setTime(self, wcd):
      '''
      sets the colours to the relevant pixels
      '''
      now = datetime.datetime.now()
      wcd.setColorBy1DCoordinates(wcd.strip, self.getIndicies(now), self.word_color)
      wcd.setMinutes(now, self.minute_color)
      
    def setDisplay(self, wcd):
      '''
      resets the display, sets the correct time
      '''
      wcd.setColorToAll(self.bg_color, includeMinutes=True)
      self.setTime(wcd)
      wcd.show()
		
    def run(self, wcd, wci):
      '''
      Displays time until aborted by user interaction on pin button_return
      '''
      while True:
        self.setDisplay(wcd)
        #@delay(2.0)
