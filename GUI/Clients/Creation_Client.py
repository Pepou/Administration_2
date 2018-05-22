# -*- coding: utf-8 -*-

"""
Module implementing Creation_Client.
"""

from PyQt4.QtCore import pyqtSlot, pyqtSignal
from PyQt4.QtGui import QMainWindow, QTableWidgetItem, QTextEdit, QMessageBox

from .Ui_Creation_Client import Ui_Creation_Client


class Creation_Client(QMainWindow, Ui_Creation_Client):
    """
    Class documentation goes here.
    """
    signalNewclient = pyqtSignal(dict)
    signalBesoinservices_efs = pyqtSignal()
    signalBesoinpostetech_efs = pyqtSignal()
    
    def __init__(self, Gui_parent,  parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super().__init__(parent)
        self.setupUi(self)
        
        
        # gestion communication entre les GUI
        self.GUI_parent = Gui_parent
        self.GUI_parent.signal_mise_a_dispo_client_efs.connect(self.service_efs)
        self.GUI_parent.signal_mise_a_dispo_poste_tech_efs.connect(self.post_tech_efs)
        
        
        
        self.lineEdit__client_tel.setInputMask('+99_999_999999')
        self.lineEdit__client_fax.setInputMask('+99_999_999999')
        self.lineEdit__client_code_p.setInputMask('99999')
#        self.lineEdit__client_courriel.setInputMask('a@xxxxxxxxxxxxxxxxxxxxxxxxxxx')
        
        self.lineEdit__site_code_p.setInputMask('99999')
        self.lineEdit__site_tel.setInputMask('+99_999_999999')
        self.lineEdit__site_fax.setInputMask('+99_999_999999')
        
        self.lineEdit_service_tel.setInputMask('+99_999_999999')
        self.lineEdit_service_fax.setInputMask('+99_999_999999')
        
        self.tableWidget__site_recap.signalSelect_site.connect(self.reaffectation_site)
        self.tableWidget__recap_service.signalSelect_site.connect(self.reaffectation_service)
        
        self.pushButton_maj.hide()
        self.pushButton_service_maj.hide()
        
    @pyqtSlot()
    def on_pushButton_service_ajouter_clicked(self):
        """
        Slot documentation goes here.
        """
        nom_site = self.comboBox_sites.currentText()
        
        if nom_site != "*":
            nom_service = self.lineEdit_service_nom.text().upper()
            abrevitaion = self.lineEdit_service_abrev.text().upper()        
            telephone = self.lineEdit_service_tel.text()
            fax = self.lineEdit_service_fax.text()
            courriel = self.lineEdit_service_courriel.text()
            contact = self.lineEdit_service_contact.text()
            
            nbr_service = self.tableWidget__recap_service.rowCount()
            self.tableWidget__recap_service.insertRow(nbr_service)
            
            self.tableWidget__recap_service.setItem(nbr_service, 0, QTableWidgetItem(nom_site))
            self.tableWidget__recap_service.setItem(nbr_service, 1, QTableWidgetItem(nom_service))
            self.tableWidget__recap_service.setItem(nbr_service, 2, QTableWidgetItem(abrevitaion))
            self.tableWidget__recap_service.setItem(nbr_service, 3, QTableWidgetItem(telephone))
            self.tableWidget__recap_service.setItem(nbr_service, 4, QTableWidgetItem(fax))
            self.tableWidget__recap_service.setItem(nbr_service, 5, QTableWidgetItem(courriel))
            self.tableWidget__recap_service.setItem(nbr_service, 6, QTableWidgetItem(contact))
            
            #nettoyage
            gen_line_edit = iter([self.lineEdit_service_nom, self.lineEdit_service_abrev,        
                                    self.lineEdit_service_tel, self.lineEdit_service_fax, 
                                    self.lineEdit_service_courriel, self.lineEdit_service_contact])
            for ele in gen_line_edit:
                ele.clear()
            
    @pyqtSlot()
    def on_pushButton_sites_ajouter_clicked(self):
        """
        Slot documentation goes here.
        """
        self.ligne_site_select = -1

        self.pushButton_maj.hide()
    
        nom_site = self.lineEdit__site_nom.text().upper()
        abreviation = self.lineEdit__site_abrev.text().upper()
        adresse = self.textEdit___site_adresse.toPlainText().capitalize()
        code_post = self.lineEdit__site_code_p.text()
        ville = self.lineEdit__site_ville.text().upper()
        telephone = self.lineEdit__site_tel.text()
        fax = self.lineEdit__site_fax.text()
        courriel = self.lineEdit__site_courriel.text()
        contact = self.lineEdit__site_contact.text()
        prefixe_sap = self.lineEdit_prefixe_sap.text()
        
        nbr_site = self.tableWidget__site_recap.rowCount()
        self.tableWidget__site_recap.insertRow(nbr_site)
        
        self.tableWidget__site_recap.setItem(nbr_site, 0, QTableWidgetItem(nom_site))
        self.tableWidget__site_recap.setItem(nbr_site, 1, QTableWidgetItem(abreviation))
        
        text_edit = QTextEdit(self.tableWidget__site_recap)
        self.tableWidget__site_recap.setCellWidget(nbr_site,2,  text_edit)
        text_edit.setPlainText(adresse)
        
        
        
        self.tableWidget__site_recap.setItem(nbr_site, 3, QTableWidgetItem(code_post))
        self.tableWidget__site_recap.setItem(nbr_site, 4, QTableWidgetItem(ville))
        self.tableWidget__site_recap.setItem(nbr_site, 5, QTableWidgetItem(telephone))
        self.tableWidget__site_recap.setItem(nbr_site, 6, QTableWidgetItem(fax))

        self.tableWidget__site_recap.setItem(nbr_site, 7, QTableWidgetItem(courriel))
        self.tableWidget__site_recap.setItem(nbr_site, 8, QTableWidgetItem(contact))
        self.tableWidget__site_recap.setItem(nbr_site, 9, QTableWidgetItem(prefixe_sap))

        #nettoyage
        gen_line_edit = iter([self.lineEdit__site_nom, self.lineEdit__site_abrev,        
                                    self.textEdit___site_adresse, self.lineEdit__site_code_p, 
                                    self.lineEdit__site_ville, self.lineEdit__site_tel, 
                                    self.lineEdit__site_fax, self.lineEdit__site_courriel, 
                                    self.lineEdit__site_contact,self.lineEdit_prefixe_sap ])
        for ele in gen_line_edit:
                ele.clear()
            
        
       
    def reaffectation_site(self, ligne):
#        
        self.ligne_site_select = ligne
        
        self.lineEdit__site_nom.setText(self.tableWidget__site_recap.item(ligne, 0).text()) 
        self.lineEdit__site_abrev.setText(self.tableWidget__site_recap.item(ligne, 1).text()) 
        self.textEdit___site_adresse.setPlainText(self.tableWidget__site_recap.cellWidget(ligne, 2).toPlainText())             
        self.lineEdit__site_code_p.setText(self.tableWidget__site_recap.item(ligne, 3).text()) 
        self.lineEdit__site_ville.setText(self.tableWidget__site_recap.item(ligne, 4).text()) 
        self.lineEdit__site_tel.setText(self.tableWidget__site_recap.item(ligne, 5).text())
        self.lineEdit__site_fax.setText(self.tableWidget__site_recap.item(ligne, 6).text())
        self.lineEdit__site_courriel.setText(self.tableWidget__site_recap.item(ligne, 7).text()) 
        self.lineEdit__site_contact.setText(self.tableWidget__site_recap.item(ligne, 8).text())
        self.lineEdit_prefixe_sap.setText(self.tableWidget__site_recap.item(ligne, 9).text())
        
        self.pushButton_maj.show()
    
    @pyqtSlot()
    def on_pushButton_maj_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.ligne_site_select != -1:
            nom_site = self.lineEdit__site_nom.text().upper()
            abreviation = self.lineEdit__site_abrev.text().upper()
            adresse = self.textEdit___site_adresse.toPlainText().capitalize()
            code_post = self.lineEdit__site_code_p.text()
            ville = self.lineEdit__site_ville.text().upper()
            telephone = self.lineEdit__site_tel.text()
            fax = self.lineEdit__site_fax.text()
            courriel = self.lineEdit__site_courriel.text()
            contact = self.lineEdit__site_contact.text()
            prefix_sap = self.lineEdit_prefixe_sap.text()

            self.tableWidget__site_recap.setItem(self.ligne_site_select, 0, QTableWidgetItem(nom_site))
            self.tableWidget__site_recap.setItem(self.ligne_site_select, 1, QTableWidgetItem(abreviation))
            
            text_edit = QTextEdit(self.tableWidget__site_recap)
            self.tableWidget__site_recap.setCellWidget(self.ligne_site_select,2,  text_edit)
            text_edit.setPlainText(adresse)
            
            
            
            self.tableWidget__site_recap.setItem(self.ligne_site_select, 3, QTableWidgetItem(code_post))
            self.tableWidget__site_recap.setItem(self.ligne_site_select, 4, QTableWidgetItem(ville))
            self.tableWidget__site_recap.setItem(self.ligne_site_select, 5, QTableWidgetItem(telephone))
            self.tableWidget__site_recap.setItem(self.ligne_site_select, 6, QTableWidgetItem(fax))
    
            self.tableWidget__site_recap.setItem(self.ligne_site_select, 7, QTableWidgetItem(courriel))
            self.tableWidget__site_recap.setItem(self.ligne_site_select, 8, QTableWidgetItem(contact))
            self.tableWidget__site_recap.setItem(self.ligne_site_select, 9, QTableWidgetItem(prefix_sap))
    
    
            self.ligne_site_select = -1

            self.pushButton_maj.hide()
            
            #nettoyage
            gen_line_edit = iter([self.lineEdit__site_nom, self.lineEdit__site_abrev,        
                                    self.textEdit___site_adresse, self.lineEdit__site_code_p, 
                                    self.lineEdit__site_ville, self.lineEdit__site_tel, 
                                    self.lineEdit__site_fax, self.lineEdit__site_courriel, 
                                    self.lineEdit__site_contact, self.lineEdit_prefixe_sap])
            for ele in gen_line_edit:
                ele.clear()
            
    
    @pyqtSlot(int)
    def on_tabWidget_currentChanged(self, index):
        """
        Slot documentation goes here.
        """
        
        if index == 2:
            self.comboBox_sites.clear()
            self.comboBox_sites.addItem("*")
            nbr_site = self.tableWidget__site_recap.rowCount()
            for ligne in range(nbr_site):
                abreviation_site = self.tableWidget__site_recap.item(ligne, 1).text()
                self.comboBox_sites.addItem(abreviation_site)
            


            
    def reaffectation_service(self, ligne):
        self.ligne_service_select = ligne
        
        index_combobox = self.comboBox_sites.findText(self.tableWidget__recap_service.item(ligne, 0).text())
        if index_combobox != -1:
            self.comboBox_sites.setCurrentIndex(index_combobox)
        
        self.lineEdit_service_nom.setText(self.tableWidget__recap_service.item(ligne, 1).text()) 
        self.lineEdit_service_abrev.setText(self.tableWidget__recap_service.item(ligne, 2).text()) 
        self.lineEdit_service_tel.setText(self.tableWidget__recap_service.item(ligne, 3).text())             
        self.lineEdit_service_fax.setText(self.tableWidget__recap_service.item(ligne, 4).text()) 
        self.lineEdit_service_courriel.setText(self.tableWidget__recap_service.item(ligne, 5).text()) 
        self.lineEdit_service_contact.setText(self.tableWidget__recap_service.item(ligne, 6).text())
      
        self.pushButton_service_maj.show()
    
    @pyqtSlot()
    def on_pushButton_service_maj_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.ligne_service_select != -1:
            service = self.comboBox_sites.currentText()
            nom_service = self.lineEdit_service_nom.text().upper()
            abreviation = self.lineEdit_service_abrev.text().upper()

            telephone = self.lineEdit_service_tel.text()
            fax = self.lineEdit_service_fax.text()
            courriel = self.lineEdit_service_courriel.text()
            contact = self.lineEdit_service_contact.text()
            
            self.tableWidget__recap_service.setItem(self.ligne_service_select, 0, QTableWidgetItem(service))
            self.tableWidget__recap_service.setItem(self.ligne_service_select, 1, QTableWidgetItem(nom_service))
            self.tableWidget__recap_service.setItem(self.ligne_service_select, 2, QTableWidgetItem(abreviation))

            self.tableWidget__recap_service.setItem(self.ligne_site_select, 3, QTableWidgetItem(telephone))
            self.tableWidget__recap_service.setItem(self.ligne_site_select, 4, QTableWidgetItem(fax))
    
            self.tableWidget__recap_service.setItem(self.ligne_site_select, 5, QTableWidgetItem(courriel))
            self.tableWidget__recap_service.setItem(self.ligne_site_select, 6, QTableWidgetItem(contact))
    
    
            self.ligne_site_select = -1

            self.pushButton_service_maj.hide()
            
            #nettoyage
            gen_line_edit = iter([self.lineEdit_service_nom, self.lineEdit_service_abrev,        
                                    self.lineEdit_service_tel, self.lineEdit_service_fax, 
                                    self.lineEdit_service_courriel, self.lineEdit_service_contact])
            for ele in gen_line_edit:
                ele.clear()
    
    @pyqtSlot()
    def on_actionSauvegarder_triggered(self):
        """
        Slot documentation goes here.
        """
        if self.lineEdit_client_nom.text().upper() and self.lineEdit__client_abrev.text().upper():
        
            new_client = {"nom_complet": self.lineEdit_client_nom.text().upper(), 
                            "abreviation": self.lineEdit__client_abrev.text().upper(), 
                            "adresse": self.textEdit_client_adresse.toPlainText().capitalize(), 
                            "code_postal": self.lineEdit__client_code_p.text(), 
                            "ville": self.lineEdit__client_ville.text().upper(), 
                            "telephone": self.lineEdit__client_tel.text(),
                            "fax": self.lineEdit__client_fax.text(), 
                            "courriel": self.lineEdit__client_courriel.text(), 
                            "contact": self.lineEdit__client_contact.text(), 
                            "sites":[]}
            
            
            #sites:
            for ligne in range(self.tableWidget__site_recap.rowCount()):
                site= {
                "nom_complet":self.tableWidget__site_recap.item(ligne, 0).text(), 
                "abreviation": self.tableWidget__site_recap.item(ligne, 1).text(), 
                "adresse":self.tableWidget__site_recap.cellWidget(ligne, 2).toPlainText(),             
                "code_postal":self.tableWidget__site_recap.item(ligne, 3).text(), 
                "ville": self.tableWidget__site_recap.item(ligne, 4).text(), 
                "tel": self.tableWidget__site_recap.item(ligne, 5).text(),
                "fax":self.tableWidget__site_recap.item(ligne, 6).text(),
                "courriel":self.tableWidget__site_recap.item(ligne, 7).text(), 
                "contact" : self.tableWidget__site_recap.item(ligne, 8).text(),
                "prefixe_sap":self.tableWidget__site_recap.item(ligne, 9).text(), 
                "services":[]}
                
                #Services:        
                for service_ligne in range(self.tableWidget__recap_service.rowCount()):
                    site_select = self.tableWidget__site_recap.item(ligne, 1).text()
                    if self.tableWidget__recap_service.item(service_ligne, 0).text() == site_select:
                        service ={
                            "nom_complet":self.tableWidget__recap_service.item(service_ligne, 1).text(), 
                            "abreviation": self.tableWidget__recap_service.item(service_ligne, 2).text(),
                            "tel": self.tableWidget__recap_service.item(service_ligne, 3).text(),
                            "fax":self.tableWidget__recap_service.item(service_ligne, 4).text(),
                            "courriel":self.tableWidget__recap_service.item(service_ligne, 5).text(), 
                            "contact" : self.tableWidget__recap_service.item(service_ligne, 6).text()}
                    
                        site["services"].append(service)
                        
            
                new_client["sites"].append(site)
            
            
            
    
            self.signalNewclient.emit(new_client)
            
            self.close()
        
        else:
#            msg = QMessageBox()
#            msg.setIcon(QMessageBox.Warning)
#            msg.setText("Merci de saisir les informations")
#            msg.show()
            
            QMessageBox.warning(self, 
                        self.trUtf8("Attention"), 
                        self.trUtf8("Merci de saisir les informations \
                                    sur le Nom et l'abreviation du client"))
    
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
    
    @pyqtSlot()
    def on_checkBox_2_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.checkBox_2.isChecked():
            self.comboBox_poste_tech_sap_efs.setEnabled(True)
            self.lineEdit_prefixe_sap.setEnabled(True)
            
            self.signalBesoinpostetech_efs.emit()
        else:
            self.comboBox_poste_tech_sap_efs.setEnabled(False)
            self.lineEdit_prefixe_sap.setEnabled(False)
            self.comboBox_poste_tech_sap_efs.clear()
    
    @pyqtSlot(str)
    def on_comboBox_poste_tech_sap_efs_currentIndexChanged(self, p0):
        """
        Slot documentation goes here.
        """
        try:
            poste = self.comboBox_poste_tech_sap_efs.currentText()
            abreviation = [x[0] for x in self.post_tech if x[1] == poste][0]
            prefixe_sap = [x[2] for x in self.post_tech if x[1] == poste][0]
            self.lineEdit__site_nom.setText(poste)
            self.lineEdit__site_abrev.setText(abreviation)
            self.lineEdit_prefixe_sap.setText(prefixe_sap)
        except:
            pass
        
        
    def post_tech_efs(self, list):        
        """fct qui met à jour le combobox suite à la reception du signal du mainadministration"""
        self.post_tech = list
        self.comboBox_poste_tech_sap_efs.clear()
        self.comboBox_poste_tech_sap_efs.addItems([x[1] for x in list])
