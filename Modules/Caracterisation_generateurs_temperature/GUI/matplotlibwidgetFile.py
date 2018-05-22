from PyQt4 import QtGui
from matplotlib.backends.backend_qt4agg import (FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
import matplotlib.dates as dates

from matplotlib.figure import Figure
#from matplotlib.widgets import Cursor

class MplCanvas(FigureCanvas):
 
    def __init__(self):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        
#        self.fig.canvas.mpl_connect('button_press_event', self.onclick)
#        self.fig.canvas.mpl_connect('button_release_event', self.onclick)
        

    def nom_graphique(self, titre):        

        self.ax.set_title(titre)
 
#    def onclick(self, event):
#        print("coucou")
#        print("values x : {}  y :{}".format(dates.num2date(event.xdata), event.ydata))

class matplotlibWidget(QtGui.QWidget):
 
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.canvas = MplCanvas()
        self.vbl = QtGui.QVBoxLayout()
        self.vbl.addWidget(self.canvas)
        
        self.vbl.addWidget(NavigationToolbar(self.canvas,self))
        self.setLayout(self.vbl)
    
    
