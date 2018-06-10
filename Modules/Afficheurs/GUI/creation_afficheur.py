# -*- coding: utf-8 -*-

"""
Module implementing Creation_afficheur.
"""

from PyQt4.QtCore import pyqtSlot, pyqtSignal
from PyQt4.QtGui import QDialog, QMessageBox
from PyQt4.QtCore import SIGNAL
from .Ui_creation_afficheur import Ui_Creation_afficheur


class Creation_afficheur(QDialog, Ui_Creation_afficheur):
    """
    Class documentation goes here.
    """
    
    
    signal_Creation_aff = pyqtSignal(dict)
    
    def __init__(self, code_client, constructeurs, service, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super(Creation_afficheur, self).__init__(parent)
        self.setupUi(self)
        
        #gestion combobox
        self.comboBox_code_client.addItems(code_client)
        self.comboBox_constructeur.addItems(constructeurs)
        self.comboBox_affectation.addItems(service)
        self.comboBox_designation_litterale.addItem("None")
        self.comboBox_ref_constructeur.addItem("None")
        #valeur par defaut resolution
        self.lineEdit_resolution.setText("0.1")
        self.lineEdit_nsap.setText("None")
        
    @pyqtSlot()
    def on_buttonBox_accepted(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        try:
            afficheur = {}
            if self.lineEdit_identification.text():
                afficheur["IDENTIFICATION"] = self.lineEdit_identification.text()
            else:
                raise ValueError
            afficheur["CODE"] = self.comboBox_code_client.currentText().upper()
            afficheur["DOMAINE_MESURE"] = self.comboBox_domaine_mesure.currentText()
            afficheur["FAMILLE"] = self.comboBox_famille.currentText().upper()
            afficheur["DESIGNATION"] = self.comboBox_designation.currentText()
            afficheur["TYPE"] = self.comboBox_type.currentText()
            afficheur["DESIGNATION_LITTERALE"] = self.comboBox_designation_litterale.currentText()
            afficheur["PARTICULARITE"] = "None"
            afficheur["CONSTRUCTEUR"] = self.comboBox_constructeur.currentText()
            afficheur["REFERENCE_CONSTRUCTEUR"] = self.comboBox_ref_constructeur.currentText()
            
            afficheur["RESOLUTION"] = float(self.lineEdit_resolution.text().replace(",", "."))
            afficheur["AFFECTATION"] = self.comboBox_affectation.currentText()
            afficheur["SOUS_AFFECTATION"] = self.textEdit_sous_affectation.toPlainText()
            afficheur["COMMENTAIRE"] = afficheur["SOUS_AFFECTATION"]
            afficheur["LOCALISATION"] = "None"
            afficheur["N_SERIE"] = self.lineEdit_nserie.text()
            afficheur["N_SAP_PM"] = self.lineEdit_nsap.text()
            afficheur["GESTIONNAIRE"] = "None"
            afficheur["STATUT"] = "Instrument de mesure"
            afficheur["PERIODICITE_QUANTITE"] = 12
            afficheur["PERIODICITE_UNITE"] = "Mois"
            afficheur["PROCEDURE"] = "None"
            afficheur["PRESTATAIRE"] = "EFS CENTRE PAYS DE LA LOIRE"
            afficheur["ETAT_UTILISATION"] = "En service"
            
            self.signal_Creation_aff.emit(afficheur)
            
            
            #clear
            self.lineEdit_identification.clear()
            self.comboBox_code_client.setCurrentIndex(0)
            self.comboBox_domaine_mesure.setCurrentIndex(0)
            self.comboBox_famille.setCurrentIndex(0)
            self.comboBox_designation.setCurrentIndex(0)
            self.comboBox_type.setCurrentIndex(0)
            self.comboBox_designation_litterale.setCurrentIndex(0)
            self.comboBox_constructeur.setCurrentIndex(0)
            self.lineEdit_resolution.setText(str(0.1))
            self.lineEdit_nserie.clear()
            self.lineEdit_nsap.setText("None")
        
        except ValueError:
            QMessageBox.warning(self, 
                        self.trUtf8("Attention"), 
                        self.trUtf8("Merci de remplir l'identification")) 
        
#        self.close()
        
    @pyqtSlot()
    def on_buttonBox_rejected(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.close()
    
    @pyqtSlot()
    def on_radioButton_automatique_clicked(self):
        """
        bloque le lineedit identification
        """
        # TODO: not implemented yet
        self.lineEdit_identification.setEnabled(False)
    
    @pyqtSlot()
    def on_radioButton_manuelle_clicked(self):
        """
        libere le lineedit identification
        """
        # TODO: not implemented yet
        self.lineEdit_identification.setEnabled(True)
