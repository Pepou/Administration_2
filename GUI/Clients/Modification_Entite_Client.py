# -*- coding: utf-8 -*-

"""
Module implementing Modification_Entite_Client.
"""

from PyQt4.QtCore import pyqtSlot, pyqtSignal
from PyQt4.QtGui import QMainWindow

from .Ui_Modification_Entite_Client import Ui_Modification_Entite_Client


class Modification_Entite_Client(QMainWindow, Ui_Modification_Entite_Client):
    """
    Class documentation goes here.
    """
    signalModif_Entite_Client = pyqtSignal(dict)
    
    def __init__(self, table_entite_client, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super().__init__(parent)
        self.setupUi(self)
        
        self.lineEdit__client_tel.setInputMask('+99_999_999999')
        self.lineEdit__client_fax.setInputMask('+99_999_999999')
        self.lineEdit__client_code_p.setInputMask('99999')

        self.table_entite_client = table_entite_client.sort_values(by="ID_ENT_CLIENT")

        
        self.comboBox_select_client.addItems(self.table_entite_client["ABREVIATION"].tolist())
        
    @pyqtSlot()
    def on_actionSauvegarder_triggered(self):
        """
        Slot documentation goes here.
        """
        abreviation= self.comboBox_select_client.currentText()
        id = self.table_entite_client[self.table_entite_client.ABREVIATION == abreviation].ID_ENT_CLIENT.values[0]
        
#        print(f"l'id du client est {id}")
        if self.comboBox_archivage.currentIndex()==0:
            archivage = False
            
        else:
            archivage = True
        
        mise_a_jour_ent = {"ID":id, 
                            "NOM":self.lineEdit_client_nom.text(), 
                            "ABREVIATION": self.lineEdit__client_abrev.text(), 
                            "ADRESSE": self.textEdit_client_adresse.toPlainText(), 
                            "CODE_POSTAL": self.lineEdit__client_code_p.text(), 
                            "VILLE": self.lineEdit__client_ville.text(), 
                            "TELEPHONE": self.lineEdit__client_tel.text(), 
                            "FAX":self.lineEdit__client_fax.text(), 
                            "COURRIEL":self.lineEdit__client_courriel.text(), 
                            "CONTACT":self.lineEdit__client_contact.text(), 
                            "ARCHIVAGE":archivage}
    
    
        self.signalModif_Entite_Client.emit(mise_a_jour_ent)
        self.close()
    
    @pyqtSlot(int)
    def on_comboBox_select_client_currentIndexChanged(self, index):
        """
        Slot documentation goes here.
        """
        abreviation= self.comboBox_select_client.currentText()
        
        nom = self.table_entite_client[self.table_entite_client.ABREVIATION == abreviation].NOM.values[0]
        adresse =  self.table_entite_client[self.table_entite_client.ABREVIATION == abreviation].ADRESSE.values[0]
        code_postal =  self.table_entite_client[self.table_entite_client.ABREVIATION == abreviation].CODE_POSTAL.values[0]
        
        ville = self.table_entite_client[self.table_entite_client.ABREVIATION == abreviation].VILLE.values[0]
        tel = self.table_entite_client[self.table_entite_client.ABREVIATION == abreviation].TELEPHONE.values[0]
        
        fax = self.table_entite_client[self.table_entite_client.ABREVIATION == abreviation].TELEPHONE.values[0]
        courriel = self.table_entite_client[self.table_entite_client.ABREVIATION == abreviation].COURRIEL.values[0]
        contact = self.table_entite_client[self.table_entite_client.ABREVIATION == abreviation].CONTACT.values[0]
        
        
        if not self.table_entite_client[self.table_entite_client.ABREVIATION == abreviation].ARCHIVAGE.values[0]:        
            self.comboBox_archivage.setCurrentIndex(0)
        else:
            self.comboBox_archivage.setCurrentIndex(1)
        
        self.lineEdit_client_nom.setText(nom)
        self.lineEdit__client_abrev.setText(abreviation)
        self.textEdit_client_adresse.setPlainText(adresse)
        self.lineEdit__client_code_p.setText(code_postal)
        self.lineEdit__client_ville.setText(ville)
        self.lineEdit__client_tel.setText(tel)        
        self.lineEdit__client_fax.setText(fax)
        self.lineEdit__client_courriel.setText(courriel)        
        self.lineEdit__client_contact.setText(contact)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
