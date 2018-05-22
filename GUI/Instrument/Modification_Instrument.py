# -*- coding: utf-8 -*-

"""
Module implementing Modification_Instrument.
"""
from PyQt4.QtCore import pyqtSlot, pyqtSignal
    
from PyQt4.QtGui import QDialog, QTableWidgetItem, QStandardItem, QStandardItemModel
#import unicodedata

from Package.AccesBdd import Instrument, Client, Secteur_exploitation, Poste_tech_sap

import pandas as pd

from .Ui_Modification_Instruments import Ui_Modification_Instrument


class Modification_Instrument(QDialog, Ui_Modification_Instrument):
    """
    Class documentation goes here.
    """
    
    
    signal_modification_ok = pyqtSignal()
    
    
    def __init__(self, engine, dataframe_instruments , parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super().__init__(parent)
        self.setupUi(self)
        
        #remplit le qtablewidget avec les instruments à modifier
        numero_colonne = 0
        for nom_colonne in list(dataframe_instruments):
#                print(numero_colonne)
            self.tableWidget.insertColumn(numero_colonne)
            self.tableWidget.setHorizontalHeaderItem(numero_colonne, QTableWidgetItem(nom_colonne))
            numero_ligne=0
            for ele in dataframe_instruments[nom_colonne]:
#                print(ele)
#                print(f"num ligne {numero_ligne} , numero colonne {numero_colonne}")
                if numero_colonne == 0:
                    self.tableWidget.insertRow(numero_ligne)
                    self.tableWidget.setItem(numero_ligne, numero_colonne, QTableWidgetItem(str(ele)))
                
                else:
                    self.tableWidget.setItem(numero_ligne, numero_colonne, QTableWidgetItem(str(ele)))
                numero_ligne+= 1
            numero_colonne += 1

        
        #recuperation des tables
        self.class_instrument = Instrument(engine)
        parc = self.class_instrument.parc_complet()
        
        self.table_secteur = Secteur_exploitation(engine)
        self.table_poste_tech_sap = Poste_tech_sap(engine)
        
        self.classe_clients = Client(engine)
        self.clients = self.classe_clients.ensemble_entites_clients()
        
        ####
        
        instrums_non_lies = parc[(parc["ETAT_UTILISATION"] != True)]
#        print(instrums_non_lies)
        
        self.comboBox_instrument.installEventFilter(self)
        model = QStandardItemModel()

        for i,word in enumerate(instrums_non_lies["IDENTIFICATION"]):
            item = QStandardItem(word)
            model.setItem(i, 0, item)

        self.comboBox_instrument.setModel(model)
        self.comboBox_instrument.setModelColumn(0)
        
        
        
        
        clients_tries = self.clients.sort_values(by = "ID_ENT_CLIENT")       
        self.comboBox_client.addItems(clients_tries["ABREVIATION"].tolist())
        

        
        domaine_mesure = list(set([x.upper() for x in parc["DOMAINE_MESURE"].tolist() if x]))
        domaine_mesure.sort()
        self.comboBox_domaine_mes.addItems(domaine_mesure)
        
        designation = list(set([x.upper() for x in parc["DESIGNATION"].tolist() if x]))
        designation.sort()
        self.comboBox_designation.addItems(designation)
        
        type = list(set([x.upper() for x in parc["TYPE"].tolist() if x]))
        type.sort()
        self.comboBox_type.addItems(type)
        
#        print(f"""commentaire {parc["COMMENTAIRE"]}""")
        commentaire = list(set([x.upper() for x in parc["COMMENTAIRE"].tolist() if x]))
        commentaire.sort()
        commentaire.insert(0, "")
        self.comboBox_commentaire.addItems(commentaire)
#        self.comboBox_commentaire.setItemData(1,"")
        
        
#        print(parc["DESIGNATION_LITTERALE"])
        designation_lit = list(set(parc["DESIGNATION_LITTERALE"].tolist()))

        self.comboBox_designation_litt.addItems(designation_lit)
        
        constructeur = list(set([x.upper() for x in parc["CONSTRUCTEUR"].tolist() if x]))
#        constructeur.sort()
        self.comboBox_constructeur.addItems(constructeur)
        
        ref_constructeur = list(set(parc["REFERENCE_CONSTRUCTEUR"].tolist()))
#        ref_constructeur.sort()
        self.comboBox_ref_constructeur.addItems(ref_constructeur)
        
        self.dict_famille = {"AR":"ANEMOMETRE", "AT":"AGITATEUR LABO", "AU":"AUTOCLAVE", "BA":"BALANCE / SYST PESEE", 
                    "BE":"MESURE DE PRESSION", "BM":"BAINS-MARIE", "CF":"CHAMBRE FROIDE", "CH":"MESURE DU TEMPS", 
                    "CN":"CONSERVAT. PLAQUETTE", "CO":"ENCEINTE T°C NEGATIV", "CP":"CENTRI GRDE CAPACITE", 
                    "CT":"CENTRI MOY CAPACITE", "DE":"DECONGELATEURS", "DI":"DISTRIBUTEUR", 
                    "EE":"EQPT ELECTRIQUE", "FG":"FOUR ET BAIN ETALON", "FO":"FOUR", 
                    "HY":"HYGROMETRES", "IN":"ETUVES - INCUBATEURS", 
                    "MC":"REFRIGERAT. DOMESTIQ", "MY":"MATERIEL CRYOGENIQUE", "PG":"POIDS ETALON", 
                    "PI":"PIPETTES", "RT":"ENCEINTE T°C POSITIV", "TH":"THERMOCYCLEUR", 
                    "TM":"MESURE POLYVAL (T°C)", "TN":"TENSIOMETRE", "TO":"TRAITEMENT DE L'EAU", 
                    "TR":"TABLE REFRIGEREE", "TY":"TACHYMETRES", "UC":"ULTRA-CENTRIFUGEUSE"}
        
        list_famille = [self.dict_famille[x] for x in self.dict_famille]
        list_famille.sort()
        self.comboBox_famille.addItems(list_famille)
        
#        self.resize(100,100)
#        self.setWindowFlags(self.windowFlags() |
#                              Qt.WindowSystemMenuHint |
#                              Qt.WindowMinMaxButtonsHint)

#        self.setFixedSize(self.size()) 
    

    
    def keyPressEvent(self, event):
        pass
#        print(f"coucou {event}")
#    def closeEvent(self, event):
#        print("coucou je me casse")
    
    @pyqtSlot()
    def on_buttonBox_accepted(self):
        """
        Slot documentation goes here.
        """
        nbr_ligne = self.tableWidget.rowCount()
        nbr_colonne =self.tableWidget.columnCount()
        
        list_dictionnaire = []
        list_non_enregistree = []
        
        for num_ligne in range(nbr_ligne, -1, -1):
            
            #test valeurs None sur CODE,DOMAINE de mesure,Designation:
            try:
                code = self.tableWidget.item(num_ligne,2).text()
                domaine_mesure= self.tableWidget.item(num_ligne,3).text()
                designation = self.tableWidget.item(num_ligne,5).text()
                
                if code!= "None" and domaine_mesure != "None" and designation !="None":
                    dict_ligne = {}
                    for num_colonne in range(nbr_colonne):
    
                        if self.tableWidget.item(num_ligne,num_colonne):
                            dict_ligne[self.tableWidget.horizontalHeaderItem(num_colonne).text()] = self.tableWidget.item(num_ligne,num_colonne).text()
                        else:
                            dict_ligne[self.tableWidget.horizontalHeaderItem(num_colonne).text()] = None
                    list_dictionnaire.append(dict_ligne)
                    
                    self.tableWidget.removeRow(num_ligne)
                
                else:
                    dict_ligne = {}
                    for num_colonne in range(nbr_colonne):
    
                        if self.tableWidget.item(num_ligne,num_colonne):
                            dict_ligne[self.tableWidget.horizontalHeaderItem(num_colonne).text()] = self.tableWidget.item(num_ligne,num_colonne).text()
                        else:
                            dict_ligne[self.tableWidget.horizontalHeaderItem(num_colonne).text()] = None
                    list_non_enregistree.append(dict_ligne)
                    
            except :                
                pass
#                QMessageBox.critical(self, 
#                    self.trUtf8("Client"), 
#                    self.trUtf8("La mise a jour n'a pu etre realisée"))
        

        self.class_instrument.update_instruments(list_dictionnaire)        

                
        if self.tableWidget.rowCount()== 0 :
            self.signal_modification_ok.emit()
            self.close()
            
        
    @pyqtSlot()
    def on_buttonBox_rejected(self):
        """
        Slot documentation goes here.
        """
        self.close()
    
    

    @pyqtSlot()
    def on_pushButton_maj_clicked(self):
        """
        Slot documentation goes here.
        """

        dict_questionnaire = {"CODE": self.comboBox_affectation.currentText(),
                            "AFFECTATION":self.comboBox_localisation.currentText(),
                            "DOMAINE_MESURE": self.comboBox_domaine_mes.currentText(),
                            "FAMILLE": self.comboBox_famille.currentText(), 
                            "DESIGNATION":self.comboBox_designation.currentText(),
                            "TYPE": self.comboBox_type.currentText(),
                            "DESIGNATION_LITTERALE":self.comboBox_designation_litt.currentText(), 
                            "CONSTRUCTEUR":self.comboBox_constructeur.currentText(), 
                            "REFERENCE_CONSTRUCTEUR": self.comboBox_ref_constructeur.currentText(), 
                            "N_SERIE": self.lineEdit_n_serie.text(),
                            "RESOLUTION": self.lineEdit_resolution.text(), 
                            "ETAT_UTILISATION":self.comboBox_etat_util.currentText(), 
                            "REF_INSTRUMENT": self.comboBox_instrument.currentText(), 
                            "COMMENTAIRE": self.comboBox_commentaire.currentText()}

        list_n_ligne = list(set([item.row() for item in self.tableWidget.selectedIndexes()]))
        list_n_ligne.sort()
        
        list_n_colonne = list(set([item.column() for item in self.tableWidget.selectedIndexes()]))
        list_n_colonne.sort()

        for ligne in list_n_ligne:
            for colonne in list_n_colonne:
#                print(f"n° colonne {colonne}")
                try:
                    nom_colonne = self.tableWidget.horizontalHeaderItem(colonne).text()
#                    print(f"nom colone {nom_colonne}")
                    if nom_colonne == "REF_INSTRUMENT":
#                        print("test0")
                        if self.checkBox_lier.isChecked():
                            value = dict_questionnaire[nom_colonne]
                            self.tableWidget.setItem(ligne, colonne, QTableWidgetItem(str(value)))
                            self.tableWidget.setItem(ligne, (colonne-1), QTableWidgetItem(str(True)))
                        else:
                            self.tableWidget.setItem(ligne, colonne, QTableWidgetItem(str("")))
                            self.tableWidget.setItem(ligne, (colonne-1), QTableWidgetItem(str(False)))
                    
                    elif nom_colonne == "CODE":
                        
                        ###faire boucle pour trouver l'adresse de la colonne "SITE" pas toujour en 11
                        value = dict_questionnaire[nom_colonne]
#                        print(value)
                        self.tableWidget.setItem(ligne, colonne, QTableWidgetItem(str(value)))                        
                        sites_clients = self.classe_clients.ensemble_sites_clients()
                        nom_site = sites_clients[sites_clients.CODE_CLIENT == value].VILLE.values[0]
                        self.tableWidget.setItem(ligne, 10, QTableWidgetItem(str(nom_site)))
                    else:                            
                        value = dict_questionnaire[nom_colonne]
    #                    print(f"value {value}")
                        self.tableWidget.setItem(ligne, colonne, QTableWidgetItem(str(value)))
                except KeyError:
                    pass
#        print(list_n_ligne)
    
    @pyqtSlot()
    def on_checkBox_lier_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.checkBox_lier.isChecked():
            self.comboBox_instrument.setEnabled(True)
            
        else:
            self.comboBox_instrument.setEnabled(False)
    
    @pyqtSlot(int)
    def on_comboBox_client_currentIndexChanged(self, index):
        """
        Slot documentation goes here.
        """
        try:
            #gestion des sites
            self.comboBox_affectation.clear()
            abreviation_siege = self.comboBox_client.currentText()
            id_siege = int(self.clients[self.clients.ABREVIATION == abreviation_siege].ID_ENT_CLIENT.values[0])
#            print(f"id_siege {id_siege}")
            sites_clients = self.classe_clients.ensemble_sites_clients()
            sites_clients_tries = sites_clients[sites_clients.ID_ENT_CLIENT == id_siege].sort_values(by = "ID_CLIENTS") 
 
            self.comboBox_affectation.addItems(sites_clients_tries["CODE_CLIENT"].tolist())
        
            #gestion des services
            
        
        except IndexError:
            pass
    
    @pyqtSlot(int)
    def on_comboBox_affectation_currentIndexChanged(self, index):
        """
        Slot documentation goes here.
        """
        try:
            self.comboBox_localisation.clear()
            site_client = self.comboBox_affectation.currentText()
#            print(site_client)
            sites_clients = self.classe_clients.ensemble_sites_clients() 
#            print(sites_clients[sites_clients.CODE_CLIENT == site_client])
            id_site = int(sites_clients[sites_clients.CODE_CLIENT == site_client].ID_CLIENTS.values[0])
#            print(f"id site {id_site}")
            services_client = self.classe_clients.ensemble_service_client()
            services_tries = services_client[services_client.ID_CLIENT == id_site].sort_values(by = "ID_SERVICE")
            
#            print(services_tries)
            
            self.comboBox_localisation.addItems(services_tries["ABREVIATION"].tolist())
        
        except IndexError:
            
#            id_site = int(sites_clients[sites_clients.CODE_CLIENT == site_client].ID_CLIENTS.values[0])
#            print(f"id site {id_site}")
            pass
