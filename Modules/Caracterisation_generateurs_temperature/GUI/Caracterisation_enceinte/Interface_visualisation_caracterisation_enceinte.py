# -*- coding: utf-8 -*-

"""
Module implementing Visualisation_Caracterisation_enceinte.
"""

from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QMainWindow
#from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import  QMessageBox
from PyQt4 import QtGui, QtCore

from .Ui_Interface_visualisation_caracterisation_enceinte import Ui_Visualisation_caracterisation_enceinte

from Modules.Caracterisation_generateurs_temperature.Package.AccesBdd_caracterisation_enceinte import AccesBdd_caracterisation_enceinte

import numpy as np

class Visualisation_Caracterisation_enceinte(QMainWindow, Ui_Visualisation_caracterisation_enceinte):
    """
    Class documentation goes here.
    """
    def __init__(self, engine, meta, donnees_caracterisation, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super(Visualisation_Caracterisation_enceinte, self).__init__(parent)
        self.setupUi(self)
        
        self.engine = engine
        self.meta = meta
        
        self.donnees_caracterisation = donnees_caracterisation
#        print(self.donnees_caracterisation)
        #reaffectation des donnees :
        
        self.lineEdit_id_caracterisation.setText (str(donnees_caracterisation["ADMIN"]["ID_CARACTERISATION"]))
        
        self.textEdit.setText(donnees_caracterisation["ADMIN"]["COMMENTAIRE"])
        
        self.spinBox.setValue(donnees_caracterisation["ADMIN"]["NBR_TEMP_STABILITE"])
        
        self.label_nb_pt.setText(str(self.spinBox.value()))
        
        self.label_pt.setText(str(1))        
        
        self.dateEdit.setDate(donnees_caracterisation["ADMIN"]["DATE"])
        
        self.nbr_pts_caracterisation = self.spinBox.value()
        
        self.db_carac = AccesBdd_caracterisation_enceinte(self.engine, self.meta)
        
        #ctes de classe
        self.sauvegarde = {}
        self.sauvegarde["ARCHIVAGE"] = False
        self.sauvegarde_maximum_par_pt = {}
        
        self.actionSauvegarder.setEnabled(False)
        self.tabWidget.setTabEnabled(2, False)

        
        

        #reaffectation responsable_mesures
        self.responsable_mesures = self.db_carac.techniciens()
        
        visa = [x[1]  for x in self.responsable_mesures]
        self.comboBox_operateur.addItems(visa)
        
        visa_find = [x[1]  for x in self.responsable_mesures if x[0] == donnees_caracterisation["ADMIN"]["ID_OPERATEUR"]][0]
        index = self.comboBox_operateur.findText(visa_find)
        if index != -1:
            self.comboBox_operateur.setCurrentIndex(index)
        
        #reaffectation enceintes
        self.enceintes =self.db_carac.enceintes()
        
        nom_enceintes = [x[1] for x in self.enceintes]       
        self.comboBox_enceinte.addItems(nom_enceintes)
        
        enceinte_find = [x[1]  for x in self.enceintes if x[0] == donnees_caracterisation["ADMIN"]["ID_GENERATEUR"]][0]
        index = self.comboBox_enceinte.findText(enceinte_find)
        if index != -1:
            self.comboBox_enceinte.setCurrentIndex(index)
        
        
        
        #reaffectation etalon        
        self.etalons =  self.db_carac.etalons()

        nom_etalon = [x[1] for x in self.etalons]
        self.comboBox_etalon.addItems(nom_etalon)
        
        etalon_find = [x[1]  for x in self.etalons if x[0] == donnees_caracterisation["MOYENS_MESURE"]["ID_ETALON"]][0]
        index = self.comboBox_etalon.findText(etalon_find)
        if index != -1:
            self.comboBox_etalon.setCurrentIndex(index)
        
        
        
        self.sondes_centrales = self.db_carac.sondes_centrales()
        self.centrales = self.db_carac.centrales()
        nom_centrales = [x[1] for x in self.centrales ]
        self.comboBox_centrale.addItems(nom_centrales)
        
        centrale_find = [x[1]  for x in self.centrales if x[0] == donnees_caracterisation["MOYENS_MESURE"]["ID_CENTRALE"]][0]
        index = self.comboBox_centrale.findText(centrale_find)
        if index != -1:
            self.comboBox_centrale.setCurrentIndex(index)
            


        #reste id_polynome
        donnees_polynome_utilise = self.db_carac.nom_poly_etalon_id(donnees_caracterisation["MOYENS_MESURE"]["ID_POLYNOME"])
        nom_polynome_utilise = donnees_polynome_utilise[3] + " du " +str(donnees_polynome_utilise[2])       
        index_poly = self.comboBox_polynome_etalon.findText(nom_polynome_utilise)        
        
        if index_poly != -1:
            self.comboBox_polynome_etalon.setCurrentIndex(index_poly)
            self.on_comboBox_polynome_etalon_activated(nom_polynome_utilise)
        
        self.on_comboBox_enceinte_activated(1)
        
        item = QtGui.QTableWidgetItem("Normale")             
        self.tableWidget_u_etalon.setItem(0, 1, item)        
        item = QtGui.QTableWidgetItem("Rectangle")        
        self.tableWidget_u_etalon.setItem(1, 1, item)        
        item = QtGui.QTableWidgetItem("Rectangle")        
        self.tableWidget_u_etalon.setItem(2, 1, item)        
        item = QtGui.QTableWidgetItem("Rectangle")        
        self.tableWidget_u_etalon.setItem(3, 1, item)        
        item = QtGui.QTableWidgetItem("Rectangle")       
        self.tableWidget_u_etalon.setItem(4, 1, item)        
        item = QtGui.QTableWidgetItem("Rectangle")        
        self.tableWidget_u_etalon.setItem(5, 1, item)      
        
            
        #reaffectation des donnees dans le tableau U_etalon
        for ligne in range( self.tableWidget_u_etalon.rowCount()):
            item_remplissage_fictif = QtGui.QTableWidgetItem(str(0))           
            self.tableWidget_u_etalon.setItem(ligne, 0, item_remplissage_fictif)
            
        ligne = 0
        for ele in donnees_caracterisation["MOYENS_MESURE"]["LISTE_U_ETALON"]:            
            item_ = QtGui.QTableWidgetItem(str(ele))
            item_.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
            self.tableWidget_u_etalon.setItem(ligne, 0, item_)            
            self.tableWidget_u_etalon.setCurrentCell(ligne, 0)
            ligne += 1
            
        
        #reaffectation donnees tableau U_centrale
        for ligne in range( self.tableWidget_u_centrale.rowCount()):
            item_remplissage_fictif = QtGui.QTableWidgetItem(str(0))
            item_remplissage_fictif.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
            self.tableWidget_u_centrale.setItem(ligne, 0, item_remplissage_fictif)
            
        ligne = 0
        for ele in donnees_caracterisation["MOYENS_MESURE"]["LISTE_U_CENTRALE"]:            
            item_ = QtGui.QTableWidgetItem(str(ele))
            item_.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
            self.tableWidget_u_centrale.setItem(ligne, 0, item_)            
            self.tableWidget_u_centrale.setCurrentCell(ligne, 0)
            ligne += 1

        self.tableWidget_u_centrale.setItem(0, 1, QtGui.QTableWidgetItem("Normale"))
        self.tableWidget_u_centrale.setItem(1, 1, QtGui.QTableWidgetItem("Normale"))
        self.tableWidget_u_centrale.setItem(2, 1, QtGui.QTableWidgetItem("Rectange"))        
        self.tableWidget_u_centrale.setItem(3, 1, QtGui.QTableWidgetItem("Rectange"))
        



        #tri des temperature dans donnees_caracterisation["MESURES"]:
        id_mesures = [id[0] for id in donnees_caracterisation["MESURES"]]
#        print("id mesures {} len {}".format(id_mesures, len(id_mesures)))
        
        
        i=1
        id_debut = id_mesures[0]
        for id_temperature in range(9, len(id_mesures), 10):
#            print(id_temperature)
            id_final = id_mesures[id_temperature]
#            print("id {}".format(id_final))
            if id_debut == id_mesures[0]:
                donnees = [x for x in donnees_caracterisation["MESURES"] if  x[0] <= id_final and x[0] >= id_debut]
            else:
                donnees = [x for x in donnees_caracterisation["MESURES"] if  x[0] <= id_final and x[0] > id_debut]
#            print("donnees {}".format(donnees))
            id_debut =id_final
            

            list_ligne_en_dictionnaire =[]
             
            
            for ele  in  donnees : 
                dict_tableau_mesure = {}
                dict_tableau_mesure["TEMPERATURE"]  = ele[12]             
                dict_tableau_mesure["EMPLACEMENT_MESURE"] = ele[2]
                dict_tableau_mesure["MIN"] = ele[3]
                dict_tableau_mesure["MAX"] = ele[4]
                dict_tableau_mesure["MOYENNE"] = ele[5]
                dict_tableau_mesure["ECART_TYPE"] = ele[6]
                dict_tableau_mesure["STABILITE"] = ele[7]
                dict_tableau_mesure["DELTA"] = ele[8]
                dict_tableau_mesure["U_MOYENS"] = ele[9]
                dict_tableau_mesure["U_HOM"] = ele[10]
                dict_tableau_mesure["U_STAB"] = ele[11]                

                list_ligne_en_dictionnaire.append(dict_tableau_mesure)
             
                self.sauvegarde[str(i)] = list_ligne_en_dictionnaire
            
            i +=1   

   
    
    @pyqtSlot(int)
    def on_comboBox_enceinte_activated(self, index):
        """
        Slot documentation goes here.
        """
        nom_enceinte = self.comboBox_enceinte.currentText()
        marque = [x[2] for x in self.enceintes if x[1] == nom_enceinte][0]
        n_serie = [x[4] for x in self.enceintes if x[1] == nom_enceinte][0]
        model =[x[3] for x in self.enceintes if x[1] == nom_enceinte][0]
        
        
        self.lineEdit_marque.setText(marque)
        self.lineEdit_n_serie.setText(n_serie)
        self.lineEdit_model.setText(model)
    
    @pyqtSlot()
    def on_pushButton_precedent_clicked(self):
        """
        Slot documentation goes here.
        """
        
        if self.lineEdit_temperature.text() !="":
            num_pt =int(self.label_pt.text())
            if num_pt - 1 < 1:
                pass
            else:
                
                 #effacement
                for ligne in range(11):
                    for colonne in range(8):
                        if colonne !=6:
    
                            self.tableWidget_mesures.setItem(ligne, colonne, QtGui.QTableWidgetItem(None))
                            self.lineEdit_temperature.clear()
                            self.lineEdit_stab_max.clear()
                            self.lineEdit_u_stab_max.clear()                 
                            self.lineEdit_hom_max_2.clear()
                            self.lineEdit_u_hom_max.clear()
                            
                        else:
                            pass
                #reafctation des donnees                
                self.reaffectation_table_widget_mesures(str(int(self.label_pt.text())-1))                    
                
                #presentation textEdit n°pt de la mesure
                self.label_pt.setText(str(num_pt -1))

                    
            
    
    @pyqtSlot()
    def on_pushButton_suivant_clicked(self):
        """
        Slot documentation goes here.
        """
        

        if self.lineEdit_temperature.text() !="":
        
            num_pt =int(self.label_pt.text())
            if num_pt + 1 > self.spinBox.value():
                pass
            else:               
                
                #effacement
                for ligne in range(11):
                    for colonne in range(8):
                        if colonne !=6:    
                            self.tableWidget_mesures.setItem(ligne, colonne, QtGui.QTableWidgetItem(None))                           
                            
                        else:
                            pass
                self.tableWidget_mesures.setItem(9, 6, QtGui.QTableWidgetItem(None))
                self.lineEdit_temperature.clear()
                self.lineEdit_stab_max.clear()
                self.lineEdit_u_stab_max.clear()                 
                self.lineEdit_hom_max_2.clear()
                self.lineEdit_u_hom_max.clear()
                
                
                 #prestation ligne text 
                self.label_pt.setText(str(num_pt +1))
                self.reaffectation_table_widget_mesures(self.label_pt.text())
    
    @pyqtSlot(int)
    def on_comboBox_centrale_currentIndexChanged(self, index):
        """
        Slot documentation goes here.
        """

        nbr_ligne = self.tableWidget_select_sondes.rowCount()
        for ligne in reversed(range(nbr_ligne)):
            self.tableWidget_select_sondes.removeRow(ligne)            
            
        nom_centrale = self.comboBox_centrale.currentText()
           
        id_centrale = [x[0] for x in self.centrales if x[1] == nom_centrale][0]
           
        sondes_centrale = [x for x in self.sondes_centrales if x[6] == id_centrale]           
           
#           
        for sonde in reversed(sondes_centrale):           
           self.tableWidget_select_sondes.insertRow(0)              
           check = QtGui.QCheckBox(self.tableWidget_select_sondes)
           
           if sonde[0] in self.donnees_caracterisation["MOYENS_MESURE"]["ID_SONDES_CENTRALES"]:
               check.setChecked(True)
               check.setEnabled(False)

           
           self.tableWidget_select_sondes.setCellWidget(0, 1, check)
           item =  QtGui.QTableWidgetItem(str(sonde[1]))
           self.tableWidget_select_sondes.setItem(0, 0, item)
    
    @pyqtSlot(int)
    def on_comboBox_etalon_currentIndexChanged(self, index):
        """
        Slot documentation goes here.
        """
        nom_etalon = self.comboBox_etalon.currentText()
        self.poly = self.db_carac.poly_etalon(nom_etalon)
        nom_poly =[str(x[3]+ " du "+ str(x[2])) for x in self.poly]
        self.comboBox_polynome_etalon.clear()
        self.comboBox_polynome_etalon.addItems(nom_poly)
           
        self.on_comboBox_polynome_etalon_activated(nom_etalon)
     
    
    @pyqtSlot(int)
    def on_tabWidget_currentChanged(self, index):
        """
        Slot documentation goes here.
        """
              
        if self.tabWidget.currentIndex() == 2:
            
            #on sauve l'onglet moyens de mesure
            #            moyens de mesure :
            try : 
                                
                id_etalon = [x[0] for x in self.etalons if x[1] == self.comboBox_etalon.currentText()][0]
                
                nom_poly = self.comboBox_polynome_etalon.currentText().split(" du")
                id_poly = [x[0] for x in self.poly if  x[3] == nom_poly[0]][0]
                
                nom_centrale = self.comboBox_centrale.currentText()           
                id_centrale = [x[0] for x in self.centrales if x[1] == nom_centrale][0]
                   
                list_id_sondes =[]
                for ligne in range(self.tableWidget_select_sondes.rowCount()):
                    if self.tableWidget_select_sondes.cellWidget(ligne, 1).isChecked():                   
                       sonde_id = [x[0] for x in self.sondes_centrales if x[1] == self.tableWidget_select_sondes.item(ligne, 0).text()][0]
                       list_id_sondes.append(sonde_id) 
                
                list_u_etalon = []
                for ligne in range (self.tableWidget_u_etalon.rowCount()):
                    list_u_etalon.append(float(self.tableWidget_u_etalon.item(ligne, 0).text()))
                    
                
                list_u_centrale = []
                for ligne in range(self.tableWidget_u_centrale.rowCount()):
                    list_u_centrale.append(float(self.tableWidget_u_centrale.item(ligne, 0).text()))
                    
               
                moyens_mesure = {"ID_ETALON": id_etalon, "ID_CENTRALE": id_centrale, 
                                "ID_SONDES_CENTRALE": list_id_sondes, "ID_POLYNOME": id_poly, "TABLEAU_U_ETALON": list_u_etalon, 
                                "TABLEAU_U_CENTRALE": list_u_centrale}
                                
    
    #           Sauvegarde  Mesures :tablewidget_mesure               
                
                self.sauvegarde["moyens_mesure"] = moyens_mesure
    
                if self.lineEdit_temperature.text() == "":
                    self.lineEdit_temperature.setStyleSheet("background-color: red;")
                    
                else:
                    self.lineEdit_temperature.setStyleSheet("background-color: white;")
                    
                self.reaffectation_table_widget_mesures(str(int(self.label_pt.text())))
                    
            except :
                QMessageBox.critical (self, "Attention","erreur de saisie dans l'onglet moyens de mesure")
                
                self.tabWidget.setCurrentIndex(1)
                
        elif self.tabWidget.currentIndex() == 1:
            #on va sauver la config administratif de l'onglet 0
            
            self.actionSauvegarder.setEnabled(False)
            self.tabWidget.setTabEnabled(2, True)

            date = self.dateEdit.date().toString("yyyy-MM-dd")
            id_generateur = [x[0] for x in self.enceintes if x[1] == self.comboBox_enceinte.currentText()][0]
            id_operateur = [x[0] for x in self.responsable_mesures if x[1] == self.comboBox_operateur.currentText()][0]
            commentaire = self.textEdit.toPlainText()
            nbr_pt = self.spinBox.value()
                
                
            admin = { "ID_GENERATEUR": id_generateur,"DATE": date , "OPERATEUR": id_operateur, "TYPE_CARACTERISATION": "TOTALE", 
                         "COMMENTAIRE": commentaire, "NBR_TEMP_STABILITE" : nbr_pt, "NBR_TEMP_HOMOGENEITE": nbr_pt , 
                         "ARCHIVAGE": False}
                         
            self.sauvegarde["admin"] = admin
            
        elif self.tabWidget.currentIndex() == 0:    
            self.actionSauvegarder.setEnabled(False)
            self.tabWidget.setTabEnabled(2, False)
#       
    @pyqtSlot(str)
    def on_comboBox_polynome_etalon_activated(self, p0):
        """
        Slot documentation goes here.
        """
        nom_poly = self.comboBox_polynome_etalon.currentText().split(" du")
        poly_select = [x for x in self.poly if  x[3] == nom_poly[0]][0]              
        
        if poly_select[5] == 2:
            self.lineEdit_ax2.setText(str(poly_select[6]))
            self.lineEdit_bx.setText(str(poly_select[7]))
            self.lineEdit_c.setText(str(poly_select[8]))
        else:
            self.lineEdit_bx.setText(str(poly_select[6]))
            self.lineEdit_c.setText(str(poly_select[7]))

    

    
    
    @pyqtSlot(int, int)
    def on_tableWidget_u_etalon_cellChanged(self, row, column):
             
        if self.tableWidget_u_etalon.currentItem() != None and self.tableWidget_u_etalon.currentColumn()== 0 and\
                                                        column not in [1, 2, 3]:
            try:
#                print("row {} colonne {}".format(row, column))
                #etalonnage:
                self.tableWidget_u_etalon.setCurrentCell(0, 0)
                etalonnage = float(self.tableWidget_u_etalon.item(0, 0).text())
                couleur = self.tableWidget_u_etalon.item(0, 0). backgroundColor().name()
                if couleur == "#ff0000":
                    self.tableWidget_u_etalon.item(0, 0).setBackgroundColor(QtGui.QColor('white'))
                
                u_etal = etalonnage/2
                self.tableWidget_u_etalon.setItem(0, 2, QtGui.QTableWidgetItem(str(u_etal)))
                self.tableWidget_u_etalon.setItem(0, 3, QtGui.QTableWidgetItem(str(np.power(u_etal, 2))))
                
                #Polynome:
                self.tableWidget_u_etalon.setCurrentCell(1, 0)
                poly = float(self.tableWidget_u_etalon.item(1, 0).text())
                couleur = self.tableWidget_u_etalon.item(1, 0). backgroundColor().name()
                if couleur == "#ff0000":
                    self.tableWidget_u_etalon.item(1, 0).setBackgroundColor(QtGui.QColor('white'))
               
                self.tableWidget_u_etalon.setItem(1, 2, QtGui.QTableWidgetItem(str(poly/np.sqrt(3))))
                self.tableWidget_u_etalon.setItem(1, 3, QtGui.QTableWidgetItem(str(np.power(poly/np.sqrt(3), 2))))
                
                #Resolution:
                self.tableWidget_u_etalon.setCurrentCell(2, 0)
                resol = float(self.tableWidget_u_etalon.item(2, 0).text())
                couleur = self.tableWidget_u_etalon.item(2, 0). backgroundColor().name()
                if couleur == "#ff0000":
                    self.tableWidget_u_etalon.item(2, 0).setBackgroundColor(QtGui.QColor('white'))
                
                self.tableWidget_u_etalon.setItem(2, 2, QtGui.QTableWidgetItem(str(resol/(2*np.sqrt(3)))))
                self.tableWidget_u_etalon.setItem(2, 3, QtGui.QTableWidgetItem(str(np.power((resol/(2*np.sqrt(3))), 2))))
                
                #Derive:
                self.tableWidget_u_etalon.setCurrentCell(3, 0)
                deriv = float(self.tableWidget_u_etalon.item(3, 0).text())
                couleur = self.tableWidget_u_etalon.item(3, 0). backgroundColor().name()
                if couleur == "#ff0000":
                    self.tableWidget_u_etalon.item(3, 0).setBackgroundColor(QtGui.QColor('white'))
                
                self.tableWidget_u_etalon.setItem(3, 2, QtGui.QTableWidgetItem(str(deriv/(np.sqrt(3)))))
                self.tableWidget_u_etalon.setItem(3, 3, QtGui.QTableWidgetItem(str(np.power((deriv/(np.sqrt(3))), 2))))
                
                #auto:
                self.tableWidget_u_etalon.setCurrentCell(4, 0)
                auto = float(self.tableWidget_u_etalon.item(4, 0).text())
                couleur = self.tableWidget_u_etalon.item(4, 0). backgroundColor().name()
                if couleur == "#ff0000":
                    self.tableWidget_u_etalon.item(4, 0).setBackgroundColor(QtGui.QColor('white'))
    
                
                self.tableWidget_u_etalon.setItem(4, 2, QtGui.QTableWidgetItem(str(auto/(np.sqrt(3)))))
                self.tableWidget_u_etalon.setItem(4, 3, QtGui.QTableWidgetItem(str(np.power((auto/(np.sqrt(3))), 2))))
                
                #Temp ambiante
                self.tableWidget_u_etalon.setCurrentCell(5, 0)
                temp_ambiante = float(self.tableWidget_u_etalon.item(5, 0).text())
                couleur = self.tableWidget_u_etalon.item(5, 0). backgroundColor().name()
                if couleur == "#ff0000":
                    self.tableWidget_u_etalon.item(5, 0).setBackgroundColor(QtGui.QColor('white'))
    
                
                self.tableWidget_u_etalon.setItem(5, 2, QtGui.QTableWidgetItem(str(temp_ambiante/(2*np.sqrt(3)))))
                self.tableWidget_u_etalon.setItem(5, 3, QtGui.QTableWidgetItem(str(np.power((temp_ambiante/(2*np.sqrt(3))), 2))))
                
                self.u_xi_moyens_mesure()
                
                
            except ValueError:
                item_select = self.tableWidget_u_etalon.currentItem()
                item_select.setBackgroundColor(QtGui.QColor('red'))
                self.u_xi_moyens_mesure()
#            
        else:
            pass
    
    @pyqtSlot(int, int)
    def on_tableWidget_u_centrale_cellChanged(self, row, column):
        """
        Slot documentation goes here.
        """
        if self.tableWidget_u_centrale.currentColumn()== 0 and\
                                                        column not in [1, 2, 3]:
                                                            
#            print("couocu")
            
            try:
                #etalonnage
                self.tableWidget_u_centrale.setCurrentCell(0, 0)
                etalonnage = float(self.tableWidget_u_centrale.item(0, 0).text())
                couleur = self.tableWidget_u_centrale.item(0, 0). backgroundColor().name()
                if couleur == "#ff0000":
                    self.tableWidget_u_centrale.item(0, 0).setBackgroundColor(QtGui.QColor('white'))
                
                u_etal = etalonnage/2
                self.tableWidget_u_centrale.setItem(0, 2, QtGui.QTableWidgetItem(str(u_etal)))
                self.tableWidget_u_centrale.setItem(0, 3, QtGui.QTableWidgetItem(str(np.power(u_etal, 2))))

                #Modelisation:
                self.tableWidget_u_centrale.setCurrentCell(1, 0)
                modelis = float(self.tableWidget_u_centrale.item(1, 0).text())
                couleur = self.tableWidget_u_centrale.item(1, 0). backgroundColor().name()
                if couleur == "#ff0000":
                    self.tableWidget_u_centrale.item(1, 0).setBackgroundColor(QtGui.QColor('white'))
               
                self.tableWidget_u_centrale.setItem(1, 2, QtGui.QTableWidgetItem(str(modelis/2)))
                self.tableWidget_u_centrale.setItem(1, 3, QtGui.QTableWidgetItem(str(np.power(modelis/2, 2))))
                
                #Resolution:
                self.tableWidget_u_centrale.setCurrentCell(2, 0)
                resol = float(self.tableWidget_u_centrale.item(2, 0).text())
                couleur = self.tableWidget_u_centrale.item(2, 0). backgroundColor().name()
                if couleur == "#ff0000":
                    self.tableWidget_u_centrale.item(2, 0).setBackgroundColor(QtGui.QColor('white'))
                
                self.tableWidget_u_centrale.setItem(2, 2, QtGui.QTableWidgetItem(str(resol/(2*np.sqrt(3)))))
                self.tableWidget_u_centrale.setItem(2, 3, QtGui.QTableWidgetItem(str(np.power((resol/(2*np.sqrt(3))), 2))))
                
                #Derive:
                self.tableWidget_u_centrale.setCurrentCell(3, 0)
                deriv = float(self.tableWidget_u_centrale.item(3, 0).text())
                couleur = self.tableWidget_u_centrale.item(3, 0). backgroundColor().name()
                if couleur == "#ff0000":
                    self.tableWidget_u_centrale.item(3, 0).setBackgroundColor(QtGui.QColor('white'))
                
                self.tableWidget_u_centrale.setItem(3, 2, QtGui.QTableWidgetItem(str(deriv/(np.sqrt(3)))))
                self.tableWidget_u_centrale.setItem(3, 3, QtGui.QTableWidgetItem(str(np.power((deriv/(np.sqrt(3))), 2))))
                
                self.u_xi_moyens_mesure()
                
            except ValueError:
                item_select = self.tableWidget_u_centrale.currentItem()
                item_select.setBackgroundColor(QtGui.QColor('red'))
#                self.u_xi_moyens_mesure()
#            
            
            
    def u_xi_moyens_mesure(self):
        try:
            self.lineEdit_u_moyens_mesure.setStyleSheet("background-color: white;")
            u_x2 = []
            for i in range(6):
                if self.tableWidget_u_etalon.item(i, 3) != None:
                    u_x2.append(float(self.tableWidget_u_etalon.item(i, 3).text()))
                
                else:
                    pass
            
            for j in range(5):
                if self.tableWidget_u_centrale.item(j, 3) != None:
                    
                    u_x2.append(float(self.tableWidget_u_centrale.item(j, 3).text()))
                else:
                    pass
                
    #        print(u_x2)
            somme_u_x2 = np.sum(u_x2)
            
            self.lineEdit_u_moyens_mesure.setText(str(somme_u_x2))
        except ValueError:
            self.lineEdit_u_moyens_mesure.setStyleSheet("background-color: red;")
            
    @pyqtSlot(int)
    def on_spinBox_valueChanged(self, p0):
        """
        Slot documentation goes here.
        """
        self.nbr_pts_caracterisation = self.spinBox.value()
    
    @pyqtSlot(int, int)
    def on_tableWidget_mesures_cellChanged(self, row, column):
        """
        Slot documentation goes here.
        """
#        print("row {} column {}".format(row, column))
        if column not in [4, 5, 7]:
            try:
                
               
                u_moyens = np.sqrt(float(self.lineEdit_u_moyens_mesure.text()))
                #Polynome etalonnage
                ax2 = float(self.lineEdit_ax2.text())
                bx = float(self.lineEdit_bx.text())
                c = float(self.lineEdit_c.text())
                
                
                if row == 9 and column != 3:
                    valeur = float(self.tableWidget_mesures.item(row, column).text())
                    correction = ax2* np.power(valeur, 2) + bx * valeur + c
                    valeur_corrigee = valeur + correction
                    item = QtGui.QTableWidgetItem(str(valeur_corrigee))
                    self.tableWidget_mesures.setItem(10, column, item)
                
                
                for ligne in range(11):
#                    print("ligne {}".format(ligne))
    
                    
                    #stabilité
                    if self.tableWidget_mesures.item(ligne, 0) != None and self.tableWidget_mesures.item(ligne, 1) != None:
                        max = float(self.tableWidget_mesures.item(ligne, 1).text())
#                        print(self.tableWidget_mesures.item(ligne, 0).text())
                        min = float(self.tableWidget_mesures.item(ligne, 0).text())
                        delta = np.absolute(max-min)
                        item = QtGui.QTableWidgetItem(str(delta))
                        self.tableWidget_mesures.setItem(ligne, 4, item)
                    
                    #delta ref sonde
                    if self.tableWidget_mesures.item(ligne, 2) != None and self.tableWidget_mesures.item(10, 2) != None:
                        moyenne_etal = float(self.tableWidget_mesures.item(10, 2).text())
                        moyenne_sonde = float(self.tableWidget_mesures.item(ligne, 2).text())
                        delta = np.absolute(moyenne_etal-moyenne_sonde)
                        item = QtGui.QTableWidgetItem(str(delta))
                        self.tableWidget_mesures.setItem(ligne, 5, item) 
                        
                    #uhom
                    if self.tableWidget_mesures.item(ligne, 5) != None and self.tableWidget_mesures.item(ligne, 6) != None:
                        delta_ref_sonde = float(self.tableWidget_mesures.item(ligne, 5).text())
                        u_hom = np.sqrt(np.power((delta_ref_sonde/np.sqrt(3)), 2)+ np.power(u_moyens, 2) )
                        item = QtGui.QTableWidgetItem(str(u_hom))
                        self.tableWidget_mesures.setItem(ligne, 7, item) 
                        
                self.gestion_line_edit_mesure() 
             
          
            except ValueError:
#                print("pb")
#                self.gestion_line_edit_mesure()
                pass
                
                
                
                
                
    def gestion_line_edit_mesure(self):
#        print("coucou")
#        try:
        #stabilite
        ecart_type = []
        stab = []
        hom = []
        u_hom = []
        ecart_type = []
#        for ligne in range(9):
#            if self.tableWidget_mesures.item(ligne, 3) != None:
#                ecart_type.append(float(self.tableWidget_mesures.item(ligne, 3).text()))
                
        for ligne in range(9):
            if self.tableWidget_mesures.item(ligne, 3) != None:
                ecart_type.append(float(self.tableWidget_mesures.item(ligne, 3).text()))
            
            if self.tableWidget_mesures.item(ligne, 4) != None:
                stab.append(float(self.tableWidget_mesures.item(ligne, 4).text()))                
            else:
                pass
            
            if self.tableWidget_mesures.item(ligne, 5) != None:                
                hom.append(float(self.tableWidget_mesures.item(ligne, 5).text()))
            else:
                pass
            
            if self.tableWidget_mesures.item(ligne, 7) != None:
                u_hom.append(float(self.tableWidget_mesures.item(ligne, 7).text()))
            else:
                pass
            

        if len(stab) !=0:
            stab_max = np.amax(stab)
            self.lineEdit_stab_max.setText(str(stab_max))
            u_stab_max = stab_max/(np.sqrt(10))
            self.lineEdit_u_stab_max.setText(str(u_stab_max))
            
        if len(ecart_type) != 0:
            ecartype_max = np.amax(ecart_type)
            u_stab_max = ecartype_max/(np.sqrt(10))
            self.lineEdit_u_stab_max.setText(str(u_stab_max))
            
        if len(hom) !=0:
            hom_max = np.amax(hom)
            self.lineEdit_hom_max_2.setText(str(hom_max))

        
        
        if len(u_hom) !=0:
            u_hom_max = np.amax(u_hom)
            self.lineEdit_u_hom_max.setText(str(u_hom_max))
            
        if len(ecart_type) != 0:
            ecartype_max = np.amax(ecart_type)
            self.lineEdit_ecarttype_max.setText(str(ecartype_max))
                

    @pyqtSlot(str)
    def on_lineEdit_u_moyens_mesure_textChanged(self, p0):
        """
        Slot documentation goes here.
        """
        u_moyens = np.sqrt(float(self.lineEdit_u_moyens_mesure.text()))
        self.lineEdit_u_moyens.setText(str(u_moyens))
        
        for ligne in range(9):
                
            item = QtGui.QTableWidgetItem(str(u_moyens))
            self.tableWidget_mesures.setItem(ligne, 6, item)
    
    @pyqtSlot(str)
    def on_lineEdit_temperature_textChanged(self, p0):
        """
        Slot documentation goes here.
        """
        try :
            float(self.lineEdit_temperature.text())
            self.lineEdit_temperature.setStyleSheet("background-color: white;")
                
        except ValueError:    
                self.lineEdit_temperature.setStyleSheet("background-color: red;")
    
   
        
 

        
    def reaffectation_table_widget_mesures(self, n_pt_mesure):    
        """Fct qui reaffect les donne"""
#        print("pt {} reaffectation {}".format(n_pt_mesure, self.sauvegarde))
        
        if self.sauvegarde.get(n_pt_mesure) !=None:
            
#            print("donnees a reacffecter {}".format(self.sauvegarde[n_pt_mesure][0]["TEMPERATURE"]))
            self.lineEdit_temperature.setText(self.sauvegarde[n_pt_mesure][0]["TEMPERATURE"])
            
            ligne=0
            for dict_mesure in self.sauvegarde[n_pt_mesure]:
                item = QtGui.QTableWidgetItem(str(dict_mesure["MIN"]))
                self.tableWidget_mesures.setItem(ligne, 0, item) 
                
                item = QtGui.QTableWidgetItem(str(dict_mesure["MAX"]))
                self.tableWidget_mesures.setItem(ligne, 1, item) 
                
                item = QtGui.QTableWidgetItem(str(dict_mesure["MOYENNE"]))
                self.tableWidget_mesures.setItem(ligne, 2, item) 
                
                item = QtGui.QTableWidgetItem(str(dict_mesure["ECART_TYPE"]))
                self.tableWidget_mesures.setItem(ligne, 3, item) 
                
                item = QtGui.QTableWidgetItem(str(dict_mesure["STABILITE"]))
                self.tableWidget_mesures.setItem(ligne, 4, item) 
                
                item = QtGui.QTableWidgetItem(str(dict_mesure["DELTA"]))
                self.tableWidget_mesures.setItem(ligne, 5, item) 
                
                if dict_mesure["U_MOYENS"] is not None:
                    item = QtGui.QTableWidgetItem(str(dict_mesure["U_MOYENS"]))
                    self.tableWidget_mesures.setItem(ligne, 6, item) 
                
                if dict_mesure["U_HOM"] is not None:
                    item = QtGui.QTableWidgetItem(str(dict_mesure["U_HOM"]))
                    self.tableWidget_mesures.setItem(ligne, 7, item)
                
                if dict_mesure["U_STAB"] is not None:
                    item = QtGui.QTableWidgetItem(str(dict_mesure["U_STAB"]))
                    self.tableWidget_mesures.setItem(ligne, 8, item)
                 
                ligne +=1

        else :
            pass





    
