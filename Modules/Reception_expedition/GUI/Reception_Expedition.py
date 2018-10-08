# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""
#import time
import datetime
from PyQt4.QtCore import pyqtSlot, QEvent
from PyQt4.QtGui import QMainWindow
from PyQt4.QtGui import QMessageBox
from PyQt4 import QtGui
#from PyQt4 import QtCore
from PyQt4.QtCore import * 
from PyQt4.QtGui import * 

import pendulum
import pandas as pd
#from PyQt4.QtGui import QStandardItemModel 

from Modules.Reception_expedition.GUI.Ui_Reception_Expedition import Ui_MainWindow
from Modules.Reception_expedition.Package.AccesBdd import AccesBdd
from Modules.Reception_expedition.Package.AccesBdd import Intervention
from Modules.Reception_expedition.BondeLivraison.GUI.BonLivraison import Bon_Livraison
from Modules.Reception_expedition.BondeReception.GUI.BonReception import Bon_Reception


class ReceptionExpedition(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self,engine,   parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super().__init__(parent)
        self.setupUi(self)
        
        self.lineEdit.tabPressed.connect(self.on_lineEdit_returnPressed)

        self.tableView.supprimerLigne.connect(self.suppression_intervention)
        
        self.engine = engine

        self.db = AccesBdd(self.engine)
        self.list_identification_instruments = self.db.identification_instrument()

        self.lineEdit.mise_a_jour_completerList(self.list_identification_instruments)

        self.interventions = Intervention(self.engine)
        
        ensemble_interventions = self.interventions.recuperation_interventions()
        ensemble_interventions.sort_values(by="DATE_INTERVENTION", ascending=False, inplace=True)
        
        annee_en_cour = pendulum.now('Europe/Paris').subtract(years = 1)
#        print(annee_en_cour)
#        print(type(ensemble_interventions["DATE_INTERVENTION"]))
#        
        ensemble_interventions["DATE_INTERVENTION"] = pd.to_datetime(ensemble_interventions["DATE_INTERVENTION"])
        self.tableView.remplir(ensemble_interventions[ensemble_interventions["DATE_INTERVENTION"]> annee_en_cour])
    
    


    @pyqtSlot()
    def on_pushButton_validation_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        instrument_saisi = self.lineEdit_identification_instrum.text()
        intervention = self.combobox_intervention.currentText()
        if (instrument_saisi in self.list_identification_instruments) != True:
            QMessageBox.information(self, 
                    self.trUtf8("Reception Expedition instruments"), 
                    self.trUtf8("L'instrument est inconnu \n merci d'en selectionner un autre"))
            self.lineEdit_identification_instrum.clear()
        else:
            
            self.tableWidget.insertRow(0)
            
            self.tableWidget.setItem(0, 0, QtGui.QTableWidgetItem(str(self.date_du_jour)))
            self.tableWidget.setItem(0, 1, QtGui.QTableWidgetItem(str(instrument_saisi)))
            
            code =self.db.return_code_intrument(instrument_saisi)
            self.tableWidget.setItem(0, 2, QtGui.QTableWidgetItem(str(code)))
            
            self.tableWidget.setItem(0, 3, QtGui.QTableWidgetItem(str(intervention)))
            
            self.tableWidget.setItem(0, 5, QtGui.QTableWidgetItem(str(self.date_prochaine)))
            
            self.lineEdit_identification_instrum.clear()
            
            

        
    @pyqtSlot()
    def on_buttonBox_accepted(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        reponse = QMessageBox.question(self, 
                    self.trUtf8("Information"), 
                    self.trUtf8("Voulez vous sauver ces interventions?"), 
                    QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        
            
        if reponse == QtGui.QMessageBox.Yes :
            nbr_ligne = self.tableWidget.rowCount()
#            print(nbr_ligne)
            
            list_interventions = []
            
            for i in range(nbr_ligne):
                try:
                    intervention = {}
                    intervention["CODE_CLIENT"] = self.tableWidget.item(i, 2).text()
                    intervention["IDENTIFICATION"] = self.tableWidget.item(i, 1).text()
                    intervention["INTERVENTION"] = self.tableWidget.item(i, 3).text()
                    intervention["DATE_INTERVENTION"] = self.tableWidget.item(i, 0).text()                    
                    intervention["COMMENTAIRE"] = self.tableWidget.item(i, 4).text()
                    intervention["DATE_PROCHAINE_INTERVENTION"] = self.tableWidget.item(i, 5).text()
                    intervention["LABORATOIRE"] = "EFS PAYS DE LA LOIRE SITE DU MANS"
                    list_interventions.append(intervention)
                except:
                    intervention["COMMENTAIRE"] = "RAS"
                    intervention["DATE_PROCHAINE_INTERVENTION"] = self.tableWidget.item(i, 5).text()
                    intervention["LABORATOIRE"] = "EFS PAYS DE LA LOIRE SITE DU MANS"
                    list_interventions.append(intervention)
                    
                
            self.db.insertion_table("INTERVENTIONS", list_interventions)
            i=0
            for i in range(nbr_ligne):
               self.tableWidget.removeRow(0)
               
            ensemble_interventions = self.interventions.recuperation_interventions()
        
#        self.tableView.clear()
            self.tableView.remplir(ensemble_interventions)

    
    @pyqtSlot()
    def on_buttonBox_rejected(self):
        """
        Slot documentation goes here.
        """

        nbr_ligne = self.tableWidget.rowCount()
        i=0
        for i in range(nbr_ligne):
            self.tableWidget.removeRow(0)

 
    @pyqtSlot()
    def on_pushButton_supp_clicked(self):
        """
        Button qui supprime la ligne ou un item est selectionné si pas de selection le bouton ne fait rien
        """
        
        ligne_selectionnee = self.tableWidget.selectionModel().currentIndex().row()
        self.tableWidget.removeRow(ligne_selectionnee)
    
    @pyqtSlot()
    def on_actionBon_de_Livaison_triggered(self):
        """
        Slot documentation goes here.
        """
        self.bon_livraison = Bon_Livraison(self.engine)
        self.bon_livraison.show()
        
    
    @pyqtSlot()
    def on_actionBon_de_Reception_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.bon_reception = Bon_Reception(self.engine)
        self.bon_reception.show()

    
    @pyqtSlot()
    def on_lineEdit_returnPressed(self):
        """
        Slot documentation goes here.
        """
#        print("on_lineEdit_returnPressed")
        instrument_saisi = self.lineEdit.text()

        intervention = self.combobox_intervention.currentText()
        if (instrument_saisi in self.list_identification_instruments) != True:
            QMessageBox.information(self, 
                    self.trUtf8("Reception Expedition instruments"), 
                    self.trUtf8("L'instrument est inconnu \n merci d'en selectionner un autre"))
           
        else:
            
            date_intervention = self.calendarWidget.selectedDate()
            french_date_intervention = date_intervention.toString('dd-MM-yyyy')
            
            periodicite = self.db.recuperation_periodicite_instrum(instrument_saisi,intervention)#self.spinBox_periodicite.value()
            
            if periodicite[1] == 'An(s)':
                date_prochaine = datetime.date((date_intervention.year() + periodicite[0]),date_intervention.month(), date_intervention.day())

            elif periodicite[1] == 'Mois':
                date_prochaine = datetime.date(date_intervention.year() , (date_intervention.month()+ periodicite[0]), date_intervention.day())
                
            french_date_prochaine = date_prochaine.strftime("%d-%m-%Y")

            self.tableWidget.insertRow(0)
            
            self.tableWidget.setItem(0, 0, QtGui.QTableWidgetItem(str(french_date_intervention)))
            self.tableWidget.setItem(0, 1, QtGui.QTableWidgetItem(str(instrument_saisi)))
            
            code =self.db.return_code_intrument(instrument_saisi)
            self.tableWidget.setItem(0, 2, QtGui.QTableWidgetItem(str(code)))
            
            self.tableWidget.setItem(0, 3, QtGui.QTableWidgetItem(str(intervention)))
            
            self.tableWidget.setItem(0, 5, QtGui.QTableWidgetItem(str(french_date_prochaine)))


        self.lineEdit.clear()

        

    def suppression_intervention(self, id):
        """fct qui appel la bdd pour supprimer la ligne de l'intervention selectionnée dans le tableau"""

        self.interventions.suppresion_intervention_by_id(id)
        
        ensemble_interventions = self.interventions.recuperation_interventions()

        self.tableView.remplir(ensemble_interventions)
        
    
