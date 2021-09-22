import time
import datetime

# Converts DMY to unix
class Convert():
    def __init__(self, start, end):
        self.start = start
        self.end = end
    
    def convert_time_to_unix(self):
        start_converted = int(time.mktime(datetime.datetime.strptime(self.start, "%d/%m/%Y").timetuple()))
        end_converted = int(time.mktime(datetime.datetime.strptime(self.end, "%d/%m/%Y").timetuple()))

        return start_converted, end_converted