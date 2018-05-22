# -*- coding: utf-8 -*-

"""
Module implementing Caracterisation_enceinte.
"""

from PyQt4.QtCore import pyqtSlot, QPoint
from PyQt4.QtGui import QMainWindow, QMessageBox, QFileDialog, QMouseEvent, QMenu
from PyQt4 import QtGui, QtCore
#from QtGui import QAction
from PyQt4.QtCore import SIGNAL

from .Ui_Interface_caracterisation_enceinte import Ui_Caracterisation_enceinte
from Modules.Caracterisation_generateurs_temperature.Package.AccesBdd_caracterisation_enceinte import AccesBdd_caracterisation_enceinte
from Modules.Caracterisation_generateurs_temperature.Package.RapportCaracterisationEnceinte import RapportCaracterisationEnceinte
import numpy as np

class Caracterisation_enceinte(QMainWindow, Ui_Caracterisation_enceinte):
    """
    Class documentation goes here.
    """
    def __init__(self, engine, meta,  parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super(Caracterisation_enceinte, self).__init__(parent)
        self.setupUi(self)
        
        self.engine = engine
        self.meta = meta
        
        self.label_pt.setText(str(1))
        self.spinBox.setValue(4)
                
        
        self.dateEdit.setDate(QtCore.QDate.currentDate())
        
        self.nbr_pts_caracterisation = self.spinBox.value()
        
        self.db_carac = AccesBdd_caracterisation_enceinte(self.engine, self.meta)
        
        #ctes de classe
        self.sauvegarde = {}
        self.sauvegarde["ARCHIVAGE"] = False
        self.sauvegarde_maximum_par_pt = {}
        
        self.actionSauvegarder.setEnabled(False)
        self.tabWidget.setTabEnabled(2, False)
      
        self.responsable_mesures = self.db_carac.techniciens()
        visa = [x[1]  for x in self.responsable_mesures]
        self.comboBox_operateur.addItems(visa)        
        
        self.enceintes =self.db_carac.enceintes()
        nom_enceintes = [x[1] for x in self.enceintes]
        self.comboBox_enceinte.addItems(nom_enceintes)
        
        self.etalons =  self.db_carac.etalons()

        nom_etalon = [x[1] for x in self.etalons]
        self.comboBox_etalon.addItems(nom_etalon)
        
        
        self.sondes_centrales = self.db_carac.sondes_centrales()
        self.centrales = self.db_carac.centrales()
        nom_centrales = [x[1] for x in self.centrales ]
        self.comboBox_centrale.addItems(nom_centrales)


        self.on_comboBox_enceinte_activated(1)
        
        item = QtGui.QTableWidgetItem("Normale")
        item.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )        
        self.tableWidget_u_etalon.setItem(0, 1, item)
        
        item = QtGui.QTableWidgetItem("Rectangle")
        item.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
        self.tableWidget_u_etalon.setItem(1, 1, item)
        
        item = QtGui.QTableWidgetItem("Rectangle")
        item.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
        self.tableWidget_u_etalon.setItem(2, 1, item)
        
        item = QtGui.QTableWidgetItem("Rectangle")
        item.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
        self.tableWidget_u_etalon.setItem(3, 1, item)
        
        item = QtGui.QTableWidgetItem("Rectangle")
        item.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
        self.tableWidget_u_etalon.setItem(4, 1, item)
        
        item = QtGui.QTableWidgetItem("Rectangle")
        item.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
        self.tableWidget_u_etalon.setItem(5, 1, item)      
        
            
        
        self.tableWidget_u_etalon.setItem(3, 0, QtGui.QTableWidgetItem(""))
        self.tableWidget_u_etalon.item(3, 0).setBackgroundColor(QtGui.QColor('red'))
        
        
        self.nom_lignes = ["CENTRE", "HAD", "HAG", "HPD", "HPG", "BAD", "BAG", "BPD", "BPG",
                                    "ETALON", "ETALON Corrigé"]
                        
        for i in range(1, self.nbr_pts_caracterisation +1) :
           
            list_ligne_en_dictionnaire =[]
            for ligne_tableau_mesure  in range (10): 
                dict_tableau_mesure = {}                
                dict_tableau_mesure["EMPLACEMENT_MESURE"] = self.nom_lignes [ligne_tableau_mesure]
                dict_tableau_mesure["MIN"] = 0
                dict_tableau_mesure["MAX"] = 0
                dict_tableau_mesure["MOYENNE"] = 0
                dict_tableau_mesure["ECART_TYPE"] = 0
                dict_tableau_mesure["STABILITE"] = 0
                dict_tableau_mesure["DELTA"] = 0
                dict_tableau_mesure["U_MOYENS"] = 0
                dict_tableau_mesure["U_HOM"] = 0
                dict_tableau_mesure["U_STAB"] = 0
                dict_tableau_mesure["TEMPERATURE"] = None
                list_ligne_en_dictionnaire.append(dict_tableau_mesure)
                
            self.sauvegarde[str(i)] = list_ligne_en_dictionnaire
            
        self.tableWidget_select_sondes.setMouseTracking(True)

    
    def keyPressEvent(self, event):

       
        items_tableWidget_mesures = self.tableWidget_mesures.selectedIndexes()

        clavier = event.key()
        
        if len(items_tableWidget_mesures) != 0:

            if clavier == 86: #"86: correspond à ctrl+V
                presse_papier =  QtGui.QApplication.clipboard()
                read_press_papier = presse_papier.text()
                press_papier_list = read_press_papier.split()
               
                
                list_float =[]
                for ele in press_papier_list:
