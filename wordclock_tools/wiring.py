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
        self.LED_COUNT   = self.WCA_WIDTH*self.WCA_HEIGHT # Number of LED pixels.
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
        
        self.WCA_GRID = [[0 for x in range(WCA_HEIGHT+1)] for x in range(self.WCA_WIDTH+1)] 
        self.WCA_GRID[0]=[99, 98, 77, 76, 55, 54, 33, 32, 11, 10]
        self.WCA_GRID[1]=[100, 97, 78, 75, 56, 53, 34, 31, 12, 9]
        self.WCA_GRID[2]=[101, 96, 79, 74, 57, 52, 35, 30, 13, 8]
        self.WCA_GRID[3]=[102, 95, 80, 73, 58, 51, 36, 29, 14, 7]
        self.WCA_GRID[4]=[103, 94, 81, 72, 59, 50, 37, 28, 15, 6]
        self.WCA_GRID[5]=[104, 93, 82, 71, 60, 49, 38, 27, 16, 5]
        self.WCA_GRID[6]=[105, 92, 83, 70, 61, 48, 39, 26, 17, 4]
        self.WCA_GRID[7]=[106, 91, 84, 69, 62, 47, 40, 25, 18, 3]
        self.WCA_GRID[8]=[107, 90, 85, 68, 63, 46, 41, 24, 19, 2]
        self.WCA_GRID[9]=[108, 89, 86, 67, 64, 45, 42, 23, 20, 1]
        self.WCA_GRID[10]=[109, 88, 87, 66, 65, 44, 43, 22, 21, 0]


    def getStripIndexFrom2D(self, x, y):
        '''
        Mapping coordinates to the wordclocks display
        Needs hardware/wiring dependent implementation
        Final range:
             (0,0): top-left
             (self.WCA_WIDTH-1, self.WCA_HEIGHT-1): bottom-right
        '''
        return self.WCA_GRID[y][x]

    def mapMinutes(self, min):
        '''
        Access minutes (1,2,3,4)
        Needs hardware/wiring dependent implementation
        This implementation assumes the minutes to be wired as first and last two leds of the led-strip
        '''
        
        if min == 1:
            return self.getStripIndexFrom2D(0, 10)
        elif min == 2:
            return self.getStripIndexFrom2D(1, 10)
        elif min == 3:
            return self.getStripIndexFrom2D(8, 10)
        elif min == 4:
            return self.getStripIndexFrom2D(9, 10)
        else:
            print('WARNING: Out of range, when mapping minutes...')
            print(min)
            return self.getStripIndexFrom2D(0, 10)
