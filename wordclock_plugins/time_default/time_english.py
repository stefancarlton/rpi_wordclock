import datetime as dt

class time_english():
    '''
    This class returns a given time as a range of LED-indices.
    Illuminating these LEDs represents the current time on an English WCA
    '''

    def __init__(self):
        self.prefix = range(0,2) +  range(3,5)
        self.minutes=[[], \
            #five past
            range(26,30) + range(40,44), \
            #ten past
            range(17,20) + range(40,44), \
            #quarter
            range(30,37) + range(40,44), \
            #twenty past
            range(20,26) + range(40,44), \
            #twentyfive past
            range(20,30) + range(40,44), \
            #half past
            range(13,17) + range(40,44), \
            #twentyfive to
            range(20,30) + range(38,40), \
            #twenty to
            range(20,26) + range(38,40), \
            #quarter to
            range(30,37) + range(38,40), \
            #ten to
            range(17,20) + range(38,40), \
            #five to
            range(26,30) + range(38,40) ]
        self.hours= [ \
            #twelve
            range(90,96), \
            #one
            range(70,73), \
            #two
            range(60,63), \
            #three
            range(45,50), \
            #four
            range(50,54), \
            #five
            range(96,100), \
            #six
            range(77,80), \
            #seven
            range(80,85), \
            #eight
            range(64,69), \
            #nine
            range(86,90), \
            #ten
            range(73,76), \
            #eleven
            range(54,60), \
            #twelve
            range(90,96)]
        self.full_hour= range(102,108)

    def get_time(self, time, withPrefix=True):
        hour=time.hour%12+(1 if time.minute/5 > 4 else 0)
        minute=time.minute/5
        # Assemble indices
        return  \
            (self.prefix if withPrefix else []) + \
            self.minutes[minute] + \
            self.hours[hour] + \
            ([60] if (hour == 1 and minute != 0) else []) + \
            (self.full_hour if (minute == 0) else [])

