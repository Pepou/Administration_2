# -*- coding: utf-8 -*-
"""
This example demonstrates the creation of a plot with a customized
AxisItem and ViewBox. 
"""
import sys

#import initExample ## Add path to library (just for examples; you do not need this)
from PyQt4.QtGui import QMainWindow
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
#import numpy as np
#import time
from datetime import datetime

class DateAxis(pg.AxisItem):
    def tickStrings(self, values, scale, spacing):
        print("values {}".format(values))
        strns = []
        for x in values:
            
            try:
                print("x {}".format(x))
                print(str(datetime.utcfromtimestamp(x).time()))
                strns.append(datetime.utcfromtimestamp(x).time())

            except ValueError:  ## Windows can't handle dates before 1970
                strns.append('')

        return strns

class CustomViewBox(pg.ViewBox):
    def __init__(self, *args, **kwds):
        pg.ViewBox.__init__(self, *args, **kwds)
        self.setMouseMode(self.RectMode)
        
    ## reimplement right-click to zoom out
    def mouseClickEvent(self, ev):
        if ev.button() == QtCore.Qt.RightButton:
            self.autoRange()
            
    def mouseDragEvent(self, ev):
        if ev.button() == QtCore.Qt.RightButton:
            ev.ignore()
        else:
            pg.ViewBox.mouseDragEvent(self, ev)

class test_graphique(QMainWindow):
    def __init__(self, parent=None):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()
#            pg.mkQApp()
            super().__init__(parent)

            axis = DateAxis(orientation='bottom')

            
            pw = pg.PlotWidget(axisItems={'bottom': axis}, enableMenu=True, title="Donnees Etalon")
            dates = [35757, 35817, 35877, 35937, 35997, 36057, 36117, 36177, 36237, 36297]
            print("dates {}".format(dates))
            pw.plot(x = dates, y=[-0.002, -0.003, -0.0018, -0.0016, -0.0018, -0.002, -0.002, -0.002, -0.0014, -0.001], symbol='o')
#            pw.show()
            pw.setWindowTitle('Donnees')


## Start Qt event loop unless running in interactive mode or using pyside.
#if __name__ == '__main__':
#    import sys
#    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
#        QtGui.QApplication.instance().exec_()
