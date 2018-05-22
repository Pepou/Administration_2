# -*- coding: utf-8 -*-

"""
Module implementing MainCaracterisation.
"""
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import pyqtSlot , QModelIndex
from PyQt4.QtGui import QMainWindow, QMouseEvent, QMessageBox
from PyQt4 import QtGui, QtCore

from .Ui_Main_Caracterisation import Ui_MainCaracterisation
from Modules.Caracterisation_generateurs_temperature.Package.AccesBdd_consultation import AccesBdd_consultation
from Modules.Caracterisation_generateurs_temperature.Package.AccesBdd_caracterisation_enceinte import AccesBdd_caracterisation_enceinte

from Modules.Caracterisation_generateurs_temperature.GUI.Caracterisation_enceinte.Interface_caracterisation_enceinte import Caracterisation_enceinte
from Modules.Caracterisation_generateurs_temperature.GUI.Caracterisation_enceinte.Interface_visualisation_caracterisation_enceinte import Visualisation_Caracterisation_enceinte
from Modules.Caracterisation_generateurs_temperature.GUI.Caracterisation_enceinte.Interface_modification_caracterisation_enceinte import Modification_caracterisation_enceinte

from Modules.Caracterisation_generateurs_temperature.GUI.Caracterisation_Bain.Caracterisation_Bain import Caracterisation_Bain
from Modules.Caracterisation_generateurs_temperature.GUI.Caracterisation_Bain.Caracterisation_Bain_maj_visualisation import Caracterisation_Bain_Maj

import numpy as np
import decimal


