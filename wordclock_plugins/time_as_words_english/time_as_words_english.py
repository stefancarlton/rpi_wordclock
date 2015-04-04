import datetime as dt

class time_as_words_english():
    '''
    This class returns a given time as words (string)::
    '''

    def __init__(self):
        self.prefix = "IT IS "
        self.minutes = ["",
            "FIVE PAST ", \
            "TEN PAST ", \
            "QUARTER PAST ", \
            "TWENTY PAST ", \
            "TWENTY FIVE PAST ", \
            "HALF PAST ", \
            "TWENTY FIVE TO ", \
            "TWENTY TO ", \
            "QUARTER TO ", \
            "TEN TO ", \
            "FIVE TO "]
        self.hours = ["TWELVE", \
            "ONE", \
            "TWO", \
            "THREE", \
            "FOUR", \
            "FIVE", \
            "SIX", \
            "SEVEN", \
            "EIGHT", \
            "NINE", \
            "TEN", \
            "ELEVEN", \
            "TWELVE"]
        self.full_hour_suffix = " O CLOCK"

    def get_time(self, time, withPrefix=True):
        hour=time.hour%12+(1 if time.minute/5 > 4 else 0)
        minute=time.minute/5
        # Assemble string
        return str( \
            (self.prefix if withPrefix else "") + \
            self.minutes[minute] + \
            self.hours[hour] + \
            # Append "S" to "EIN" (in case of "EIN UHR")
            ("S" if (hour == 1 and minute != 0) else "") + \
            (self.full_hour_suffix if (minute == 0) else "")) + " " + \
            ('*' * int(time.minute%5))