#                    print(ele)
                    try:
                        number = ele.replace(",", ".")
                        float(number)
                        list_float.append(number)
                    except ValueError:
                        pass
                        
                
                if len(list_float) == 40:
                    
                    for ligne in range(10):
                        index = 4*ligne
                        for colonne in range(4):

                            item =QtGui.QTableWidgetItem(str(list_float[index]))
#                        
                            self.tableWidget_mesures.setItem(ligne, colonne, item)
                            
                            index +=1          
            else:
                pass
                
        else:
            pass
    
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
                #enregistrement des valeurs a l'ecran
                self.sauvegarde[ self.label_pt.text()] = self.sauvegarde_tableau_mesure()
                
                self.sauvegarde_maximum_par_pt[ self.label_pt.text()] = {"TEMPERATURE" : self.lineEdit_temperature.text(), 
                                                                    "STABILITE" : self.lineEdit_stab_max.text(), 
                                                                    "HOMOGENEITE" :  self.lineEdit_hom_max_2.text(), 
                                                                    "U_HOM" : self.lineEdit_u_hom_max.text(), 
                                                                    "U_STAB" : self.lineEdit_u_stab_max.text(),
                                                                    "ECART_TYPE": self.lineEdit_ecarttype_max.text()
                                                                     }
                for ligne in range(9):
                    #emplacement hom :
                    if self.tableWidget_mesures.item(ligne,5).text() == self.lineEdit_hom_max_2.text():
                        self.sauvegarde_maximum_par_pt[ self.label_pt.text()]["POSIT_HOMOGENEITE"] = self.tableWidget_mesures.verticalHeaderItem(ligne).text()
                 
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
                            self.lineEdit_ecarttype_max.clear()
                            
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
        
#        print(self.lineEdit_temperature .text())
        if self.lineEdit_temperature.text() !="":
        
            num_pt =int(self.label_pt.text())
            if num_pt + 1 > self.spinBox.value():
                pass
            else:
                
    
                self.sauvegarde[ self.label_pt.text()] = self.sauvegarde_tableau_mesure()
                
                self.sauvegarde_maximum_par_pt[ self.label_pt.text()] = {"TEMPERATURE" : self.lineEdit_temperature.text(), 
                                                                    "STABILITE" : self.lineEdit_stab_max.text(), 
                                                                    "HOMOGENEITE" :  self.lineEdit_hom_max_2.text(), 
                                                                    "U_HOM" : self.lineEdit_u_hom_max.text(), 
                                                                    "U_STAB" : self.lineEdit_u_stab_max.text(), 
                                                                    "ECART_TYPE": self.lineEdit_ecarttype_max.text()}
                for ligne in range(9):
                    #emplacement hom :
                    if self.tableWidget_mesures.item(ligne,5).text() == self.lineEdit_hom_max_2.text():
                        self.sauvegarde_maximum_par_pt[ self.label_pt.text()]["POSIT_HOMOGENEITE"] = self.tableWidget_mesures.verticalHeaderItem(ligne).text()

                
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
                self.lineEdit_ecarttype_max.clear()
                
                self.reaffectation_table_widget_mesures(str(int(self.label_pt.text())+1))
                self.label_pt.setText(str(num_pt +1))
                
#                self. on_lineEdit_u_moyens_mesure_textChanged("toto")
    
    @pyqtSlot(int)
    def on_comboBox_centrale_currentIndexChanged(self, index):
        """
        Slot documentation goes here.
        """
#        print("index {}".format(index))
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
           
           #connection au slot
           check.stateChanged.connect(self.gestion_sondes_centrale_selectionnees)
           
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
        nom_poly =[str(x[3]+ " du "+ str(x[4])) for x in self.poly]
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
                self.actionSauvegarder.setEnabled(True)
                
                id_etalon = [x[0] for x in self.etalons if x[1] == self.comboBox_etalon.currentText()][0]
                
                nom_poly = self.comboBox_polynome_etalon.currentText().split(" du")
                self.id_poly = [x[0] for x in self.poly if  x[3] == nom_poly[0]][0]
                
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
                                "ID_SONDES_CENTRALE": list_id_sondes, "ID_POLYNOME": self.id_poly, "TABLEAU_U_ETALON": list_u_etalon, 
                                "TABLEAU_U_CENTRALE": list_u_centrale}
                                
    
    #           Sauvegarde  Mesures :tablewidget_mesure               
                
                self.sauvegarde["moyens_mesure"] = moyens_mesure
    
                if self.lineEdit_temperature.text() == "":
                    self.lineEdit_temperature.setStyleSheet("background-color: red;")
                    
                else:
                    self.lineEdit_temperature.setStyleSheet("background-color: white;")
                    
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
        
        if poly_select [10] != None:
            incertitude = (poly_select [10], poly_select [11] )
        else:
            incertitude = (None , None)
        
        
        if poly_select[5] == 2:
            self.lineEdit_ax2.setText(str(poly_select[6]))
            self.lineEdit_bx.setText(str(poly_select[7]))
            self.lineEdit_c.setText(str(poly_select[8]))
        else:
            self.lineEdit_bx.setText(str(poly_select[6]))
            self.lineEdit_c.setText(str(poly_select[7]))
        
        #Polynome
        
        if incertitude[0]!= None:
            item_1 =  QtGui.QTableWidgetItem(str(incertitude[0]))

            item_3 = QtGui.QTableWidgetItem(str(incertitude[1]))
            item_3.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
            
            item_4 =QtGui.QTableWidgetItem(str(incertitude[1]*incertitude[1]))
            item_4.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
        else:
            item_1 =  QtGui.QTableWidgetItem("None")
