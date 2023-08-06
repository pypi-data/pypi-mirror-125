from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from pyrateshield.gui.main_controller import MainController
from pyrateshield.dosemapper import Dosemapper
from PyQt5.QtGui import QIcon
import os
import multiprocessing

_LICENCE_FILE = os.path.join(os.path.split(__file__)[0], 'LICENSE')


DISCLAIMER =\
("PyRateShield is free to use under the GNU GPLv3 license. The developers do "
 "not take any responsibility for any damages that might arise from using this"
 " software.\n\n\nUse at your own risk!")

with open (_LICENCE_FILE, "r") as file:
    LICENCE=''.join(file.readlines())

def showdialog():
   msg = QMessageBox()
   msg.setIcon(QtWidgets.QMessageBox.Information)

   msg.setText("Disclaimer!")
   msg.setInformativeText(DISCLAIMER)
   msg.setWindowTitle("Disclaimer")
   msg.setDetailedText(LICENCE)
   msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
   return msg
    
def main(*args):
    #QtWidgets.QApplication.setStyle("Windows")
    app = QtWidgets.QApplication([])    
    button =showdialog().exec()

    
    if button != QMessageBox.Ok:
        return

    with Dosemapper() as dm:
        
        icon = os.path.join(os.path.split(__file__)[0], 'gui', 'icon.png')
        app.setWindowIcon(QIcon(icon))     
        
        controller = MainController(dm)
        window = controller.view
        window.showMaximized()
        window.show()    
        
        app.exec_()
    return controller

if __name__ == "__main__":
    multiprocessing.freeze_support()
    controller = main()

