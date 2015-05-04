import datetime as dt

class time_english():
    '''
    This class returns a given time as a range of LED-indices.
    Illuminating these LEDs represents the current time on an English WCA
    '''

    def __init__(self):
        self.prefix = range(0,1) +  range(3,4)
        self.minutes=[[], \
            #five past
            range(20,23) + range(45,49), \
            #ten past
            range(10,12) + range(45,49), \
            #quarter
            range(33,39) + range(45,49), \
            #twenty past
            range(25,29) + range(45,49), \
            #twentyfive past
            range(20,29) + range(45,49), \
            #half past
            range(13,16) + range(45,49), \
            #twentyfive to
            range(20,29) + range(30,31), \
            #twenty to
            range(25,29) + range(30,31), \
            #quarter to
            range(33,39) + range(30,31), \
            #ten to
            range(10,12) + range(30,31), \
            #five to
            range(20,23) + range(30,31) ]
        self.hours= [ \
            #twelve
            range(90,95)
            #one
            range(70,72), \
            #two
            range(60,62), \
            #three
            range(45,49), \
            #four
            range(50,53), \
            #five
            range(96,99), \
            #six
            range(77,79), \
            #seven
            range(80,84), \
            #eight
            range(64,68), \
            #nine
            range(86,89), \
            #ten
            range(73,75), \
            #eleven
            range(54,59), \
            #twelve
            range(90,95)]
        self.full_hour= range(102,107)

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