#            item_1.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
#            item_2 = QtGui.QTableWidgetItem("Rectangle")
            item_3 = QtGui.QTableWidgetItem("None")
            item_3.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
            
            item_4 =QtGui.QTableWidgetItem("None") 
            item_4.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
        
        
        self.tableWidget_u_etalon.setItem(1, 0, item_1)       
#        self.tableWidget_u_etalon.setItem(1, 1, item_2)  
        self.tableWidget_u_etalon.setItem(1, 2, item_3)
        self.tableWidget_u_etalon.setItem(1, 3, item_4)
        
        #resolution
        item_5 =  QtGui.QTableWidgetItem("0.001")
        self.tableWidget_u_etalon.setItem(2, 0, item_5)
        
#        self.tableWidget_u_etalon.setItem(2, 1, QtGui.QTableWidgetItem("Rectangle"))
        
        item_6 =  QtGui.QTableWidgetItem(str(0.001/(2*np.sqrt(3))))
        item_6.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
        self.tableWidget_u_etalon.setItem(2, 2, item_6)
        
        item_7 =QtGui.QTableWidgetItem(str(np.power((0.001/(2*np.sqrt(3))), 2)))
        item_7.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
        self.tableWidget_u_etalon.setItem(2, 3, item_7)
        
        
        #etalonnage (deux possibilité soit table Polynome_table_etalonnage soit etalonnage_resultat 
        u_etalonnage = self.db_carac.incertitude_etal(nom_poly[0], poly_select[0])
#        print(u_etalonnage)
        
        if len (u_etalonnage)!=0:
            max_u_etal = np.amax(u_etalonnage)            
            self.tableWidget_u_etalon.setItem(0, 0, QtGui.QTableWidgetItem(str(max_u_etal)))
            
            u_etal = QtGui.QTableWidgetItem(str(max_u_etal/2))
            u_etal.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )  
            self.tableWidget_u_etalon.setItem(0, 2, u_etal)
            
            
            u_etal2 = QtGui.QTableWidgetItem(str(np.power((max_u_etal/2), 2)))
            u_etal2.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
            self.tableWidget_u_etalon.setItem(0, 3, u_etal2)
        
        else:
            item_none = QtGui.QTableWidgetItem("None")
#            item_none.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )  
            self.tableWidget_u_etalon.setItem(0, 0, item_none)
            
            item_none_1 = QtGui.QTableWidgetItem("None")
            item_none_1.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
            self.tableWidget_u_etalon.setItem(0, 2, item_none_1)
            
            item_none_2 = QtGui.QTableWidgetItem("None")
            item_none_2.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
            self.tableWidget_u_etalon.setItem(0, 3, item_none_2)
        

    

    
    def gestion_sondes_centrale_selectionnees(self):
        #gestion des sondes
        
        nbr_ligne = self.tableWidget_select_sondes.rowCount()
        list_sondes_selectionnees =[]
        for ligne in range(nbr_ligne):
            
            if self.tableWidget_select_sondes.cellWidget(ligne, 1).isChecked():
                list_sondes_selectionnees.append(self.tableWidget_select_sondes.item(ligne, 0).text())
