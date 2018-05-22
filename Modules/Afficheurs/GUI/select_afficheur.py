# -*- coding: utf-8 -*-

"""
Module implementing Modification_afficheur.
"""

from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QStandardItemModel, QStandardItem 
from .Ui_select_afficheur import Ui_Modification_afficheur

from PyQt4.QtCore import SIGNAL

class Select_afficheur(QDialog, Ui_Modification_afficheur):
    """
    Class documentation goes here.
    """
    def __init__(self, afficheurs, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super(Select_afficheur, self).__init__(parent)
        self.setupUi(self)
        
         #insertion combobox
        
        self.comboBox.installEventFilter(self)
        model = QStandardItemModel()

        for i,word in enumerate(afficheurs):
            item = QStandardItem(word)
            model.setItem(i, 0, item)

        self.comboBox.setModel(model)
        self.comboBox.setModelColumn(0)
    
    @pyqtSlot()
    def on_okButton_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        afficheur = self.comboBox.currentText()
        self.emit(SIGNAL("fermetureselectafficheur(PyQt_PyObject)"), afficheur)
        self.close()
        return afficheur
    @pyqtSlot()
    def on_cancelButton_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.close()
