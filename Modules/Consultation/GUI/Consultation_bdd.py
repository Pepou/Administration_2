# -*- coding: utf-8 -*-

"""
Module implementing Consultation_Bdd.
"""
from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QMainWindow
from Modules.Consultation.Package.AccesBdd import AccesBdd
from .Ui_Consultation_bdd import Ui_MainWindow


class Consultation_Bdd(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, engine, meta, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super().__init__(parent)
        self.setupUi(self)
        #bdd
        self.engine = engine
        self.meta = meta
        self.db = AccesBdd(engine, meta)
        
        nom_tables = self.db.nom_tables()
        self.comboBox_nom_tables.addItems (nom_tables)
    
    @pyqtSlot(str)
    def on_comboBox_nom_tables_activated(self, p0):
        """
        Slot documentation goes here.
        """ 
        # TODO: not implemented yet
                
        nom_table = self.comboBox_nom_tables.currentText()
        nom_colonnes = self.db.nom_colonnes(nom_table)
        donnees_table = self.db.recuperation_donnees_table(nom_table)
        
        #gestion du tableView
        self.tableWidget.clear()
        nbr_colonnes = len(nom_colonnes)
        nbr_lignes = len(donnees_table)
        self.tableWidget.setRowCount (nbr_lignes)
        self.tableWidget.setColumnCount(nbr_colonnes)
        self.tableWidget.setHorizontalHeaderLabels (nom_colonnes)
        
        for i in range(0, nbr_lignes):
            for j in range (0, nbr_colonnes):
                item = QtGui.QTableWidgetItem(str(donnees_table[i][j]))
                self.tableWidget.setItem(i, j, item)
        
    
    @pyqtSlot()
    def on_radioButton_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        if self.radioButton.isChecked():
            self.tableWidget.setSortingEnabled (True)
        else:
            self.tableWidget.setSortingEnabled (False)