#        print("sondes selectionnees {}".format(list_sondes_selectionnees))
        if list_sondes_selectionnees:
            recup_etalonnage = self.db_carac.incertitude_max_sondes_centrale(list_sondes_selectionnees)
            u_etal = recup_etalonnage[0]
        else:
            u_etal = 0
        
        if u_etal != 0:
            
            self.textEdit_list_ce_centrale.clear()
            self.textEdit_list_ce_centrale.setText("{}".format(recup_etalonnage[1]))
            
            #etalonnage
            self.tableWidget_u_centrale.setItem(0, 0, QtGui.QTableWidgetItem(str(u_etal)))
            
            item_1 = QtGui.QTableWidgetItem("Normale")
            item_1.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )            
            self.tableWidget_u_centrale.setItem(0, 1,item_1) 
            
            item_2 = QtGui.QTableWidgetItem(str(u_etal/2))
            item_2.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
            self.tableWidget_u_centrale.setItem(0, 2, item_2 )
            
            item_3 = QtGui.QTableWidgetItem(str(np.power((u_etal/2), 2)))
            item_3.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
            self.tableWidget_u_centrale.setItem(0, 3, item_3)
            
            #modelisation
            self.tableWidget_u_centrale.setItem(1, 0, QtGui.QTableWidgetItem(str(u_etal)))
            
            item_1 = QtGui.QTableWidgetItem("Normale")
            item_1.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )  
            self.tableWidget_u_centrale.setItem(1, 1, item_1)
           
            item_2 = QtGui.QTableWidgetItem(str(u_etal/2))
            item_2.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
            self.tableWidget_u_centrale.setItem(1, 2,item_2)
            
            item_3 = QtGui.QTableWidgetItem(str(np.power((u_etal/2), 2)))
            item_3.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
            self.tableWidget_u_centrale.setItem(1, 3, item_3)
            
            
            #resolution
            item_4 = QtGui.QTableWidgetItem("")
            self.tableWidget_u_centrale.setItem(2, 0, item_4)
            item_5 = QtGui.QTableWidgetItem("Rectange")
            self.tableWidget_u_centrale.setItem(2, 1, item_5)
            item_6 = QtGui.QTableWidgetItem("")
            item_6.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
            self.tableWidget_u_centrale.setItem(2, 2, item_6)
            item_7 = QtGui.QTableWidgetItem("")
            item_7.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
            self.tableWidget_u_centrale.setItem(2, 3, item_7)
            
            #derive
            item_8 = QtGui.QTableWidgetItem("")
            self.tableWidget_u_centrale.setItem(3, 0, item_8)
            item_9 = QtGui.QTableWidgetItem("Rectange")
            self.tableWidget_u_centrale.setItem(3, 1, item_9)
            item_10 = QtGui.QTableWidgetItem("")
            item_10.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
            self.tableWidget_u_centrale.setItem(3, 2, item_10)
            item_11 = QtGui.QTableWidgetItem("")
            item_11.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
            self.tableWidget_u_centrale.setItem(3, 3, item_11)
        
        else:
            
            #etalonnage
            self.tableWidget_u_centrale.setItem(0, 0, QtGui.QTableWidgetItem(str(0)))
            
            item_1 = QtGui.QTableWidgetItem("Normale")
            item_1.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled ) 
            self.tableWidget_u_centrale.setItem(0, 1, item_1)
           
            item_2 = QtGui.QTableWidgetItem(str(0))
            item_2.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
            self.tableWidget_u_centrale.setItem(0, 2, item_2)
            
            
            item_3 = QtGui.QTableWidgetItem(str(0))
            item_3.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
            self.tableWidget_u_centrale.setItem(0, 3, item_3)            
            
             #modelisation
            self.tableWidget_u_centrale.setItem(1, 0, QtGui.QTableWidgetItem(str(u_etal)))
            
            
            item_1 = QtGui.QTableWidgetItem("Normale")
            item_1.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled ) 
            self.tableWidget_u_centrale.setItem(1, 1, item_1)           
          
            item_2 = QtGui.QTableWidgetItem(str(u_etal/2))
            item_2.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
            self.tableWidget_u_centrale.setItem(1, 2, item_2)
            
            item_3 = QtGui.QTableWidgetItem(str(np.power((u_etal/2), 2)))
            item_3.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
            self.tableWidget_u_centrale.setItem(1, 3, QtGui.QTableWidgetItem(str(item_3)))
            
            #resolution
            item_4 = QtGui.QTableWidgetItem("")
            self.tableWidget_u_centrale.setItem(2, 0, item_4)
            item_5 = QtGui.QTableWidgetItem("Rectange")
            self.tableWidget_u_centrale.setItem(2, 1, item_5)
            item_6 = QtGui.QTableWidgetItem("")
            item_6.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
            self.tableWidget_u_centrale.setItem(2, 2, item_6)
            item_7 = QtGui.QTableWidgetItem("")
            item_7.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
            self.tableWidget_u_centrale.setItem(2, 3, item_7)
            
             #derive
            item_8 = QtGui.QTableWidgetItem("")
            self.tableWidget_u_centrale.setItem(3, 0, item_8)
            item_9 = QtGui.QTableWidgetItem("Rectange")
            self.tableWidget_u_centrale.setItem(3, 1, item_9)
            item_10 = QtGui.QTableWidgetItem("")
            item_10.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
            self.tableWidget_u_centrale.setItem(3, 2, item_10)
            item_11 = QtGui.QTableWidgetItem("")
            item_11.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
            self.tableWidget_u_centrale.setItem(3, 3, item_11)
            
    
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
#        print("coucou")
        self.nbr_pts_caracterisation = self.spinBox.value()
        
        if int(self.label_pt.text()) > self.spinBox.value():
#            print("coucou 2")
            
            self.reaffectation_table_widget_mesures(str(self.nbr_pts_caracterisation))
            self.label_pt.setText(str(self.spinBox.value()))
                
            self. on_lineEdit_u_moyens_mesure_textChanged("toto")
