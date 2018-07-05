# -*- coding: utf-8 -*-

"""
Module implementing Modification_Site_Client.
"""

from PyQt4.QtCore import pyqtSlot, pyqtSignal
from PyQt4.QtGui import QMainWindow, QMessageBox

from .Ui_Modification_Site_Client import Ui_Modification_Site_Client


class Modification_Site_Client(QMainWindow, Ui_Modification_Site_Client):
    """
    Class documentation goes here.
    """
    signalModif_Site_Client = pyqtSignal(dict)
    signalAjout_Site_Client = pyqtSignal(dict)
    
    signalModif_Service_Client = pyqtSignal(dict)
    signalAjout_Service_Client = pyqtSignal(dict)
    
    signalBesoinservices_efs = pyqtSignal()
    signalBesoinpostetech_efs = pyqtSignal()
    
#    signal_modification_ok = pyqtSignal()
    
    def __init__(self, Gui_parent, table_entite_client, table_site_client, table_services_client, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super().__init__(parent)
        self.setupUi(self)
        
        
        self.radioButton_modif.setChecked(True)
        self.on_radioButton_modif_clicked()
        
        # gestion communication entre les GUI
        self.GUI_parent = Gui_parent
        self.GUI_parent.signalMAJ_Site_Client.connect(self.maj_sites)
        self.GUI_parent.signalMAJ_Service_Client.connect(self.maj_service)
        self.GUI_parent.signal_mise_a_dispo_client_efs.connect(self.service_efs)
        self.GUI_parent.signal_mise_a_dispo_poste_tech_efs.connect(self.post_tech_efs)
        
        
        self.index_combobox_site= None
        
        self.lineEdit__client_code_p.setInputMask('99999')
        self.lineEdit__client_tel.setInputMask('+99_999_999999')
        self.lineEdit__client_fax.setInputMask('+99_999_999999')
        
        self.lineEdit_service_tel.setInputMask('+99_999_999999')
        self.lineEdit_service_fax.setInputMask('+99_999_999999')
        
        self.table_entite_client = table_entite_client.sort_values(by ="ID_ENT_CLIENT")
        self.table_site_client = table_site_client.sort_values(by = "ID_CLIENTS")
        self.table_services_client = table_services_client.sort_values(by = "ID_SERVICE")
#        print(self.table_site_client)
        self.comboBox_select_Site.addItems(self.table_site_client["CODE_CLIENT"].tolist())
        self.comboBox_select_Site.insertItem(0, "*")
        self.comboBox_select_Site.setCurrentIndex(0)
        
        self.comboBox_select_client.addItems(self.table_entite_client["ABREVIATION"].tolist())
        self.comboBox_select_client.insertItem(0, "*")
        self.comboBox_select_client.setCurrentIndex(0)
        #connexion signal click sur un service
        self.tableView_services.signalSelect_service.connect(self.reaffectation_service)
        

    @pyqtSlot(str)
    def on_comboBox_select_Site_currentIndexChanged(self, p0):
        """
        Slot documentation goes here.
        """
#        print(f"p0 {p0}")
        try:
            abreviation_site = self.comboBox_select_Site.currentText()
#            print(f"{abreviation_site}") 
#            print(self.table_site_client[self.table_site_client.CODE_CLIENT == abreviation_site].ID_ENT_CLIENT.values[0])
#            print(self.table_site_client[self.table_site_client.CODE_CLIENT == abreviation_site])
            try:
                id_siege = int(self.table_site_client[self.table_site_client.CODE_CLIENT == str(abreviation_site)].ID_ENT_CLIENT.values[0])
            except:
                id_siege = 0
            #gestion du siege
            if id_siege in self.table_entite_client["ID_ENT_CLIENT"].tolist():
                abreviation_siege = self.table_entite_client[self.table_entite_client.ID_ENT_CLIENT == id_siege].ABREVIATION.values[0]
                index = self.comboBox_select_client.findText(str(abreviation_siege))
                self.comboBox_select_client.setCurrentIndex(index)
            
            #gestion des services
            self.id_site = self.table_site_client[self.table_site_client.CODE_CLIENT == abreviation_site].ID_CLIENTS.values[0]
            
            service = self.table_services_client[self.table_services_client.ID_CLIENT == self.id_site]
            
            self.tableView_services.remplir(service)
            
            #Reaffectation des donnees:
            nom = str(self.table_site_client[self.table_site_client.CODE_CLIENT == abreviation_site].SOCIETE.values[0])
            self.lineEdit_client_nom.setText(nom)
            
            abrev = str(self.table_site_client[self.table_site_client.CODE_CLIENT == abreviation_site].CODE_CLIENT.values[0])
            self.lineEdit__client_abrev.setText(abrev)
            
            adresse = str(self.table_site_client[self.table_site_client.CODE_CLIENT == abreviation_site].ADRESSE.values[0])
            self.textEdit_client_adresse.setPlainText(adresse)
            
            code_p=str(self.table_site_client[self.table_site_client.CODE_CLIENT == abreviation_site].CODE_POSTAL.values[0])
            self.lineEdit__client_code_p.setText(code_p)
            
            ville = str(self.table_site_client[self.table_site_client.CODE_CLIENT == abreviation_site].VILLE.values[0])
            self.lineEdit__client_ville.setText(ville)
            
            tel = str(self.table_site_client[self.table_site_client.CODE_CLIENT == abreviation_site].TELEPHONE.values[0])
            self.lineEdit__client_tel.setText(tel)
            
            fax= str(self.table_site_client[self.table_site_client.CODE_CLIENT == abreviation_site].FAX.values[0])
            self.lineEdit__client_fax.setText(fax)
            
            courriel= str(self.table_site_client[self.table_site_client.CODE_CLIENT == abreviation_site].COURRIEL.values[0])
            self.lineEdit__client_courriel.setText(courriel)
            
            contact=str(self.table_site_client[self.table_site_client.CODE_CLIENT == abreviation_site].CONTACT.values[0])
            self.lineEdit__client_contact.setText(contact)
            
            prefixe_sap=str(self.table_site_client[self.table_site_client.CODE_CLIENT == abreviation_site].PREFIXE_POSTE_TECH_SAP.values[0])
            self.lineEdit_prefixe_sap.setText(prefixe_sap)
            
            if self.table_site_client[self.table_site_client.CODE_CLIENT == abreviation_site].ARCHIVAGE.values[0]:
                self.comboBox_archivage_service.setCurrentIndex(1)            
            else:
                self.comboBox_archivage_service.setCurrentIndex(0)
        
        except IndexError:
            self.lineEdit_prefixe_sap.clear()
            self.lineEdit_client_nom.clear()
            self.lineEdit__client_abrev.clear()
            self.textEdit_client_adresse.clear()
            self.lineEdit__client_code_p.clear()
            self.lineEdit__client_ville.clear()
            self.lineEdit__client_tel.clear()
            self.lineEdit__client_fax.clear()
            self.lineEdit__client_courriel.clear()
            self.lineEdit__client_contact.clear()
            
#            pass
        
    def reaffectation_service(self, ligne):       
        
#        print(self.table_services_client)
        self.id_service = self.table_services_client[self.table_services_client["ID_CLIENT"]== self.id_site].iloc[ligne]["ID_SERVICE"]

        
        service_select = self.table_services_client[self.table_services_client.ID_SERVICE == self.id_service]
        
        self.lineEdit_service_nom.setText(service_select.NOM.values[0])
        self.lineEdit_service_abrev.setText(service_select.ABREVIATION.values[0])        
        self.lineEdit_service_tel.setText(service_select.TELEPHONE.values[0])
        self.lineEdit_service_fax.setText(service_select.FAX.values[0])
        self.lineEdit_service_courriel.setText(service_select.COURRIEL.values[0])
        self.lineEdit_service_contact.setText(service_select.CONTACT.values[0])
        
        
        if service_select.ARCHIVAGE.values[0]:
            self.comboBox_archivage_service.setCurrentIndex(1)            
        else:
            self.comboBox_archivage_service.setCurrentIndex(0)
    
    @pyqtSlot()
    def on_pushButton_maj_service_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.comboBox_archivage_service.currentIndex()== 0:
            archivage = False
        else:
            archivage = True
        
        
        maj_service= {"ID_SERVICE" : self.id_service, 
                    "NOM":self.lineEdit_service_nom.text().upper(), 
                    "ABREVIATION":self.lineEdit_service_abrev.text().upper(), 
                    "TELEPHONE":self.lineEdit_service_tel.text(), 
                    "FAX":self.lineEdit_service_fax.text(), 
                    "COURRIEL":self.lineEdit_service_courriel.text(), 
                    "CONTACT":self.lineEdit_service_contact.text(), 
                    "ARCHIVAGE": archivage}
    
        self.signalModif_Service_Client.emit(maj_service)
        

    
    @pyqtSlot()
    def on_pushButton_ajoute_service_clicked(self):
        """
        Slot documentation goes here.
        """
        
        
        if self.comboBox_archivage_service.currentIndex()==0:
            archivage = False
        else:
            archivage = True
        
        
        abreviation_site = self.comboBox_select_Site.currentText()
        id_siege = self.table_site_client[self.table_site_client.CODE_CLIENT == abreviation_site].ID_ENT_CLIENT.values[0]
        id_site = self.table_site_client[self.table_site_client.CODE_CLIENT == abreviation_site].ID_CLIENTS.values[0]
        
        new_service= { "ID_CLIENT":int(id_site), 
                    "ID_ENTITE_CLIENT":int(id_siege), 
                    "NOM":self.lineEdit_service_nom.text().upper(), 
                    "ABREVIATION":self.lineEdit_service_abrev.text().upper(), 
                    "TELEPHONE":self.lineEdit_service_tel.text(), 
                    "FAX":self.lineEdit_service_fax.text(), 
                    "COURRIEL":self.lineEdit_service_courriel.text(), 
                    "CONTACT":self.lineEdit_service_contact.text(), 
                    "ARCHIVAGE": archivage}
        

        
        #emission du signal
        self.signalAjout_Service_Client.emit(new_service)
    
    @pyqtSlot()
    def on_pushButton_maj_site_clicked(self):
        """
        Slot documentation goes here.
        """
        
        if self.comboBox_archivage_service.currentIndex()==0:
            archivage = False
        else:
            archivage = True
        
        abreviation_site = self.comboBox_select_Site.currentText()
        abreviation_siege = self.comboBox_select_client.currentText()
        id_siege = int(self.table_entite_client[self.table_entite_client.ABREVIATION == abreviation_siege].ID_ENT_CLIENT.values[0])
        id_site = int(self.table_site_client[self.table_site_client.CODE_CLIENT == abreviation_site].ID_CLIENTS.values[0])
        
        maj_site= {"ID_CLIENTS":int(id_site), 
                    "ID_ENT_CLIENT" : int(id_siege), 
                    "SOCIETE":self.lineEdit_client_nom.text().upper(), 
                    "CODE_CLIENT":self.lineEdit__client_abrev.text().upper(),
                    "ADRESSE": self.textEdit_client_adresse.toPlainText(), 
                    "VILLE":self.lineEdit__client_ville.text().upper(), 
                    "CODE_POSTAL":self.lineEdit__client_code_p.text(), 
                    "TELEPHONE":self.lineEdit__client_tel.text(), 
                    "FAX":self.lineEdit__client_fax.text(), 
                    "COURRIEL":self.lineEdit__client_courriel.text(), 
                    "CONTACT":self.lineEdit__client_contact.text(), 
                    "ARCHIVAGE": archivage, 
                    "PREFIXE_POSTE_TECH_SAP":self.lineEdit_prefixe_sap.text()}
    
        self.signalModif_Site_Client.emit(maj_site)
    
        #mise à jour datatframe et du combobox se fait automatiquement par maj 
        self.index_combobox_site = self.comboBox_select_Site.currentIndex()
    
    
    @pyqtSlot()
    def on_pushButton_ajoute_site_clicked(self):
        """
        Slot documentation goes here.
        """
        self.index_combobox_site = None
        
        if self.comboBox_archivage_service.currentIndex()==0:
            archivage = False
        else:
            archivage = True
        
        
        abreviation_siege = self.comboBox_select_client.currentText()
        id_siege = int(self.table_entite_client[self.table_entite_client.ABREVIATION == abreviation_siege].ID_ENT_CLIENT.values[0])

#        id_site = int(self.table_site_client[self.table_site_client.CODE_CLIENT == abreviation_site].ID_CLIENTS.values[0])
        
        new_site= { "ID_ENT_CLIENT" : int(id_siege), 
                    "SOCIETE":self.lineEdit_client_nom.text().upper(), 
                    "CODE_CLIENT":self.lineEdit__client_abrev.text().upper(),
                    "ADRESSE": self.textEdit_client_adresse.toPlainText(), 
                    "VILLE":self.lineEdit__client_ville.text().upper(), 
                    "CODE_POSTAL":self.lineEdit__client_code_p.text(), 
                    "TELEPHONE":self.lineEdit__client_tel.text(), 
                    "FAX":self.lineEdit__client_fax.text(), 
                    "COURRIEL":self.lineEdit__client_courriel.text(), 
                    "CONTACT":self.lineEdit__client_contact.text(), 
                    "ARCHIVAGE": archivage , 
                    "PREFIXE_POSTE_TECH_SAP":self.lineEdit_prefixe_sap.text()}
    
        self.signalAjout_Site_Client.emit(new_site)
    
    def maj_sites(self, pandas_dataframe):
        
        self.table_site_client = pandas_dataframe.sort_values(by = "ID_CLIENTS")
        self.comboBox_select_Site.clear()        
        self.comboBox_select_Site.addItems(self.table_site_client["CODE_CLIENT"].tolist())
        
        if self.index_combobox_site:
            self.comboBox_select_Site.setCurrentIndex(self.index_combobox_site)
        else:
            self.comboBox_select_Site.setCurrentIndex(self.comboBox_select_Site.maxCount())
        
        self.index_combobox_site= None
    
    def maj_service(self, pandas_dataframe):
                #mise à jour du tableau et de la dataframe:
        
        self.table_services_client = pandas_dataframe.sort_values(by = "ID_SERVICE")

        abreviation_site = self.comboBox_select_Site.currentText()
        id_site = self.table_site_client[self.table_site_client.CODE_CLIENT == abreviation_site].ID_CLIENTS.values[0]        
        service = self.table_services_client[self.table_services_client.ID_CLIENT == id_site]        
        
        self.tableView_services.remplir(service)
        
        #nettoyage des lineedits:
        self.lineEdit_service_nom.clear()
        self.lineEdit_service_abrev.clear()
        self.lineEdit_service_tel.clear()
        self.lineEdit_service_fax.clear()
        self.lineEdit_service_courriel.clear()
        self.lineEdit_service_contact.clear()
    

    @pyqtSlot()
    def on_checkBox_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.checkBox.isChecked():
            self.comboBox_service_efs.setEnabled(True)
            
            self.signalBesoinservices_efs.emit()
        else:
            self.comboBox_service_efs.setEnabled(False)
            self.comboBox_service_efs.clear()
            
    def service_efs(self, list):        
        """fct qui met à jour le combobox suite à la reception du signal du mainadministration"""
        
        self.comboBox_service_efs.clear()
        self.comboBox_service_efs.addItems(list)
    
    @pyqtSlot(str)
    def on_comboBox_service_efs_currentIndexChanged(self, p0):
        """
        Slot documentation goes here.
        """
        nom_service = self.comboBox_service_efs.currentText()
        
        self.lineEdit_service_nom.setText(nom_service)
        self.lineEdit_service_tel.clear()
        self.lineEdit_service_fax.clear()
        self.lineEdit_service_courriel.clear()
        self.lineEdit_service_contact.clear()
        self.comboBox_archivage_service.setCurrentIndex(0)       
        
        
    
    @pyqtSlot()
    def on_checkBox_2_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.checkBox_2.isChecked():
            self.comboBox_poste_tech_sap_efs.setEnabled(True)
#            self.lineEdit_prefixe_sap.setEnabled(True)
            
            self.signalBesoinpostetech_efs.emit()
        else:
            self.comboBox_poste_tech_sap_efs.setEnabled(False)
#            self.lineEdit_prefixe_sap.setEnabled(False)
            self.comboBox_poste_tech_sap_efs.clear()
    
    @pyqtSlot(str)
    def on_comboBox_poste_tech_sap_efs_currentIndexChanged(self, p0):
        """
        Slot documentation goes here.
        """
        try:
#            print(self.post_tech)
            poste = self.comboBox_poste_tech_sap_efs.currentText()
            abreviation = [x[0] for x in self.post_tech if x[1] == poste][0]
            prefixe_sap = [x[2] for x in self.post_tech if x[1] == poste][0]
            
            self.lineEdit_client_nom.setText(poste)
            self.lineEdit__client_abrev.setText(abreviation)
            self.lineEdit_prefixe_sap.setText(prefixe_sap)
            
            reponse = QMessageBox.question(self, 
                    self.trUtf8("Information"), 
                    self.trUtf8("Voulez vous effacer les données precedentes"), 
                    QMessageBox.Yes, QMessageBox.No)
            if reponse == QMessageBox.Yes :
                self.textEdit_client_adresse.clear()
                self.lineEdit__client_code_p.clear()
                self.lineEdit__client_ville.clear()
                self.lineEdit__client_tel.clear()
                self.lineEdit__client_fax.clear()
                self.lineEdit__client_courriel.clear()
                self.lineEdit__client_contact.clear()
                
                
                self.comboBox_archivage.setCurrentIndex(0)
        
        except:
            pass
        
    def post_tech_efs(self, list):        
        """fct qui met à jour le combobox suite à la reception du signal du mainadministration"""
        self.post_tech = list
        self.comboBox_poste_tech_sap_efs.clear()
        self.comboBox_poste_tech_sap_efs.addItems([x[1] for x in list])
    
    @pyqtSlot()
    def on_radioButton_modif_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.radioButton_modif.isChecked():
            self.pushButton_maj_site.setEnabled(True)
            self.pushButton_ajoute_site.setEnabled(False)
            self.tab_2.setEnabled(True)
            self.comboBox_select_Site.setEnabled(True)
            self.checkBox_2.setEnabled(True)
#        else:
#            self.pushButton_ajoute_site.setEnabled(True)
#            self.tab_2.setEnabled(False)
    
    @pyqtSlot()
    def on_radioButton_creation_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.radioButton_creation.isChecked():
            self.pushButton_maj_site.setEnabled(False)
            self.pushButton_ajoute_site.setEnabled(True)
            self.tab_2.setEnabled(False)
            self.comboBox_select_Site.setEnabled(False)
            self.checkBox_2.setEnabled(False)
