

from TaskGiro import *
from ProjectGiro import *
from TFSTask import *
from Piece import *
from Duty import *

class BacklogData:

     def __init__(self):
        
      self.projectGirolist = list()

      self.taskTFSGirolist = list()

      self.pieces = list()

      self.currDuty = Duty()

      self.currPiece = Piece('','','')

      self.currTFSTask = TFSTask('','','','')

      self.currProjectCode = ""

      self.currTaskCode = ""

      self.isTimerRunning = False




        