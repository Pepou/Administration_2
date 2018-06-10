# -*- coding: utf-8 -*-

"""
Module implementing Creation_afficheur.
"""

from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QDialog
from PyQt4.QtCore import SIGNAL
from .Ui_creation_afficheur import Ui_Creation_afficheur


class Modification_afficheur(QDialog, Ui_Creation_afficheur):
    """
    Class documentation goes here.
    """
    def __init__(self, afficheur, code_client, constructeurs, service,parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super(Modification_afficheur, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Modification Afficheur")
        
        self.id_afficheur = afficheur[0]
        
        self.comboBox_code_client.addItems(code_client)
        self.comboBox_constructeur.addItems(constructeurs)
        self.comboBox_affectation.addItems(service)
        self.comboBox_designation_litterale.addItem("None")
        self.comboBox_ref_constructeur.addItem("None")
        self.radioButton_manuelle.setChecked(True)
        
        print(afficheur)
        self.lineEdit_identification.setText(afficheur[1])
        
        #reaffectation combobox
        id_code_client = self.comboBox_code_client.findText(afficheur[2])
        self.comboBox_code_client.setCurrentIndex(id_code_client)
        
        id_domaine = self.comboBox_domaine_mesure.findText(afficheur[3])
        self.comboBox_domaine_mesure.setCurrentIndex(id_domaine)
        
        id_famille = self.comboBox_famille.findText(afficheur[4])
        self.comboBox_famille.setCurrentIndex(id_famille)
        
        id_designation = self.comboBox_designation.findText(afficheur[5])        
        self.comboBox_designation.setCurrentIndex(id_designation)
                
        id_type = self.comboBox_type.findText(afficheur[6])
        self.comboBox_type.setCurrentIndex(id_type)

        
        id_designation_litt = self.comboBox_designation_litterale.findText(afficheur[7])  
        if id_designation_litt == -1:
            self.comboBox_designation_litterale.addItem(afficheur[7])
            id_designation_litt = self.comboBox_designation_litterale.findText(afficheur[7])
            self.comboBox_designation_litterale.setCurrentIndex(id_designation_litt)
        else:
            self.comboBox_designation_litterale.setCurrentIndex(id_designation_litt)
            
        id_constructeur = self.comboBox_constructeur.findText(afficheur[8])
        self.comboBox_constructeur.setCurrentIndex(id_constructeur)
        
        id_ref_constructeur = self.comboBox_ref_constructeur.findText(afficheur[9])
        if id_ref_constructeur == -1:
            self.comboBox_ref_constructeur.addItem(afficheur[9])
            id_ref_constructeur = self.comboBox_ref_constructeur.findText(afficheur[9])
            self.comboBox_ref_constructeur.setCurrentIndex(id_ref_constructeur)
        else:
            self.comboBox_ref_constructeur.setCurrentIndex(id_ref_constructeur)

        
        
        self.lineEdit_resolution.setText(str(afficheur[11]))
        
        id_affectation = self.comboBox_affectation.findText(afficheur[12])
        self.comboBox_affectation.setCurrentIndex(id_affectation)
        
        self.textEdit_sous_affectation.setText(str(afficheur[13]))
        
        self.lineEdit_nserie.setText(str(afficheur[15]))
        
        self.lineEdit_nsap.setText(str(afficheur[16]))
        
    @pyqtSlot()
    def on_buttonBox_accepted(self):
        """
        Slot documentation goes here.
        """

        afficheur = {}
        afficheur["ID_INSTRUM"]= self.id_afficheur
        afficheur["IDENTIFICATION"] = self.lineEdit_identification.text()
        afficheur["CODE"] = self.comboBox_code_client.currentText()
        afficheur["DOMAINE_MESURE"] = self.comboBox_domaine_mesure.currentText()
        afficheur["FAMILLE"] = self.comboBox_famille.currentText().upper()
        afficheur["DESIGNATION"] = self.comboBox_designation.currentText()
        afficheur["TYPE"] = self.comboBox_type.currentText()
        afficheur["DESIGNATION_LITTERALE"] = self.comboBox_designation_litterale.currentText()
        afficheur["PARTICULARITE"] = "None"
        afficheur["CONSTRUCTEUR"] = self.comboBox_constructeur.currentText()
        afficheur["REFERENCE_CONSTRUCTEUR"] = self.comboBox_ref_constructeur.currentText()
        
        afficheur["RESOLUTION"] = self.lineEdit_resolution.text().replace(",", ".")
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
        afficheur["PRESTATAIRE"] = "EFS PAYS DE LA LOIRE SITE DU MANS"
        afficheur["ETAT_UTILISATION"] = "En service"
        
        self.emit(SIGNAL("fermeturemodifafficheur(PyQt_PyObject)"), afficheur)
        self.close()
        
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
