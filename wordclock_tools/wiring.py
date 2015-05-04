import ast

class wiring:
    '''
    A class, holding all information of the wordclock's layout to map given
    timestamps, 2d-coordinates to the corresponding LEDs (corresponding to
    the individual wiring/layout of any wordclock).
    If a different wordclock wiring/layout is chosen, this class needs to be
    adopted.
    '''

    def __init__(self, config):

        # LED strip configuration:
        language=config.get('stancil_parameter', 'language')
        stancil_content  = ast.literal_eval(config.get('language_options', language))
        self.WCA_HEIGHT  = len(stancil_content)
        self.WCA_WIDTH   = len(stancil_content[0].decode('utf-8'))
        self.LED_COUNT   = self.WCA_WIDTH*self.WCA_HEIGHT+4 # Number of LED pixels.
        self.LED_PIN     = 18      # GPIO pin connected to the pixels (must support PWM!).
        self.LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
        self.LED_DMA     = 5       # DMA channel to use for generating signal (try 5)
        self.LED_INVERT  = False   # True to invert the signal (when using NPN transistor level shift)
        print('Wiring configuration')
        print('  WCA_WIDTH: ' + str(self.WCA_WIDTH))
        print('  WCA_HEIGHT: ' + str(self.WCA_HEIGHT))
        print('  Num of LEDs: ' + str(self.LED_COUNT))

        wiring_layout = config.get('wordclock_display', 'wiring_layout')
        self.wcl = english_wiring(self.WCA_WIDTH, self.WCA_HEIGHT)
        
    def setColorBy1DCoordinates(self, strip, ledCoordinates, color):
        '''
        Linear mapping from top-left to bottom right
        '''
        for i in ledCoordinates:
            self.setColorBy2DCoordinates(strip, i%self.WCA_WIDTH, i/self.WCA_WIDTH, color)

    def setColorBy2DCoordinates(self, strip, x, y, color):
        '''
        Mapping coordinates to the wordclocks display
        Needs hardware/wiring dependent implementation
        Final range:
             (0,0): top-left
             (self.WCA_WIDTH-1, self.WCA_HEIGHT-1): bottom-right
        '''
        strip.setPixelColor(self.wcl.getStripIndexFrom2D(x,y), color)
    def getStripIndexFrom2D(self, x,y):
        return self.wcl.getStripIndexFrom2D(x,y)

    def mapMinutes(self, min):
        '''
        Access minutes (1,2,3,4)
        '''
        return self.wcl.mapMinutes(min)

class english_wiring:
    '''
    A class, holding all information of the wordclock's layout to map given
    timestamps, 2d-coordinates to the corresponding LEDs (corresponding to
    the individual wiring/layout of any wordclock).
    If a different wordclock wiring/layout is chosen, this class needs to be
    adopted.
    '''

    def __init__(self, WCA_WIDTH, WCA_HEIGHT):
        self.WCA_WIDTH   = WCA_WIDTH
        self.WCA_HEIGHT  = WCA_HEIGHT

    def getStripIndexFrom2D(self, x, y):
        '''
        Mapping coordinates to the wordclocks display
        Needs hardware/wiring dependent implementation
        Final range:
             (0,0): top-left
             (self.WCA_WIDTH-1, self.WCA_HEIGHT-1): bottom-right
        '''
        if x%2 == 0:
            pos = (self.WCA_WIDTH-x-1)*self.WCA_HEIGHT+y+2
        else:
            pos = (self.WCA_WIDTH*self.WCA_HEIGHT)-(self.WCA_HEIGHT*x)-y+1
        return pos

    def mapMinutes(self, min):
        '''
        Access minutes (1,2,3,4)
        Needs hardware/wiring dependent implementation
        This implementation assumes the minutes to be wired as first and last two leds of the led-strip
        '''
        if min == 1:
            return 100
        elif min == 2:
            return 101
        elif min == 3:
            return 108
        elif min == 4:
            return 109
        else:
            print('WARNING: Out of range, when mapping minutes...')
            print(min)
            return 0