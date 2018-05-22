# -*- coding: utf-8 -*-

"""
Module implementing Indicateur.
"""
from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QMainWindow
from PyQt4.QtGui import QInputDialog

from .Ui_Indicateurs import Ui_MainWindow
from Modules.Indicateurs.Package.AccesBdd import AccesBdd
from Modules.Indicateurs.Package.Export_excel import Export_excel

import numpy

class Indicateur(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self,  engine, meta, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super().__init__(parent)
        self.setupUi(self)
        self.engine = engine
        self.meta = meta
        self.db = AccesBdd(engine, meta)
        self.instruments = self.db.resencement_instrument_utilises()

        
        #configuration largeur colonnes tablewidget
        self.tableWidget.setColumnWidth(0,600)
        self.tableWidget.setColumnWidth(1,600)
        
        #calendrier
        date_du_jour = self.dateEdit_2.selectedDate()
        self.dateEdit.setCurrentPage(date_du_jour.year(), (date_du_jour.month() - 3))
        
    @pyqtSlot(str)
    def on_comboBox_activated(self, p0):
        """
        Slot documentation goes here.
        """
        
        self.supprimer_lignes()
        indicateur = self.comboBox.currentText()

        if indicateur == "Composition Parc":
            self.composition_parc_utilises()
        elif indicateur == "Temperature":
            self.indicateurs_temperature()
        
        elif indicateur == "Delais":
            self.indicateurs_delais()
            
        elif indicateur == "Afficheurs":
            self.indicateurs_afficheur()
    
    def composition_parc_utilises(self):
        '''fct qui rappatrie et trie l'ensemble du parc de la base et renvoie un dictionnaire avec le nbr d'instrument pas designation
        '''
        clients = ["Total","EFS_PL", "EFS_BRETAGNE", "EFS_NORMANDIE", "EFS_CA", "HORS_PDL"]
        client_choisi = QInputDialog.getItem(self, 
                       self.trUtf8("Numero certificats"), 
                       self.trUtf8("Choisir un numero"),
                       clients)

            #list des designations:
        designations = list(set([ele[2] for ele in self.instruments]))
        designations.sort()
#        print(designations)
            #Indicateurs:
                #clients
#        efs_pl =["ABG__-44"]
        efs_pl = ["ABG__-44", "EFS  -53", "EFS  -72", "EFS  -85", 
                    "EFSNA-44", "EFS  -49", "EFS  -44", "EFSNO-44"]
                    
        efs_bretagne = ["EFS  -35"]
        efs_normandie = ["EFS  -14"]
        efs_centre_atlantique = ["EFSCA-16", "EFSCA-18", "EFSCA-28", "EFSCA-36", 
                                "EFSCA-37", "EFSCA-45", "EFSCA-79", "EFSCA-86", 
                                "EFSRO-17", "EFSSA-17", "EFSCA-41"]
                                
        total = efs_pl + efs_bretagne+ efs_normandie+ efs_centre_atlantique
        hors_pdl = efs_bretagne+ efs_normandie+ efs_centre_atlantique
        
            
                #parc designations:       
      
        

        for ele in reversed(designations):
            
            if client_choisi[0] == "Total" and client_choisi[1] == True:
                list_totale =  [x[0] for x in self.instruments if x[2] == ele and x[3] in  total]
                
            elif client_choisi[0] == "EFS_PL" and client_choisi[1] == True:
                list_totale =  [x[0] for x in self.instruments if x[2] == ele and x[3] in  efs_pl]
                
            elif client_choisi[0] == "EFS_BRETAGNE" and client_choisi[1] == True:
                list_totale =  [x[0] for x in self.instruments if x[2] == ele and x[3] in  efs_bretagne]
                
            elif client_choisi[0] == "EFS_NORMANDIE" and client_choisi[1] == True:
                list_totale =  [x[0] for x in self.instruments if x[2] == ele and x[3] in  efs_normandie]
                
            elif client_choisi[0] == "EFS_CA" and client_choisi[1] == True:
                list_totale =  [x[0] for x in self.instruments if x[2] == ele and x[3] in  efs_centre_atlantique]
                
            elif client_choisi[0] == "HORS_PDL" and client_choisi[1] == True:
                list_totale =  [x[0] for x in self.instruments if x[2] == ele and x[3] in  hors_pdl]
                
                
#            print(list_totale)
            self.tableWidget.insertRow(0)
                
                
            nbr_instrument  =len(list_totale)
                
                
            self.tableWidget.setItem(0, 0, QtGui.QTableWidgetItem(str(str(ele) + " "+str(client_choisi[0]))))
            self.tableWidget.setItem(0, 1, QtGui.QTableWidgetItem(str(nbr_instrument)))


        
        
    def indicateurs_temperature(self):
        '''fct gerant les differents indicateurs dommaine temperature'''
        
        date_debut = self.dateEdit.selectedDate().toString('yyyy-MM-dd')
        date_fin = self.dateEdit_2.selectedDate().toString('yyyy-MM-dd')
        
        parc_temperature = [ele for ele in self.instruments if ele[1] == "Température" and  (ele[2] == "Enregistreur de température" or  ele[2] == "Chaîne de mesure de température")]
#        print(parc_temperature)
#        identification_instruments_temperature = [ele[0] for ele in parc_temperature]
        indicateurs_temperature = self.db.indicateur_temperature(date_debut, date_fin, parc_temperature)
       
        recensement_conformite = self.db.recensement_conformite(date_debut, date_fin)
        nbr_declaration_conformite = len(recensement_conformite)
        
        indicateurs_temperature["nbr de CV"] = nbr_declaration_conformite
        

        #Presentation tableWidget final
            
        self.tableWidget.insertRow(0)                 
        self.tableWidget.setItem(0, 0, QtGui.QTableWidgetItem(str("nbr d'instruments receptionnés")))
        self.tableWidget.setItem(0, 1, QtGui.QTableWidgetItem(str(indicateurs_temperature["nbr_instruments_receptionnes"])))
        
        self.tableWidget.insertRow(1)                 
        self.tableWidget.setItem(1, 0, QtGui.QTableWidgetItem(str("nbr d'instruments expédiés")))
        self.tableWidget.setItem(1, 1, QtGui.QTableWidgetItem(str(indicateurs_temperature["nbr_instruments_expedies"])))
       
        #campagne
        self.tableWidget.insertRow(2)                 
        self.tableWidget.setItem(2, 0, QtGui.QTableWidgetItem(str("Nbr de campagne d'etalonnage")))
        self.tableWidget.setItem(2, 1, QtGui.QTableWidgetItem(str(indicateurs_temperature["nbr_campagne"])))
        
        self.tableWidget.insertRow(3)                 
        self.tableWidget.setItem(3, 0, QtGui.QTableWidgetItem(str("Nbr d'instruments moyen par campagne d'etalonnage")))
        self.tableWidget.setItem(3, 1, QtGui.QTableWidgetItem(str(indicateurs_temperature["nbr_moyen_intrument_par_campagne"])))
        
        self.tableWidget.insertRow(4)                 
        self.tableWidget.setItem(4, 0, QtGui.QTableWidgetItem(str("Ecart type d'instruments par campagne d'etalonnage")))
        self.tableWidget.setItem(4, 1, QtGui.QTableWidgetItem(str(indicateurs_temperature["ecart_type_nbr_instrument_campagne"])))
        
        self.tableWidget.insertRow(5)                 
        self.tableWidget.setItem(5, 0, QtGui.QTableWidgetItem(str("Max nbr d'instruments par campagne d'etalonnage")))
        self.tableWidget.setItem(5, 1, QtGui.QTableWidgetItem(str(indicateurs_temperature["nbr_instruments_max_par_campagne"])))
        
        self.tableWidget.insertRow(6)                 
        self.tableWidget.setItem(6, 0, QtGui.QTableWidgetItem(str("Min nbr d'instruments par campagne d'etalonnage")))
        self.tableWidget.setItem(6, 1, QtGui.QTableWidgetItem(str(indicateurs_temperature["nbr_instruments_min_par_campagne"])))
        
        self.tableWidget.insertRow(7)                 
        self.tableWidget.setItem(7, 0, QtGui.QTableWidgetItem(str("Nbr moyen de point par campagne ")))
        self.tableWidget.setItem(7, 1, QtGui.QTableWidgetItem(str(indicateurs_temperature["nbr_moyen_pt_etal_par_campagne"])))
        
        self.tableWidget.insertRow(8)                 
        self.tableWidget.setItem(8, 0, QtGui.QTableWidgetItem(str("Ecart type nbr moyen de point par campagne ")))
        self.tableWidget.setItem(8, 1, QtGui.QTableWidgetItem(str(indicateurs_temperature["ecart_type_nbr_pt_etal_campagne"])))
        
        self.tableWidget.insertRow(9)                 
        self.tableWidget.setItem(9, 0, QtGui.QTableWidgetItem(str("Max nbr de point par campagne ")))
        self.tableWidget.setItem(9, 1, QtGui.QTableWidgetItem(str(indicateurs_temperature["nbr_pt_max_par_campagne"])))
        
        self.tableWidget.insertRow(10)                 
        self.tableWidget.setItem(10, 0, QtGui.QTableWidgetItem(str("Min nbr de point par campagne ")))
        self.tableWidget.setItem(10, 1, QtGui.QTableWidgetItem(str(indicateurs_temperature["nbr_pt_min_par_campagne"])))
        
        self.tableWidget.insertRow(11)                 
        self.tableWidget.setItem(11, 0, QtGui.QTableWidgetItem(str("Nombre d'etalonnages")))
        self.tableWidget.setItem(11, 1, QtGui.QTableWidgetItem(str(indicateurs_temperature["nbr_etalonnage"])))
        
        self.tableWidget.insertRow(12)                 
        self.tableWidget.setItem(12, 0, QtGui.QTableWidgetItem(str("Nombre d'etalonnages : milieu air")))
        self.tableWidget.setItem(12, 1, QtGui.QTableWidgetItem(str(indicateurs_temperature["nbr_etalonnage_air"])))
        
        self.tableWidget.insertRow(13)                 
        self.tableWidget.setItem(13, 0, QtGui.QTableWidgetItem(str("Nombre d'etalonnages : milieu liquide")))
        self.tableWidget.setItem(13, 1, QtGui.QTableWidgetItem(str(indicateurs_temperature["nbr_etalonnage_liquide"])))
        

        self.tableWidget.insertRow(14)                 
        self.tableWidget.setItem(14, 0, QtGui.QTableWidgetItem(str("Nbr de declaration de conformite")))
        self.tableWidget.setItem(14, 1, QtGui.QTableWidgetItem(str(indicateurs_temperature["nbr_declaration_conformite"])))
        
        self.tableWidget.insertRow(15)                 
        self.tableWidget.setItem(15, 0, QtGui.QTableWidgetItem(str("Nbr d'instruments conformes")))
        self.tableWidget.setItem(15, 1, QtGui.QTableWidgetItem(str(indicateurs_temperature["nbr_instruments_conforme"])))
        
        self.tableWidget.insertRow(16)                 
        self.tableWidget.setItem(16, 0, QtGui.QTableWidgetItem(str("Nbr d'instruments non conformes")))
        self.tableWidget.setItem(16, 1, QtGui.QTableWidgetItem(str(indicateurs_temperature["nbr_instruments_non_conforme"])))
        
    
    def indicateurs_afficheur(self):
        date_debut = self.dateEdit.selectedDate().toString('yyyy-MM-dd')
        date_fin = self.dateEdit_2.selectedDate().toString('yyyy-MM-dd')
#        print(self.instruments)
        parc_afficheur = [ele for ele in self.instruments if ele[2] == "Afficheur de temps" 
                            or ele[2] == "Afficheur de température"  
                            or ele[2] == "Afficheur de vitesse"
                            or ele[2] == "Sonde alarme température"
                            or ele[2] == "Sonde d'hygrométrie"]
                            
#        print(parc_afficheur)
#        identification_instruments_temperature = [ele[0] for ele in parc_temperature]
        indicateurs_afficheurs = self.db.indicateurs_afficheur(date_debut, date_fin, parc_afficheur)
        
#        print(indicateurs_afficheurs)
        
        
        
        self.tableWidget.insertRow(0)                 
        self.tableWidget.setItem(0, 0, QtGui.QTableWidgetItem(str("nbr d'afficheurs receptionnés")))
        self.tableWidget.setItem(0, 1, QtGui.QTableWidgetItem(str(indicateurs_afficheurs["nbr_afficheurs_receptionnes"])))
        
        self.tableWidget.insertRow(1)                 
        self.tableWidget.setItem(1, 0, QtGui.QTableWidgetItem(str("nbr d'instruments expédiés")))
        self.tableWidget.setItem(1, 1, QtGui.QTableWidgetItem(str(indicateurs_afficheurs["nbr_afficheurs_expedies"])))
       
        #campagne
        self.tableWidget.insertRow(2)                 
        self.tableWidget.setItem(2, 0, QtGui.QTableWidgetItem(str("Nbr de contrôle d'afficheurs")))
        self.tableWidget.setItem(2, 1, QtGui.QTableWidgetItem(str(indicateurs_afficheurs["Nbr_controle"])))
        
        self.tableWidget.insertRow(3)                 
        self.tableWidget.setItem(3, 0, QtGui.QTableWidgetItem(str("Nbr d'afficheur conforme")))
        self.tableWidget.setItem(3, 1, QtGui.QTableWidgetItem(str(indicateurs_afficheurs["nbr_afficheurs_conformes"])))
        
        self.tableWidget.insertRow(4)                 
        self.tableWidget.setItem(4, 0, QtGui.QTableWidgetItem(str("Nbr d'afficheur non conforme")))
        self.tableWidget.setItem(4, 1, QtGui.QTableWidgetItem(str(indicateurs_afficheurs["nbr_afficheurs_non_conformes"])))
        
        self.tableWidget.insertRow(5)                 
        self.tableWidget.setItem(5, 0, QtGui.QTableWidgetItem(str("Nbr moyen de point  par contrôle")))
        self.tableWidget.setItem(5, 1, QtGui.QTableWidgetItem(str(indicateurs_afficheurs["nbr_pt_moyen_afficheur"])))
        
        self.tableWidget.insertRow(6)                 
        self.tableWidget.setItem(6, 0, QtGui.QTableWidgetItem(str("Ecart type nbr moyen de point par contrôle")))
        self.tableWidget.setItem(6, 1, QtGui.QTableWidgetItem(str(indicateurs_afficheurs["ecart_type_nbr_pt_afficheur"])))
        
        self.tableWidget.insertRow(7)                 
        self.tableWidget.setItem(7, 0, QtGui.QTableWidgetItem(str("Nbr de point maximum par contrôle")))
        self.tableWidget.setItem(7, 1, QtGui.QTableWidgetItem(str(indicateurs_afficheurs["nbr_pt_max_afficheur"])))
        
        self.tableWidget.insertRow(8)                 
        self.tableWidget.setItem(8, 0, QtGui.QTableWidgetItem(str("Nbr de point minimum par contrôle")))
        self.tableWidget.setItem(8, 1, QtGui.QTableWidgetItem(str(indicateurs_afficheurs["nbr_pt_min_afficheur"])))
        
       
    
    
        
    def supprimer_lignes(self):
        '''Supprime l'ensemble des lignes du qtablewidget'''
        nbr_ligne = self.tableWidget.rowCount()
        
        if nbr_ligne != 0:
            for i in range(0, nbr_ligne):
                self.tableWidget.removeRow(0)
    
    @pyqtSlot()
    def on_actionExport_parc_triggered(self):
        """
        permet d'exporter sur excel
        """
        rapport = Export_excel()
        rapport.export_instruments(self.instruments)
    
    @pyqtSlot()
    def on_actionExport_indicateurs_triggered(self):
        """
        Slot documentation goes here.
        """
        date_debut = self.dateEdit.selectedDate ().toString('yyyy-MM-dd')
        date_fin = self.dateEdit_2.selectedDate ().toString('yyyy-MM-dd')
        parc_temperature = [ele for ele in self.instruments if ele[1] == "Température" and  (ele[2] == "Enregistreur de température" or  ele[2] == "Chaîne de mesure de température")]
        
        parc_afficheur = [ele for ele in self.instruments if ele[2] == "Afficheur de temps" 
                            or ele[2] == "Afficheur de température"  
                            or ele[2] == "Afficheur de vitesse"
                            or ele[2] == "Sonde alarme température"
                            or ele[2] == "Sonde d'hygrométrie"]
#        print(parc_afficheur)
        
        temperature = self.db.instrument_temperature_etal(date_debut, date_fin)
        pb_expedition_reception_temperature = self.db.indicateur_temperature(date_debut, date_fin, parc_temperature)["list_instruments_receptionnes_non_expedies"]
        pb_reception_expedition_temperature = self.db.indicateur_temperature(date_debut, date_fin, parc_temperature)["list_instruments_expedies_non_receptionnes"]
        
        list_expedition_reception_temperature = self.db.recup_date_pb_expedition_reception(date_debut, date_fin, pb_expedition_reception_temperature)
        list_reception_expedition_temperature = self.db.recup_date_pb_expedition_reception(date_debut, date_fin, pb_reception_expedition_temperature)
        

        
        afficheur = self.db.afficheur_etal(date_debut, date_fin)
        pb_expedition_reception_afficheurs = self.db.indicateurs_afficheur(date_debut, date_fin, parc_afficheur)["list_afficheur_receptionnes_non_expedies"]
        pb_reception_expedition_afficheurs =self.db.indicateurs_afficheur(date_debut, date_fin, parc_afficheur)["list_afficheur_expedies_non_receptionnes"]
#        
        list_expedition_reception_afficheurs = self.db.recup_date_pb_expedition_reception(date_debut, date_fin, pb_expedition_reception_afficheurs)
        list_reception_expedition_afficheurs = self.db.recup_date_pb_expedition_reception(date_debut, date_fin, pb_reception_expedition_afficheurs)
#        print(list_reception_expedition_afficheurs)
        delais = self.db.delais_export_excel(date_debut, date_fin,  self.instruments)

        rapport = Export_excel()
        rapport.export_temperature(temperature, afficheur, delais, list_expedition_reception_temperature, list_reception_expedition_temperature, \
                                    list_expedition_reception_afficheurs, list_reception_expedition_afficheurs)
        
        
    def indicateurs_delais(self):
        date_debut = self.dateEdit.selectedDate ().toString('yyyy-MM-dd')
        date_fin = self.dateEdit_2.selectedDate ().toString('yyyy-MM-dd')        
#        print(date_debut)
        delais = self.db.indicateur_delais(date_debut, date_fin,  self.instruments)
#        
#        print(delais)
        set_designation = set([x[2] for x in self.instruments])
        for designation in set_designation:
            nbr_ligne_tableau = self.tableWidget.rowCount()
            
            if len(delais["list_instruments_recep_expe_delais" + " " + str(designation)]) !=0:
#                
#                print("coucou")
                self.tableWidget.insertRow(nbr_ligne_tableau )                 
                self.tableWidget.setItem(nbr_ligne_tableau , 0, QtGui.QTableWidgetItem("delais_moyen_immobilisation" + " " + str(designation)))
                self.tableWidget.setItem(nbr_ligne_tableau , 1, QtGui.QTableWidgetItem(str(delais["delais_moyen_immobilisation" + " " + str(designation)])))
                
                self.tableWidget.insertRow(nbr_ligne_tableau + 1)                 
                self.tableWidget.setItem(nbr_ligne_tableau + 1 , 0, QtGui.QTableWidgetItem("ecart_type_immobilisation" +  " " + str(designation)))
                self.tableWidget.setItem(nbr_ligne_tableau + 1, 1, QtGui.QTableWidgetItem(str(delais["ecart_type_immobilisation" +  " " + str(designation)])))
                
                self.tableWidget.insertRow(nbr_ligne_tableau + 2 )                 
                self.tableWidget.setItem(nbr_ligne_tableau + 2 , 0, QtGui.QTableWidgetItem("delais_max_immobilisation" +  " " + str(designation)))
                self.tableWidget.setItem(nbr_ligne_tableau + 2, 1, QtGui.QTableWidgetItem(str(delais["delais_max_immobilisation" +  " " + str(designation)])))
                
                self.tableWidget.insertRow(nbr_ligne_tableau + 3 )                 
                self.tableWidget.setItem(nbr_ligne_tableau + 3 , 0, QtGui.QTableWidgetItem("delais_min_immobilisation" +  " " + str(designation)))
                self.tableWidget.setItem(nbr_ligne_tableau + 3, 1, QtGui.QTableWidgetItem(str(delais["delais_min_immobilisation" +  " " + str(designation)])))
                     
                    
                    
                   
        
            
