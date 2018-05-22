# -*- coding: utf-8 -*-

"""
Module implementing Graphique.
"""

from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QMainWindow

from .Ui_Affichage_graphique import Ui_Graphique


class Graphique(QMainWindow, Ui_Graphique):
    """
    Class documentation goes here.
    """
    def __init__(self, donnees, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super(Graphique, self).__init__(parent)
        self.setupUi(self)
        print(donnees)
        self.PlotFunc(donnees)
        
        
    @pyqtSlot()
    def on_buttonBox_accepted(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSlot()
    def on_buttonBox_rejected(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    def PlotFunc(self, valeurs):
#        randomNumbers = random.sample(range(0, 10), 10)
        
        
        self.graphique.canvas.ax.clear()
        self.graphique.canvas.ax.plot(valeurs)
        self.graphique.canvas.draw()
