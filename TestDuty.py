import unittest

from Task import *
from Duty import *
from Piece import *

class TestDuty(unittest.TestCase):

    def test_registerTask(self):
        
        dty = Duty()

        taskToAdd = Task("TLVHAS-DVS-04", "Importer des champs UDs", "123456")
        dt1 = 7.0
        pce = Piece(taskToAdd, '2020-04-22 8:08:03.0', '2020-04-22 8:08:10.0')

        dty.addPiece(pce)

        self.assertEqual(len(dty.tasksRegistered), 1, \
                           "Length of task registered in duty should be 1.")     
        self.assertEqual(dty.tasksRegistered[0].completedTime, dt1, \
                           "Completed time should be equal")
        
        dt2 = 5.0
        pce2 = Piece(taskToAdd, '2020-04-22 8:08:10.0', '2020-04-22 8:08:15.0')
        dty.addPiece(pce2)
        self.assertEqual(len(dty.tasksRegistered), 1, \
                    "Length of task registered in duty should be 1.") 

        self.assertEqual(dty.tasksRegistered[0].completedTime, (dt1 + dt2))
        

        dt3 = 3.0
        taskToAdd2 = Task("TLVHAS-DVS-04", "Importer des champs UDs", "")
        pce3 = Piece(taskToAdd2, '2020-04-22 8:08:15.0', '2020-04-22 8:08:18.0')
        dty.addPiece(pce3)
        self.assertEqual(len(dty.tasksRegistered), 2)

        self.assertEqual(dty.tasksRegistered[1].completedTime, (dt3))

        dt4 = 3.0
        taskToAdd3 = Task("BRAHA19", "Fixer bug", "")
        pce4 = Piece(taskToAdd3, '2020-04-22 8:08:15.0', '2020-04-22 8:08:18.0')
        dty.addPiece(pce4)
        self.assertEqual(len(dty.tasksRegistered), 3)

        self.assertEqual(dty.tasksRegistered[0].completedTime, (dt1 + dt2))
        self.assertEqual(dty.tasksRegistered[1].completedTime, (dt3))
        self.assertEqual(dty.tasksRegistered[2].completedTime, (dt4))


if __name__ == '__main__':
    unittest.main()