class MainCaracterisation(QMainWindow, Ui_MainCaracterisation):
    """
    Class documentation goes here.
    """
    def __init__(self, engine,meta  , parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super(MainCaracterisation, self).__init__(parent)
        self.setupUi(self)
        
        self.engine =engine
        self.meta = meta
        
        
        
        self.groupBox_individuel.setChecked(False)
        
        self.db_consult = AccesBdd_consultation(self.engine, self.meta )
        self.db_carac = AccesBdd_caracterisation_enceinte(self.engine, self.meta)
        
        #constantes de Classe :
        self.generateurs_temperature = self.db_consult.generateurs()
        self.techniciens = self.db_consult.techniciens()
        self.nom_generateur = list(set([x[1] for x in self.generateurs_temperature]))
        self.nom_generateur.sort()
        self.comboBox_generateur.addItems(self.nom_generateur)
        
        self.comboBox_generateur_2.addItems(self.nom_generateur)
        
        self.initialisation()
        
        
            
        self.tableWidget.viewport().installEventFilter(self)


    def eventFilter(self, tableWidget, event):
        if event.type()  == QtCore.QEvent.MouseButtonPress:

            self.boutton_souris = QMouseEvent.button(event)

        else:
            pass
        return False
   
    def closeEvent(self, event):

        self.db_consult.__del__()
        self.db_carac.__del__()

    def initialisation(self):
        
        self.table_caracterisation_gen_admin = self.db_consult.table_caracterisation_gen_admin()
        self.table_caracterisation_gen_resultats = self.db_consult.table_caracterisation_gen_resultats()
        
        self.caracterisation_enceintes_mesures = self.db_consult.table_caracterisation_enceintes_mesures_stab_hom()
        
        
        
        nbr_ligne = self.tableWidget.rowCount()
        for ligne in  reversed(range(nbr_ligne)):
            self.tableWidget.removeRow(ligne)
        
        
        #remplissage du tableau :
        
        self.tableau_en_list = []
        
        for caract in reversed(self.table_caracterisation_gen_admin):
            
            self.tableWidget.insertRow(0)
            id_caracterisation_admin = caract[0]
            self.tableWidget.setItem(0, 11, QtGui.QTableWidgetItem(str(id_caracterisation_admin)))
            
            list_result_carac = [x for x in self.table_caracterisation_gen_resultats if x[1] == id_caracterisation_admin][0] #attention c'est un tupple

            #date
            date = caract[1]
            self.tableWidget.setItem(0, 0, QtGui.QTableWidgetItem(str(caract[1])))
            #Generateur
            nom_generateur = [x[1] for x in self.generateurs_temperature if x[0] == caract[2]][0]
            self.tableWidget.setItem(0, 1, QtGui.QTableWidgetItem(str(nom_generateur)))
            #operateur
            visa_operateur = [ x[1] for x in self.techniciens if x[0] == caract[3]][0]
            self.tableWidget.setItem(0, 2, QtGui.QTableWidgetItem(str(visa_operateur)))
            #Commentaire 
            commentaire = str(caract[4])
            self.tableWidget.setItem(0, 3, QtGui.QTableWidgetItem(str(caract[4])))
            
            #stabilité
            stab = list_result_carac[2]
            self.tableWidget.setItem(0, 4, QtGui.QTableWidgetItem(str(stab)))
            #temp_stab
            temp_stab = list_result_carac[3]
            self.tableWidget.setItem(0, 5, QtGui.QTableWidgetItem(str(temp_stab)))
            #hom
            homogene = list_result_carac[4]
            self.tableWidget.setItem(0, 6, QtGui.QTableWidgetItem(str(homogene)))
            #temp_hom
            temp_homogene = list_result_carac[6]
            self.tableWidget.setItem(0, 7, QtGui.QTableWidgetItem(str(temp_homogene)))
            #diag_hom
            diag_homogene = list_result_carac[5]
            self.tableWidget.setItem(0, 8, QtGui.QTableWidgetItem(str(diag_homogene)))
            #diag_hom
            u_generateur = list_result_carac[7]
            self.tableWidget.setItem(0, 9, QtGui.QTableWidgetItem(str(u_generateur)))
            
            #○Archivage
            check_box = QtGui.QCheckBox (self.tableWidget)
            self.tableWidget.setCellWidget(0, 10, check_box)
            check_box.setEnabled(False)
            
            if caract[7] == True:
                check_box.setChecked(True)
                
            self.tableau_en_list.append((date, nom_generateur,visa_operateur,  commentaire, stab, temp_stab, homogene, temp_homogene, diag_homogene, u_generateur, caract[7]))
        
    def PlotFunc(self):
        
        if self.groupBox_total.isChecked():
            
            if self.comboBox_archivage_carcaterisations.currentText() == "Toutes":
                etat = ""
            elif self.comboBox_archivage_carcaterisations.currentText() == "Archivées":
                etat = True
            elif self.comboBox_archivage_carcaterisations.currentText() == "Non Archivées":
                etat = False
            
            nom_generateur = self.comboBox_generateur.currentText()
            type_donnees = self.comboBox_type_donnees.currentText()
            
            titre_graphique = nom_generateur+" : "+type_donnees
            
            if etat != "":
    
                date = [x[0] for x in self.tableau_en_list if x[1] == nom_generateur and x[10] == etat]
                if type_donnees == "u_generateur":
                    donnee =[x[9] for x in self.tableau_en_list if x[1] == nom_generateur and x[10] == etat]
                
                elif type_donnees == "Stabilite":
                    donnee =[x[4] for x in self.tableau_en_list if x[1] == nom_generateur and x[10] == etat] 
                    
                    
                elif type_donnees == "Homogeneite":
                    donnee =[x[6] for x in self.tableau_en_list if x[1] == nom_generateur and x[10] == etat]
                    
            else:
                date = [x[0] for x in self.tableau_en_list if x[1] == nom_generateur]
                if type_donnees == "u_generateur":
                    donnee =[x[9] for x in self.tableau_en_list if x[1] == nom_generateur]
                
                elif type_donnees == "Stabilite":
                    donnee =[x[4] for x in self.tableau_en_list if x[1] == nom_generateur]
                    
                    
                elif type_donnees == "Homogeneite":
                    donnee =[x[6] for x in self.tableau_en_list if x[1] == nom_generateur]
                
    #        donnee =[x[0] for x in self.tableau_en_list if x[1] == nom_generateur]
            
            self.graphique.canvas.ax.clear()
            self.graphique.canvas.nom_graphique(str(titre_graphique))
            
            self.graphique.canvas.ax.plot_date(date, donnee, 'o-',xdate=True, ydate=False,   linewidth=2)
           
            self.graphique.canvas.draw()
        
        elif self.groupBox_individuel.isChecked():
#            print(self.generateurs_temperature)            
            nom_generateur = self.comboBox_generateur_2.currentText()
            type_generateur = [x[6] for x in self.generateurs_temperature if x [1] == nom_generateur][0]
            
            if type_generateur == 'Enceinte climatique':
                type_donnees = self.comboBox_type_donnees_2.currentText()
                id_caracterisation = int(self.comboBox_caracterisation.currentText().split()[2])
                
                temp_caracterisation = set([x[3] for x in self.caracterisation_enceintes_mesures if x[0] == id_caracterisation])                
                
                list_max_hom_temperature = []
                list_max_stab_temperature = []
                for temp in temp_caracterisation:
                                        
                    donnees_hom = [decimal.Decimal(x[2]) for x in self.caracterisation_enceintes_mesures if x[0] == id_caracterisation and x[3] == temp]
                                        
                    if len(donnees_hom):
                        max_hom = np.amax(donnees_hom)
                    else:
                        max_hom = 0
                    list_max_hom_temperature.append((temp, max_hom))
                                        
                    donnees_stab = [decimal.Decimal(x[1]) for x in self.caracterisation_enceintes_mesures if x[0] == id_caracterisation and x[3] == temp]
                    
                    if len (donnees_stab):
                        max_stab = np.amax(donnees_stab)
                    else:
                        max_stab = 0
                        
                    list_max_stab_temperature.append((temp, max_stab))
           
                if type_donnees == "Stabilite":
                    titre_graphique = nom_generateur+" : "+type_donnees 
                    
                    list_max_stab_temperature.sort()
                    
                    list_x = [x[0] for x in list_max_stab_temperature]
                    list_y = [x[1] for x in list_max_stab_temperature]
                    
                    self.graphique.canvas.ax.clear()
                    self.graphique.canvas.nom_graphique(str(titre_graphique))
            
                    self.graphique.canvas.ax.plot(list_x, list_y)#, 'o-',x=True, y=False,   linewidth=2)
           
                    self.graphique.canvas.draw()
                        
                        
                elif type_donnees == "Homogeneite":
                    titre_graphique = nom_generateur+" : "+type_donnees 
                    
                    list_max_hom_temperature.sort()
                    
                    list_x = [x[0] for x in list_max_hom_temperature]
                    list_y = [x[1] for x in list_max_hom_temperature]
                    
                    self.graphique.canvas.ax.clear()
                    self.graphique.canvas.nom_graphique(str(titre_graphique))
            
                    self.graphique.canvas.ax.plot(list_x, list_y)#, 'o-',x=True, y=False,   linewidth=2)
           
                    self.graphique.canvas.draw()
                        
                        
            
            
    @pyqtSlot()
    def on_tracer_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.PlotFunc()
    
    @pyqtSlot()
    def on_groupBox_total_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.groupBox_total.isChecked():
            self.groupBox_individuel.setChecked(False)
        else:
            self.groupBox_individuel.setChecked(True)
    
    @pyqtSlot()
    def on_groupBox_individuel_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.groupBox_individuel.isChecked():
            self.groupBox_total.setChecked(False)
        else:
            self.groupBox_total.setChecked(True)
            


    
    @pyqtSlot()
    def on_actionModifier_caracterisation_enceinte_triggered(self):
        """
        Slot documentation goes here.
        """
        ligne = self.tableWidget.currentRow()
#        print(ligne)
        if ligne != -1:
            ligne_liste = []
            for colonne in range(10):
                ligne_liste.append(self.tableWidget.item(ligne, colonne).text())    
            
            id_caracterisation = int(self.tableWidget.item(ligne, 11).text())
            
        
            #test si la caracterisation concerne enceintes / bains :
            if [x[6] for x in self.generateurs_temperature if x[1] == ligne_liste[1] ][0] == 'Enceinte climatique':
                
                generateur = "Enceinte"
                #recuperation des donnees de caracterisation :
                    
                caracterisation_selectionnee = self.db_consult.recup_caracterisation_id (id_caracterisation, generateur)
                self.modif_caracterisation_enceinte = Modification_caracterisation_enceinte(self.engine,self.meta, caracterisation_selectionnee, id_caracterisation )  
                
                self.connect(self.modif_caracterisation_enceinte, SIGNAL("fermeturemodif_caracterisation_enceinte(PyQt_PyObject)"), self.initialisation)
        

                      
                self.modif_caracterisation_enceinte.show()
        
        
        
        else:
                QMessageBox.critical (self,"Attention"
                ,  "Aucune ligne de caraceterisation selectionnnée")
        
    @pyqtSlot()
    def on_actionNouvelle_caracterisation_enceinte_triggered(self):
        """
        Slot documentation goes here.
        """
        
        self.caracterisation_enceinte = Caracterisation_enceinte(self.engine,self.meta )
        
        self.connect(self.caracterisation_enceinte, SIGNAL("nouvellecaracterisation_enceinte(PyQt_PyObject)"), self.initialisation)
        self.caracterisation_enceinte.show()
        
    
    @pyqtSlot(QModelIndex)
    def on_tableWidget_doubleClicked(self, index):
        """
        Slot documentation goes here.
        """

        if self.boutton_souris == 1:

            ligne = self.tableWidget.currentRow()
#            ligne_liste = []
#            for colonne in range(10):
#                ligne_liste.append(self.tableWidget.item(ligne, colonne).text())    
            
            id_caracterisation = int(self.tableWidget.item(ligne, 11).text())
            nom_generateur = self.tableWidget.item(ligne, 1).text()

            #test si la caracterisation concerne enceintes / bains :
            if next(x[6] for x in self.generateurs_temperature if x[1] == nom_generateur) == 'Enceinte climatique':
                
                generateur = "Enceinte"
                #recuperation des donnees de caracterisation :
                
                caracterisation_selectionnee = self.db_consult.recup_caracterisation_id (id_caracterisation, generateur)
                
                
                self.visualisation_caracterisation_enceinte = Visualisation_Caracterisation_enceinte(self.engine, self.meta, caracterisation_selectionnee )
                self.visualisation_caracterisation_enceinte.show()
            
            elif next(x[6] for x in self.generateurs_temperature if x[1] == nom_generateur) == '''Bain d'etalonnage''': 
                
                self.caracterisation_bain_maj= Caracterisation_Bain_Maj(self.engine,self.meta,  str(id_caracterisation), True)
                self.caracterisation_bain_maj.show() 
             
        
        elif self.boutton_souris == 2:
            reponse = QMessageBox.question (self,"Demande"
                , "Voulez vous archivez cette caracterisation?", QMessageBox.Yes, QMessageBox.No )
                
#            print(reponse)
            
            if reponse == QMessageBox.Yes:
                id  =  self.tableWidget.item(self.tableWidget.currentRow(), 11).text()
                self.db_carac.caracterisation_generateurs_admin_archiver(id)
                self.initialisation()
            
        

    
    @pyqtSlot(str)
    def on_comboBox_generateur_2_activated(self, p0):
        """
        Slot documentation goes here.
        """
        nom_generateur = self.comboBox_generateur_2.currentText()
        id_generateur = [x[0] for x in self.generateurs_temperature if x[1] == nom_generateur][0]
        
        liste_date_caracterisation = ["ID_Caracterisation n° {} du {}".format(x[0], x[1]) for x in self.table_caracterisation_gen_admin if x[2] == id_generateur]
#        print(liste_date_caracterisation)
        
        self.comboBox_caracterisation.clear()
        self.comboBox_caracterisation.addItems(liste_date_caracterisation)
        

    
    @pyqtSlot()
    def on_actionNouvelle_caracterisation_bain_triggered(self):
        """
        Slot documentation goes here.
        """
        self.caracterisation_bain = Caracterisation_Bain(self.engine,self.meta )
        
        self.connect(self.caracterisation_bain, SIGNAL("nouvellecaracterisation_bain(PyQt_PyObject)"), self.initialisation)
        self.caracterisation_bain.show()
    
    @pyqtSlot()
    def on_actionModifier_caracterisation_bain_triggered(self):
        """
        Slot documentation goes here.
        """
        ligne = self.tableWidget.currentRow()

        if ligne != -1:
            nom_generateur = self.tableWidget.item(ligne, 1).text()
#            print(nom_generateur)

            
            id_caracterisation = self.tableWidget.item(ligne, 11).text()
            
#            print(next(x[6] for x in self.generateurs_temperature if x[1] == nom_generateur))
        
            #test si la caracterisation concerne enceintes / bains :
            if next(x[6] for x in self.generateurs_temperature if x[1] == nom_generateur) == '''Bain d'etalonnage''':
                

                self.caracterisation_bain_maj= Caracterisation_Bain_Maj(self.engine,self.meta,  id_caracterisation, False)
                

        
                self.connect(self.caracterisation_bain_maj, SIGNAL("nouvellecaracterisation_bain(PyQt_PyObject)"), self.initialisation)
                self.caracterisation_bain_maj.show()
                
            
        else:
                QMessageBox.critical (self,"Attention"
                ,  "Aucune ligne de caraceterisation selectionnnée")