#            print("test {}".format(self.sauvegarde.get(str(self.spinBox.value()))))
            

    
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
                
                
                for ligne in range(9):
    
                    
                    #stabilité
                    if self.tableWidget_mesures.item(ligne, 0) != None and self.tableWidget_mesures.item(ligne, 1) != None:
                        max = float(self.tableWidget_mesures.item(ligne, 1).text())
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
#            u_stab_max = stab_max/(np.sqrt(10))
#            self.lineEdit_u_stab_max.setText(str(u_stab_max))
            
        if len(ecart_type) != 0:
            ecartype_max = np.amax(ecart_type)
            self.lineEdit_ecarttype_max.setText(str(ecartype_max))
            u_stab_max = ecartype_max/(np.sqrt(10))
            self.lineEdit_u_stab_max.setText(str(u_stab_max))
            
        if len(hom) !=0:
            hom_max = np.amax(hom)
            self.lineEdit_hom_max_2.setText(str(hom_max))

        
        
        if len(u_hom) !=0:
            u_hom_max = np.amax(u_hom)
            self.lineEdit_u_hom_max.setText(str(u_hom_max))
                

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
    
   
        
    
    @pyqtSlot()
    def on_actionSauvegarder_triggered(self):
        """
        Slot documentation goes here.
        """
        if self.lineEdit_temperature.text():
            if int(self.label_pt.text()) == self.spinBox.value() :
                
                reponse = QMessageBox.question(self, 
                                    self.trUtf8("Information"), 
                                    self.trUtf8("Voulez-vous creer un rapport de caracterisation"), 
                                    QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
                                    
                if reponse == QtGui.QMessageBox.Yes:
                    dossier = QFileDialog.getExistingDirectory(None ,  "Selectionner le dossier de sauvegarde des Rapports", 'y:/1.METROLOGIE/MATERIEL/1-GENERATEURS/AIR/')
                else:
                    dossier =None
#        if dossier !="":
                
                self.sauvegarde[self.label_pt.text()] = self.sauvegarde_tableau_mesure()
                self.sauvegarde_maximum_par_pt[ self.label_pt.text()] = {"TEMPERATURE" : self.lineEdit_temperature.text(), 
                                                                        "STABILITE" : self.lineEdit_stab_max.text(), 
                                                                        "HOMOGENEITE" :  self.lineEdit_hom_max_2.text(), 
                                                                        "U_HOM" : self.lineEdit_u_hom_max.text(), 
                                                                        "U_STAB" : self.lineEdit_u_stab_max.text(), 
                                                                        "ECART_TYPE": self.lineEdit_ecarttype_max.text()}
                for ligne in range(9):
                        #emplacement hom :
                        if self.tableWidget_mesures.item(ligne,5).text() == self.lineEdit_hom_max_2.text():
                            self.sauvegarde_maximum_par_pt[ self.label_pt.text()]["POSIT_HOMOGENEITE"] = self.tableWidget_mesures.verticalHeaderItem(ligne).text()
                        else:
                            self.sauvegarde_maximum_par_pt[ self.label_pt.text()]["POSIT_HOMOGENEITE"] = None
                    
                id_caract = self.db_carac.caracterisation_generateurs_admin(self.sauvegarde["admin"])
                self.sauvegarde["moyens_mesure"]["ID_CARACTERISATION"] = id_caract                
        
                self.db_carac.caracterisation_generateurs_moyens_mesure(self.sauvegarde["moyens_mesure"])
                
                
                for i in range(1, self.spinBox.value()+1):
                    for ele in self.sauvegarde[str(i)]:
                        ele["ID_CARACTERISATION"] = id_caract
    
                    self.db_carac.caracterisation_enceinte_mesure(self.sauvegarde[str(i)])
                       
                            
                    #gestion table resultats        
    
                stab_max = [(float(self.sauvegarde_maximum_par_pt[x]["STABILITE"]), self.sauvegarde_maximum_par_pt[x]["TEMPERATURE"]) for x in self.sauvegarde_maximum_par_pt]
                max_stab_max = max([x[0] for x in stab_max])
                temp_max_stab = stab_max[[x[0] for x in stab_max].index(max_stab_max)][1]   
                
                ecartype_max = [(float(self.sauvegarde_maximum_par_pt[x]["ECART_TYPE"]), self.sauvegarde_maximum_par_pt[x]["TEMPERATURE"]) for x in self.sauvegarde_maximum_par_pt]
                max_ecartype_max = max([x[0] for x in ecartype_max])
          
                hom_max = [(float(self.sauvegarde_maximum_par_pt[x]["HOMOGENEITE"]), self.sauvegarde_maximum_par_pt[x]["TEMPERATURE"], self.sauvegarde_maximum_par_pt[x]["POSIT_HOMOGENEITE"]) for x in self.sauvegarde_maximum_par_pt]
                max_hom_max = max([x[0] for x in hom_max])
                temp_hom_max = hom_max[[x[0] for x in hom_max].index(max_hom_max)][1] 
                position_hom_max = hom_max[[x[0] for x in hom_max].index(max_hom_max)][2]
                
                u_hom_max = [(float(self.sauvegarde_maximum_par_pt[x]["U_HOM"]), self.sauvegarde_maximum_par_pt[x]["TEMPERATURE"], self.sauvegarde_maximum_par_pt[x]["POSIT_HOMOGENEITE"]) for x in self.sauvegarde_maximum_par_pt]
                u_max_hom_max = max([x[0] for x in u_hom_max])
    
           
                u_generateur = np.sqrt(np.power((float(max_ecartype_max)/np.sqrt(10)), 2) + np.power(float(u_max_hom_max), 2))
    
                
                caracterisation_resultat = {"ID_CARACT" : id_caract , "STABILITE" : max_stab_max, "TEMP_STAB" : temp_max_stab, 
                                                        "HOMOGENEITE" : max_hom_max ,  "POSIT_HOMOGENEITE":position_hom_max ,  
                                                        "TEMP_HOMOGENEITE":temp_hom_max, "u_generateur": u_generateur, 
                                                        "ECART_TYPE": max_ecartype_max}
                        
                self.db_carac.caracterisation_enceinte_resultats(caracterisation_resultat)
                
                
                #gestion rapport
                if dossier :
                    nom_fichier = "caracterisation n"+ " " + str(id_caract) + " " + str(self.sauvegarde["admin"]["DATE"])
                    
                    etalon = [(x[1], x[6], x[7], x[8])for x in self.poly if x[0] == self.id_poly] [0]
                   
                    enceinte = [(x[1], x[2], x[3], x[4]) for x in self.enceintes if x[0] == self.sauvegarde["admin"]["ID_GENERATEUR"]][0]
                    
#                    print(self.db_carac.table_caracterisation_gen_admin())
                    id_caract_enceinte = [x[0] for x in self.db_carac.table_caracterisation_gen_admin() if x[7] == False and x[2] == self.sauvegarde["admin"]["ID_GENERATEUR"]]
#                    print(" id caract {}".format(id_caract_enceinte))
                    
                    id_carat_enceinte_autre =  [x[0] for x in self.db_carac.table_caracterisation_gen_admin() if x[7] == False and x[2] != self.sauvegarde["admin"]["ID_GENERATEUR"]]
#                    print(" id caract autre {}".format(id_carat_enceinte_autre))
                    
                    list_u_generateur_max_tout_tps = [float(x[7]) for x in self.db_carac.table_caracterisation_gen_resultats() if x[1] in id_caract_enceinte]
                    list_u_generateur_autre_max_tout_tps = [float(x[7]) for x in self.db_carac.table_caracterisation_gen_resultats() if x[1] in id_carat_enceinte_autre]

                    if list_u_generateur_max_tout_tps:
                        u_generateur_max_tout_tps = np.amax(list_u_generateur_max_tout_tps)
                    else:
                        u_generateur_max_tout_tps = 0
                    
                    if list_u_generateur_autre_max_tout_tps:
                        u_generateur_autre_max_tout_tps =np.amax(list_u_generateur_autre_max_tout_tps) 
                    else:
                        u_generateur_autre_max_tout_tps =0
                    
                    nom_operateur =  [x[1]  for x in self.responsable_mesures if x[0] == self.sauvegarde["admin"]["OPERATEUR"]][0]

                    centrale = [x[1] for x in self.centrales if x[0] == self.sauvegarde["moyens_mesure"]["ID_CENTRALE"]][0]
                    
                    
                    self.sauvegarde["rapport"] = {"etalon": etalon,  "enceinte" : enceinte,  "operateur": nom_operateur, 
                                                                "centrale": centrale ,"u_enceinte": u_generateur, "u_enceinte_max": u_generateur_max_tout_tps, 
                                                                "u_enceinte_autre_max": u_generateur_autre_max_tout_tps}
                                                                
                                                                
                    rapport = RapportCaracterisationEnceinte(dossier, nom_fichier)
                    rapport.mise_en_forme(self.sauvegarde )                    
                
                self.reinitialisation_des_donnees()
                
                self.emit(SIGNAL("nouvellecaracterisation_enceinte(PyQt_PyObject)"),self )
                self.close()
                
            else :
                response = QMessageBox.critical (self, "Attention", "Vous n'avez pas saisi l'ensemble des temperatures de caracterisation_enceinte_mesure"  \
                                                                        + "\n Voulez sauver quand meme?", QMessageBox.Cancel,
                                QMessageBox.Save)
                                

                if response ==2048 :  #(correspond à save)
                    #on va sauver les donnees presentes et des zero pour les autres
                    
                    self.sauvegarde[self.label_pt.text()] = self.sauvegarde_tableau_mesure()
                    self.sauvegarde_maximum_par_pt[ self.label_pt.text()] = {"TEMPERATURE" : self.lineEdit_temperature.text(), 
                                                                            "STABILITE" : self.lineEdit_stab_max.text(), 
                                                                            "HOMOGENEITE" :  self.lineEdit_hom_max_2.text(), 
                                                                            "U_HOM" : self.lineEdit_u_hom_max.text(), 
                                                                            "U_STAB" : self.lineEdit_u_stab_max.text(), 
                                                                             }
                    for ligne in range(11):
                            #emplacement hom :
                            if self.tableWidget_mesures.item(ligne,5).text() == self.lineEdit_hom_max_2.text():
                                self.sauvegarde_maximum_par_pt[ self.label_pt.text()]["POSIT_HOMOGENEITE"] = self.tableWidget_mesures.verticalHeaderItem(ligne).text()
        
                        
                    id_caract = self.db_carac.caracterisation_generateurs_admin(self.sauvegarde["admin"])
                    self.sauvegarde["moyens_mesure"]["ID_CARACTERISATION"] = id_caract                
            
                    self.db_carac.caracterisation_generateurs_moyens_mesure(self.sauvegarde["moyens_mesure"])
                    
    #                print("complet {}".format(self.sauvegarde))
                    for i in range(1, self.spinBox.value()+1):                  
                            
                        for ele in self.sauvegarde[str(i)]:
                            ele["ID_CARACTERISATION"] = id_caract                    
                        
                        
                        self.db_carac.caracterisation_enceinte_mesure(self.sauvegarde[str(i)])
                      #gestion table resultats
        
    
                    stab_max = [(float(self.sauvegarde_maximum_par_pt[x]["STABILITE"]), self.sauvegarde_maximum_par_pt[x]["TEMPERATURE"]) for x in self.sauvegarde_maximum_par_pt]
                    max_stab_max = max([x[0] for x in stab_max])
                    temp_max_stab = stab_max[[x[0] for x in stab_max].index(max_stab_max)][1]   
                    
        
                    hom_max = [(float(self.sauvegarde_maximum_par_pt[x]["HOMOGENEITE"]), self.sauvegarde_maximum_par_pt[x]["TEMPERATURE"], self.sauvegarde_maximum_par_pt[x]["POSIT_HOMOGENEITE"]) for x in self.sauvegarde_maximum_par_pt]
                    max_hom_max = max([x[0] for x in hom_max])
                    temp_hom_max = hom_max[[x[0] for x in hom_max].index(max_hom_max)][1] 
                    position_hom_max = hom_max[[x[0] for x in hom_max].index(max_hom_max)][2]
        
               
                    u_generateur = np.sqrt(np.power((float(max_stab_max)/np.sqrt(10)), 2) + np.power((float(max_hom_max)/np.sqrt(3)), 2))
        
                    
                    caracterisation_resultat = {"ID_CARACT" : id_caract , "STABILITE" : max_stab_max, "TEMP_STAB" : temp_max_stab, 
                                                            "HOMOGENEITE" : max_hom_max ,  "POSIT_HOMOGENEITE":position_hom_max ,  
                                                            "TEMP_HOMOGENEITE":temp_hom_max, "u_generateur": u_generateur}
                            
                    self.db_carac.caracterisation_enceinte_resultats(caracterisation_resultat)
                        
                    
                    self.reinitialisation_des_donnees()

                    self.emit(SIGNAL("nouvellecaracterisation_enceinte(PyQt_PyObject)"),self )
                    self.close()
#            if dossier
        else: 
            QMessageBox.critical (self, "Attention", "Pas de temperature de caracterisation saisie")
            
            
    def sauvegarde_tableau_mesure(self):       
                
        list_ligne_en_dictionnaire = []                
                
        for ligne in range (10):
            
            dict_tableau_mesure = {}
            dict_tableau_mesure["TEMPERATURE"] = self.lineEdit_temperature.text()
            
            nom_emplacement = self.tableWidget_mesures.verticalHeaderItem (ligne).text()
#            print(nom_emplacement)
    
            dict_tableau_mesure["EMPLACEMENT_MESURE"] = nom_emplacement
            if self.tableWidget_mesures.item(ligne, 0)!= None :
                dict_tableau_mesure["MIN"] = float(self.tableWidget_mesures.item(ligne, 0).text())
            else:
                dict_tableau_mesure["MIN"] = 0.0
            if self.tableWidget_mesures.item(ligne, 1)!= None :    
                dict_tableau_mesure["MAX"] = float(self.tableWidget_mesures.item(ligne, 1).text())
            else:
                dict_tableau_mesure["MAX"]= 0.0
            if self.tableWidget_mesures.item(ligne, 2) != None:
                dict_tableau_mesure["MOYENNE"] = float(self.tableWidget_mesures.item(ligne, 2).text())
            else:
                dict_tableau_mesure["MOYENNE"]= 0.0
            if self.tableWidget_mesures.item(ligne, 3) != None:
                dict_tableau_mesure["ECART_TYPE"] = float(self.tableWidget_mesures.item(ligne, 3).text())
            else:
                dict_tableau_mesure["ECART_TYPE"] = 0.0
                
            if self.tableWidget_mesures.item(ligne, 4) != None :
                dict_tableau_mesure["STABILITE"] = float(self.tableWidget_mesures.item(ligne, 4).text())
            else:
                dict_tableau_mesure["STABILITE"]  = 0.0
                
            if self.tableWidget_mesures.item(ligne, 5) != None:
                dict_tableau_mesure["DELTA"] = float(self.tableWidget_mesures.item(ligne, 5).text())
            else :
                dict_tableau_mesure["DELTA"] = 0.0
                
            if nom_emplacement == "ETALON" or  nom_emplacement == "ETALON corrigé":
                              
               dict_tableau_mesure["U_MOYENS"] = None                  
               dict_tableau_mesure["U_HOM"] = None            
               dict_tableau_mesure["U_STAB"] = None
                
            else : 
                dict_tableau_mesure["U_MOYENS"] = float(self.tableWidget_mesures.item(ligne, 6).text())
                if self.tableWidget_mesures.item(ligne, 7) != None:
                    dict_tableau_mesure["U_HOM"] = float(self.tableWidget_mesures.item(ligne, 7).text())
                else:
                    dict_tableau_mesure["U_HOM"] = 0.0
                if self.tableWidget_mesures.item(ligne, 8) != None :   
                    dict_tableau_mesure["U_STAB"] = float(self.tableWidget_mesures.item(ligne, 8).text())
                else:
                    dict_tableau_mesure["U_STAB"] = 0.0
            
            list_ligne_en_dictionnaire.append(dict_tableau_mesure)
#        print("liste ligne dic {}".format(list_ligne_en_dictionnaire))

        return list_ligne_en_dictionnaire


        
    def reaffectation_table_widget_mesures(self, n_pt_mesure):    
        """Fct qui reaffect les donne"""
#        print("reaffectation {}".format(self.sauvegarde))
        
        if self.sauvegarde.get(n_pt_mesure) !=None:
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
                
                if dict_mesure["U_MOYENS"] is not None and ligne not in [9, 10]:
                    if dict_mesure["U_MOYENS"] != 0:
                        item = QtGui.QTableWidgetItem(str(dict_mesure["U_MOYENS"]))
                    else:
                         item = QtGui.QTableWidgetItem(str(np.sqrt(float(self.lineEdit_u_moyens_mesure.text()))))
                         
                    self.tableWidget_mesures.setItem(ligne, 6, item) 
                
                if dict_mesure["U_HOM"] is not None:
                    item = QtGui.QTableWidgetItem(str(dict_mesure["U_HOM"]))
                    self.tableWidget_mesures.setItem(ligne, 7, item)
                
                if dict_mesure["U_STAB"] is not None:
                    item = QtGui.QTableWidgetItem(str(dict_mesure["U_STAB"]))
                    self.tableWidget_mesures.setItem(ligne, 8, item)
                 
                ligne +=1

        else :
            list_ligne_en_dictionnaire = []
            for ligne_tableau_mesure  in range (10): 
                dict_tableau_mesure = {}                
                dict_tableau_mesure["EMPLACEMENT_MESURE"] = self.nom_lignes [ligne_tableau_mesure]
                dict_tableau_mesure["MIN"] = 0
                dict_tableau_mesure["MAX"] = 0
                dict_tableau_mesure["MOYENNE"] = 0
                dict_tableau_mesure["ECART_TYPE"] = 0
                dict_tableau_mesure["STABILITE"] = 0
                dict_tableau_mesure["DELTA"] = 0
                dict_tableau_mesure["U_MOYENS"] = 0
                dict_tableau_mesure["U_HOM"] = 0
                dict_tableau_mesure["U_STAB"] = 0
                dict_tableau_mesure["TEMPERATURE"] = None
                list_ligne_en_dictionnaire.append(dict_tableau_mesure)
#            print("nouveau créé {}".format(list_ligne_en_dictionnaire))
            self.sauvegarde[str(n_pt_mesure)] = list_ligne_en_dictionnaire
            
            self.reaffectation_table_widget_mesures(n_pt_mesure)





    def reinitialisation_des_donnees(self):
        """Reinitialise toutes les donnees et replace l'application en onglet 0"""
        
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
        self.lineEdit_ecarttype_max.clear()
        
        #gestion des ctes de classe
        self.sauvegarde = {}
        self.sauvegarde["ARCHIVAGE"] = False
        self.sauvegarde_maximum_par_pt = {}
        
        self.actionSauvegarder.setEnabled(False)
        self.tabWidget.setTabEnabled(2, False)
        

        for i in range(1, self.nbr_pts_caracterisation +1) :
           
            list_ligne_en_dictionnaire =[]
            for ligne_tableau_mesure  in range (10): 
                dict_tableau_mesure = {}                
                dict_tableau_mesure["EMPLACEMENT_MESURE"] = self.nom_lignes [ligne_tableau_mesure]
                dict_tableau_mesure["MIN"] = 0
                dict_tableau_mesure["MAX"] = 0
                dict_tableau_mesure["MOYENNE"] = 0
                dict_tableau_mesure["ECART_TYPE"] = 0
                dict_tableau_mesure["STABILITE"] = 0
                dict_tableau_mesure["DELTA"] = 0
                dict_tableau_mesure["U_MOYENS"] = 0
                dict_tableau_mesure["U_HOM"] = 0
                dict_tableau_mesure["U_STAB"] = 0
                
                list_ligne_en_dictionnaire.append(dict_tableau_mesure)
                
            self.sauvegarde[str(i)] = list_ligne_en_dictionnaire
        
        self.label_pt.setText("1")
        self.tableWidget_u_etalon.setItem(3,  0, QtGui.QTableWidgetItem(None))
        
        self.tableWidget_u_centrale.setItem(2, 0, QtGui.QTableWidgetItem(None))
        self.tableWidget_u_centrale.setItem(3, 0, QtGui.QTableWidgetItem(None))
        
        
        
        nbr_ligne = self.tableWidget_select_sondes.rowCount()
        for ligne in reversed(range(nbr_ligne)):
            self.tableWidget_select_sondes.removeRow(ligne)
        self.on_comboBox_centrale_currentIndexChanged(0)
        self.tabWidget.setCurrentIndex(0)
    
    

    
    

