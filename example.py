import sys

# Setting the Qt bindings for QtPy
import os
os.environ["QT_API"] = "pyqt5"

from PyQt5.QtCore import *
from PyQt5 import QtWidgets #figure out difference
#from qtpy import QtWidgets
from PyQt5.QtWidgets import QToolBar, QSlider, QFileDialog, QRadioButton, QPushButton


import numpy as np

import pyvista as pv
from pyvistaqt import QtInteractor, MainWindow

class MyMainWindow(MainWindow):

    def __init__(self, parent=None, show=True):
        QtWidgets.QMainWindow.__init__(self, parent)

        # variables
        self.show_edges = True

        # create the frame
        self.frame = QtWidgets.QFrame()
        vlayout = QtWidgets.QVBoxLayout()

        # add the pyvista interactor object
        self.plotter = QtInteractor(self.frame)
        vlayout.addWidget(self.plotter.interactor)
        self.signal_close.connect(self.plotter.close)

        # # add 2nd pyvista interactor object
        # self.plotter2 = QtInteractor(self.frame)
        # vlayout.addWidget(self.plotter2.interactor)
        # self.signal_close.connect(self.plotter2.close)

        self.frame.setLayout(vlayout)
        self.setCentralWidget(self.frame)

        # simple menu to demo functions
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        exitButton = QtWidgets.QAction('Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)
        addFileButton = QtWidgets.QAction('Add Mesh from File', self)
        addFileButton.setShortcut('Ctrl+A')
        addFileButton.triggered.connect(self.add_file)
        fileMenu.addAction(addFileButton)

        # allow adding a sphere
        meshMenu = mainMenu.addMenu('Mesh')
        self.add_sphere_action = QtWidgets.QAction('Add Sphere', self)
        self.add_sphere_action.triggered.connect(self.add_sphere)
        meshMenu.addAction(self.add_sphere_action)

        # allow disabling interactive camera
        self.disable_interactive_camera_action = QtWidgets.QAction('Disable Interactive Camera', self)
        self.disable_interactive_camera_action.triggered.connect(self.disable_interactive_camera)
        meshMenu.addAction(self.disable_interactive_camera_action)

        # allow enabling interactive camera
        self.enable_interactive_camera_action = QtWidgets.QAction('Enable Interactive Camera', self)
        self.enable_interactive_camera_action.triggered.connect(self.enable_interactive_camera)
        meshMenu.addAction(self.enable_interactive_camera_action)


        # add Toolbar
        self._createToolBars()

        if show:
            self.show()

    def add_file(self):
        """ add a file to read from """
        filename = QFileDialog.getOpenFileName(self, 'Open file', 
         '/home/batman/uni/CAP/visualization-code/examples', 'PLY files(*.ply)')
        if filename[0]:
            toBeplotted = pv.read(filename[0])
            self.plotter.clear()
            self.plotter.add_mesh(toBeplotted, show_edges=self.show_edges)
            self.plotter.reset_camera()


    def add_sphere(self):
        """ add a sphere to the pyqt frame """
        sphere = pv.Sphere()
        self.plotter.clear()
        self.plotter.add_mesh(sphere, show_edges=self.show_edges)
        # self.plotter2.clear()
        # self.plotter2.add_mesh(sphere, show_edges=self.show_edges)
        self.plotter.reset_camera()

    def disable_interactive_camera(self):
        """ disable the interactive camera of the plotter """
        self.plotter.disable()
        self.plotter.reset_camera()

    def enable_interactive_camera(self):
        """ enable the interactive camera of the plotter """
        self.plotter.enable()
        self.plotter.reset_camera()

    def _createToolBars(self):
        """ add toolbars to Frame """
        # Zoom toolbar
        zoomToolBar = QToolBar("Zoom", self)
        # settings for zoom
        self.zoomSlider = QSlider(Qt.Vertical)
        self.zoomSlider.setMinimum(1)
        self.zoomSlider.setMaximum(3)
        self.zoomSlider.setValue(1)
        self.zoomSlider.setTickPosition(QSlider.TicksRight)
        self.zoomSlider.setTickInterval(1)
        self.zoomSlider.setFocusPolicy(Qt.NoFocus)
        #add callbackfunction to slider
        self.zoomSlider.valueChanged.connect(self.changeZoom)
        #add WIdget to Toolbar
        zoomToolBar.addWidget(self.zoomSlider)

        generalToolBar = QToolBar("General", self)
        self.edgeToggle = QRadioButton("toggle edges")
        self.edgeToggle.setChecked(True)
        self.edgeToggle.toggled.connect(self.toggle_edge_display)

        self.resetCameraBtn = QPushButton("Reset Camera")
        self.resetCameraBtn.setCheckable(True)
        self.resetCameraBtn.clicked.connect(self.reset_camera)
        
        generalToolBar.addWidget(self.resetCameraBtn)
        generalToolBar.addWidget(self.edgeToggle)
        
        self.addToolBar(Qt.TopToolBarArea, generalToolBar)
        self.addToolBar(Qt.LeftToolBarArea, zoomToolBar)

    def changeZoom(self):
        zoom = self.zoomSlider.value()
        self.plotter.camera.zoom(zoom)

    def toggle_edge_display(self):
        self.show_edges = self.edgeToggle.isChecked()

    def reset_camera(self):
        self.plotter.reset_camera()





if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyMainWindow()
    sys.exit(app.exec_())