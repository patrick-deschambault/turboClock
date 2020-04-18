import datetime
from datetime import timedelta

class Piece():

    def __init__(self, iTFSTask, iStartDateTime, iEndDateTime):

        self.tfsTask = iTFSTask

        self.datetimeFormat = '%Y-%m-%d %H:%M:%S.%f'
        self.startDateTime = iStartDateTime
        self.endDateTime = iEndDateTime

        self.deltaTime = 0
        self.computeDeltaTime()
        
    def setStartTime(self, iStartDateTime):

        self.startDateTime = iStartDateTime

    def setEndTime(self, iEndDateTime):

        self.endDateTime = iEndDateTime

    def computeDeltaTime(self):

        if self.endDateTime != '' and self.startDateTime != '':

            self.deltaTime = (datetime.datetime.strptime(str(self.endDateTime), self.datetimeFormat) \
                           - datetime.datetime.strptime(str(self.startDateTime), self.datetimeFormat) ).total_seconds()


    
