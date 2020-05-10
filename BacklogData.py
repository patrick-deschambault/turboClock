

from Task import *
from Piece import *
from Duty import *

from enum import Enum

class BacklogData:

     def __init__(self):
        
      self.tasks = list()

      self.currTask = Task("", "", "")

      self.currPiece = Piece("", "", "")

      self.currDuty = Duty()

      self.isTimerRunning = False

      self.timeTimerStart = ""

      self.timeTimerEnd = ""

      self.pathWeekData = ""

      self.filenameDutyData = ""

      self.pathTasksData = ""

      self.pathData = ""

      self.currDate = ""


        