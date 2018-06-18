# -*- coding: utf-8 -*-

"""
Module implementing Cartographie.
"""

from PyQt4.QtCore import pyqtSlot, Qt,pyqtSignal
from PyQt4.QtGui import QMainWindow, QTableWidgetItem, QAbstractItemView, QMessageBox

from .Ui_Main_Carto import Ui_Cartographie
from Modules.Cartographie.GUI.Interface_Centrales import  Exploitation_Centrales
from Modules.Cartographie.GUI.Visu_Modif.Interface_Centrales_Visu_Modif import  Exploitation_Centrales_Visu_Modif
from Modules.Cartographie.GUI.Annule_Remplace.Interface_Centrales_Annule_Remplace import  Exploitation_Centrales_Annule_Remplace


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
        self.tableWidget_recap.annule_et_remplace.connect(self.carto_select_annule)
        self.tableWidget_recap.nouvelle.connect(self.on_actionNouvelle_Cartographie_triggered)
        
        self.tableWidget_recap.selectRow(0)
        
    def remplir_tableau_recap(self):
        """fct qui remplie le tableau apres avoir recuperer dans la bdd la table admin"""
        self.tableWidget_recap.setRowCount(0)
        list_tableau = self.carto_bdd.table_admin_entier()

        for ligne_a_remplir in reversed(list_tableau):
            self.tableWidget_recap.insertRow(0)
            colonne = 0
            for colonne_remplir in ligne_a_remplir:
                item = QTableWidgetItem(str(colonne_remplir))                
                self.tableWidget_recap.setItem(0, colonne, item)
                colonne += 1
    
    def carto_select(self, ligne):
        """fct appelee par le signal double click"""        
        n_ce = self.tableWidget_recap.item(ligne,4 ).text() 
        self.visu_modif_carto = Exploitation_Centrales_Visu_Modif(self.engine, n_ce)
        self.visu_modif_carto.fermeture.connect(self.remplir_tableau_recap)
        self.visu_modif_carto.showMaximized()
        
    def carto_select_annule(self, ligne):
        
        n_ce = self.tableWidget_recap.item(ligne,4 ).text()
        self.visu_annule_carto = Exploitation_Centrales_Annule_Remplace(self.engine, n_ce)
        self.visu_annule_carto.fermeture.connect(self.remplir_tableau_recap)
        self.visu_annule_carto.showMaximized()
        
    @pyqtSlot()
    def on_actionNouvelle_Cartographie_triggered(self):
        """
        Slot documentation goes here.
        """
        def gestion_signal_fermeture_ouverture():
            """fct qui permet de nettoyer et mettre a jour le tableau recap et de reouvrir une
            gui exploitation centrale pour une autre saisie"""
            
            self.tableWidget_recap.setRowCount(0)
            self.remplir_tableau_recap()
            self.on_actionNouvelle_Cartographie_triggered()
            
        self.new_carto = Exploitation_Centrales(self.engine)
        self.new_carto.fermeture_reouverture.connect(gestion_signal_fermeture_ouverture)
        self.new_carto.showMaximized()
    


    @pyqtSlot()
    def on_actionAnnule_et_Remplace_triggered(self):
        """
        Permet d'ouvrir la carto et de faire un annule et ramplce
        """
        ligne = self.tableWidget_recap.currentRow()
#        carto = self.tableWidget_recap.item(ligne, 4).text()
        res = QMessageBox.question(
                self,
                self.trUtf8("Seelction"),
                self.trUtf8(f"""Voulez vous faire un annule et remplace sur {self.tableWidget_recap.item(ligne, 4).text()}"""),
                QMessageBox.StandardButtons(
                    QMessageBox.No |
                    QMessageBox.Yes))
        if  res == QMessageBox.Yes:
            self.carto_select_annule(ligne)

    
    @pyqtSlot()
    def on_actionModifier_triggered(self):
        """permet d'ouvrir une carto et de la modifier si necessaire"""
        
        ligne = self.tableWidget_recap.currentRow()
#        carto = self.tableWidget_recap.item(ligne, 4).text()
        res = QMessageBox.question(
                self,
                self.trUtf8("Seelction"),
                self.trUtf8(f"""Voulez vous visualiser ou modifier {self.tableWidget_recap.item(ligne, 4).text()}"""),
                QMessageBox.StandardButtons(
                    QMessageBox.No |
                    QMessageBox.Yes))
        if  res == QMessageBox.Yes:
            self.carto_select(ligne)










