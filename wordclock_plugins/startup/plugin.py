import os
import wordclock_tools.wordclock_colors as wcc
import time

class plugin:
    '''
    A class to shutdown the RPI

    ..note:: This should be done before disconnecting the wordclock from its power supply.
    '''

    def __init__(self, config):
        '''
        Initializations for the startup of the current wordclock plugin
        '''
        # Get plugin name (according to the folder, it is contained in)
        self.name = os.path.dirname(__file__).split('/')[-1]

    def run(self, wcd, wci):
        '''
        Startup message wordclock
        Display... it is Lina o'clock
        '''
        indicies = [0,1,3,4,55,65,75,85,102,103,104,105,106,107]
        self.bg_color   = wcc.BLACK
        self.word_color = wcc.WWHITE
        self.rb_pos     = 0
        for x in range(0,300):
          if self.rb_pos < 85:
              self.word_color = self.minute_color = wcc.Color(3*self.rb_pos, 255-3*self.rb_pos, 0)
          elif self.rb_pos < 170:
              self.word_color = self.minute_color = wcc.Color(255-3*(self.rb_pos-85), 0, 3*(self.rb_pos-85))
          else:
              self.word_color = self.minute_color = wcc.Color(0, 3*(self.rb_pos-170), 255-3*(self.rb_pos-170))
          # END: Rainbow generation as done in rpi_ws281x strandtest example! Thanks to Tony DiCola for providing :)
          wcd.setColorBy1DCoordinates(wcd.strip, indicies, self.word_color)
          wcd.show()
          self.rb_pos += 1
          if self.rb_pos == 256: self.rb_pos = 0
          time.sleep(0.02)

        
        return
