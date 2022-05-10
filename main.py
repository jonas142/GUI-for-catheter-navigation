from cProfile import label
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

def window():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(200, 200, 300, 300)
    win.setWindowTitle("Visualization")

    label = QtWidgets.QLabel(win)
    label.setText("The Model!")
    label.move(100,100)

    buttuon = QtWidgets.QPushButton(win)
    buttuon.move(100, 150)



    win.show()
    sys.exit(app.exec_())


window()