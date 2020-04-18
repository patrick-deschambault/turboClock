

from TFSTask import *
from ProjectGiro import *
from TaskGiro import *

class InputDataMgr():

    def __init__(self):

        self.currentTFSTask = TFSTask('','','','')
        self.currentProjectCode = ProjectGiro()
        self.currentTaskCode = TaskGiro()
    

