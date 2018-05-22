# -*- coding: utf-8 -*-

"""
Module implementing Cartographie.
"""

from PyQt4.QtCore import pyqtSlot, Qt,pyqtSignal
from PyQt4.QtGui import QMainWindow, QTableWidgetItem, QAbstractItemView

from .Ui_Main_Carto import Ui_Cartographie
from Modules.Cartographie.GUI.Interface_Centrales import  Exploitation_Centrales
from Modules.Cartographie.GUI.Visu_Modif.Interface_Centrales_Visu_Modif import  Exploitation_Centrales_Visu_Modif
from Modules.Cartographie.Package.AccesBdd import AccesBdd, Carto_BDD


class Cartographie(QMainWindow, Ui_Cartographie):
    """
    Class documentation goes here.
    """
    def __init__(self, engine, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super().__init__(parent)
        self.setupUi(self)
        self.engine = engine
        
        self.carto_bdd = Carto_BDD(self.engine)
#        carto_bdd.table_admin_entier()
        self.remplir_tableau_recap()
        self.tableWidget_recap.ligne_clic.connect(self.carto_select)
        
    def remplir_tableau_recap(self):
        """fct qui remplie le tableau apres avoir recuperer dans la bdd la table admin"""
        list_tableau = self.carto_bdd.table_admin_entier()

        for ligne_a_remplir in reversed(list_tableau):
            self.tableWidget_recap.insertRow(0)
            colonne = 0
            for colonne_remplir in ligne_a_remplir:
                item = QTableWidgetItem(str(colonne_remplir))                
                self.tableWidget_recap.setItem(0, colonne, item)
                colonne += 1
    
    def carto_select(self, ligne):
        
        n_ce = self.tableWidget_recap.item(ligne,4 ).text()
        
        
        self.visu_modif_carto = Exploitation_Centrales_Visu_Modif(self.engine, n_ce)
        self.visu_modif_carto.showMaximized()
        
    @pyqtSlot()
    def on_actionNouvelle_Cartographie_triggered(self):
        """
        Slot documentation goes here.
        """
        self.new_carto = Exploitation_Centrales(self.engine)
        self.new_carto.showMaximized()
    
    @pyqtSlot()
    def on_actionModifier_une_cartographie_triggered(self):
        """
        Slot documentation goes here.
        """
        items = self.tableWidget_recap.findItems("RICHER", Qt.MatchContains)#Qt::MatchContains
        # Temporarily set MultiSelection
        self.tableWidget_recap.setSelectionMode(QAbstractItemView.MultiSelection)
        for ele in items:
            print(ele.row())
            print(ele.column())
            self.tableWidget_recap.selectRow(ele.row())
            
        # Revert MultiSelection to ExtendedSelection
        self.tableWidget_recap.setSelectionMode(QAbstractItemView.ExtendedSelection)
#        print(items.row)


    @pyqtSlot()
    def on_actionAnnule_et_Remplace_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
