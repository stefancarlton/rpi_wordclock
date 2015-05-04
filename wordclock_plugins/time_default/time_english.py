import datetime as dt

class time_english():
    '''
    This class returns a given time as a range of LED-indices.
    Illuminating these LEDs represents the current time on an English WCA
    '''

    def __init__(self):
        self.prefix = range(0,2) +  range(3,6)
        self.minutes=[[], \
            #five past
            range(26,29) + range(40,43), \
            #ten past
            range(17,19) + range(40,43), \
            #quarter
            range(30,36) + range(40,43), \
            #twenty past
            range(20,25) + range(40,43), \
            #twentyfive past
            range(20,29) + range(40,43), \
            #half past
            range(13,16) + range(40,43), \
            #twentyfive to
            range(20,29) + range(38,39), \
            #twenty to
            range(20,25) + range(38,39), \
            #quarter to
            range(30,36) + range(38,39), \
            #ten to
            range(17,19) + range(38,39), \
            #five to
            range(26,29) + range(38,39) ]
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

